#!/usr/bin/env python3
"""B01: evidence-tiered A32 *candidate* callsites into seven named C++ bodies.

A linear scan of executable ELF bytes may decode literal pools as BL/B/BLX.
Neither a possible owner nor a structural checkpoint establishes an executed
caller, an object layout, a valid R0 pointer or a real call contract.
"""
import argparse
import json
from collections import Counter
from pathlib import Path

from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
from elftools.elf.elffile import ELFFile

import b01_overlap_cfg_callers as cfg
import b01_overlap_elf_evidence as original
import b01_source_evidence_filter as source
import b01_seven_cpp_contracts as methods


CANDIDATE_TIERS = {
    "structurally_anchored_candidate": 0,
    "explicitly_unresolved_source": 1,
    "unresolved_source": 2,
    "no_inventory_owner": 3,
}


def classify(incoming, entries, checkpoints, binary_sha, inventory_sha, scanned):
    if binary_sha != original.PINNED_ELF_SHA:
        raise ValueError("B01 source must use pinned original ELF")
    targets = set(methods.SEVEN)
    if set(incoming) != targets:
        raise ValueError("Incomplete seven-method target population")
    # Preserve all source candidates without treating a linear decode as proven.
    starts = [item["start"] for item in entries]
    if starts != sorted(starts):
        raise ValueError("Inventory entries not sorted")
    prefix, greatest = [], 0
    for item in entries:
        greatest = max(greatest, item["end"])
        prefix.append(greatest)
    rows = []
    seen = set()
    for dest in sorted(targets):
        candidates = incoming[dest]
        if len(candidates["witnesses"]) != candidates["total"]:
            raise ValueError("Truncated candidate evidence")
        for candidate in candidates["witnesses"]:
            if candidate["target"] != f"{dest:08x}":
                raise ValueError("Target witness mismatch")
            site = int(candidate["source"], 16)
            opcode = candidate["instruction_hex"]
            key = (site, dest)
            if key in seen:
                raise ValueError("Duplicate source/target pair")
            seen.add(key)
            owners = source.candidate_owners(entries, site, starts, prefix)
            tier, anchors = source.evidence_tier(site, owners, checkpoints, binary_sha)
            if tier not in CANDIDATE_TIERS:
                raise ValueError("Unknown checkpoint tier")
            name = candidate["mnemonic"].lower()
            call_kind = ("candidate_direct_call" if name.startswith(("bl",))
                         else "candidate_branch_or_tail_call")
            # Only ranks work, never promotes any address to verified status.
            rows.append({
                "candidate_source": candidate["source"],
                "candidate_target": candidate["target"],
                "encoded_instruction_hex": opcode,
                "decoded_mnemonic": candidate["mnemonic"],
                "candidate_kind": call_kind,
                "source_inventory_owners": [f"{x['start']:08x}" for x in owners],
                "source_checkpoint_tier": tier,
                "source_checkpoint_details": anchors,
                "review_priority": CANDIDATE_TIERS[tier],
                "linear_sweep_not_execution": True,
                "caller_reachable": False,
                "real_this_pointer_proven": False,
                "object_layout_proven": False,
                "original_function_invoked": False
            })
    rows.sort(key=lambda x: (x["review_priority"],
                             x["candidate_kind"] != "candidate_direct_call",
                             x["candidate_target"], x["candidate_source"]))
    counts = Counter(x["source_checkpoint_tier"] for x in rows)
    by_target = {f"{x:08x}": sum(r["candidate_target"] == f"{x:08x}"
                               for r in rows) for x in sorted(targets)}
    return {
        "schema": 1, "task": "B01", "elf_sha256": binary_sha,
        "inventory_csv_sha256": inventory_sha,
        "scanned_executable_segment_bytes": scanned,
        "targets": [f"{x:08x}" for x in sorted(targets)],
        "linear_sweep_candidate_callsites": len(rows),
        "by_target": by_target,
        "tiers": dict(sorted(counts.items())),
        "candidate_callsites": rows,
        "verified_original_callers": 0,
        "verified_this_pointer_sources": 0,
        "verified_object_layouts": 0,
        "semantic_certificates_added": 0,
        "B01_done": False,
        "caution": "A32 linear-sweep candidates may be inline data, alternate ISA or unreachable code."
    }


def audit(binary, inventory, checkpoints):
    if original.sha256(binary) != original.PINNED_ELF_SHA:
        raise ValueError("Original ELF digest changed")
    entries = original.get_entries(inventory)
    methods.names_by_entry(inventory)  # Fail closed if seven names/sizes drift.
    decoder = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    decoder.detail = True
    with binary.open("rb") as stream:
        elf = ELFFile(stream)
        if elf.elfclass != 32 or not elf.little_endian or elf["e_machine"] != "EM_ARM":
            raise ValueError("Expected original ELF32 A32 ARM")
        incoming, scanned = cfg.candidate_callers(
            elf, stream, set(methods.SEVEN), decoder, max_witnesses=50000)
    return classify(incoming, entries, checkpoints,
                    original.PINNED_ELF_SHA, original.sha256(inventory), scanned)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    root = Path(__file__).resolve().parents[2]
    p.add_argument("--binary", type=Path,
                   default=root / "src/lib/armeabi/libgl2jni.so")
    p.add_argument("--inventory", type=Path,
                   default=root / "docs/RE_FUNCTION_INVENTORY.csv")
    p.add_argument("--results", type=Path,
                   default=root / "docs/re-results")
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()
    report = audit(args.binary, args.inventory, args.results)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, sort_keys=True, indent=2) + "\n",
                           encoding="utf-8")
    print("B01_SEVEN_CALLSITE_CANDIDATES=" + str(report["linear_sweep_candidate_callsites"]))
    for target, count in report["by_target"].items():
        print("B01_CALLSITE_CANDIDATES_" + target + "=" + str(count))
    print("B01_VERIFIED_ORIGINAL_CALLERS=0")
    print("B01_NEW_SEMANTIC_CERTIFICATES=0")


if __name__ == "__main__":
    main()
