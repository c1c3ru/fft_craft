#!/usr/bin/env python3
"""A04 bounded ELF BL-boundary audit and one isolated original caller prefix.

Audit two BL blocks, their immediate callees and return continuations, and
the zero-case conditional fallthrough. Execute only the simple MOV/B ->
PUSH/MOV/MOV prefix of 0xb461c, stopping BEFORE its BL; never execute an
unmodeled function/callee, and never issue formal semantic certificates.
"""
import argparse
import hashlib
import json
from pathlib import Path

from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
from capstone.arm import ARM_OP_IMM

import semantic_a02_branch_11 as a02
import semantic_a04_destinations as a04
import semantic_evidence
import semantic_loop_250 as prior

SHA = a04.ELF_DIGEST
PAIR = ((0x000ab674, 0x000b6620), (0x000b461c, 0x000b45d0))
FALLTHROUGH = 0x002b1bb8
SOURCE = 0x000b4700
SIMPLE_TARGET = 0x000b461c
RETURN = 0x710100
SP = 0x600ffc
STACK_BASE = 0x600000
MASK = 0xffffffff
SCAN_BYTES = 96


def scan(binary, address):
    raw = semantic_evidence.read_function(binary, address, SCAN_BYTES)
    dis = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    dis.detail = True
    rows = []
    for ins in dis.disasm(raw, address):
        rows.append({"pc": f"{ins.address:08x}", "hex": ins.bytes.hex(),
                     "mnemonic": ins.mnemonic, "operands": ins.op_str})
        if len(rows) >= 24:
            break
    if not rows or rows[0]["pc"] != f"{address:08x}":
        raise ValueError("Original ELF candidate disassembly missing")
    return {"address": f"{address:08x}", "raw_hex": raw.hex(),
            "candidate_insns": rows, "executed": False,
            "code_data_verified": False}


def first_call(binary, address, expected_callee):
    entry = scan(binary, address)
    rows = entry["candidate_insns"]
    matches = [i for i, ins in enumerate(rows) if ins["mnemonic"] == "bl"]
    if not matches:
        raise ValueError("No direct BL in verified original ELF scan")
    pos = matches[0]
    # ARM B(L) immediate: independently decode PC + 8 sign-extended imm24*4.
    call = rows[pos]
    word = int.from_bytes(bytes.fromhex(call["hex"]), "little")
    if word >> 24 != 0xeb:
        raise ValueError("First BL is not unconditional A32 immediate")
    offset = (word & 0xffffff) << 2
    if offset & (1 << 25):
        offset -= 1 << 26
    target = (int(call["pc"], 16) + 8 + offset) & MASK
    if target != expected_callee or pos == 0:
        raise ValueError("Original BL target or prefix boundary changed")
    entry["call"] = {"pc": call["pc"], "target": f"{target:08x}",
                     "prefix_insns": pos, "executed": False,
                     "continuation": f"{int(call['pc'], 16) + 4:08x}"}
    entry["prefix"] = rows[:pos]
    return entry


def verified(binary, static_checkpoint):
    if hashlib.sha256(binary.read_bytes()).hexdigest() != SHA:
        raise ValueError("A04 original ELF identity changed")
    state = json.loads(static_checkpoint.read_text(encoding="utf-8"))
    targets = {row["address"]: row for row in state.get("targets", [])}
    if (state.get("elf_sha256") != SHA or state.get("new_certificates") != 0
            or len(targets) != 7
            or not all(f"{addr:08x}" in targets for addr, _ in PAIR)):
        raise ValueError("A04 prior seven-target checkpoint not established")
    a04.verify_sources(binary)
    callsites = [first_call(binary, addr, dest) for addr, dest in PAIR]
    scans = [
        {"kind": "callee_entry", **scan(binary, dest)}
        for _, dest in PAIR
    ] + [
        {"kind": "post_call", **scan(binary, int(row["call"]["continuation"], 16))}
        for row in callsites
    ] + [
        {"kind": "conditional_zero_fallthrough", **scan(binary, FALLTHROUGH)}
    ]
    # This is a first-block hypothesis only. Never execute these scans.
    return {"schema": 1, "elf_sha256": SHA,
            "prior_a04_static_sha256": hashlib.sha256(static_checkpoint.read_bytes()).hexdigest(),
            "callsites": callsites, "unexecuted_scans": scans,
            "total_scanned_entries": len(callsites) + len(scans),
            "scanned_bytes": SCAN_BYTES * (len(callsites) + len(scans)),
            "callees_executed": 0, "new_certificates": 0}


