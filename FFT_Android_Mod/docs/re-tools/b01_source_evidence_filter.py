#!/usr/bin/env python3
"""B01: classify ALL A32 linear-sweep xrefs against same-ELF v3 checkpoints.

A checkpoint records structural evidence, not proof of execution. This script
never labels a candidate as a confirmed instruction, caller, or byte coverage.
"""
import argparse
import bisect
import json
from collections import Counter, defaultdict
from pathlib import Path

from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
from elftools.elf.elffile import ELFFile

import b01_overlap_cfg_callers as callers
import b01_overlap_elf_evidence as baseline

PINNED = baseline.PINNED_ELF_SHA


def candidate_owners(entries, address, starts, max_end_prefix):
    i = bisect.bisect_right(starts, address) - 1
    out = []
    while i >= 0 and max_end_prefix[i] > address:
        item = entries[i]
        if item["start"] <= address < item["end"]:
            out.append(item)
        i -= 1
    return out


def evidence_tier(source, owners, results, digest=PINNED):
    """Return candidate tiers; refuse promoting unbound/old checkpoint data."""
    statuses = []
    for item in owners:
        start = item["start"]
        path = results / f"{start:08x}.json"
        if not path.is_file():
            statuses.append({"owner": f"{start:08x}", "tier": "no_v3_anchor"})
            continue
        try:
            state = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            statuses.append({"owner": f"{start:08x}", "tier": "invalid_checkpoint"})
            continue
        if not (state.get("address") == f"{start:08x}"
                and state.get("size") == item["size"]
                and state.get("binary_sha256") == digest
                and state.get("pipeline_version") == 2
                and state.get("structural_version") == 3
                and isinstance(state.get("structural_v3"), dict)):
            statuses.append({"owner": f"{start:08x}", "tier": "stale_or_non_v3_checkpoint"})
            continue
        v3 = state["structural_v3"]
        addr = f"0x{source:08x}"
        def addresses(items):
            return {str(k).lower() for k in items if isinstance(k, str)}
        unknown = addresses(v3.get("unexplained_slots", []))
        literal = addresses(v3.get("literal_slots", []))
        if addr in unknown or addr in literal:
            tier = "v3_explicitly_unexplained_or_literal_slot"
        elif v3.get("status") == "auto_structural" and not unknown and not literal:
            tier = "v3_structurally_approved_candidate"
        else:
            # Being absent from unexplained_slots alone does NOT prove code.
            tier = "v3_reviewed_but_code_unproven"
        statuses.append({"owner": f"{start:08x}", "tier": tier,
                         "checkpoint_status": v3.get("status", "unknown")})
    if not statuses:
        return "no_inventory_owner", []
    tiers = {x["tier"] for x in statuses}
    if "v3_structurally_approved_candidate" in tiers:
        overall = "structurally_anchored_candidate"
    elif "v3_explicitly_unexplained_or_literal_slot" in tiers:
        overall = "explicitly_unresolved_source"
    else:
        overall = "unresolved_source"
    return overall, statuses


def audit(binary, inventory, results):
    if baseline.sha256(binary) != PINNED:
        raise ValueError("Original ELF SHA mismatch")
    entries = baseline.get_entries(inventory)
    pairs = baseline.get_pairs(entries)
    if len(pairs) != 15:
        raise ValueError("Canonical overlap pair count drift")
    targets = {x["start"] for pair in pairs for x in pair}
    decoder = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    decoder.detail = True
    with binary.open("rb") as stream:
        elf = ELFFile(stream)
        incoming, scanned = callers.candidate_callers(
            elf, stream, targets, decoder, max_witnesses=100000)
    starts = [x["start"] for x in entries]
    max_end_prefix = []
    max_end = 0
    for row in entries:
        max_end = max(max_end, row["end"])
        max_end_prefix.append(max_end)
    grouped = defaultdict(list)
    counts = Counter()
    total = 0
    for target, data in sorted(incoming.items()):
        if len(data["witnesses"]) != data["total"]:
            raise ValueError("Full source evidence truncated")
        for candidate in data["witnesses"]:
            source = int(candidate["source"], 16)
            tier, anchors = evidence_tier(
                source, candidate_owners(entries, source, starts, max_end_prefix),
                results)
            counts[tier] += 1
            total += 1
            grouped[f"{target:08x}"].append({
                "source": candidate["source"], "target": candidate["target"],
                "opcode": candidate["instruction_hex"],
                "mnemonic": candidate["mnemonic"],
                "tier": tier, "anchors": anchors,
                "actual_instruction_execution_proven": False,
            })
    if total != sum(v["total"] for v in incoming.values()):
        raise ValueError("Candidate accounting loss")
    return {
        "schema": 1, "source_elf_sha256": PINNED,
        "input_inventory_sha256": baseline.sha256(inventory),
        "scanned_executable_segment_bytes": scanned,
        "all_linear_sweep_candidates": total,
        "tier_counts": dict(sorted(counts.items())),
        "sources_by_target": dict(sorted(grouped.items())),
        "structurally_anchored_not_semantically_certified": True,
        "inline_data_ambiguity_retained": True,
        "confirmed_runtime_callers": 0,
        "confirmed_executable_source_instructions": 0,
        "new_semantic_certificates": 0,
        "B01_done": False
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--binary", type=Path, required=True)
    p.add_argument("--inventory", type=Path, required=True)
    p.add_argument("--results", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()
    x = audit(args.binary, args.inventory, args.results)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(x, indent=2, sort_keys=True)+"\n", encoding="utf-8")
    print("B01_ALL_CANDIDATES="+str(x["all_linear_sweep_candidates"]))
    for tier, count in x["tier_counts"].items():
        print("B01_"+tier.upper()+"="+str(count))
    print("B01_CONFIRMED_RUNTIME_CALLERS=0")
    print("B01_NEW_SEMANTIC_CERTIFICATES=0")


if __name__ == "__main__":
    main()
