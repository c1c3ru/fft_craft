#!/usr/bin/env python3
"""Differential entire A04 R1!=0 path: original ELF ARM + modeled libc imports.

Runs original ARM caller 0xb6620, both original PLT veneers, the original
0xb942c normalization loop, and original Shift-JIS helper 0xb8be4.
Only imported strcpy/strlen are replaced by explicitly bounded deterministic
ABI stubs. This does NOT execute Android libc or certify unsafe inputs.
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
from unicorn.arm_const import (
    UC_ARM_REG_CPSR, UC_ARM_REG_PC, UC_ARM_REG_LR, UC_ARM_REG_SP,
    UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3,
    UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7,
    UC_ARM_REG_R8, UC_ARM_REG_IP)
import semantic_evidence
from semantic_a04_714a0_slot import SHA, elf_provenance
from semantic_a04_714a0_strcpy import verify_strcpy_provenance
from semantic_a04_b942c_strlen import veneer_slot, slot_relocation, check_import
from semantic_a04_sjis_loop_differential import expected_loop

ROOT = Path(__file__).resolve().parents[2]
BINARY = ROOT / "src/lib/armeabi/libgl2jni.so"
MODELS = Path(__file__).resolve().parent / "c-models"
CALLER, LOOP, HELPER = 0xb6620, 0xb942c, 0xb8be4
PLT_COPY, PLT_LEN = 0x714a0, 0x71494
GOT_COPY, GOT_LEN = 0x347d70, 0x347d6c
COPY_STUB, LEN_STUB = 0x720000, 0x721000
RETURN, DATA, SOURCE, STACK, SP = 0x730000, 0x500000, 0x510000, 0x600000, 0x600ffc
META_OFFSET, SIZE = 0x104, 0x1000
REG_SAVED = ((UC_ARM_REG_R4, 0x11111111), (UC_ARM_REG_R5, 0x22222222),
             (UC_ARM_REG_R6, 0x33333333), (UC_ARM_REG_R7, 0x44444444),
             (UC_ARM_REG_R8, 0x55555555))


def original_sections():
    if hashlib.sha256(BINARY.read_bytes()).hexdigest() != SHA:
        raise ValueError("A04 ELF SHA-256 identity drift")
    verify_strcpy_provenance(elf_provenance(BINARY))
    v = veneer_slot(BINARY)
    check_import(v, slot_relocation(BINARY, GOT_LEN))
    caller = semantic_evidence.read_function(BINARY, CALLER, 0x34)
    loop = semantic_evidence.read_function(BINARY, LOOP, 0x58)
    helper = semantic_evidence.read_function(BINARY, HELPER, 36)
    copy_plt = semantic_evidence.read_function(BINARY, PLT_COPY, 12)
    len_plt = semantic_evidence.read_function(BINARY, PLT_LEN, 12)
    cs = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    caller_ops = list(cs.disasm(caller, CALLER))
    expected_caller = ["cmp","push","mov","beq","bl","mov","mov","mov",
                       "bl","mov","str","mov","pop"]
    if [op.mnemonic for op in caller_ops] != expected_caller:
        raise ValueError("Original A04 caller opcodes changed")
    if [op.mnemonic for op in cs.disasm(helper, HELPER)] != [
            "add","add","and","and","cmp","cmphi","movhi","movls","bx"]:
        raise ValueError("Original A04 lead-byte helper changed")
    return caller, loop, helper, copy_plt, len_plt


def run_original(sections, content, seed, flags):
    if len(content) > 128 or b"\x00" in content:
        raise ValueError("Only bounded NUL-free source contents accepted")
    caller, loop, helper, copy_plt, len_plt = sections
    em = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    pages = {CALLER & ~0xfff, LOOP & ~0xfff, HELPER & ~0xfff,
             PLT_COPY & ~0xfff, GOT_COPY & ~0xfff, COPY_STUB,
             LEN_STUB, RETURN, DATA, SOURCE, STACK}
    for page in pages:
        em.mem_map(page, SIZE, UC_PROT_ALL)
    for addr, code in ((CALLER,caller),(LOOP,loop),(HELPER,helper),
                       (PLT_COPY,copy_plt),(PLT_LEN,len_plt)):
        em.mem_write(addr, code)
    em.mem_write(GOT_COPY, COPY_STUB.to_bytes(4,"little"))
    em.mem_write(GOT_LEN, LEN_STUB.to_bytes(4,"little"))
    # Both stubs execute only BX LR. Their data transformations happen
    # explicitly in the code hook and are audited separately from ARM writes.
    bx_lr = (0xe12fff1e).to_bytes(4,"little")
    em.mem_write(COPY_STUB, bx_lr)
    em.mem_write(LEN_STUB, bx_lr)
    before = bytearray(b"\xa5"*SIZE)
    before[META_OFFSET:META_OFFSET+4] = seed.to_bytes(4,"little")
    src_before = bytearray(b"\x7c"*SIZE)
    src_before[:len(content)] = content
    src_before[len(content)] = 0
    stack_before = bytes(b"\xcc"*SIZE)
    em.mem_write(DATA, bytes(before))
    em.mem_write(SOURCE, bytes(src_before))
    em.mem_write(STACK, stack_before)
    em.reg_write(UC_ARM_REG_CPSR, 0x10 | flags)
    for reg, value in REG_SAVED:
        em.reg_write(reg, value)
    for reg, val in ((UC_ARM_REG_R0, DATA), (UC_ARM_REG_R1, SOURCE),
                     (UC_ARM_REG_R2, 0x2222ffff), (UC_ARM_REG_R3, 0x66666666),
                     (UC_ARM_REG_SP, SP), (UC_ARM_REG_LR, RETURN),
                     (UC_ARM_REG_IP, 0xdeadbeef)):
        em.reg_write(reg,val)
    pcs, arm_reads, arm_writes, libc_events = [], [], [], []
    def on_code(uc, pc, size, unused):
        pcs.append(pc)
        if pc == RETURN:
            uc.emu_stop()
            return
        if pc == COPY_STUB:
            dest = uc.reg_read(UC_ARM_REG_R0)
            src = uc.reg_read(UC_ARM_REG_R1)
            if dest != DATA or src != SOURCE:
                raise AssertionError(f"strcpy stub ABI arguments differ: {dest:x}, {src:x}")
            original = bytes(uc.mem_read(SOURCE, len(content)+1))
            if original != content + b"\x00":
                raise AssertionError("Modeled source differs from actual mapped bytes")
            uc.mem_write(DATA, original)
            libc_events.append(("strcpy", DATA, SOURCE, len(content)+1))
            uc.reg_write(UC_ARM_REG_R0, DATA)
        elif pc == LEN_STUB:
            ptr = uc.reg_read(UC_ARM_REG_R0)
            if ptr != DATA:
                raise AssertionError("strlen stub received unexpected pointer")
            observed = bytes(uc.mem_read(DATA, len(content)+1))
            if observed != content + b"\x00":
                raise AssertionError("strlen stub observed incorrect copied bytes")
            uc.reg_write(UC_ARM_REG_R0, len(content))
            libc_events.append(("strlen", DATA, len(content)))
        else:
            safe = ((CALLER <= pc <= 0xb6650) or
                    (LOOP <= pc <= 0xb9480) or
                    (HELPER <= pc <= 0xb8c04) or
                    (PLT_COPY <= pc <= PLT_COPY+8) or
                    (PLT_LEN <= pc <= PLT_LEN+8))
            if not safe:
                raise AssertionError(f"Unrecognized original ARM PC: {pc:08x}")
    def on_read(uc, kind, address, size, value, unused):
        arm_reads.append((address, size))
        if (address in (GOT_COPY, GOT_LEN) and size == 4):
            return
        if STACK <= address < STACK+SIZE and size == 4:
            return
        if DATA <= address <= DATA+len(content) and size == 1:
            return
        raise AssertionError(f"Unmodeled ARM read: {address:08x} {size}")
    def on_write(uc, kind, address, size, value, unused):
        val = value & ((1 << (8*size))-1)
        arm_writes.append((address, size, val))
        if STACK <= address < STACK+SIZE and size == 4:
            return
        if DATA <= address < DATA+len(content) and size == 1 and val == 0x2f:
            return
        if address == DATA+META_OFFSET and size == 4 and val == 0:
            return
        raise AssertionError(f"Unmodeled ARM write: {address:08x} {size} {val:x}")
    em.hook_add(UC_HOOK_CODE, on_code)
    em.hook_add(UC_HOOK_MEM_READ, on_read)
    em.hook_add(UC_HOOK_MEM_WRITE, on_write)
    em.emu_start(CALLER, RETURN+4, timeout=4_000_000, count=1500)
    if not pcs or pcs[-1] != RETURN or em.reg_read(UC_ARM_REG_PC) != RETURN:
        raise AssertionError(f"Main A04 did not reach return: {pcs[-12:]}")
    if [event[0] for event in libc_events] != ["strcpy","strlen"]:
        raise AssertionError(f"Unexpected imported call sequence: {libc_events}")
    if [pc for pc in pcs if pc == COPY_STUB] != [COPY_STUB]:
        raise AssertionError("Expected exactly one imported strcpy stub execution")
    if [pc for pc in pcs if pc == LEN_STUB] != [LEN_STUB]:
        raise AssertionError("Expected exactly one imported strlen stub execution")
    if any(em.reg_read(r) != v for r,v in REG_SAVED):
        raise AssertionError("Callee-saved R4-R8 were not restored")
    if em.reg_read(UC_ARM_REG_R0) != DATA or em.reg_read(UC_ARM_REG_R1) != 0x5c:
        raise AssertionError("A04 caller ABI return or argument registers differ")
    if em.reg_read(UC_ARM_REG_R3) != 0 or em.reg_read(UC_ARM_REG_SP) != SP:
        raise AssertionError("A04 caller R3/SP did not match")
    if em.reg_read(UC_ARM_REG_LR) != 0xb6644:
        raise AssertionError("Original ARM BL left unexpected volatile LR")
    if em.reg_read(UC_ARM_REG_IP) != GOT_LEN:
        raise AssertionError("Original strlen PLT did not write back IP")
    loop_expected = expected_loop(content)
    if em.reg_read(UC_ARM_REG_R2) != loop_expected["r2"]:
        raise AssertionError("Unexpected loop R2")
    if (em.reg_read(UC_ARM_REG_CPSR) & 0xf0000000) != loop_expected["nzcv"]:
        raise AssertionError("Unexpected loop flags")
    copy_expected = bytearray(before)
    copy_expected[:len(content)+1] = content + b"\x00"
    for addr, size, value in loop_expected["writes"]:
        copy_expected[addr-DATA] = value
    copy_expected[META_OFFSET:META_OFFSET+4] = b"\x00"*4
    if bytes(em.mem_read(DATA, SIZE)) != copy_expected:
        raise AssertionError(f"ARM final destination differs for {content.hex()}")
    if bytes(em.mem_read(SOURCE,SIZE)) != src_before:
        raise AssertionError("Original ARM modified source buffer")
    stack_expected = bytearray(stack_before)
    main_push = [(SP-8,4,REG_SAVED[0][1]),(SP-4,4,RETURN)]
    inner_push = [(SP-32,4,DATA),(SP-28,4,REG_SAVED[1][1]),
                  (SP-24,4,REG_SAVED[2][1]),(SP-20,4,REG_SAVED[3][1]),
                  (SP-16,4,REG_SAVED[4][1]),(SP-12,4,0xb6644)]
    expected_writes = main_push + inner_push + loop_expected["writes"] + [
        (DATA+META_OFFSET,4,0)]
    if sorted(arm_writes) != sorted(expected_writes):
        raise AssertionError(f"ARM stack/string write trace diverges: {arm_writes}")
    for addr, size, val in main_push + inner_push:
        stack_expected[addr-STACK:addr-STACK+size] = val.to_bytes(size,"little")
    if bytes(em.mem_read(STACK,SIZE)) != stack_expected:
        raise AssertionError("Original ARM stack contents differ")
    for addr, width in arm_reads:
        if addr in (GOT_COPY, GOT_LEN) and width != 4:
            raise AssertionError("Unexpected veneer pointer read")
    if (GOT_COPY,4) not in arm_reads or (GOT_LEN,4) not in arm_reads:
        raise AssertionError("One of two original veneer GOT reads missing")
    return bytes(copy_expected)


def main():
    sections = original_sections()
    with tempfile.TemporaryDirectory(prefix="a04-nonzero-") as temp:
        so = Path(temp)/"caller.so"
        subprocess.run(["cc","-std=c11","-O2","-Wall","-Wextra","-Werror",
                        "-fPIC","-shared",
                        str(MODELS/"a04_sjis_lead.c"),
                        str(MODELS/"a04_sjis_slash_loop.c"),
                        str(MODELS/"a04_nonzero_full.c"),
                        "-o",str(so)],check=True)
        fn = ctypes.CDLL(str(so)).a04_copy_normalize_nonzero
        fn.argtypes = [ctypes.c_void_p,ctypes.c_size_t,
                       ctypes.c_void_p,ctypes.c_size_t]
        fn.restype = ctypes.c_int
        samples = [b"",b"abc",b"\\",b"\\root\\dir",b"a\\b\\c",
                   b"\x81\\",b"\xe0\\",b"foo\\\xe0\\bar",b"\xff\\"]
        samples += [bytes([i]) for i in range(1,256)]
        samples += [bytes([i,0x5c,0x41]) for i in
                    (0x40,0x5c,0x80,0x81,0x9f,0xa0,0xdf,0xe0,0xfc,0xfd)]
        samples += [b"alpha\\beta"*5, b"\x81\\x\\z", b"\xe0\\x\\z"]
        checked = 0
        for content in samples:
            for flags in (0,0xf0000000):
                for metadata in (0,0xf0e1d2c3):
                    observed = run_original(sections,content,metadata,flags)
                    dest = bytearray(b"\xa5"*SIZE)
                    dest[META_OFFSET:META_OFFSET+4] = metadata.to_bytes(4,"little")
                    src = bytearray(b"\x7c"*SIZE)
                    src[:len(content)] = content
                    src[len(content)] = 0
                    dest_ptr = (ctypes.c_uint8*SIZE).from_buffer(dest)
                    src_ptr = (ctypes.c_uint8*SIZE).from_buffer(src)
                    if fn(dest_ptr,SIZE,src_ptr,SIZE) != 1 or bytes(dest) != observed:
                        raise AssertionError(f"ARM/C whole-path divergence: {content.hex()}")
                    expected_src = bytearray(b"\x7c"*SIZE)
                    expected_src[:len(content)] = content
                    expected_src[len(content)] = 0
                    if src != expected_src:
                        raise AssertionError("Host C modified source")
                    checked += 1
        for bad in (b"\x81"*0x104,b"\x81"*0x105):
            dest=bytearray(b"\xa5"*SIZE)
            src=bytearray(b"\x7c"*SIZE)
            src[:len(bad)] = bad
            src[len(bad)] = 0
            dp=(ctypes.c_uint8*SIZE).from_buffer(dest)
            sp=(ctypes.c_uint8*SIZE).from_buffer(src)
            if fn(dp,SIZE,sp,SIZE) != 0 or dest != bytearray(b"\xa5"*SIZE):
                raise AssertionError("C model did not reject unbounded copy")
    print(json.dumps({"elf_sha256":SHA,"caller":f"{CALLER:08x}",
                      "bounded_nonzero_cases":checked,"failures":0,
                      "original_arm_caller":True,"original_arm_sjis_loop":True,
                      "original_arm_sjis_classifier":True,
                      "original_arm_plt":True,
                      "libc_imports":"synthetic_bounded_strcpy_and_strlen",
                      "invalid_arm_inputs_executed":0,"new_certificates":0}))


if __name__=="__main__":
    main()