def prefix_original(binary):
    original = semantic_evidence.read_function(binary, SOURCE, 8)
    if original.hex() != a02.EXPECTED[f"{SOURCE:08x}"][0]:
        raise ValueError("A02 original MOV/B caller changed")
    src = a02.decode(original, SOURCE)
    if src is None or src["target"] != SIMPLE_TARGET:
        raise ValueError("A02 original branch no longer reaches BL block")
    body = semantic_evidence.read_function(binary, SIMPLE_TARGET, 16)
    dis = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    dis.detail = True
    op = list(dis.disasm(body, SIMPLE_TARGET))
    if (len(op) != 4 or [x.mnemonic for x in op] != ["push", "mov", "mov", "bl"]
            or op[0].op_str.replace(" ", "") != "{r4,r5,r6,lr}"
            or op[1].op_str.replace(" ", "") != "r5,r0"
            or op[2].op_str.replace(" ", "") != "r4,r1"):
        raise ValueError("Original simple A04 prologue is not modeled safely")
    call_word = int.from_bytes(body[12:16], "little")
    offset = (call_word & 0xffffff) << 2
    if offset & (1 << 25):
        offset -= 1 << 26
    if call_word >> 24 != 0xeb or (SIMPLE_TARGET + 12 + 8 + offset) != PAIR[1][1]:
        raise ValueError("Original A04 direct BL target changed")
    return original, body


def oracle(seed):
    initial = [(seed ^ (i * 0x11111111)) & MASK for i in range(13)]
    after = initial.copy()
    after[1] = 0
    after[5] = initial[0]
    after[4] = 0
    writes = [(SP - 16 + 4*i, 4, val) for i, val in enumerate(
        (initial[4], initial[5], initial[6], RETURN))]
    return after, writes


def execute(binary, seed, flags):
    from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_PROT_ALL, UC_HOOK_CODE, UC_HOOK_MEM_READ, UC_HOOK_MEM_WRITE
    from unicorn.arm_const import (UC_ARM_REG_CPSR, UC_ARM_REG_PC, UC_ARM_REG_SP, UC_ARM_REG_LR,
        UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_R4, UC_ARM_REG_R5,
        UC_ARM_REG_R6, UC_ARM_REG_R7, UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10,
        UC_ARM_REG_R11, UC_ARM_REG_R12)
    source, body = prefix_original(binary)
    regs = (UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3,
            UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7,
            UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11, UC_ARM_REG_R12)
    initial = [(seed ^ (i * 0x11111111)) & MASK for i in range(13)]
    expected_regs, writes_expected = oracle(seed)
    uc = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    for page in sorted({SOURCE & ~0xfff, SIMPLE_TARGET & ~0xfff,
                        STACK_BASE & ~0xfff}):
        uc.mem_map(page, 0x1000, UC_PROT_ALL)
    uc.mem_write(SOURCE, source)
    uc.mem_write(SIMPLE_TARGET, body)
    memory_initial = bytes((i * 7 + seed) & 255 for i in range(0x1000))
    uc.mem_write(STACK_BASE, memory_initial)
    uc.reg_write(UC_ARM_REG_CPSR, flags | 0x10)
    for reg, val in zip(regs, initial):
        uc.reg_write(reg, val)
    uc.reg_write(UC_ARM_REG_SP, SP)
    uc.reg_write(UC_ARM_REG_LR, RETURN)
    trace, reads, writes = [], [], []
    stop = SIMPLE_TARGET + 12

    def code_hook(emu, pc, size, unused):
        trace.append(pc)
        if pc == stop:
            emu.emu_stop()  # never execute BL or its target

    def on_read(emu, access, addr, size, value, unused):
        reads.append((addr, size))

    def on_write(emu, access, addr, size, value, unused):
        writes.append((addr, size, value & ((1 << (8 * size)) - 1)))

    uc.hook_add(UC_HOOK_CODE, code_hook)
    uc.hook_add(UC_HOOK_MEM_READ, on_read)
    uc.hook_add(UC_HOOK_MEM_WRITE, on_write)
    uc.emu_start(SOURCE, MASK, timeout=1_000_000, count=7)
    expected_trace = [SOURCE, SOURCE + 4] + [SIMPLE_TARGET + 4*i for i in range(4)]
    if trace != expected_trace or uc.reg_read(UC_ARM_REG_PC) != stop:
        raise AssertionError("Unexpected PC flow or entered an unmodeled BL")
    if reads or writes != writes_expected:
        raise AssertionError(f"Unmodeled stack/memory access: {reads}, {writes}")
    memory_expected = bytearray(memory_initial)
    for addr, width, val in writes_expected:
        memory_expected[addr - STACK_BASE:addr - STACK_BASE + width] = val.to_bytes(width, "little")
    if bytes(uc.mem_read(STACK_BASE, len(memory_initial))) != memory_expected:
        raise AssertionError("Unexpected memory mutation outside original PUSH effects")
    if any(uc.reg_read(r) != v for r, v in zip(regs, expected_regs)):
        raise AssertionError("Unknown register changes before direct BL")
    if uc.reg_read(UC_ARM_REG_SP) != SP - 16 or uc.reg_read(UC_ARM_REG_LR) != RETURN:
        raise AssertionError("SP/LR not preserved as modeled")
    if uc.reg_read(UC_ARM_REG_CPSR) & 0xf000003f != (flags | 0x10) & 0xf000003f:
        raise AssertionError("NZCV changed during no-flags prefix")


