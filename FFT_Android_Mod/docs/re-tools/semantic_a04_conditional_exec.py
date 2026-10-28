#!/usr/bin/env python3
"""A04: bounded A02 caller -> conditional return at 0x2b1bb0.

For nonzero source R2: executes SUBS/BXNE LR until caller return.
For zero: stops immediately BEFORE the unmodeled fallthrough instruction.
No execution of unknown code or formal semantic certification.
"""
import argparse
import hashlib
import json
from pathlib import Path

from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM

import semantic_a02_branch_11 as a02
import semantic_evidence
import semantic_loop_250 as prior

SHA256 = "bf913415ab9458a83b14ac8c8a0fa3430d1f5d18bfbcd7c7472d6f5e8b4850bc"
SOURCE = 0x72910
TARGET = 0x2b1bb0
RETURN = 0x710100
FALLTHROUGH = TARGET + 8
BASE = 0x500100
MASK = 0xffffffff
PREFIX_HEX = "002050e21eff2f11"
VALUES = (0, 1, 0x80000000, 0xffffffff)


def exact_original(binary):
    expected = a02.EXPECTED[f"{SOURCE:08x}"][0]
    source = semantic_evidence.read_function(binary, SOURCE, 8)
    target = semantic_evidence.read_function(binary, TARGET, 8)
    if source.hex() != expected or target.hex() != PREFIX_HEX:
        raise ValueError("Original ELF conditional trace bytes have changed")
    if a02.decode(source, SOURCE)["target"] != TARGET:
        raise ValueError("A02 original source no longer branches to target")
    md = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    ops = list(md.disasm(target, TARGET))
    if (len(ops) != 2 or ops[0].mnemonic != "subs"
            or ops[1].mnemonic != "bxne" or ops[1].op_str != "lr"):
        raise ValueError("Original A32 decoding differs from bounded return contract")
    return source, target


def model(seed, value):
    registers = [(seed ^ (i*0x11111111)) & MASK for i in range(13)]
    registers[2] = value
    registers[0] = value
    # SUBS R2,R0,#0: R2=R0, NZCV = N(value), Z(value==0), C=1, V=0.
    n = (value >> 31) & 1
    z = int(value == 0)
    cpsr_masked = (n << 31) | (z << 30) | (1 << 29) | 0x10
    end = FALLTHROUGH if value == 0 else RETURN
    return registers, cpsr_masked, end


def execute(binary, seed, value, flags):
    from unicorn import (Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_PROT_ALL,
                         UC_HOOK_CODE, UC_HOOK_MEM_READ, UC_HOOK_MEM_WRITE)
    from unicorn.arm_const import (
        UC_ARM_REG_CPSR, UC_ARM_REG_PC, UC_ARM_REG_SP, UC_ARM_REG_LR,
        UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3,
        UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7,
        UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11,
        UC_ARM_REG_R12)
    source, target = exact_original(binary)
    expected_regs, expected_flags, stop = model(seed, value)
    initial = [(seed ^ (i*0x11111111)) & MASK for i in range(13)]
    initial[2] = value
    regs = (UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3,
            UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7,
            UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11,
            UC_ARM_REG_R12)
    uc = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    for page in sorted({SOURCE & ~0xfff, TARGET & ~0xfff, RETURN & ~0xfff, BASE & ~0xfff}):
        uc.mem_map(page, 0x1000, UC_PROT_ALL)
    uc.mem_write(SOURCE, source)
    uc.mem_write(TARGET, target)
    uc.mem_write(RETURN, bytes(4))
    guard = bytes((seed+i*13) & 255 for i in range(64))
    uc.mem_write(BASE, guard)
    uc.reg_write(UC_ARM_REG_CPSR, flags | 0x10)
    for reg, rvalue in zip(regs, initial):
        uc.reg_write(reg, rvalue)
    uc.reg_write(UC_ARM_REG_SP, 0x700ffc)
    uc.reg_write(UC_ARM_REG_LR, RETURN)
    trace, reads, writes = [], [], []

    def on_code(machine, pc, width, unused):
        trace.append(pc)
        if pc == stop:
            machine.emu_stop()

    def on_read(machine, access, addr, width, value, unused):
        reads.append((addr, width))

    def on_write(machine, access, addr, width, value, unused):
        writes.append((addr, width, value))

    uc.hook_add(UC_HOOK_CODE, on_code)
    uc.hook_add(UC_HOOK_MEM_READ, on_read)
    uc.hook_add(UC_HOOK_MEM_WRITE, on_write)
    try:
        uc.emu_start(SOURCE, MASK, timeout=1_000_000, count=5)
    except Exception as exc:
        raise AssertionError(f"A04 conditional Unicorn failed trace={trace}") from exc
    trace_expected = [SOURCE, SOURCE+4, TARGET, TARGET+4, stop]
    if trace != trace_expected or uc.reg_read(UC_ARM_REG_PC) != stop:
        raise AssertionError(f"Wrong BXNE branch decision {trace} vs {trace_expected}")
    if reads or writes or bytes(uc.mem_read(BASE, len(guard))) != guard:
        raise AssertionError("Unmodeled memory effects for conditional return")
    if any(uc.reg_read(r) != v for r, v in zip(regs, expected_regs)):
        raise AssertionError("Unexpected ARM registers at conditional boundary")
    if uc.reg_read(UC_ARM_REG_SP) != 0x700ffc or uc.reg_read(UC_ARM_REG_LR) != RETURN:
        raise AssertionError("SP/LR changed")
    if (uc.reg_read(UC_ARM_REG_CPSR) & 0xf000003f) != expected_flags:
        raise AssertionError("SUBS NZCV independent oracle mismatch")


