#!/usr/bin/env python3
"""Read-only, untrusted Craft Anything evidence -> T39 ARM queue annotations.

Never use the source's confidence labels as equivalence or runtime proof.
Only a verified SHA-256 target match and address location may join a queue;
the exporter record IDs are retained as unverified provenance references.
"""
import argparse
import json
import re
from collections import defaultdict
from pathlib import Path

MAX_BYTES = 8 * 1024 * 1024
MAX_RECORDS = 5000
EVIDENCE_ID = re.compile(r"ev_[0-9a-f]{64}\Z")
HEX_ADDRESS = re.compile(r"0x[0-9a-fA-F]{1,8}\Z")
OPERATIONS = {
    "native_function_show", "native_function_disassemble",
    "native_function_callers_list", "native_function_callees_list",
    "native_function_references_list", "native_function_pseudocode",
    "native_function_study", "native_call_graph_show",
    "native_call_path_find", "native_value_flow_show",
    "native_instruction_show", "native_call_site_resolve",
    "native_function_find", "native_function_instructions_list",
    "native_xrefs_list", "native_functions_decompile",
}


def load_limited(path):
    path = Path(path)
    if path.stat().st_size > MAX_BYTES:
        raise ValueError("Oversized external evidence file")
    return json.loads(path.read_text(encoding="utf-8"))


def index_queue(queue):
    if queue.get("schema") != 1 or queue.get("task_count") != 40:
        raise ValueError("Invalid T39 queue or task count")
    sha = queue.get("elf_sha256")
    if not isinstance(sha, str) or not re.fullmatch(r"[a-f0-9]{64}", sha):
        raise ValueError("No ELF identity on T39 queue")
    gaps = queue.get("t04", {}).get("candidates", [])
    reviews = queue.get("t06", {}).get("candidates", [])
    if (len(gaps) != queue["t04"].get("interval_count")
            or len(reviews) != queue["t06"].get("current_review_count")):
        raise ValueError("Truncated official T39 review queue")
    ranges = []
    for item in gaps:
        start = int(item["address"], 16)
        size = item["size"]
        if not isinstance(size, int) or size < 1:
            raise ValueError("Invalid gap length")
        ranges.append((start, start + size, item["address"]))
    review_map = {int(x["address"], 16): x["address"] for x in reviews}
    if len(review_map) != len(reviews):
        raise ValueError("Duplicate T06 review address")
    return sha, ranges, review_map


def reconcile(queue, bundle):
    sha, ranges, review_map = index_queue(queue)
    if (not isinstance(bundle, dict)
            or bundle.get("format") != "craft-anything-evidence-bundle"
            or bundle.get("version") != 1
            or not isinstance(bundle.get("records"), list)):
        raise ValueError("Expected Craft Anything export bundle v1")
    records = bundle["records"]
    if len(records) > MAX_RECORDS:
        raise ValueError("Too many external evidence records")
    seen = set()
    annotations = defaultdict(list)
    ignored_irrelevant, ignored_addressless = 0, 0
    for item in records:
        if not isinstance(item, dict):
            raise ValueError("Malformed evidence record")
        identifier, target, operation = (item.get("id"), item.get("subject"),
                                          item.get("operation"))
        if not isinstance(identifier, str) or not EVIDENCE_ID.fullmatch(identifier):
            raise ValueError("Invalid external evidence ID")
        if identifier in seen:
            raise ValueError("Duplicate external evidence record")
        seen.add(identifier)
        if not isinstance(target, dict) or target.get("sha256") != sha:
            raise ValueError("Foreign or unpinned original binary evidence")
        if target.get("kind") != "native":
            raise ValueError("External record not tied to native target")
        if operation not in OPERATIONS:
            ignored_irrelevant += 1
            continue
        locations = item.get("locations", [])
        if not isinstance(locations, list):
            raise ValueError("Invalid external location set")
        addresses = set()
        for place in locations:
            if not isinstance(place, dict):
                raise ValueError("Malformed external location")
            if place.get("kind") != "address":
                continue
            raw = place.get("value")
            if not isinstance(raw, str) or not HEX_ADDRESS.fullmatch(raw):
                raise ValueError("Non-hex external address")
            addresses.add(int(raw, 16))
        if not addresses:
            ignored_addressless += 1
        for addr in addresses:
            destinations = [("T04", label) for lo, hi, label in ranges
                            if lo <= addr < hi]
            if addr in review_map:
                destinations.append(("T06", review_map[addr]))
            for task, label in destinations:
                # Only carry safe metadata, never target bytes, pseudo-C,
                # generated text, recommendations or untrusted instructions.
                annotations[(task, label)].append({
                    "evidence_id_unverified": identifier,
                    "operation": operation,
                    "address": f"0x{addr:08x}",
                    "independent_validation_required": True,
                })
    items = [{"task": task, "queue_address": label,
              "craft_evidence_count": len(records),
              "external_evidence": records}
             for (task, label), records in sorted(annotations.items())]
    return {
        "schema": 1, "target_elf_sha256": sha,
        "input_format": "craft-anything-evidence-bundle/v1",
        "input_records": len(bundle["records"]),
        "unique_input_evidence_ids": len(seen),
        "ignored_operations": ignored_irrelevant,
        "relevant_records_without_locations": ignored_addressless,
        "queue_matches": len(items), "matched": items,
        "source_id_cryptographic_verification_performed": False,
        "original_elf_reexecuted": False,
        "new_semantic_certificates": 0, "new_structural_approvals": 0,
        "task_status_changed": False, "integrated_third_party_code": False,
        "purpose": "triage_only_no_equivalence_claims"
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--queue", type=Path, required=True)
    parser.add_argument("--bundle", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    a = parser.parse_args()
    result = reconcile(load_limited(a.queue), load_limited(a.bundle))
    a.output.parent.mkdir(parents=True, exist_ok=True)
    a.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n",
                        encoding="utf-8")
    print("CRAFT_EVIDENCE_MATCHED_QUEUE_ITEMS=" + str(result["queue_matches"]))
    print("CRAFT_NEW_SEMANTIC_CERTIFICATES=0")
    print("CRAFT_AUTO_APPROVALS=0")


if __name__ == "__main__":
    main()
