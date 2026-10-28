#!/usr/bin/env python3
"""A04: bounded static audit of seven original-ELF A02 branch destinations.

Static disassembly is only a hypothesis; never asserts full CFG, semantic
equivalence, code/data certainty, or application completion.
"""
import argparse
import hashlib
import json
from collections import defaultdict
from pathlib import Path

from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
from capstone.arm import (
    ARM_INS_B, ARM_INS_BL, ARM_INS_BLX, ARM_INS_BX, ARM_INS_LDR,
    ARM_INS_POP, ARM_OP_IMM, ARM_REG_PC,
)

import semantic_a02_branch_11 as a02
import semantic_evidence

ELF_DIGEST = "bf913415ab9458a83b14ac8c8a0fa3430d1f5d18bfbcd7c7472d6f5e8b4850bc"
BYTES_PER_DEST = 96
MAX_INSNS = 24
TRANSFERS = {ARM_INS_B, ARM_INS_BL, ARM_INS_BLX, ARM_INS_BX}


def mapped_sources():
    mapping = defaultdict(list)
    for key, (hexbytes, operation) in a02.EXPECTED.items():
        spec = a02.decode(bytes.fromhex(hexbytes), int(key, 16))
        if spec is None or spec["op"] != operation:
            raise ValueError("Invalid A02 byte-based source")
        if operation != "self_branch":
            mapping[spec["target"]].append({"entry": key, "op": operation})
    if len(mapping) != 7 or sum(len(v) for v in mapping.values()) != 10:
        raise ValueError("A02 expected ten sources into seven targets")
    return {f"{addr:08x}": sorted(rows, key=lambda x: x["entry"])
            for addr, rows in sorted(mapping.items())}


def verify_sources(binary):
    md = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    for addr, (expected, op) in a02.EXPECTED.items():
        address = int(addr, 16)
        data = semantic_evidence.read_function(binary, address, len(bytes.fromhex(expected)))
        ins = list(md.disasm(data, address))
        if data.hex() != expected or a02.decode(data, address) is None:
            raise ValueError("A02 original ELF source mismatch: " + addr)
        if op == "self_branch":
            if len(ins) != 1 or ins[0].mnemonic != "b":
                raise ValueError("A02 self-loop not proven")
        elif len(ins) != 2 or ins[1].mnemonic != "b":
            raise ValueError("A02 original branch disagrees with Capstone")


def is_transfer(ins):
    if ins.id in TRANSFERS:
        return True
    if ins.id == ARM_INS_POP and "pc" in ins.op_str:
        return True
    if ins.id == ARM_INS_LDR and ins.operands and ins.operands[0].reg == ARM_REG_PC:
        return True
    return False


def inspect(binary, addr, from_entries):
    raw = semantic_evidence.read_function(binary, addr, BYTES_PER_DEST)
    md = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    md.detail = True
    instructions = []
    boundary = None
    for ins in md.disasm(raw, addr):
        if len(instructions) >= MAX_INSNS:
            break
        instructions.append({"pc": f"{ins.address:08x}", "hex": ins.bytes.hex(),
                             "mnemonic": ins.mnemonic, "operands": ins.op_str})
        if is_transfer(ins):
            direct = None
            if ins.id in TRANSFERS and ins.operands and ins.operands[0].type == ARM_OP_IMM:
                direct = f"{ins.operands[0].imm & 0xffffffff:08x}"
            boundary = {"pc": f"{ins.address:08x}", "op": ins.mnemonic,
                        "immediate_destination": direct, "executed": False}
            break
    if not instructions or instructions[0]["pc"] != f"{addr:08x}":
        raise ValueError("Destination not aligned to candidate ARM disassembly")
    return {"address": f"{addr:08x}", "from": from_entries,
            "raw_hex": raw.hex(), "read_bytes": len(raw),
            "candidate_insns": instructions, "first_transfer": boundary,
            "status": "bounded_static_candidate", "code_vs_data": "unproven",
            "semantics": "unexecuted", "whole_function": "unknown"}


def build(binary):
    if hashlib.sha256(binary.read_bytes()).hexdigest() != ELF_DIGEST:
        raise ValueError("Original A04 ELF hash mismatch")
    verify_sources(binary)
    mapping = mapped_sources()
    targets = [inspect(binary, int(target, 16), entries)
               for target, entries in mapping.items()]
    if len(targets) != 7:
        raise AssertionError("Missing distinct destinations")
    return {"schema": 1, "elf_sha256": ELF_DIGEST,
            "sources_checked": len(a02.EXPECTED),
            "unique_external_targets": len(targets),
            "original_file_bytes": sum(x["read_bytes"] for x in targets),
            "destinations_executed": 0, "new_certificates": 0,
            "self_loop": {"address": "002a1268",
                          "termination": "unproven", "reachability": "unknown"},
            "targets": targets}


def report(state):
    lines = ["# A04: original ELF destinations, bounded structural inspection",
             "", "ELF SHA-256: " + state["elf_sha256"], "",
             "Seven unique external destinations, 672 original file-backed "
             "bytes inspected, zero executed destinations, zero new certificates.",
             "", "This is a first-block *candidate* scan in ARM mode. "
             "An executable ELF segment does NOT prove bytes represent code.",
             "", "| Destination | A02 incoming entries | Candidate instructions | First transfer |",
             "|---|---|---:|---|"]
    for target in state["targets"]:
        b = target["first_transfer"]
        desc = (b["op"] + " at " + b["pc"]
                + (" to " + b["immediate_destination"] if b["immediate_destination"] else "")
                if b else "not reached within 96 bytes")
        lines.append("| " + target["address"] + " | " +
                     ", ".join(row["entry"] for row in target["from"]) + " | " +
                     str(len(target["candidate_insns"])) + " | " + desc + " |")
    for target in state["targets"]:
        lines.extend(["", "## " + target["address"], "",
                      "Incoming: " + ", ".join(row["entry"] + "/" + row["op"]
                                                for row in target["from"]),
                      "", "~~~asm"])
        for ins in target["candidate_insns"]:
            lines.append(ins["pc"] + ": " + ins["mnemonic"] + " " + ins["operands"])
        lines.extend(["~~~"])
    lines.extend(["", "## Semantics not yet established", "",
                  "- Shared 0x000b6c58 receives four different R2 values, "
                  "but the dispatcher effects remain unverified.",
                  "- All destination instruction execution, downstream CFG, "
                  "code/data provenance and full function equivalence are pending.",
                  "- 0x002a1268 is an observed self-branch, without termination "
                  "or dynamic reachability proof.",
                  "- No semantic certificates were created.", ""])
    return "\n".join(lines)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--binary", type=Path, required=True)
    p.add_argument("--checkpoint", type=Path, required=True)
    p.add_argument("--report", type=Path, required=True)
    args = p.parse_args()
    result = build(args.binary)
    serialized = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.checkpoint.is_file():
        if args.checkpoint.read_text(encoding="utf-8") != serialized:
            raise ValueError("A04 static checkpoint not reproducible")
    else:
        args.checkpoint.parent.mkdir(parents=True, exist_ok=True)
        args.checkpoint.write_text(serialized, encoding="utf-8")
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(report(result), encoding="utf-8")
    print("A04_ORIGINAL_ELF=1")
    print(f"A04_DISTINCT_TARGETS={result['unique_external_targets']}")
    print(f"A04_AUDITED_FILE_BYTES={result['original_file_bytes']}")
    print("A04_TARGETS_EXECUTED=0")
    print("A04_NEW_CERTIFICATES=0")
    print("A04_AUDIT_REPLAY=PASS")


if __name__ == "__main__":
    main()
