#!/usr/bin/env python3
"""Differential original-ELF ARM vs independent C for A04 0xb45d0.

Bounded to mapped aligned inputs and return path; never creates certificates.
"""
import ctypes
import hashlib
import json
import subprocess
import tempfile
from pathlib import Path

from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_PROT_ALL, UC_HOOK_CODE, UC_HOOK_MEM_READ, UC_HOOK_MEM_WRITE
from unicorn.arm_const import (UC_ARM_REG_PC, UC_ARM_REG_SP, UC_ARM_REG_LR,
    UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3,
    UC_ARM_REG_CPSR)
import semantic_evidence

ELF_SHA = "bf913415ab9458a83b14ac8c8a0fa3430d1f5d18bfbcd7c7472d6f5e8b4850bc"
ENTRY = 0xb45d0
RET = 0x710000
BASE = 0x500000
MASK = 0xffffffff
ROOT = Path(__file__).resolve().parents[2]
BINARY = ROOT / "src/lib/armeabi/libgl2jni.so"
SOURCE = Path(__file__).resolve().parent / "c-models/a04_index_slot.c"


def execute(code, index, word, flags):
    uc = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    for page in (ENTRY & ~0xfff, BASE, RET):
        uc.mem_map(page, 0x1000, UC_PROT_ALL)
    uc.mem_write(ENTRY, code)
    offset = 0x14c + 12 * index
    memory = bytearray([0xa5] * 0x1000)
    memory[offset:offset + 4] = word.to_bytes(4, "little")
    uc.mem_write(BASE, memory)
    uc.reg_write(UC_ARM_REG_R0, BASE)
    uc.reg_write(UC_ARM_REG_R1, index)
    uc.reg_write(UC_ARM_REG_R2, 0x12345678)
    uc.reg_write(UC_ARM_REG_R3, 0xdeadbeef)
    uc.reg_write(UC_ARM_REG_SP, 0x600ffc)
    uc.reg_write(UC_ARM_REG_LR, RET)
    uc.reg_write(UC_ARM_REG_CPSR, 0x10 | flags)
    trace, reads, writes = [], [], []

    def instruction(emu, pc, size, _):
        trace.append(pc)
        if pc == RET:
            emu.emu_stop()

    uc.hook_add(UC_HOOK_CODE, instruction)
    uc.hook_add(UC_HOOK_MEM_READ, lambda emu, access, addr, size, value, _: reads.append((addr, size)))
    uc.hook_add(UC_HOOK_MEM_WRITE, lambda emu, access, addr, size, value, _: writes.append((addr, size, value)))
    uc.emu_start(ENTRY, RET + 4, timeout=1_000_000, count=24)
    result = uc.reg_read(UC_ARM_REG_R0)
    expected_pc = list(range(ENTRY, ENTRY + 36, 4)) + [RET]
    if trace != expected_pc or uc.reg_read(UC_ARM_REG_PC) != RET:
        raise AssertionError(f"Unexpected control flow: {trace}")
    if reads != [(BASE + offset, 4)] or writes:
        raise AssertionError(f"Unexpected memory effects: {reads}, {writes}")
    if bytes(uc.mem_read(BASE, 0x1000)) != memory:
        raise AssertionError("Memory changed")
    if uc.reg_read(UC_ARM_REG_R2) != 0x12345678:
        raise AssertionError("Unmodeled R2 mutation")
    if uc.reg_read(UC_ARM_REG_R1) != (index * 12) & MASK:
        raise AssertionError("R1 multiplication not observed")
    if uc.reg_read(UC_ARM_REG_R3) != word:
        raise AssertionError("R3 load not observed")
    # CMN r3,#1: Z iff r3 = 0xffffffff. CMN sets N,Z,C,V.
    sum64 = word + 1
    z = int((sum64 & MASK) == 0)
    n = ((sum64 & MASK) >> 31) & 1
    carry = int(sum64 > MASK)
    overflow = int(word == 0x7fffffff)
    nzcv = (n << 31) | (z << 30) | (carry << 29) | (overflow << 28)
    if uc.reg_read(UC_ARM_REG_CPSR) & 0xf0000000 != nzcv:
        raise AssertionError("Unexpected arithmetic flags")
    return result


def main():
    if hashlib.sha256(BINARY.read_bytes()).hexdigest() != ELF_SHA:
        raise ValueError("ELF SHA changed")
    code = semantic_evidence.read_function(BINARY, ENTRY, 36)
    # Exact shape: nine original A32 instructions with no calls or stores.
    from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
    insns = list(Cs(CS_ARCH_ARM, CS_MODE_ARM).disasm(code, ENTRY))
    expected = ["mov", "mul", "add", "ldr", "cmn", "addne", "addne", "moveq", "bx"]
    if len(insns) != 9 or [x.mnemonic for x in insns] != expected:
        raise ValueError("Original leaf instruction contract changed")
    with tempfile.TemporaryDirectory(prefix="a04-diff-") as directory:
        library = Path(directory) / "liba04.so"
        subprocess.run(["cc", "-std=c11", "-Wall", "-Wextra", "-Werror", "-O2",
                        "-shared", "-fPIC", str(SOURCE), "-o", str(library)], check=True)
        fn = ctypes.CDLL(str(library)).a04_index_slot_offset
        fn.argtypes = [ctypes.c_void_p, ctypes.c_size_t, ctypes.c_uint32]
        fn.restype = ctypes.c_uint32
        count = 0
        for index in (0, 1, 2, 7, 29, 50):
            offset = 0x14c + 12 * index
            for word in (0, 1, 0xffffffff, 0x7fffffff, 0x80000000, 0x12345678):
                memory = bytearray([0xa5] * 0x1000)
                memory[offset:offset+4] = word.to_bytes(4, "little")
                arr = (ctypes.c_ubyte * len(memory)).from_buffer(memory)
                model = fn(arr, len(memory), index)
                for flags in (0, 0x20000000, 0x40000000, 0xf0000000):
                    original = execute(code, index, word, flags)
                    expected = 0 if word == MASK else BASE + model
                    if original != expected:
                        raise AssertionError(f"ARM/C mismatch: index={index}, word={word:x}, flags={flags:x}")
                    count += 1
    print(json.dumps({"elf_sha256": ELF_SHA, "entry": f"{ENTRY:08x}",
                      "differential_cases": count, "failures": 0,
                      "memory_writes": 0, "new_certificates": 0,
                      "scope": "aligned_controlled_leaf_inputs"}))


if __name__ == "__main__":
    main()
