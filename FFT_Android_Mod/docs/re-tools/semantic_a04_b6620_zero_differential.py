#!/usr/bin/env python3
"""Bounded original-ELF A04 0xb6620 R1=0 path vs independent C effects."""
import ctypes
import hashlib
import json
import subprocess
import tempfile
from pathlib import Path

from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_PROT_ALL, UC_HOOK_CODE, UC_HOOK_MEM_WRITE, UC_HOOK_MEM_READ
from unicorn.arm_const import (UC_ARM_REG_CPSR, UC_ARM_REG_PC, UC_ARM_REG_SP, UC_ARM_REG_LR,
                               UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R3, UC_ARM_REG_R4)
import semantic_evidence

SHA = "bf913415ab9458a83b14ac8c8a0fa3430d1f5d18bfbcd7c7472d6f5e8b4850bc"
ROOT = Path(__file__).resolve().parents[2]
BINARY = ROOT / "src/lib/armeabi/libgl2jni.so"
MODEL = Path(__file__).resolve().parent / "c-models/a04_b6620_zero.c"
ENTRY, BASE, STACK, SP, RETURN = 0xb6620, 0x500000, 0x600000, 0x600ffc, 0x710000
PATH = [ENTRY, ENTRY+4, ENTRY+8, ENTRY+12, ENTRY+0x24, ENTRY+0x28, ENTRY+0x2c, ENTRY+0x30, RETURN]


def run_original(code, original_word, saved_r4, seed_flags):
    uc = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    for page in (ENTRY & ~0xfff, BASE, STACK, RETURN):
        uc.mem_map(page, 0x1000, UC_PROT_ALL)
    uc.mem_write(ENTRY, code)
    before = bytearray([0xa5] * 0x1000)
    before[0x104:0x108] = original_word.to_bytes(4, "little")
    uc.mem_write(BASE, bytes(before))
    stack_before = bytes([0xcc] * 0x1000)
    uc.mem_write(STACK, stack_before)
    uc.reg_write(UC_ARM_REG_CPSR, 0x10 | seed_flags)
    for reg, value in ((UC_ARM_REG_R0, BASE), (UC_ARM_REG_R1, 0),
                       (UC_ARM_REG_R3, 0x12345678), (UC_ARM_REG_R4, saved_r4),
                       (UC_ARM_REG_SP, SP), (UC_ARM_REG_LR, RETURN)):
        uc.reg_write(reg, value)
    pcs, writes, reads = [], [], []
    def code_hook(emu, pc, size, unused):
        pcs.append(pc)
        if pc == RETURN:
            emu.emu_stop()
        if pc == ENTRY + 0x10:
            raise AssertionError("Unmodeled external BL path reached")
    uc.hook_add(UC_HOOK_CODE, code_hook)
    uc.hook_add(UC_HOOK_MEM_WRITE, lambda emu, access, addr, size, val, unused: writes.append((addr, size, val & ((1 << (8*size))-1))))
    uc.hook_add(UC_HOOK_MEM_READ, lambda emu, access, addr, size, val, unused: reads.append((addr, size)))
    uc.emu_start(ENTRY, RETURN+4, timeout=1_000_000, count=20)
    if pcs != PATH:
        raise AssertionError(f"Unexpected A04 path {pcs}")
    expected_writes = [(SP-8, 4, saved_r4), (SP-4, 4, RETURN), (BASE+0x104, 4, 0)]
    if writes != expected_writes or reads != [(SP-8, 4), (SP-4, 4)]:
        raise AssertionError(f"Memory effects differ: {writes} / {reads}")
    expected = bytearray(before)
    expected[0x104:0x108] = bytes(4)
    if bytes(uc.mem_read(BASE, 0x1000)) != expected:
        raise AssertionError("Global data changed outside word")
    stack_expected = bytearray(stack_before)
    stack_expected[SP-8-STACK:SP-4-STACK] = saved_r4.to_bytes(4, "little")
    stack_expected[SP-4-STACK:SP-STACK] = RETURN.to_bytes(4, "little")
    if bytes(uc.mem_read(STACK, 0x1000)) != stack_expected:
        raise AssertionError("Stack changed unexpectedly")
    for reg, val in ((UC_ARM_REG_R0, BASE), (UC_ARM_REG_R1, 0),
                     (UC_ARM_REG_R3, 0), (UC_ARM_REG_R4, saved_r4),
                     (UC_ARM_REG_SP, SP), (UC_ARM_REG_LR, RETURN), (UC_ARM_REG_PC, RETURN)):
        if uc.reg_read(reg) != val:
            raise AssertionError(f"Unexpected register {reg}")
    # CMP 0,#0 => N=0, Z=1, C=1, V=0
    if uc.reg_read(UC_ARM_REG_CPSR) & 0xf0000000 != 0x60000000:
        raise AssertionError("Incorrect CMP flags")
    return bytes(expected)


def main():
    if hashlib.sha256(BINARY.read_bytes()).hexdigest() != SHA:
        raise ValueError("Unexpected original ELF SHA")
    code = semantic_evidence.read_function(BINARY, ENTRY, 0x34)
    md = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    rows = {ins.address: ins for ins in md.disasm(code, ENTRY)}
    expected = {ENTRY: "cmp", ENTRY+4: "push", ENTRY+8: "mov",
                ENTRY+12: "beq", ENTRY+0x10: "bl", ENTRY+0x24: "mov",
                ENTRY+0x28: "str", ENTRY+0x2c: "mov", ENTRY+0x30: "pop"}
    for pc, op in expected.items():
        if pc not in rows or rows[pc].mnemonic != op:
            raise ValueError(f"Unexpected original A32 instruction at {pc:x}")
    if int(rows[ENTRY+12].operands[0].imm) != ENTRY+0x24:
        raise ValueError("Original BEQ target changed")
    with tempfile.TemporaryDirectory() as directory:
        library = Path(directory) / "model.so"
        subprocess.run(["cc", "-std=c11", "-O2", "-fPIC", "-shared", "-Wall",
                        "-Wextra", "-Werror", str(MODEL), "-o", str(library)], check=True)
        fn = ctypes.CDLL(str(library)).a04_zero_path
        fn.argtypes = [ctypes.c_void_p, ctypes.c_size_t, ctypes.c_uint32]
        fn.restype = ctypes.c_int
        cases = 0
        for word in (0, 1, 0xffffffff, 0x12345678):
            for saved in (0, 0xabcdef01, 0xffffffff):
                for flags in (0, 0x20000000, 0x40000000, 0xf0000000):
                    arm = run_original(code, word, saved, flags)
                    memory = bytearray([0xa5] * 0x1000)
                    memory[0x104:0x108] = word.to_bytes(4, "little")
                    ptr = (ctypes.c_ubyte * len(memory)).from_buffer(memory)
                    if fn(ptr, len(memory), 0) != 1 or bytes(memory) != arm:
                        raise AssertionError("Original ARM/C mismatch")
                    cases += 1
    print(json.dumps({"elf_sha256": SHA, "entry": "000b6620",
                      "bounded_path": "r1_zero_no_external_BL",
                      "cases": cases, "failed": 0, "new_certificates": 0}))


if __name__ == "__main__":
    main()
