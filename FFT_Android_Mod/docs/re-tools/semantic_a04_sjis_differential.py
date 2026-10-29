#!/usr/bin/env python3
"""Original ELF A32 0xb8be4 vs independently written C Shift-JIS model.

Exhaustive 8-bit inputs x four initial NZCV settings, bounded original-ELF
execution in Unicorn with all external execution forbidden.
"""
import ctypes
import hashlib
import json
import subprocess
import tempfile
from pathlib import Path

from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
from unicorn import (Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_PROT_ALL,
                     UC_HOOK_CODE, UC_HOOK_MEM_READ, UC_HOOK_MEM_WRITE)
from unicorn.arm_const import (UC_ARM_REG_CPSR, UC_ARM_REG_PC, UC_ARM_REG_LR,
                               UC_ARM_REG_SP, UC_ARM_REG_R0, UC_ARM_REG_R1,
                               UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_R4,
                               UC_ARM_REG_IP)
import semantic_evidence
from semantic_a04_714a0_slot import SHA

ROOT = Path(__file__).resolve().parents[2]
BINARY = ROOT / "src/lib/armeabi/libgl2jni.so"
MODEL = Path(__file__).resolve().parent / "c-models/a04_sjis_lead.c"
ENTRY, RETURN = 0xb8be4, 0x710000
MASK = 0xffffffff
EXPECTED_MNEMONICS = ["add", "add", "and", "and", "cmp",
                      "cmphi", "movhi", "movls", "bx"]


def model_side_effects(value):
    x = (value + 0x7f) & 0xff
    y = (value + 0x20) & 0xff
    final_cmp_left, cmp_right = (y, 0x1c) if x > 0x1e else (x, 0x1e)
    diff = (final_cmp_left - cmp_right) & MASK
    n = (diff >> 31) & 1
    z = int(diff == 0)
    carry = int(final_cmp_left >= cmp_right)
    overflow = 0  # both operands <=255; no signed ARM subtraction overflow
    nzcv = n << 31 | z << 30 | carry << 29 | overflow << 28
    return y, nzcv


def run_original(code, value, flags):
    uc = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    uc.mem_map(ENTRY & ~0xfff, 0x1000, UC_PROT_ALL)
    uc.mem_map(RETURN, 0x1000, UC_PROT_ALL)
    uc.mem_write(ENTRY, code)
    uc.reg_write(UC_ARM_REG_CPSR, 0x10 | flags)
    regs = [(UC_ARM_REG_R1, 0x12345678), (UC_ARM_REG_R2, 0x87654321),
            (UC_ARM_REG_R4, 0xdeadbeef), (UC_ARM_REG_IP, 0xbad0c0de),
            (UC_ARM_REG_SP, 0x600ffc), (UC_ARM_REG_LR, RETURN)]
    for reg, initial in regs:
        uc.reg_write(reg, initial)
    uc.reg_write(UC_ARM_REG_R0, value)
    uc.reg_write(UC_ARM_REG_R3, 0xcccccccc)
    trace, reads, writes = [], [], []
    def code_hook(emulator, pc, width, unused):
        trace.append(pc)
        if pc == RETURN:
            emulator.emu_stop()
        elif not (ENTRY <= pc < ENTRY + 36):
            raise AssertionError(f"Unknown original ARM PC 0x{pc:x}")
    uc.hook_add(UC_HOOK_CODE, code_hook)
    uc.hook_add(UC_HOOK_MEM_READ, lambda emu, typ, addr, n, val, u: reads.append((addr, n)))
    uc.hook_add(UC_HOOK_MEM_WRITE, lambda emu, typ, addr, n, val, u: writes.append((addr, n)))
    uc.emu_start(ENTRY, RETURN + 4, count=16, timeout=1000000)
    if uc.reg_read(UC_ARM_REG_PC) != RETURN or not trace or trace[-1] != RETURN:
        raise AssertionError(f"ARM routine did not reach LR sentinel: {trace}")
    if reads or writes:
        raise AssertionError(f"Unexpected ARM memory access: {reads}, {writes}")
    for reg, initial in regs:
        if uc.reg_read(reg) != initial:
            raise AssertionError(f"Unexpected preserved register change {reg}")
    r3, expected_nzcv = model_side_effects(value)
    if uc.reg_read(UC_ARM_REG_R3) != r3:
        raise AssertionError("Unexpected R3 byte arithmetic")
    if uc.reg_read(UC_ARM_REG_CPSR) & 0xf0000000 != expected_nzcv:
        raise AssertionError(f"Unexpected NZCV: value={value:x}, flags={flags:x}")
    return uc.reg_read(UC_ARM_REG_R0)


def main():
    if hashlib.sha256(BINARY.read_bytes()).hexdigest() != SHA:
        raise ValueError("A04 original ELF identity changed")
    code = semantic_evidence.read_function(BINARY, ENTRY, 36)
    ops = list(Cs(CS_ARCH_ARM, CS_MODE_ARM).disasm(code, ENTRY))
    if len(ops) != 9 or [op.mnemonic for op in ops] != EXPECTED_MNEMONICS:
        raise ValueError("Original ARM Shift-JIS instruction sequence changed")
    with tempfile.TemporaryDirectory(prefix="a04-sjis-") as directory:
        library = Path(directory) / "libsjis.so"
        subprocess.run(["cc", "-std=c11", "-O2", "-Wall", "-Wextra",
                        "-Werror", "-fPIC", "-shared", str(MODEL), "-o", str(library)],
                       check=True)
        fn = ctypes.CDLL(str(library)).a04_sjis_lead_byte
        fn.argtypes, fn.restype = [ctypes.c_uint32], ctypes.c_uint32
        cases = 0
        for byte in range(256):
            for flags in (0, 0x20000000, 0x40000000, 0xf0000000):
                model = fn(byte)
                expected = int(0x81 <= byte <= 0x9f or 0xe0 <= byte <= 0xfc)
                if model != expected:
                    raise AssertionError(f"C reference differs from independent interval oracle: {byte}")
                actual = run_original(code, byte, flags)
                if actual != model:
                    raise AssertionError(f"ARM/C mismatch {byte=}, {flags=}, {model=}, {actual=}")
                cases += 1
        for value in (0x00000181, 0x1234009f, 0xf00000fc, 0xffffffff):
            for flags in (0, 0x20000000, 0x40000000, 0xf0000000):
                if run_original(code, value, flags) != fn(value):
                    raise AssertionError(f"High-byte alias differs {value:x}")
                cases += 1
    print(json.dumps({"schema": 1, "elf_sha256": SHA, "entry": f"{ENTRY:08x}",
                      "cases": cases, "failures": 0,
                      "entire_8bit_domain_covered": True,
                      "original_subcalls_executed": 0, "new_certificates": 0,
                      "scope": "single leaf, synthetic ARM state; not string loop"}))


if __name__ == "__main__":
    main()
