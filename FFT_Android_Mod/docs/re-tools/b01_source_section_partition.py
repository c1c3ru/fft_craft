#!/usr/bin/env python3
"""B01: partition all 2,126 A32 references by real ELF sections and owner gaps.

A PF_X segment or SHF_EXECINSTR section does NOT establish that a linear-sweep
instruction is code. Every emitted source stays unresolved until CFG proof.
"""
import argparse
import bisect
import json
from collections import Counter
from pathlib import Path

from elftools.elf.elffile import ELFFile
import b01_source_evidence_filter as source
import b01_overlap_elf_evidence as baseline


def section_for_address(sections, addr):
    hits = [s for s in sections if s["start"] <= addr < s["end"]]
    if not hits:
        return None
    # Smallest containing section is the most specific, deterministically.
    return sorted(hits, key=lambda x: (x["end"]-x["start"], x["name"]))[0]


def section_inventory(elf):
    sections = []
    for s in elf.iter_sections():
        size = int(s["sh_size"])
        if not size or s["sh_type"] == "SHT_NOBITS":
            continue
        start = int(s["sh_addr"])
        sections.append({"start": start, "end": start+size,
                         "name": s.name, "elf_exec_flag": bool(int(s["sh_flags"]) & 4)})
    return sections


def classify(report, sections, entries):
    if report["source_elf_sha256"] != baseline.PINNED_ELF_SHA:
        raise ValueError("Unexpected ELF digest in source evidence")
    if report["confirmed_runtime_callers"] or report["confirmed_executable_source_instructions"]:
        raise ValueError("Cannot assume runtime/static proof from linear sweep")
    items = []
    counts = Counter()
    detail = Counter()
    starts = [x["start"] for x in entries]
    seen = set()
    for target, rows in sorted(report["sources_by_target"].items()):
        for row in rows:
            key = (row["source"], target)
            if key in seen:
                raise ValueError("Duplicate ARM xref source/target")
            seen.add(key)
            if row["target"] != target:
                raise ValueError("Inconsistent candidate target")
            addr = int(row["source"], 16)
            sec = section_for_address(sections, addr)
            zone = ("unmapped_to_named_section" if sec is None else
                    "exec_flagged_section" if sec["elf_exec_flag"] else
                    "non_exec_section")
            category = (
                "inventory_gap_unproven" if row["tier"] == "no_inventory_owner"
                else "owned_unresolved_not_confirmed"
                if row["tier"] in ("unresolved_source", "explicitly_unresolved_source")
                else "structural_candidate_still_not_runtime_proven"
            )
            prior_idx = bisect.bisect_right(starts, addr) - 1
            near = entries[prior_idx] if prior_idx >= 0 else None
            next_idx = bisect.bisect_right(starts, addr)
            after = entries[next_idx] if next_idx < len(entries) else None
            if sec and sec["name"].startswith(".plt"):
                # PLT mapping is descriptive, not confirmation of executable code.
                detail["plt_named_section_candidate"] += 1
            counts[category] += 1
            detail[zone] += 1
            items.append({
                "source": row["source"], "target": target, "opcode": row["opcode"],
                "candidate_mnemonic": row["mnemonic"],
                "source_evidence_tier": row["tier"],
                "owners": row["anchors"],
                "region": zone, "section": sec["name"] if sec else None,
                "nearest_preceding_declared_entry":
                    f"{near['start']:08x}" if near else None,
                "nearest_following_declared_entry":
                    f"{after['start']:08x}" if after else None,
                "classification": category,
                "source_instruction_confirmed": False,
                "edge_reachable_from_proven_entry": False,
                "indirect_edges_resolved": False,
                "proof_type": "ELF_section_and_inventory_metadata_only"
            })
    if len(items) != report["all_linear_sweep_candidates"]:
        raise ValueError("Lost candidate source evidence")
    return {
        "schema": 1, "stage": "B01",
        "source_elf_sha256": baseline.PINNED_ELF_SHA,
        "inventory_csv_sha256": report["input_inventory_sha256"],
        "xref_candidate_count": len(items),
        "original_source_evidence_tiers": report["tier_counts"],
        "partition_counts": dict(sorted(counts.items())),
        "elf_section_counts": dict(sorted(detail.items())),
        "candidates": items,
        "confirmed_instructions": 0, "confirmed_call_edges": 0,
        "indirect_branch_equivalence_proven": False,
        "semantic_certificates_issued": 0, "B01_done": False
    }


def audit(binary, inventory, checkpoints):
    if baseline.sha256(binary) != baseline.PINNED_ELF_SHA:
        raise ValueError("Original ELF digest changed")
    report = source.audit(binary, inventory, checkpoints)
    with binary.open("rb") as f:
        elf = ELFFile(f)
        if elf.elfclass != 32 or not elf.little_endian or elf["e_machine"] != "EM_ARM":
            raise ValueError("Expected original ELF32 ARM little endian")
        sections = section_inventory(elf)
    return classify(report, sections, baseline.get_entries(inventory))


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--binary",type=Path,required=True)
    p.add_argument("--inventory",type=Path,required=True)
    p.add_argument("--checkpoints",type=Path,required=True)
    p.add_argument("--output",type=Path,required=True)
    args=p.parse_args()
    result=audit(args.binary,args.inventory,args.checkpoints)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    print("B01_GAP_OR_UNKNOWN_XREFS="+str(result["xref_candidate_count"]))
    for kind,count in result["partition_counts"].items():
        print("B01_PARTITION_"+kind.upper()+"="+str(count))
    for kind,count in result["elf_section_counts"].items():
        print("B01_SECTION_"+kind.upper()+"="+str(count))
    print("B01_CODE_PROVEN=0")
    print("B01_SEMANTIC_CERTIFICATES_ADDED=0")


if __name__ == "__main__":
    main()
