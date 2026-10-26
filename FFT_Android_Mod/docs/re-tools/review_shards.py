#!/usr/bin/env python3
"""Deterministically partition outstanding ARM reviews among independent workers.

This tool only writes separate manifests. It never modifies checkpoints.
"""
import argparse
import csv
import json
from pathlib import Path


def build_shards(queue, results, workers=5, limit=25):
    if not (1 <= workers <= 16 and limit >= 1):
        raise ValueError("workers must be 1..16 and limit positive")
    with Path(queue).open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    tasks, seen = [], set()
    for row in rows:
        address = row["address"].strip().lower().removeprefix("0x")
        if len(address) != 8 or any(c not in "0123456789abcdef" for c in address):
            raise ValueError(f"invalid address: {address}")
        if address in seen:
            continue
        seen.add(address)
        checkpoint = json.loads((Path(results) / (address + ".json")).read_text())
        if (checkpoint.get("address", "").lower().removeprefix("0x") != address
                or checkpoint.get("status") != "needs_review"
                or int(checkpoint.get("size", 0)) <= 0
                or not checkpoint.get("binary_sha256")):
            raise ValueError(f"invalid review checkpoint: {address}")
        tasks.append({
            "address": address,
            "name": checkpoint.get("name", row.get("name", "")),
            "size": int(checkpoint["size"]),
            "binary_sha256": checkpoint["binary_sha256"],
            "reason": checkpoint.get("structural_v3", {}).get("reason", "unclassified"),
        })
    tasks.sort(key=lambda x: (-x["size"], x["address"]))
    shards = [[] for _ in range(workers)]
    byte_loads = [0] * workers
    for task in tasks[:limit]:
        worker = min(range(workers), key=lambda i: (byte_loads[i], i))
        shards[worker].append(task)
        byte_loads[worker] += task["size"]
    return shards


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    root = Path(__file__).resolve().parents[1]
    parser.add_argument("--queue", type=Path, default=root / "re-results/REVIEW_QUEUE.csv")
    parser.add_argument("--results", type=Path, default=root / "re-results")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--workers", type=int, default=5)
    parser.add_argument("--limit", type=int, default=25)
    args = parser.parse_args()
    shards = build_shards(args.queue, args.results, args.workers, args.limit)
    args.output.mkdir(parents=True, exist_ok=True)
    for i, tasks in enumerate(shards, 1):
        manifest = {
            "schema": 1,
            "worker": i,
            "work_bytes": sum(t["size"] for t in tasks),
            "tasks": tasks,
            "instructions": (
                "Inspect only assigned addresses; write a separate evidence artifact. "
                "Do not modify shared reports or approve semantic equivalence."
            ),
        }
        path = args.output / f"worker-{i:02d}.json"
        path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")
        print(f"{path}: {len(tasks)} tasks, {manifest['work_bytes']} bytes")
    print(f"TOTAL_TASKS={sum(map(len, shards))}")


if __name__ == "__main__":
    main()
