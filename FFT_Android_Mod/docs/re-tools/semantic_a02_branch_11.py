#!/usr/bin/env python3
"""A02: original ARM ELF bounded prefix/branch differential loop.

Ten original AL opcodes followed by B: execute prefix and branch, stop in
code hook BEFORE destination. One original self-B: execute exactly one opcode.
All specs require byte-exact ELF evidence. No new semantic certification.
"""
import argparse
import hashlib
import json
from pathlib import Path

from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM

import semantic_a01_memory_21 as a01
import semantic_evidence
import semantic_manifest_audit as audit_tool
import semantic_loop_250 as prior
import semantic_remaining_34 as earlier

MASK = 0xffffffff
BASE = 0x500100
CANARY = bytes.fromhex("197dda3c89fe2011")
MEM_SIZE = 0x400
RETURN = 0x710100

EXPECTED = {
    "00072910": ("0200a0e1a5fc08ea", "mov_r0_r2"),
    "00082404": ("920100e036bcffea", "mul_r0_r2_r1"),
    "0008240c": ("0100a0e131bcffea", "mov_r0_r1"),
    "000a94bc": ("1c0080e26b0800ea", "add_r0_28"),
    "000b4700": ("0010a0e3c4ffffea", "mov_r1_zero"),
    "000b6c68": ("0020a0e3f9ffffea", "mov_r2_zero"),
    "000b6cd0": ("0120a0e3dfffffea", "mov_r2_one"),
    "000b6ee0": ("0220a0e35bffffea", "mov_r2_two"),
    "000b6ee8": ("0320a0e359ffffea", "mov_r2_three"),
    "000b6f80": ("000090e5a30600ea", "ldr_r0_ptr"),
    "002a1268": ("feffffea", "self_branch"),
}
FIRST = {
    "mov_r0_r2": 0xe1a00002,
    "mul_r0_r2_r1": 0xe0000192,
    "mov_r0_r1": 0xe1a00001,
    "add_r0_28": 0xe280001c,
    "mov_r1_zero": 0xe3a01000,
    "mov_r2_zero": 0xe3a02000,
    "mov_r2_one": 0xe3a02001,
    "mov_r2_two": 0xe3a02002,
    "mov_r2_three": 0xe3a02003,
    "ldr_r0_ptr": 0xe5900000,
}


def branch_target(word, address):
    if word >> 24 != 0xea:
        raise ValueError("Only unconditional direct A32 B is accepted")
    offset = (word & 0xffffff) << 2
    if offset & (1 << 25):
        offset -= (1 << 26)
    return (address + 8 + offset) & MASK


def decode(raw, address):
    key = f"{address:08x}"
    if address & 3 or key not in EXPECTED or raw.hex() != EXPECTED[key][0]:
        return None
    op = EXPECTED[key][1]
    if op == "self_branch":
        if len(raw) != 4 or branch_target(int.from_bytes(raw, "little"), address) != address:
            return None
        return {"op": op, "target": address, "raw_hex": raw.hex()}
    if len(raw) != 8 or int.from_bytes(raw[:4], "little") != FIRST[op]:
        return None
    target = branch_target(int.from_bytes(raw[4:], "little"), address + 4)
    if target in (address, address + 4) or target & 3:
        return None
    return {"op": op, "target": target, "raw_hex": raw.hex()}


