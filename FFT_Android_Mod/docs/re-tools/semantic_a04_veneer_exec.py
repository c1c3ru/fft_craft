#!/usr/bin/env python3
"""Bounded original ELF A32 MOV/MUL+B through two indirect PC-load veneers.

Reads synthetic GOT entries and stops in CODE hook before indirect targets.
A live linker target, runtime relocation and full call behaviour are unknown.
"""
import argparse
import hashlib
import json
from pathlib import Path

import semantic_a02_branch_11 as a02
import semantic_evidence
import semantic_loop_250 as prior

ELF_SHA = "bf913415ab9458a83b14ac8c8a0fa3430d1f5d18bfbcd7c7472d6f5e8b4850bc"
MASK = 0xffffffff
TRAP = 0x710200
STACK = 0x700ffc
VENEERS = {
    0x714dc: {"source": 0x8240c, "opcode": "02c68fe2d6ca8ce2a0f8bce5",
              "slot": 0x347d84, "kind": "mov"},
    0x714e8: {"source": 0x82404, "opcode": "02c68fe2d6ca8ce298f8bce5",
              "slot": 0x347d88, "kind": "mul"},
}


def original(binary, address, expected):
    word = semantic_evidence.read_function(binary, address, len(bytes.fromhex(expected)))
    if word.hex() != expected:
        raise ValueError(f"Original ELF byte mismatch 0x{address:x}")
    return word


def validate_sources(binary):
    for target, cfg in VENEERS.items():
        original(binary, target, cfg["opcode"])
        src = cfg["source"]
        raw = original(binary, src, a02.EXPECTED[f"{src:08x}"][0])
        if a02.decode(raw, src)["target"] != target:
            raise ValueError("A02 source branch changed")
        computed_slot = target + 8 + 0x200000 + 0xd6000
        computed_slot += 0x8a0 if cfg["kind"] == "mov" else 0x898
        if computed_slot != cfg["slot"]:
            raise ValueError("A32 PC+8/GOT slot mismatch")


def expected(seed, kind, slot):
    initial = [(seed ^ (r * 0x11111111)) & MASK for r in range(13)]
    regs = initial.copy()
    if kind == "mov":
        regs[0] = initial[1]
    elif kind == "mul":
        regs[0] = (initial[2] * initial[1]) & MASK
    else:
        raise ValueError("Unknown branch source")
    regs[12] = slot
    got = bytearray((i*37 + seed) & 255 for i in range(0x100))
    got[slot & 0xff: (slot & 0xff)+4] = TRAP.to_bytes(4, "little")
    return initial, regs, bytes(got)


def execute(binary, target, seed, flags):
    from unicorn import (Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_PROT_ALL,
                         UC_HOOK_CODE, UC_HOOK_MEM_READ, UC_HOOK_MEM_WRITE)
    from unicorn.arm_const import (
        UC_ARM_REG_CPSR, UC_ARM_REG_PC, UC_ARM_REG_SP, UC_ARM_REG_LR,
        UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3,
        UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7,
        UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11, UC_ARM_REG_R12)
    if target not in VENEERS:
        raise ValueError("Unlisted indirect veneer target")
    config = VENEERS[target]
    source = config["source"]
    src_bytes = original(binary, source, a02.EXPECTED[f"{source:08x}"][0])
    ven_bytes = original(binary, target, config["opcode"])
    initial, desired, got = expected(seed, config["kind"], config["slot"])
    regs = (UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3,
            UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7,
            UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10,
            UC_ARM_REG_R11, UC_ARM_REG_R12)
    uc = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    pages = {source & ~0xfff, target & ~0xfff,
             config["slot"] & ~0xfff, TRAP & ~0xfff}
    for page in sorted(pages):
        uc.mem_map(page, 0x1000, UC_PROT_ALL)
    uc.mem_write(source, src_bytes)
    uc.mem_write(target, ven_bytes)
    uc.mem_write(config["slot"] & ~0xff, got)
    uc.mem_write(TRAP, bytes(4))
    uc.reg_write(UC_ARM_REG_CPSR, flags | 0x10)
    for reg, val in zip(regs, initial):
        uc.reg_write(reg, val)
    uc.reg_write(UC_ARM_REG_SP, STACK)
    uc.reg_write(UC_ARM_REG_LR, 0x710100)
    trace, reads, writes = [], [], []

    def on_code(machine, pc, size, unused):
        trace.append(pc)
        if pc == TRAP:
            machine.emu_stop()

    def on_read(machine, access, addr, size, value, unused):
        reads.append((addr, size))

    def on_write(machine, access, addr, size, value, unused):
        writes.append((addr, size, value))

    uc.hook_add(UC_HOOK_CODE, on_code)
    uc.hook_add(UC_HOOK_MEM_READ, on_read)
    uc.hook_add(UC_HOOK_MEM_WRITE, on_write)
    try:
        uc.emu_start(source, MASK, timeout=1_000_000, count=7)
    except Exception as exc:
        raise AssertionError(f"Unicorn failed A04 veneer 0x{target:x}: {trace}") from exc
    want_trace = [source, source+4, target, target+4, target+8, TRAP]
    if trace != want_trace or uc.reg_read(UC_ARM_REG_PC) != TRAP:
        raise AssertionError(f"Unexpected branch trace {trace} vs {want_trace}")
    if reads != [(config["slot"], 4)] or writes:
        raise AssertionError(f"Unexpected indirect GOT effects {reads} {writes}")
    if bytes(uc.mem_read(config["slot"] & ~0xff, len(got))) != got:
        raise AssertionError("GOT synthetic region modified")
    if any(uc.reg_read(reg) != val for reg, val in zip(regs, desired)):
        raise AssertionError("GOT veneer does not match independent model")
    if uc.reg_read(UC_ARM_REG_SP) != STACK or uc.reg_read(UC_ARM_REG_LR) != 0x710100:
        raise AssertionError("SP or LR unexpectedly changed")
    if (uc.reg_read(UC_ARM_REG_CPSR) & 0xf000003f) != ((flags | 0x10) & 0xf000003f):
        raise AssertionError("Flags changed in arithmetic/indirect jump")


