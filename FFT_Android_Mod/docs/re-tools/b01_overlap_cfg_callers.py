#!/usr/bin/env python3
"""B01: bounded, candidate-only CFG and global direct caller audit for 9 ELF ARM groups.

An A32 linear sweep can interpret embedded data as instructions; all caller
and CFG edges here are *candidates*, not runtime or semantic proof.
"""
import argparse
import hashlib
import json
from collections import defaultdict, deque
from pathlib import Path

from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
from capstone.arm import (
    ARM_INS_B, ARM_INS_BL, ARM_INS_BLX, ARM_OP_IMM,
)
from elftools.elf.elffile import ELFFile

import b01_overlap_elf_evidence as baseline
from semantic_cfg import build_cfg

MAX_CALLER_WITNESSES = 40
MAX_EXEC_SCAN_BYTES = 16 * 1024 * 1024


def fmt(value):
    return f"{value:08x}"


def direct_target(insn):
    if (insn.id in (ARM_INS_B, ARM_INS_BL, ARM_INS_BLX)
            and len(insn.operands) == 1
            and insn.operands[0].type == ARM_OP_IMM):
        return int(insn.operands[0].imm) & 0xFFFFFFFF
    return None


def bounded_reachable(successors, entry):
    if entry not in successors:
        return set()
    pending = deque([entry])
    reached = {entry}
    while pending:
        node = pending.popleft()
        for target, _kind in successors[node]:
            if target not in reached:
                reached.add(target)
                pending.append(target)
    return reached


def candidate_callers(elf, stream, targets, md):
    """Linear-sweep A32 candidate XREFs; no claim of correct code/data split."""
    result = {entry: {"total": 0, "witnesses": []} for entry in targets}
    scanned = 0
    for segment in elf.iter_segments():
        if segment["p_type"] != "PT_LOAD" or not (int(segment["p_flags"]) & 1):
            continue
        size = int(segment["p_filesz"])
        start = int(segment["p_vaddr"])
        offset = int(segment["p_offset"])
        if size < 4:
            continue
        scanned += size
        if scanned > MAX_EXEC_SCAN_BYTES:
            raise ValueError("Executable scan exceeds size budget")
        stream.seek(offset)
        raw = stream.read(size)
        if len(raw) != size:
            raise ValueError("Truncated executable LOAD segment")
        # Keep alignment, so a byte in a literal pool cannot shift following
        # instruction slots. The sweep remains potentially unsound on data.
        aligned = (-start) % 4
        data = raw[aligned:]
        md.skipdata = True
        for insn in md.disasm(data, start + aligned):
            if insn.size != 4 or insn.address % 4:
                continue
            target = direct_target(insn)
            if target not in result:
                continue
            evidence = result[target]
            evidence["total"] += 1
            if len(evidence["witnesses"]) < MAX_CALLER_WITNESSES:
                evidence["witnesses"].append({
                    "source": fmt(insn.address), "instruction_hex": insn.bytes.hex(),
                    "mnemonic": insn.mnemonic, "target": fmt(target),
                    "candidate_only": True,
                })
    return result, scanned