def classify(binary, rows):
    dis = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    found = []
    for previous in rows:
        if previous["contract"] is not None:
            continue
        address = int(previous["address"], 16)
        raw = semantic_evidence.read_function(binary, address, previous["size"])
        if raw.hex() != previous["raw_hex"]:
            raise ValueError("The A01 checkpoint disagrees with original ELF bytes")
        spec = decode(raw, address)
        if spec is None:
            raise ValueError("Unknown A02 opcode " + previous["address"])
        asm = list(dis.disasm(raw, address))
        expected_mnemonic = {
            "mul_r0_r2_r1": "mul", "add_r0_28": "add",
            "ldr_r0_ptr": "ldr",
        }.get(spec["op"], "mov")
        if spec["op"] == "self_branch":
            if len(asm) != 1 or asm[0].mnemonic != "b":
                raise ValueError("Capstone disagrees on self loop")
        elif (len(asm) != 2 or asm[0].mnemonic != expected_mnemonic
              or asm[1].mnemonic != "b"):
            raise ValueError("Capstone disagrees with original A32 at " + previous["address"])
        found.append({"address": previous["address"], "size": previous["size"],
                      "raw_hex": raw.hex(), "assembly": previous["assembly"],
                      "contract": spec, "status": (
                          "one_step_self_loop" if spec["op"] == "self_branch"
                          else "prefix_and_direct_branch_only")})
    if len(found) != 11 or {r["address"] for r in found} != set(EXPECTED):
        raise ValueError("Original A02 entry set incomplete or duplicated")
    return found


def reference(spec, seed):
    registers = [(seed ^ (i * 0x11111111)) & MASK for i in range(13)]
    memory = bytearray((i * 29 + (seed & 255)) & 255 for i in range(MEM_SIZE))
    memory[0x300:0x308] = CANARY
    op = spec["op"]
    reads = []
    if op == "mov_r0_r2":
        registers[0] = registers[2]
    elif op == "mul_r0_r2_r1":
        registers[0] = (registers[2] * registers[1]) & MASK
    elif op == "mov_r0_r1":
        registers[0] = registers[1]
    elif op == "add_r0_28":
        registers[0] = (registers[0] + 28) & MASK
    elif op == "mov_r1_zero":
        registers[1] = 0
    elif op in ("mov_r2_zero", "mov_r2_one", "mov_r2_two", "mov_r2_three"):
        registers[2] = {"mov_r2_zero": 0, "mov_r2_one": 1,
                        "mov_r2_two": 2, "mov_r2_three": 3}[op]
    elif op == "ldr_r0_ptr":
        registers[0] = int.from_bytes(memory[:4], "little")
        reads = [(BASE, 4)]
    elif op != "self_branch":
        raise ValueError("Unknown reference opcode")
    return registers, bytes(memory), reads


