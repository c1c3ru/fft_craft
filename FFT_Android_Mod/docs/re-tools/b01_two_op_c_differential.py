#!/usr/bin/env python3
"""B01 bounded original-ELF A32 two-op differential against independent C11.

Whitelist: non-flag-setting ALU into R1..R12 followed by one LDR/STR/LDRB/
STRB via fixed R0. Only two opcodes are executed; no arbitrary calls/branches.
Never treats execution of a prefix as function-level semantic equivalence.
"""
import argparse
import ctypes
import hashlib
import json
import subprocess
import tempfile
from pathlib import Path

from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
from elftools.elf.elffile import ELFFile
from unicorn import (Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_PROT_ALL, UC_HOOK_CODE,
                     UC_HOOK_MEM_READ, UC_HOOK_MEM_WRITE)
from unicorn.arm_const import (UC_ARM_REG_CPSR, UC_ARM_REG_PC, UC_ARM_REG_SP,
    UC_ARM_REG_LR, UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2,
    UC_ARM_REG_R3, UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6,
    UC_ARM_REG_R7, UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10,
    UC_ARM_REG_R11, UC_ARM_REG_R12)

import b01_overlap_elf_evidence as baseline
import b01_safe_alu_differential as alu

DATA_BASE = 0x500000
MEM_SIZE = 0x800
CANARY = bytes.fromhex("5ac37e19d2f084b16e495a211bd0ac73")
MAX_REAL_PAIR_SAMPLES = 32
REPETITIONS = 12
REGS = (UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3,
        UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7,
        UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11,
        UC_ARM_REG_R12)


def safe_memory_op(raw):
    """No register shift, no writeback or negative/conditional accesses."""
    if len(raw) != 4:
        return None
    w = int.from_bytes(raw, "little")
    if (w >> 28 != 14 or ((w >> 26) & 3) != 1 or
            ((w >> 25) & 1) or not ((w >> 24) & 1) or
            not ((w >> 23) & 1) or ((w >> 21) & 1) or
            ((w >> 16) & 15) != 0):
        return None
    rt = (w >> 12) & 15
    offset = w & 0xfff
    width = 1 if ((w >> 22) & 1) else 4
    if not 1 <= rt <= 12 or offset > 0x500 or (width == 4 and offset % 4):
        return None
    load = bool((w >> 20) & 1)
    return {"mnemonic": ("ldr" if load else "str") + ("b" if width == 1 else ""),
            "rt": rt, "offset": offset, "width": width, "load": load,
            "raw_hex": raw.hex()}


def safe_pair(raw, address, disassembler):
    if len(raw) != 8 or address % 4:
        return None
    first = alu.decode_safe(raw[:4])
    second = safe_memory_op(raw[4:])
    if not first or not second or first["dest"] == 0:
        return None
    inst = list(disassembler.disasm(raw, address))
    if (len(inst) != 2 or inst[0].size != 4 or inst[1].size != 4
            or inst[0].mnemonic != first["opcode"]
            or inst[1].mnemonic != second["mnemonic"]):
        return None
    return {"first": first, "second": second}


def build_c_model(path, destination):
    subprocess.run(["cc", "-std=c11", "-O2", "-Wall", "-Wextra", "-Werror",
                    "-pedantic", "-fPIC", "-shared", str(path), "-o",
                    str(destination)], check=True, capture_output=True)
    library = ctypes.CDLL(str(destination))
    fn = library.b01_two_op_model
    fn.argtypes = [ctypes.c_uint32, ctypes.c_uint32,
                   ctypes.POINTER(ctypes.c_uint32),
                   ctypes.POINTER(ctypes.c_uint8), ctypes.c_size_t]
    fn.restype = ctypes.c_int
    return fn


def sample_state(seed):
    registers = [(seed ^ (i * 0x11111111)) & 0xffffffff for i in range(13)]
    registers[0] = DATA_BASE
    memory = bytearray(((i * 29) + seed) & 255 for i in range(MEM_SIZE))
    memory[0x780:0x790] = CANARY
    return registers, memory


