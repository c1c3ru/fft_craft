#!/usr/bin/env python3
"""Bounded original ARM 0xb942c loop versus independent C, with synthetic strlen.

The real ARM code for the loop, its Shift-JIS helper and the PLT veneer runs
in Unicorn; only libc strlen is represented by a purpose-built return stub.
This is not a proof of the full 0xb6620/strcpy flow or of Android libc.
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
                               UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7,
                               UC_ARM_REG_R8)
import semantic_evidence
from semantic_a04_714a0_slot import SHA
from semantic_a04_b942c_strlen import veneer_slot, slot_relocation, check_import

ROOT = Path(__file__).resolve().parents[2]
BINARY = ROOT / "src/lib/armeabi/libgl2jni.so"
MODELS = Path(__file__).resolve().parent / "c-models"
ENTRY, HELPER, VENEER = 0xb942c, 0xb8be4, 0x71494
SLOT, STUB, RETURN = 0x347d6c, 0x720000, 0x730000
DATA, STACK, SP = 0x500000, 0x600000, 0x600ffc
MASK = 0xffffffff
SAVED = [(UC_ARM_REG_R4, 0x11111111), (UC_ARM_REG_R5, 0x22222222),
         (UC_ARM_REG_R6, 0x33333333), (UC_ARM_REG_R7, 0x44444444),
         (UC_ARM_REG_R8, 0x55555555)]


def expected_loop(content):
    length = len(content)
    index, last_r0 = 0, 0
    last_r2 = DATA
    last_r3 = 0x66666666
    writes = []
    while index < length:
        byte = content[index]
        lead = int(0x81 <= byte <= 0x9f or 0xe0 <= byte <= 0xfc)
        last_r0, last_r3 = lead, DATA + index
        if lead:
            index += 2
        else:
            last_r2 = byte
            if byte == 0x5c:
                writes.append((DATA+index, 1, 0x2f))
            index += 1
    # Zero-length path: flags from SUBS R6,#0. Other path: CMP R6,R4.
    delta = (length-index) & MASK
    flags = ((delta >> 31) << 31) | (int(delta == 0) << 30) | (int(length >= index) << 29)
    return {"r0": last_r0, "r2": last_r2, "r3": last_r3,
            "nzcv": flags, "writes": writes}


def run_original(function, helper, veneer, content, initial_flags):
    if not content or len(content) > 250 or 0 in content:
        # Empty string is valid; corrected below. Reject NUL-bearing payloads.
        if content or len(content) > 250:
            raise ValueError("Expected bounded non-NUL bytes")
    length = len(content)
    uc = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    for page in {ENTRY & ~0xfff, HELPER & ~0xfff, VENEER & ~0xfff,
                 SLOT & ~0xfff, STUB, RETURN, DATA, STACK}:
        uc.mem_map(page, 0x1000, UC_PROT_ALL)
    uc.mem_write(ENTRY, function)
    uc.mem_write(HELPER, helper)
    uc.mem_write(VENEER, veneer)
    uc.mem_write(SLOT, STUB.to_bytes(4, "little"))
    # Synthetic libc strlen(length) returning the known size; no host libc runs.
    stub = (0xe3a00000 | length).to_bytes(4, "little") + (0xe12fff1e).to_bytes(4, "little")
    uc.mem_write(STUB, stub)
    before = bytearray(b"\xa5"*4096)
    before[:length] = content
    before[length] = 0
    uc.mem_write(DATA, bytes(before))
    stack_original = bytes(b"\xcc"*4096)
    uc.mem_write(STACK, stack_original)
    uc.reg_write(UC_ARM_REG_CPSR, initial_flags | 0x10)
    for reg, val in SAVED:
        uc.reg_write(reg, val)
    for reg, val in ((UC_ARM_REG_R0, 0x2f), (UC_ARM_REG_R1, 0x5c),
                     (UC_ARM_REG_R2, DATA), (UC_ARM_REG_R3, 0x66666666),
                     (UC_ARM_REG_SP, SP), (UC_ARM_REG_LR, RETURN)):
        uc.reg_write(reg, val)
    pcs, writes = [], []
    def on_code(em, pc, size, unused):
        pcs.append(pc)
        if pc == RETURN:
            em.emu_stop()
            return
        allowed = ((ENTRY <= pc <= 0xb9480) or (HELPER <= pc <= 0xb8c04)
                   or (VENEER <= pc <= VENEER+8) or (STUB <= pc <= STUB+4))
        if not allowed:
            raise AssertionError(f"Unmodeled ARM PC {pc:08x}")
    uc.hook_add(UC_HOOK_CODE, on_code)
    uc.hook_add(UC_HOOK_MEM_WRITE, lambda em, access, addr, width, value, unused:
                writes.append((addr, width, value & ((1 << (8 * width))-1))))
    uc.emu_start(ENTRY, RETURN+4, count=1200, timeout=2_000_000)
    if not pcs or pcs[-1] != RETURN or uc.reg_read(UC_ARM_REG_PC) != RETURN:
        raise AssertionError(f"Loop failed to return: last PCs {pcs[-12:]}")
    expected = expected_loop(content)
    model_buffer = bytearray(before)
    for addr, size, val in expected["writes"]:
        model_buffer[addr-DATA] = val
    if bytes(uc.mem_read(DATA, 4096)) != model_buffer:
        raise AssertionError(f"Original loop memory differs for {content.hex()}")
    if any(uc.reg_read(reg) != val for reg, val in SAVED):
        raise AssertionError("Callee-saved registers not restored")
    for reg, value in ((UC_ARM_REG_R0, expected["r0"]),
                       (UC_ARM_REG_R1, 0x5c), (UC_ARM_REG_R2, expected["r2"]),
                       (UC_ARM_REG_R3, expected["r3"]),
                       (UC_ARM_REG_LR, RETURN), (UC_ARM_REG_SP, SP)):
        if uc.reg_read(reg) != value:
            raise AssertionError(f"Unexpected ARM register {reg} for {content.hex()}")
    if (uc.reg_read(UC_ARM_REG_CPSR) & 0xf0000000) != expected["nzcv"]:
        raise AssertionError(f"Loop NZCV mismatch for {content.hex()}")
    saved_words = [v for _, v in SAVED] + [RETURN]
    stack_expected = bytearray(stack_original)
    expected_stack_writes = []
    for i, val in enumerate(saved_words):
        addr = SP-24+4*i
        expected_stack_writes.append((addr, 4, val))
        stack_expected[addr-STACK:addr-STACK+4] = val.to_bytes(4, "little")
    if bytes(uc.mem_read(STACK, 4096)) != stack_expected:
        raise AssertionError("Unmodeled original stack effects")
    if sorted(writes) != sorted(expected_stack_writes + expected["writes"]):
        raise AssertionError(f"Unexpected original writes: {writes}")
    return bytes(model_buffer)


def main():
    if hashlib.sha256(BINARY.read_bytes()).hexdigest() != SHA:
        raise ValueError("Original ARM ELF identity changed")
    v = veneer_slot(BINARY)
    if v["slot"] != f"{SLOT:08x}":
        raise ValueError("GOT slot mismatch")
    check_import(v, slot_relocation(BINARY, SLOT))
    function = semantic_evidence.read_function(BINARY, ENTRY, 0x58)
    helper = semantic_evidence.read_function(BINARY, HELPER, 36)
    veneer = semantic_evidence.read_function(BINARY, VENEER, 12)
    if [i.mnemonic for i in Cs(CS_ARCH_ARM, CS_MODE_ARM).disasm(helper, HELPER)] != [
            "add", "add", "and", "and", "cmp", "cmphi", "movhi", "movls", "bx"]:
        raise ValueError("Shift-JIS helper opcode baseline changed")
    with tempfile.TemporaryDirectory(prefix="a04-sjis-loop-") as tmp:
        so = Path(tmp) / "loop.so"
        subprocess.run(["cc", "-std=c11", "-O2", "-Wall", "-Wextra", "-Werror",
                        "-fPIC", "-shared",
                        str(MODELS / "a04_sjis_lead.c"),
                        str(MODELS / "a04_sjis_slash_loop.c"),
                        "-o", str(so)], check=True)
        fn = ctypes.CDLL(str(so)).a04_normalize_sjis_slashes
        fn.argtypes = [ctypes.c_void_p, ctypes.c_size_t]
        fn.restype = ctypes.c_int
        samples = [b"", b"abc", b"\\", b"a\\b\\c", b"\\root\\dir",
                   b"\x81\\", b"\x9f\\", b"\xe0\\", b"\xfc\\",
                   b"\x80\\", b"\xfd\\", b"\x81\\abc", b"foo\\\xe0\\bar"]
        samples += [bytes([c]) for c in range(1, 256)]
        samples += [bytes([c, 0x5c, 0x41]) for c in
                    (0x40, 0x5c, 0x80, 0x81, 0x9f, 0xa0, 0xdf, 0xe0, 0xfc, 0xfd)]
        count = 0
        for content in samples:
            for flags in (0, 0xf0000000):
                original = run_original(function, helper, veneer, content, flags)
                data = bytearray(b"\xa5" * 4096)
                data[:len(content)] = content
                data[len(content)] = 0
                buf = (ctypes.c_uint8 * len(data)).from_buffer(data)
                if fn(buf, len(data)) != 1 or bytes(data) != original:
                    raise AssertionError(f"Independent C differs for {content.hex()}")
                count += 1
    print(json.dumps({"elf_sha256": SHA, "entry": f"{ENTRY:08x}",
                      "cases": count, "failures": 0,
                      "strlen": "synthetic_return_stub_only",
                      "shift_jis_helper": "original_arm_executed",
                      "strcpy": "not_executed",
                      "new_certificates": 0}))


if __name__ == "__main__":
    main()