def execute(binary, row, seed, flags):
    from unicorn import (Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_PROT_ALL,
                         UC_HOOK_CODE, UC_HOOK_MEM_READ, UC_HOOK_MEM_WRITE)
    from unicorn.arm_const import (
        UC_ARM_REG_CPSR, UC_ARM_REG_PC, UC_ARM_REG_SP, UC_ARM_REG_LR,
        UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3,
        UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7,
        UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11, UC_ARM_REG_R12)
    spec = row["contract"]
    if spec is None:
        raise ValueError("Cannot execute an unmodeled original ELF instruction")
    address = int(row["address"], 16)
    raw = semantic_evidence.read_function(binary, address, row["size"])
    if raw.hex() != row["raw_hex"] or decode(raw, address) != spec:
        raise ValueError("Original ELF opcode changed")
    desired, memory, reads_expected = reference(spec, seed)
    initial = [(seed ^ (i * 0x11111111)) & MASK for i in range(13)]
    if spec["op"] == "ldr_r0_ptr":
        initial[0] = BASE
    target = spec["target"]
    regs = (UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3,
            UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7,
            UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11, UC_ARM_REG_R12)
    uc = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    for page in sorted({address & ~0xfff, (address + len(raw) - 4) & ~0xfff,
                        target & ~0xfff, BASE & ~0xfff}):
        uc.mem_map(page, 0x1000, UC_PROT_ALL)
    uc.mem_write(address, raw)
    if target != address:
        uc.mem_write(target, bytes(4))   # Trap site, not original target code.
    uc.mem_write(BASE, memory)
    uc.reg_write(UC_ARM_REG_CPSR, flags | 0x10)
    for reg, value in zip(regs, initial):
        uc.reg_write(reg, value)
    uc.reg_write(UC_ARM_REG_SP, 0x700ffc)
    uc.reg_write(UC_ARM_REG_LR, RETURN)
    trace, reads, writes = [], [], []

    def on_code(engine, pc, size, unused):
        trace.append(pc)
        if pc == target and pc != address:
            engine.emu_stop()  # Hook fires BEFORE executing the target.

    def on_read(engine, access, position, size, value, unused):
        reads.append((position, size))

    def on_write(engine, access, position, size, value, unused):
        writes.append((position, size, value))

    uc.hook_add(UC_HOOK_CODE, on_code)
    uc.hook_add(UC_HOOK_MEM_READ, on_read)
    uc.hook_add(UC_HOOK_MEM_WRITE, on_write)
    try:
        uc.emu_start(address, MASK, timeout=1_000_000,
                     count=1 if address == target else 3)
    except Exception as exc:
        raise AssertionError(f"A02 Unicorn failure at {row['address']} trace={trace}") from exc
    expected_trace = [address] if address == target else [address, address + 4, target]
    if trace != expected_trace or uc.reg_read(UC_ARM_REG_PC) != target:
        raise AssertionError(f"Unmodeled control flow: {trace} target={target:08x}")
    if reads != reads_expected or writes:
        raise AssertionError(f"Unmodeled memory accesses: reads={reads}, writes={writes}")
    if bytes(uc.mem_read(BASE, MEM_SIZE)) != memory:
        raise AssertionError("Memory changes or damaged canary")
    if any(uc.reg_read(r) != value for r, value in zip(regs, desired)):
        raise AssertionError("Unmodeled registers changed")
    if uc.reg_read(UC_ARM_REG_SP) != 0x700ffc or uc.reg_read(UC_ARM_REG_LR) != RETURN:
        raise AssertionError("SP or LR changed")
    if (uc.reg_read(UC_ARM_REG_CPSR) & 0xf000003f) != ((flags | 0x10) & 0xf000003f):
        raise AssertionError("NZCV or privilege mode changed")


def snapshot(digest, audit_fingerprint, source_fingerprint, entries, rounds):
    return {"schema": 1, "elf_sha256": digest,
            "audit_rows_sha256": audit_fingerprint,
            "a01_checkpoint_sha256": source_fingerprint,
            "entries": entries, "rounds": rounds, "new_certificates": 0}