def snapshot(digest, static_hash, rounds):
    return {"schema": 1, "elf_sha256": digest,
            "a04_static_checkpoint_sha256": static_hash,
            "rounds": rounds, "new_certificates": 0}


def report(data):
    total = sum(r["cases"] for r in data["rounds"])
    return "\n".join([
        "# A04 original ARM conditional return vs unmodeled fallthrough", "",
        "Original ELF SHA256: " + data["elf_sha256"], "",
        f"Bounded microexecutions: {total}; 96 nonzero-return, 32 zero-fallthrough stops.",
        "", "Original A02 source: MOV R0,R2; B 0x002b1bb0.",
        "Original target: SUBS R2,R0,#0; BXNE LR.", "",
        "Independent NZCV: N=bit31(R0), Z=(R0==0), C=1, V=0. "
        "On R0 != 0, BXNE returns. On R0 == 0, BXNE is not taken and "
        "the emulator stops BEFORE executing address 0x002b1bb8.",
        "", "All registers, SP/LR, memory and PC trace checked against "
        "a standalone Python oracle. No memory access or writes expected.",
        "", "Unknown: the fallthrough body after 0x002b1bb8, caller "
        "reachability in real Android and equivalence of the entire function.",
        "No new formal certificates.", "",
    ])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--binary", required=True, type=Path)
    parser.add_argument("--a04-static-checkpoint", required=True, type=Path)
    parser.add_argument("--checkpoint", required=True, type=Path)
    parser.add_argument("--report", required=True, type=Path)
    a = parser.parse_args()
    digest = hashlib.sha256(a.binary.read_bytes()).hexdigest()
    if digest != SHA256:
        raise ValueError("Changed original ELF SHA")
    state = json.loads(a.a04_static_checkpoint.read_text(encoding="utf-8"))
    listing = {i["address"]: i for i in state.get("targets", [])}
    if (state.get("elf_sha256") != SHA256 or len(listing) != 7
            or state.get("destinations_executed") != 0
            or state.get("new_certificates") != 0
            or not listing[f"{TARGET:08x}"]["raw_hex"].startswith(PREFIX_HEX)):
        raise ValueError("Missing original A04 static boundary checkpoint")
    exact_original(a.binary)
    source_sha = hashlib.sha256(a.a04_static_checkpoint.read_bytes()).hexdigest()
    rounds = []
    if a.checkpoint.is_file():
        previous = json.loads(a.checkpoint.read_text(encoding="utf-8"))
        if previous != snapshot(digest, source_sha, previous.get("rounds", [])):
            raise ValueError("Conditional return checkpoint differs")
        rounds = previous["rounds"]
    if len(rounds) > 4:
        raise ValueError("Too many prior rounds")
    for iteration, val in enumerate(VALUES, 1):
        for seed in prior.SEEDS:
            for flags in prior.FLAGS:
                execute(a.binary, seed, val, flags)
        item = {"iteration": iteration, "r2_input": val,
                "cases": len(prior.SEEDS)*len(prior.FLAGS),
                "branch": "fallthrough_stopped" if val == 0 else "returned",
                "status": "bounded_pass"}
        if iteration <= len(rounds):
            if rounds[iteration-1] != item:
                raise ValueError("Conditional checkpoint replay divergence")
        else:
            rounds.append(item)
            a.checkpoint.parent.mkdir(parents=True, exist_ok=True)
            tmp = a.checkpoint.with_suffix(".json.tmp")
            tmp.write_text(json.dumps(snapshot(digest, source_sha, rounds),
                                      indent=2, sort_keys=True) + "\n", encoding="utf-8")
            tmp.replace(a.checkpoint)
    result = snapshot(digest, source_sha, rounds)
    a.report.parent.mkdir(parents=True, exist_ok=True)
    a.report.write_text(report(result), encoding="utf-8")
    print(f"A04_CONDITIONAL_CASES={sum(x['cases'] for x in rounds)}")
    print("A04_RETURN_CASES=96")
    print("A04_FALLTHROUGH_STOPPED=32")
    print("A04_UNKNOWN_FALLTHROUGH_EXECUTED=0")
    print("A04_FAILED=0")
    print("A04_NEW_CERTIFICATES=0")


if __name__ == "__main__":
    main()