def differential_two(addr, code, contract, model, seed, flags):
    regs, memory = sample_state(seed)
    reg_buf = (ctypes.c_uint32 * len(regs))(*regs)
    mem_buf = (ctypes.c_uint8 * MEM_SIZE).from_buffer_copy(memory)
    first, second = (int.from_bytes(code[:4], "little"),
                     int.from_bytes(code[4:], "little"))
    rc = model(first, second, reg_buf, mem_buf, MEM_SIZE)
    if rc != 0:
        raise AssertionError(f"Independent C model unexpectedly refused eligible pair ({rc})")
    expected_regs = list(reg_buf)
    expected_mem = bytes(mem_buf)
    if expected_mem[0x780:0x790] != CANARY:
        raise AssertionError("Reference C corrupted memory canary")

    emu = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    pages = sorted({addr & ~0xfff, (addr + 4) & ~0xfff, DATA_BASE})
    for page in pages:
        emu.mem_map(page, 0x1000, UC_PROT_ALL)
    emu.mem_write(addr, code)
    emu.mem_write(DATA_BASE, memory)
    emu.reg_write(UC_ARM_REG_CPSR, 0x10 | flags)
    for register, value in zip(REGS, regs):
        emu.reg_write(register, value)
    emu.reg_write(UC_ARM_REG_SP, 0x700ffc)
    emu.reg_write(UC_ARM_REG_LR, 0x710000)
    trace, reads, writes = [], [], []

    def track_code(u, pc, size, unused):
        trace.append(pc)
    def track_read(u, access, location, size, val, unused):
        reads.append((location, size))
    def track_write(u, access, location, size, value, unused):
        writes.append((location, size, value & ((1 << (size*8)) - 1)))
    emu.hook_add(UC_HOOK_CODE, track_code)
    emu.hook_add(UC_HOOK_MEM_READ, track_read)
    emu.hook_add(UC_HOOK_MEM_WRITE, track_write)
    emu.emu_start(addr, addr + 8, timeout=1_000_000, count=2)
    if trace != [addr, addr + 4] or emu.reg_read(UC_ARM_REG_PC) != addr + 8:
        raise AssertionError("Original A32 prefix changed control flow")
    if [emu.reg_read(r) for r in REGS] != expected_regs:
        raise AssertionError("ARM vs independent C register mismatch")
    if bytes(emu.mem_read(DATA_BASE, MEM_SIZE)) != expected_mem:
        raise AssertionError("ARM vs C memory mismatch, including canary")
    spec = contract["second"]
    location = DATA_BASE + spec["offset"]
    if spec["load"]:
        if reads != [(location, spec["width"])] or writes:
            raise AssertionError("Unexpected ARM memory read footprint")
    else:
        value = expected_regs[spec["rt"]] & ((1 << (8*spec["width"])) - 1)
        if writes != [(location, spec["width"], value)] or reads:
            raise AssertionError("Unexpected ARM memory write footprint")
    if emu.reg_read(UC_ARM_REG_SP) != 0x700ffc or emu.reg_read(UC_ARM_REG_LR) != 0x710000:
        raise AssertionError("Stack or link register changed")
    if (emu.reg_read(UC_ARM_REG_CPSR) & 0xf000003f) != (flags | 0x10):
        raise AssertionError("CPSR unexpectedly changed")
    return True


def audit(binary, inventory, c_source, maximum=MAX_REAL_PAIR_SAMPLES):
    if baseline.sha256(binary) != baseline.PINNED_ELF_SHA:
        raise ValueError("Original ELF changed")
    if maximum < 1 or maximum > 64:
        raise ValueError("Invalid bounded pair limit")
    entries = baseline.get_entries(inventory)
    overlap = baseline.get_pairs(entries)
    if len(overlap) != 15:
        raise ValueError("Original overlap inventory changed")
    overlap_addresses = {x["start"] for pair in overlap for x in pair}
    decoder = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    selected = []
    with binary.open("rb") as file:
        elf = ELFFile(file)
        if elf.elfclass != 32 or not elf.little_endian or elf["e_machine"] != "EM_ARM":
            raise ValueError("Original ELF architecture changed")
        for item in sorted(entries, key=lambda x: (x["start"] not in overlap_addresses,x["start"])):
            if item["size"] < 8:
                continue
            raw, offset = baseline.read_executable(elf, file, item["start"], 8)
            if raw is None:
                continue
            pair = safe_pair(raw, item["start"], decoder)
            if pair is not None:
                selected.append((item["start"], raw, pair, offset))
            if len(selected) >= maximum:
                break
    with tempfile.TemporaryDirectory(prefix="b01-c-model-") as tmp:
        model = build_c_model(c_source, Path(tmp) / "b01_two_op.so")
        results = []
        for addr, raw, pair, offset in selected:
            count = 0
            for seed in (0,1,0xffffffff,0x7fffffff,0x12345678,0x80000000):
                for flags in (0,0xf0000000):
                    differential_two(addr, raw, pair, model, seed, flags)
                    count += 1
            results.append({
                "entry": f"{addr:08x}", "two_original_opcode_bytes": raw.hex(),
                "file_offset": offset, "contract": pair,
                "is_overlap_entry": addr in overlap_addresses,
                "bounded_differential_samples_passed": count,
                "full_function_equivalence": False
            })
    return {
        "schema":1, "elf_sha256":baseline.PINNED_ELF_SHA,
        "model_sha256":hashlib.sha256(c_source.read_bytes()).hexdigest(),
        "inventory_sha256":baseline.sha256(inventory),
        "unique_entrypoints_scanned":len(entries),
        "safe_two_opcode_entries":len(results),
        "bounded_samples_passed":sum(x["bounded_differential_samples_passed"] for x in results),
        "results":results,
        "whole_function_equivalence_proven":False,
        "original_process_execution_proven":False,
        "new_semantic_certificates":0,
        "B01_done":False
    }


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--binary",type=Path,required=True)
    p.add_argument("--inventory",type=Path,required=True)
    p.add_argument("--model",type=Path,default=Path(__file__).parent/"c-models/b01_two_op.c")
    p.add_argument("--output",type=Path,required=True)
    args=p.parse_args()
    r=audit(args.binary,args.inventory,args.model)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(r,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print("B01_ORIGINAL_ELF_ENTRIES_SCANNED="+str(r["unique_entrypoints_scanned"]))
    print("B01_TWO_OPCODE_C_MODEL_CANDIDATES="+str(r["safe_two_opcode_entries"]))
    print("B01_TWO_OPCODE_DIFFERENTIAL_SAMPLES_PASSED="+str(r["bounded_samples_passed"]))
    print("B01_NEW_FULL_FUNCTION_CERTIFICATES=0")


if __name__ == "__main__":
    main()