def render(state):
    rows = state["entries"]
    samples = sum(x["samples"] for x in state["rounds"])
    lines = ["# A02: original ELF ARM prefix and branch boundary", "",
             "ELF SHA-256: " + state["elf_sha256"], "",
             f"Entries: {len(rows)}; bounded tests: {samples}; new certificates: 0.", "",
             "| Address | Original bytes | Instruction pair | Contract | Target NOT executed |",
             "|---|---|---|---|---|"]
    for row in rows:
        spec = row["contract"]
        lines.append(f"| {row['address']} | {row['raw_hex']} | "
                     + "; ".join(row["assembly"]).replace("|", "/")
                     + f" | {spec['op']} | {spec['target']:08x} |")
    lines += ["", "## Safety and limits", "",
              "Ten entries execute a modeled A32 prefix and direct B, stopping in "
              "a code hook BEFORE the first instruction of the destination.",
              "The eleventh entry is a self-loop: exactly one branch instruction "
              "is stepped, NOT a proof of termination.",
              "Original ARM vs independent Python reference: R0-R12, SP/LR, NZCV, "
              "PC, memory contents, reads, zero writes, and a canary, across "
              "8 seeds and 4 flags. No external callee or target was executed.",
              "The destination CFG and full function are not proven. "
              "The 303 old certificates are unmodified.", ""]
    return "\n".join(lines)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    for name in ("binary", "manifests", "pilot", "full-checkpoint",
                 "remaining-checkpoint", "a01-checkpoint", "checkpoint", "report"):
        p.add_argument("--" + name, required=True, type=Path)
    p.add_argument("--round-size", type=int, default=4)
    args = p.parse_args()
    if not 1 <= args.round_size <= 11:
        p.error("Invalid A02 round size")
    audited = audit_tool.audit(args.binary, args.manifests, args.pilot)
    inventory_hash = hashlib.sha256(json.dumps(audited["rows"], sort_keys=True).encode()).hexdigest()
    full = json.loads(args.full_checkpoint.read_text(encoding="utf-8"))
    old = json.loads(args.remaining_checkpoint.read_text(encoding="utf-8"))
    old_a01 = json.loads(args.a01_checkpoint.read_text(encoding="utf-8"))
    if (full.get("elf_sha256") != audited["digest"]
            or full.get("eligible") != len(full.get("selected", []))
            or full.get("new_certificates") != 0):
        raise ValueError("Prior ELF full checkpoint mismatch")
    real_34 = earlier.catalog(args.binary, audited["rows"], full["selected"])
    if old != earlier.build(audited["digest"], inventory_hash,
                            real_34, old.get("rounds", [])):
        raise ValueError("Prior 34 checkpoint mismatch")
    real_21 = a01.classify(args.binary, old["entries"])
    prior_hash = hashlib.sha256(args.remaining_checkpoint.read_bytes()).hexdigest()
    if old_a01 != a01.checkpoint(audited["digest"], inventory_hash,
                                 prior_hash, real_21, old_a01.get("rounds", [])):
        raise ValueError("Prior A01 checkpoint mismatch")
    if (len(real_21) != 21 or sum(bool(x["contract"]) for x in real_21) != 10
            or sum(x["samples"] for x in old_a01["rounds"]) != 320):
        raise ValueError("Unproven A01 prerequisite")
    entries = classify(args.binary, old_a01["entries"])
    a01_hash = hashlib.sha256(args.a01_checkpoint.read_bytes()).hexdigest()
    rounds = []
    if args.checkpoint.is_file():
        earlier_result = json.loads(args.checkpoint.read_text(encoding="utf-8"))
        if earlier_result != snapshot(audited["digest"], inventory_hash, a01_hash,
                                     entries, earlier_result.get("rounds", [])):
            raise ValueError("Stale or tampered A02 checkpoint")
        rounds = earlier_result["rounds"]
    batches = [entries[i:i + args.round_size] for i in range(0, len(entries), args.round_size)]
    if len(rounds) > len(batches):
        raise ValueError("Checkpoint has excess batches")
    for index, batch in enumerate(batches, 1):
        for row in batch:
            for seed in prior.SEEDS:
                for flags in prior.FLAGS:
                    execute(args.binary, row, seed, flags)
        record = {"iteration": index, "addresses": [x["address"] for x in batch],
                  "samples": len(batch) * len(prior.SEEDS) * len(prior.FLAGS),
                  "status": "bounded_pass"}
        if index <= len(rounds):
            if rounds[index - 1] != record:
                raise ValueError("Replayed A02 round differs")
        else:
            rounds.append(record)
            args.checkpoint.parent.mkdir(parents=True, exist_ok=True)
            temp = args.checkpoint.with_suffix(".json.tmp")
            temp.write_text(json.dumps(snapshot(audited["digest"], inventory_hash,
                                               a01_hash, entries, rounds),
                                       indent=2, sort_keys=True) + "\n", encoding="utf-8")
            temp.replace(args.checkpoint)
    result = snapshot(audited["digest"], inventory_hash, a01_hash, entries, rounds)
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(render(result), encoding="utf-8")
    samples = sum(x["samples"] for x in rounds)
    print(f"A02_ENTRIES={len(entries)}")
    print(f"A02_PREFIX_BRANCHES={sum(x['contract']['op'] != 'self_branch' for x in entries)}")
    print(f"A02_SELF_LOOP_ONE_STEP={sum(x['contract']['op'] == 'self_branch' for x in entries)}")
    print(f"A02_DYNAMIC_CASES={samples}")
    print("A02_BRANCH_TARGETS_EXECUTED=0")
    print("A02_FAILED=0")
    print("A02_NEW_CERTIFICATES=0")


if __name__ == "__main__":
    main()