def analyze_group(elf, stream, md, end, entrypoints, incoming):
    starts = sorted(int(s, 16) for s in entrypoints)
    lower, upper = starts[0], int(end, 16)
    if any(x % 4 for x in starts + [upper]) or lower >= upper:
        raise ValueError("Non A32-aligned or invalid common interval")
    raw, fileoff = baseline.read_executable(elf, stream, lower, upper - lower)
    if raw is None:
        raise ValueError("Group not file-backed executable")
    decoded = list(md.disasm(raw, lower))
    if not decoded or sum(i.size for i in decoded) != len(raw):
        raise ValueError("Group has incomplete A32 linear decode")
    instructions = {x.address: x for x in decoded}
    if len(instructions) != len(decoded) or any(i.address != lower + 4 * idx
                                                  for idx, i in enumerate(decoded)):
        raise ValueError("Decode slots not a contiguous A32 interval")
    successors, unknown = build_cfg(instructions)
    internal_edges = []
    external_calls = []
    for insn in decoded:
        target = direct_target(insn)
        if target is None:
            continue
        item = {"source": fmt(insn.address), "target": fmt(target),
                "mnemonic": insn.mnemonic, "instruction_hex": insn.bytes.hex()}
        if target in instructions:
            internal_edges.append(item)
        else:
            external_calls.append(item)
    rows = []
    for start in starts:
        reached = bounded_reachable(successors, start)
        candidates = incoming[start]
        # A direct reference inside a group may be a branch or simply a
        # decoded pool word. Witness locations must be proven separately.
        local = [r for r in candidates["witnesses"]
                 if lower <= int(r["source"], 16) < upper]
        outside = [r for r in candidates["witnesses"]
                   if not lower <= int(r["source"], 16) < upper]
        rows.append({
            "entrypoint": fmt(start),
            "first_instruction": {
                "address": fmt(start),
                "hex": instructions[start].bytes.hex(),
                "mnemonic": instructions[start].mnemonic,
                "operands": instructions[start].op_str,
            },
            "modeled_reachable_slots": len(reached),
            "modeled_reaches_common_end_last_slot": (upper - 4) in reached,
            "linear_sweep_incoming_count": candidates["total"],
            "incoming_inside_group": local,
            "incoming_outside_group": outside,
            "incoming_witnesses_truncated": candidates["total"] > len(candidates["witnesses"]),
            "runtime_reachable": None,
            "entrypoint_proven_by_real_control_flow": False,
        })
    return {
        "common_end": fmt(upper), "entrypoints": [fmt(x) for x in starts],
        "file_offset_first_entry": fileoff,
        "combined_interval_sha256": hashlib.sha256(raw).hexdigest(),
        "a32_decoded_slots": len(decoded),
        "direct_internal_branch_candidates": internal_edges,
        "direct_external_branch_call_candidates": external_calls,
        "unknown_cfg_edges": [{
            "at": fmt(address), "kind": kind,
            "target": fmt(target) if isinstance(target, int) else None,
        } for address, kind, target in unknown],
        "entrypoint_routes": rows,
        "all_edges_executed_or_verified": False,
        "all_entrypoints_reachability_proven": False,
    }


def audit(binary, inventory):
    if baseline.sha256(binary) != baseline.PINNED_ELF_SHA:
        raise ValueError("ELF SHA-256 mismatch")
    entries = baseline.get_entries(inventory)
    overlaps = baseline.get_pairs(entries)
    if len(overlaps) != 15:
        raise ValueError("Expected 15 overlapping pairs")
    ends = defaultdict(set)
    for first, second in overlaps:
        if first["end"] != second["end"]:
            raise ValueError("Unexpected non-coterminal overlap")
        ends[first["end"]].update((fmt(first["start"]), fmt(second["start"])))
    if len(ends) != 9:
        raise ValueError("Expected 9 groups")
    targets = {int(s, 16) for starts in ends.values() for s in starts}
    decoder = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    decoder.detail = True
    with binary.open("rb") as file:
        elf = ELFFile(file)
        if elf["e_machine"] != "EM_ARM" or elf.elfclass != 32 or not elf.little_endian:
            raise ValueError("Expected original 32-bit ARM ELF")
        incoming, scan_bytes = candidate_callers(elf, file, targets, decoder)
        decoder.skipdata = False
        groups = [analyze_group(elf, file, decoder, fmt(end), starts, incoming)
                  for end, starts in sorted(ends.items())]
    return {
        "schema": 1, "phase": "B01",
        "source_elf_sha256": baseline.PINNED_ELF_SHA,
        "inventory_csv_sha256": baseline.sha256(inventory),
        "a32_sweep_executable_bytes": scan_bytes,
        "a32_linear_sweep_may_decode_inline_data": True,
        "group_count": len(groups), "pair_count": len(overlaps),
        "groups": groups,
        "total_candidate_direct_incoming": sum(v["total"] for v in incoming.values()),
        "all_groups_cfg_proven": False,
        "original_process_executed": False,
        "semantic_certificates_issued": 0,
        "B01_done": False,
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--binary", type=Path, required=True)
    p.add_argument("--inventory", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()
    report = audit(args.binary, args.inventory)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("B01_GROUPS=%d" % report["group_count"])
    print("B01_LINEAR_SWEEP_INCOMING_CANDIDATES=%d" % report["total_candidate_direct_incoming"])
    print("B01_CFG_PROVEN=0")
    print("B01_CERTIFICATES_ADDED=0")


if __name__ == "__main__":
    main()
