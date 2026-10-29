#!/usr/bin/env python3
"""Fail-closed consistency gate for the unresolved A04 original-ELF boundaries.

This is a tracker integrity gate, not a semantic certificate or ELF execution.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRACKER = ROOT / "re-results" / "RE_COMPLETION_TRACKER.json"
EXPECTED_ELF = "bf913415ab9458a83b14ac8c8a0fa3430d1f5d18bfbcd7c7472d6f5e8b4850bc"
REQUIRED = {
    "0x000ab674", "0x000b6620", "0x000b461c", "0x000b45d0",
    "0x002b1bb0", "0x002b1bb8", "0x002a1268",
}
PAIRS = (("0x000ab674", "0x000b6620"), ("0x000b461c", "0x000b45d0"))


def audit(tracker):
    if tracker.get("elf_sha256") != EXPECTED_ELF:
        raise ValueError("A04 ELF baseline changed: create a new verified baseline")
    tasks = [t for t in tracker.get("tasks", []) if t.get("id") == "A04"]
    if len(tasks) != 1:
        raise ValueError("A04 must appear exactly once")
    task = tasks[0]
    if task.get("status") != "in_progress":
        raise ValueError("A04 must remain in_progress until whole-flow evidence is reviewed")
    next_action = task.get("next_action", "").lower()
    missing = sorted(address for address in REQUIRED if address not in next_action)
    if missing:
        raise ValueError("A04 next_action omits original ELF boundaries: " + ", ".join(missing))
    if "reachability" not in next_action and "alcançabilidade" not in next_action:
        raise ValueError("A04 must explicitly track self-loop reachability")
    if not task.get("acceptance") or not task.get("evidence"):
        raise ValueError("A04 needs acceptance criteria and traceable existing evidence")
    return {"elf_sha256": EXPECTED_ELF, "task": "A04", "status": "in_progress",
            "unresolved_addresses": sorted(REQUIRED), "bl_pairs": PAIRS,
            "semantic_certificates_created": 0, "callees_executed_by_gate": 0}


def main():
    result = audit(json.loads(TRACKER.read_text(encoding="utf-8")))
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