def snapshot(digest, static_sha, rounds):
    return {"schema": 1, "elf_sha256": digest,
            "static_a04_sha256": static_sha,
            "rounds": rounds, "new_certificates": 0}


def render(data):
    total = sum(x["cases"] for x in data["rounds"])
    lines = ["# A04: two original ELF indirect PC-load veneers", "",
             "ELF: " + data["elf_sha256"], "",
             f"Bounded synthetically modeled runs: {total}, no indirect destination executed.",
             "", "| A02 source | A04 veneer | PIC/GOT word slot | Behaviour boundary |",
             "|---|---|---|---|"]
    for target, cfg in VENEERS.items():
        lines.append(f"| {cfg['source']:08x} | {target:08x} | {cfg['slot']:08x} | "
                     + cfg["kind"] + "; two ADDs to IP, LDR PC preindexed writeback |")
    lines += ["", "Inputs: arbitrary seed-based ARM registers, four NZCV patterns. "
              "PC+8 and immediate encodings verified against original bytes; "
              "synthetic GOT words point to a mapped stop hook, never executable target code.",
              "", "Effects tested: branch trace, IP writeback to GOT slot, "
              "R0 source MOV/MUL, all other GPRs, SP/LR, NZCV, one memory read, "
              "no writes, unchanged GOT bytes.",
              "", "Unknown: actual resolved linker target at runtime, effects "
              "of the target and whole-function semantics. No formal certificates.",
              ""]
    return "\n".join(lines)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--binary", type=Path, required=True)
    p.add_argument("--static-a04-checkpoint", type=Path, required=True)
    p.add_argument("--checkpoint", type=Path, required=True)
    p.add_argument("--report", type=Path, required=True)
    a = p.parse_args()
    digest = hashlib.sha256(a.binary.read_bytes()).hexdigest()
    if digest != ELF_SHA:
        raise ValueError("Wrong ELF original digest")
    static = json.loads(a.static_a04_checkpoint.read_text(encoding="utf-8"))
    targets = {r["address"]: r for r in static.get("targets", [])}
    if (static.get("elf_sha256") != ELF_SHA or len(targets) != 7
            or static.get("new_certificates") != 0 or static.get("destinations_executed") != 0):
        raise ValueError("Missing A04 static boundary evidence")
    for target, cfg in VENEERS.items():
        if f"{target:08x}" not in targets or not targets[f"{target:08x}"]["raw_hex"].startswith(cfg["opcode"]):
            raise ValueError("Indirect veneer does not match static original bytes")
    validate_sources(a.binary)
    static_sha = hashlib.sha256(a.static_a04_checkpoint.read_bytes()).hexdigest()
    rounds = []
    if a.checkpoint.is_file():
        earlier = json.loads(a.checkpoint.read_text(encoding="utf-8"))
        if earlier != snapshot(digest, static_sha, earlier.get("rounds", [])):
            raise ValueError("Changed A04 veneer checkpoint")
        rounds = earlier["rounds"]
    if len(rounds) > len(VENEERS):
        raise ValueError("Excess prior rounds")
    for pos, target in enumerate(VENEERS, 1):
        for seed in prior.SEEDS:
            for flags in prior.FLAGS:
                execute(a.binary, target, seed, flags)
        current = {"iteration": pos, "target": f"{target:08x}",
                   "cases": len(prior.SEEDS)*len(prior.FLAGS),
                   "status": "synthetic_got_boundary_pass"}
        if len(rounds) >= pos:
            if rounds[pos-1] != current:
                raise ValueError("Replay divergence at A04 veneer")
        else:
            rounds.append(current)
            a.checkpoint.parent.mkdir(parents=True, exist_ok=True)
            tmp = a.checkpoint.with_suffix(".json.tmp")
            tmp.write_text(json.dumps(snapshot(digest, static_sha, rounds),
                                      sort_keys=True, indent=2)+"\n", encoding="utf-8")
            tmp.replace(a.checkpoint)
    result = snapshot(digest, static_sha, rounds)
    a.report.parent.mkdir(parents=True, exist_ok=True)
    a.report.write_text(render(result), encoding="utf-8")
    print("A04_VENEER_TARGETS=2")
    print(f"A04_VENEER_CASES={sum(r['cases'] for r in rounds)}")
    print("A04_GOT_SLOTS_VERIFIED=2")
    print("A04_INDIRECT_DESTINATIONS_EXECUTED=0")
    print("A04_FAILED=0")
    print("A04_NEW_CERTIFICATES=0")


if __name__ == "__main__":
    main()