def checkpoint(state, rounds):
    return {"schema": 1, "elf_sha256": SHA,
            "static_sha256": hashlib.sha256(json.dumps(state, sort_keys=True).encode()).hexdigest(),
            "static_scan": state, "rounds": rounds,
            "new_certificates": 0}


def report(state):
    lines = ["# A04 — BL boundaries of original ARM ELF (no callee execution)", "",
             f"Original ELF SHA256: {SHA}", "",
             "Two direct BL callsites and five related first-block scans, "
             "all file-backed and code-vs-data unproven.", "",
             "| Entry | First BL | Callee (NOT executed) | Continuation |",
             "|---|---|---|---|"]
    for row in state["static_scan"]["callsites"]:
        x = row["call"]
        lines.append(f"| {row['address']} | {x['pc']} | {x['target']} | {x['continuation']} |")
    lines += ["", "## Limited semantic experiment", "",
              "A02 000b4700 MOV R1,#0; B 000b461c; then original "
              "PUSH {R4,R5,R6,LR}; MOV R5,R0; MOV R4,R1, stopping "
              "BEFORE direct BL 000b45d0.",
              "Independent checks: PC trace, stack writes/widths/values, "
              "SP, R0-R12, LR, NZCV, all other stack bytes. "
              f"Bounded local tests: {sum(r['cases'] for r in state['rounds'])}; "
              "zero BL targets executed. No full function equivalence.", "",
              "Next: independently model BL callees 000b6620 and 000b45d0, "
              "global data effects at 000ab674, post-BL continuations, "
              "conditional zero fallthrough and 002a1268 self-loop reachability.",
              "Never claim runtime Android GOT values or new certificates.", ""]
    return "\n".join(lines)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    for name in ("binary", "a04-static-checkpoint", "checkpoint", "report"):
        p.add_argument("--" + name, type=Path, required=True)
    a = p.parse_args()
    state = verified(a.binary, a.a04_static_checkpoint)
    rounds = []
    if a.checkpoint.is_file():
        old = json.loads(a.checkpoint.read_text(encoding="utf-8"))
        if old != checkpoint(state, old.get("rounds", [])):
            raise ValueError("Stale A04 BL boundary checkpoint")
        rounds = old["rounds"]
    if len(rounds) > 1:
        raise ValueError("Excess prefix rounds")
    for seed in prior.SEEDS:
        for flags in prior.FLAGS:
            execute(a.binary, seed, flags)
    item = {"iteration": 1, "addresses": ["000b4700", "000b461c"],
            "cases": len(prior.SEEDS)*len(prior.FLAGS),
            "scope": "stop_before_original_BL"}
    if rounds and rounds[0] != item:
        raise ValueError("A04 bounded BL checkpoint mismatch")
    if not rounds:
        rounds.append(item)
        a.checkpoint.parent.mkdir(parents=True, exist_ok=True)
        a.checkpoint.write_text(json.dumps(checkpoint(state, rounds), sort_keys=True, indent=2)+"\n", encoding="utf-8")
    result = checkpoint(state, rounds)
    a.report.parent.mkdir(parents=True, exist_ok=True)
    a.report.write_text(report(result), encoding="utf-8")
    print(f"A04_BL_CALLSITES={len(state['callsites'])}")
    print(f"A04_BL_CANDIDATE_BYTES={state['scanned_bytes']}")
    print(f"A04_BL_PREFIX_CASES={sum(x['cases'] for x in rounds)}")
    print("A04_BL_CALLEES_EXECUTED=0")
    print("A04_BL_FAILED=0")
    print("A04_BL_NEW_CERTIFICATES=0")


if __name__ == "__main__":
    main()
