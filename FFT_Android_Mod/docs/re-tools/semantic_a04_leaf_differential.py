#!/usr/bin/env python3
"""Original ARM -> independent C comparison for leaf at 0x000b45d0."""
import ctypes
import hashlib
import json
import subprocess
import tempfile
from pathlib import Path

from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_PROT_ALL, UC_HOOK_CODE, UC_HOOK_MEM_READ, UC_HOOK_MEM_WRITE
from unicorn.arm_const import (UC_ARM_REG_PC, UC_ARM_REG_SP, UC_ARM_REG_LR, UC_ARM_REG_R0,
    UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_CPSR)
import semantic_evidence

SHA = "bf913415ab9458a83b14ac8c8a0fa3430d1f5d18bfbcd7c7472d6f5e8b4850bc"
ROOT = Path(__file__).resolve().parents[2]
BINARY = ROOT / "src/lib/armeabi/libgl2jni.so"
MODEL = Path(__file__).resolve().parent / "c-models/a04_slot.c"
ENTRY, BASE, RETURN, MASK = 0xb45d0, 0x500000, 0x710000, 0xffffffff


def execute(code, index, value, initial_flags):
    offset = 0x14c + 12 * index
    uc = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    for addr in (ENTRY & ~0xfff, BASE, RETURN):
        uc.mem_map(addr, 0x1000, UC_PROT_ALL)
    uc.mem_write(ENTRY, code)
    memory = bytearray(b"\xa5" * 0x1000)
    memory[offset:offset + 4] = value.to_bytes(4, "little")
    uc.mem_write(BASE, bytes(memory))
    # Configure processor mode before writing banked SP/LR.
    uc.reg_write(UC_ARM_REG_CPSR, 0x10 | initial_flags)
    for register, val in ((UC_ARM_REG_R0, BASE), (UC_ARM_REG_R1, index),
                          (UC_ARM_REG_R2, 0x12345678), (UC_ARM_REG_R3, 0xdeadbeef),
                          (UC_ARM_REG_LR, RETURN), (UC_ARM_REG_SP, 0x600ffc)):
        uc.reg_write(register, val)
    trace, reads, writes = [], [], []
    def on_code(emu, pc, size, ignored):
        trace.append(pc)
        if pc == RETURN:
            emu.emu_stop()
    uc.hook_add(UC_HOOK_CODE, on_code)
    uc.hook_add(UC_HOOK_MEM_READ, lambda emu, access, addr, size, val, ignored: reads.append((addr, size)))
    uc.hook_add(UC_HOOK_MEM_WRITE, lambda emu, access, addr, size, val, ignored: writes.append((addr, size)))
    try:
        uc.emu_start(ENTRY, RETURN + 4, timeout=1000000, count=24)
    except Exception as exc:
        raise AssertionError(f"ARM fetch failure: pc={uc.reg_read(UC_ARM_REG_PC):08x}, "
                             f"lr={uc.reg_read(UC_ARM_REG_LR):08x}, trace={trace}, "
                             f"index={index}, value={value:08x}, flags={initial_flags:08x}") from exc
    assert trace == list(range(ENTRY, ENTRY + 36, 4)) + [RETURN], trace
    assert uc.reg_read(UC_ARM_REG_PC) == RETURN
    assert reads == [(BASE + offset, 4)] and not writes, (reads, writes)
    assert bytes(uc.mem_read(BASE, len(memory))) == memory
    assert uc.reg_read(UC_ARM_REG_R1) == 12 * index
    assert uc.reg_read(UC_ARM_REG_R2) == 0x12345678
    assert uc.reg_read(UC_ARM_REG_R3) == value
    assert uc.reg_read(UC_ARM_REG_SP) == 0x600ffc
    assert uc.reg_read(UC_ARM_REG_LR) == RETURN
    summed = value + 1
    nzcv = (((summed & MASK) >> 31) << 31
            | (int((summed & MASK) == 0) << 30)
            | (int(summed > MASK) << 29)
            | (int(value == 0x7fffffff) << 28))
    assert (uc.reg_read(UC_ARM_REG_CPSR) & 0xf0000000) == nzcv
    return uc.reg_read(UC_ARM_REG_R0)


def main():
    if hashlib.sha256(BINARY.read_bytes()).hexdigest() != SHA:
        raise ValueError("Original ELF baseline mismatch")
    code = semantic_evidence.read_function(BINARY, ENTRY, 36)
    mnemonic = [ins.mnemonic for ins in Cs(CS_ARCH_ARM, CS_MODE_ARM).disasm(code, ENTRY)]
    if mnemonic != ["mov", "mul", "add", "ldr", "cmn", "addne", "addne", "moveq", "bx"]:
        raise ValueError("Leaf opcode contract changed")
    with tempfile.TemporaryDirectory() as td:
        lib = Path(td) / "slot.so"
        subprocess.run(["cc", "-std=c11", "-O2", "-fPIC", "-shared", "-Wall",
                        "-Wextra", "-Werror", str(MODEL), "-o", str(lib)], check=True)
        fn = ctypes.CDLL(str(lib)).a04_slot_offset
        fn.argtypes = [ctypes.c_void_p, ctypes.c_size_t, ctypes.c_uint32]
        fn.restype = ctypes.c_uint32
        cases = 0
        for index in (0, 1, 2, 7, 29, 50):
            offset = 0x14c + 12 * index
            for value in (0, 1, MASK, 0x7fffffff, 0x80000000, 0x12345678):
                memory = bytearray(b"\xa5" * 0x1000)
                memory[offset:offset+4] = value.to_bytes(4, "little")
                buf = (ctypes.c_uint8 * len(memory)).from_buffer(memory)
                expected_offset = fn(buf, len(memory), index)
                expected_result = 0 if value == MASK else BASE + expected_offset
                for flags in (0, 0x20000000, 0x40000000, 0xf0000000):
                    actual = execute(code, index, value, flags)
                    if actual != expected_result:
                        raise AssertionError(f"ARM/C mismatch: {index=}, {value=}, {flags=}")
                    cases += 1
    print(json.dumps({"elf_sha256": SHA, "entry": "000b45d0",
                      "cases": cases, "failures": 0, "certificates_created": 0,
                      "scope": "bounded_aligned_inputs"}))


if __name__ == "__main__":
    main()
