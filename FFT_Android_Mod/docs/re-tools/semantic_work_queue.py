#!/usr/bin/env python3
"""Build deterministic semantic-analysis work manifests for every uncertified symbol.

Read-only against semantic certificates; never promotes partial evidence.
"""
import argparse
import hashlib
import json
from pathlib import Path

import semantic_coverage


def partition(rows, digest, workers, limit, priority_addresses=()):
    if not 1 <= workers <= 32 or limit < 1:
        raise ValueError("workers must be 1..32 and limit >= 1")
    pending = [r for r in rows if r["semantic_status"] != "certified"]
    priority = set(priority_addresses)
    pending.sort(key=lambda r: (
        0 if r["address"] in priority else
        1 if r["semantic_status"] == "partial" else 2,
        r["size"], r["address"]))
    shards = [[] for _ in range(workers)]
    loads = [0] * workers
    for row in pending[:limit]:
        worker = min(range(workers), key=lambda n: (loads[n], n))
        shards[worker].append({
            "address": row["address"], "size": row["size"],
            "name": row["name"], "prior_status": row["semantic_status"],
            "binary_sha256": digest,
            "required_evidence": [
                "complete_control_flow", "call_targets", "register_contract",
                "memory_contract", "boundary_conditions",
                "differential_or_reference_tests", "unresolved_paths"
            ],
        })
        loads[worker] += row["size"]
    return shards


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--inventory", type=Path, default=semantic_coverage.INVENTORY)
    p.add_argument("--binary", type=Path, default=semantic_coverage.BINARY)
    p.add_argument("--certificates", type=Path,
                   default=semantic_coverage.RESULTS / "semantic-certificates.json")
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--workers", type=int, default=5)
    p.add_argument("--candidate-evidence-dir", type=Path,
                   help="Optional same-ELF BX LR proof candidates to prioritize")
    p.add_argument("--limit", type=int, default=100)
    args = p.parse_args()
    digest = hashlib.sha256(args.binary.read_bytes()).hexdigest()
    certificates = (json.loads(args.certificates.read_text(encoding="utf-8"))
                    if args.certificates.is_file() else {})
    rows = semantic_coverage.ledger(args.inventory, digest, certificates)
    priorities = set()
    if args.candidate_evidence_dir is not None:
        for path in sorted(args.candidate_evidence_dir.glob("*.json")):
            record = json.loads(path.read_text(encoding="utf-8"))
            if not record.get("contract_candidate"):
                continue
            if record.get("binary_sha256") != digest or record.get("certified") is not False:
                raise ValueError(f"stale or invalid contract candidate: {path}")
            address = str(record.get("address", "")).lower().removeprefix("0x")
            if address != path.stem or record.get("size") != 4:
                raise ValueError(f"mismatched candidate address: {path}")
            priorities.add(address)
    shards = partition(rows, digest, args.workers, args.limit, priorities)
    args.output.mkdir(parents=True, exist_ok=True)
    for i, tasks in enumerate(shards, 1):
        output = args.output / f"semantic-worker-{i:02d}.json"
        output.write_text(json.dumps({
            "schema": 1, "worker": i, "elf_sha256": digest,
            "total_bytes": sum(t["size"] for t in tasks), "tasks": tasks
        }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"WORKER_{i:02d}_TASKS={len(tasks)}")
    print(f"TOTAL_TASKS={sum(len(s) for s in shards)}")
    print(f"PRIORITIZED_CONTRACT_CANDIDATES={len(priorities)}")
    print(f"SEMANTIC_PENDING={sum(r['semantic_status'] != 'certified' for r in rows)}")


if __name__ == "__main__":
    main()
