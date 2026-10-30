#!/usr/bin/env python3
"""B01: bounded one-instruction A32 ALU differential, original ELF vs Python model.

Only unconditional, S=0 ALU operations involving R0..R12 are eligible.
No calls, stack, memory ops, PC modifications or indirect branches are run.
A one-instruction comparison is NOT a whole function semantic certificate.
"""
import argparse
import json
from pathlib import Path

from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
from unicorn import (Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_PROT_ALL,
                     UC_HOOK_MEM_READ, UC_HOOK_MEM_WRITE)
from unicorn.arm_const import (UC_ARM_REG_CPSR, UC_ARM_REG_PC, UC_ARM_REG_SP,
                               UC_ARM_REG_LR, UC_ARM_REG_R0, UC_ARM_REG_R1,
                               UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_R4,
                               UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7,
                               UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10,
                               UC_ARM_REG_R11, UC_ARM_REG_R12)
from elftools.elf.elffile import ELFFile

import b01_overlap_elf_evidence as baseline

MASK = 0xffffffff
REGS = (UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3,
        UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7,
        UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11, UC_ARM_REG_R12)
OPNAMES = {0: "and", 1: "eor", 2: "sub", 4: "add", 12: "orr", 13: "mov"}


def ror(value, bits):
    bits %= 32
    return ((value >> bits) | ((value << (32-bits)) & MASK)) & MASK if bits else value & MASK


def decode_safe(raw):
    if len(raw) != 4:
        return None
    w = int.from_bytes(raw, "little")
    if (w >> 28 != 14 or ((w >> 26) & 3) != 0 or ((w >> 20) & 1) != 0):
        return None
    op = (w >> 21) & 15
    if op not in OPNAMES:
        return None
    dest, source = (w >> 12) & 15, (w >> 16) & 15
    if dest > 12 or (op != 13 and source > 12):
        return None
    imm_mode = bool((w >> 25) & 1)
    if imm_mode:
        operand = ror(w & 255, 2 * ((w >> 8) & 15))
    else:
        # Reject all shifts, RRX, register-controlled shifts, and PC/SP.
        if (w & 0xff0) != 0:
            return None
        operand = w & 15
        if operand > 12:
            return None
    return {
        "opcode": OPNAMES[op], "dest": dest, "source": source if op != 13 else None,
        "immediate": imm_mode, "operand": operand,
        "raw_hex": raw.hex()
    }


def expected_result(spec, registers):
    operand = spec["operand"] if spec["immediate"] else registers[spec["operand"]]
    lhs = registers[spec["source"]] if spec["source"] is not None else 0
    operation = spec["opcode"]
    if operation == "mov":
        value = operand
    elif operation == "add":
        value = lhs + operand
    elif operation == "sub":
        value = lhs - operand
    elif operation == "and":
        value = lhs & operand
    elif operation == "eor":
        value = lhs ^ operand
    elif operation == "orr":
        value = lhs | operand
    else:
        raise AssertionError("Unrecognized ALU")
    out = registers.copy()
    out[spec["dest"]] = value & MASK
    return out


def execute_one(addr, raw, spec, seed, flags):
    baseline_regs = [(seed ^ (i * 0x11111111)) & MASK for i in range(13)]
    expected = expected_result(spec, baseline_regs)
    uc = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    uc.mem_map(addr & ~0xfff, 0x1000, UC_PROT_ALL)
    uc.mem_write(addr, raw)
    uc.reg_write(UC_ARM_REG_CPSR, 0x10 | flags)
    for r, val in zip(REGS, baseline_regs):
        uc.reg_write(r, val)
    uc.reg_write(UC_ARM_REG_SP, 0x700ffc)
    uc.reg_write(UC_ARM_REG_LR, 0x710000)
    accesses = []
    def on_memory(emu, kind, location, size, value, _user):
        accesses.append((location, size))
    uc.hook_add(UC_HOOK_MEM_READ, on_memory)
    uc.hook_add(UC_HOOK_MEM_WRITE, on_memory)
    uc.emu_start(addr, addr + 4, timeout=500_000, count=1)
    if accesses:
        raise AssertionError("Unexpected ALU memory side effects")
    if [uc.reg_read(r) for r in REGS] != expected:
        raise AssertionError("Single instruction ELF ARM differs from independent ALU model")
    if uc.reg_read(UC_ARM_REG_SP) != 0x700ffc or uc.reg_read(UC_ARM_REG_LR) != 0x710000:
        raise AssertionError("SP/LR changed")
    if uc.reg_read(UC_ARM_REG_PC) != addr + 4:
        raise AssertionError("Unexpected PC transfer")
    if (uc.reg_read(UC_ARM_REG_CPSR) & 0xf000003f) != (flags | 0x10):
        raise AssertionError("CPSR changed")
    return True


def audit(binary, inventory):
    if baseline.sha256(binary) != baseline.PINNED_ELF_SHA:
        raise ValueError("Original ELF mismatch")
    entries = baseline.get_entries(inventory)
    pairs = baseline.get_pairs(entries)
    if len(pairs) != 15:
        raise ValueError("B01 inventory changed")
    candidates = sorted({row["start"] for pair in pairs for row in pair})
    md = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    outcomes = []
    with binary.open("rb") as handle:
        elf = ELFFile(handle)
        if elf["e_machine"] != "EM_ARM":
            raise ValueError("Not ARM ELF")
        for addr in candidates:
            raw, _offset = baseline.read_executable(elf, handle, addr, 4)
            if raw is None:
                raise ValueError("Entry is not file-backed executable")
            contract = decode_safe(raw)
            d = list(md.disasm(raw, addr))
            if contract is not None and (len(d) != 1 or d[0].mnemonic != contract["opcode"]):
                raise ValueError("Independent Capstone opcode disagrees with ALU decoder")
            samples = 0
            if contract is not None:
                for seed in (0, 1, 0x7fffffff, 0xffffffff, 0x12345678):
                    for flags in (0, 0xf0000000):
                        execute_one(addr, raw, contract, seed, flags)
                        samples += 1
            outcomes.append({
                "entry": f"{addr:08x}", "first_opcode_hex": raw.hex(),
                "safe_alu_contract": contract,
                "single_instruction_differential_samples_passed": samples,
                "whole_function_executed": False,
                "callers_or_callees_executed": False,
            })
    return {
        "schema": 1, "stage": "B01",
        "elf_sha256": baseline.PINNED_ELF_SHA,
        "entries_examined": len(candidates),
        "safe_ALU_entries": sum(x["safe_alu_contract"] is not None for x in outcomes),
        "single_instruction_samples_passed": sum(x["single_instruction_differential_samples_passed"] for x in outcomes),
        "entries": outcomes, "failures": 0,
        "original_function_equivalence_proven": False,
        "new_semantic_certificates": 0, "B01_done": False,
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--binary", type=Path, required=True)
    p.add_argument("--inventory", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    a = p.parse_args()
    result = audit(a.binary, a.inventory)
    a.output.parent.mkdir(parents=True, exist_ok=True)
    a.output.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print("B01_ELF_ENTRIES_EXAMINED="+str(result["entries_examined"]))
    print("B01_ELIGIBLE_ALU_PREFIXES="+str(result["safe_ALU_entries"]))
    print("B01_DIFFERENTIAL_SAMPLES_PASSED="+str(result["single_instruction_samples_passed"]))
    print("B01_FULL_FUNCTION_CERTIFICATES=0")


if __name__ == "__main__":
    main()
