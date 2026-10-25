#!/usr/bin/env python3
"""Audit checkpoints against the CSV; keep review separate from completion."""
import argparse
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path

ACCEPTED = {"auto_structural", "confirmed_by_similarity"}
REVIEW = {"needs_review"}
PREVIOUS = {"read_full", "read_structural", "confirmed_by_similarity"}


def summarize(inventory: Path, results: Path, binary: Path) -> dict:
    with inventory.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    digest = hashlib.sha256(binary.read_bytes()).hexdigest()
    statuses = Counter()
    sizes = Counter()
    reviews = []
    expected = {row["address"]: row for row in rows}
    seen = set()
    for path in sorted(results.glob("*.json")):
        try:
            record = json.loads(path.read_text(encoding="utf-8"))
        except (ValueError, OSError):
            continue
        address = record.get("address")
        row = expected.get(address)
        if not row or address in seen:
            continue
        if (record.get("binary_sha256") != digest
                or record.get("size") != int(row["size"])
                or record.get("pipeline_version") != 2):
            continue
        seen.add(address)
        status = record.get("status", "unknown")
        statuses[status] += 1
        sizes[status] += int(row["size"])
        if status in REVIEW or status == "error":
            reviews.append((int(row["size"]), address, row["demangled"],
                            status, record.get("coverage_pct", 0),
                            record.get("tables_unresolved", 0),
                            record.get("tables_resolved", 0)))
    historical = [r for r in rows if r["status"] in PREVIOUS]
    pending = [r for r in rows if r["status"] not in PREVIOUS and r["address"] not in seen]
    reviews.sort(reverse=True)
    total_bytes = sum(int(r["size"]) for r in rows)
    baseline_bytes = sum(int(r["size"]) for r in historical)
    accepted_bytes = sum(sizes[x] for x in ACCEPTED)
    return {"digest": digest, "rows": len(rows), "total_bytes": total_bytes,
            "historical_count": len(historical), "historical_bytes": baseline_bytes,
            "checkpoints": len(seen), "status_count": statuses,
            "accepted_count": sum(statuses[x] for x in ACCEPTED),
            "accepted_bytes": accepted_bytes,
            "review_count": sum(statuses[x] for x in REVIEW),
            "pending_count": len(pending), "pending_bytes": sum(int(r["size"]) for r in pending),
            "review_rows": reviews}


def render(data: dict) -> str:
    total = data["total_bytes"]
    accepted = data["accepted_bytes"]
    historical = data["historical_bytes"]
    lines = ["# Reverse engineering progress", "",
             f"Binary SHA-256: `{data['digest']}`", "",
             "| Metric | Quantity |",
             "|---|---:|",
             f"| Inventory total | {data['rows']:,} functions / {total:,} bytes |",
             f"| Previously analyzed in CSV | {data['historical_count']:,} functions / {historical:,} bytes |",
             f"| JSON checkpoints (all statuses) | {data['checkpoints']:,} |",
             f"| Newly accepted structurally | {data['accepted_count']:,} functions / {accepted:,} bytes |",
             f"| Needs review | {data['review_count']:,} functions |",
             f"| Not yet checkpointed | {data['pending_count']:,} functions / {data['pending_bytes']:,} bytes |",
             "", "## Checkpoint status", "",
             "| Status | Functions |",
             "|---|---:|"]
    for status, count in sorted(data["status_count"].items()):
        lines.append(f"| {status} | {count:,} |")
    lines.extend(["", "## Review queue (largest first)", "",
                  "| Address | Function | Bytes | Coverage % | Resolved tables | Unresolved tables |",
                  "|---|---|---:|---:|---:|---:|"])
    for size, address, name, status, coverage, unresolved, resolved in data["review_rows"]:
        clean_name = name.replace("|", "/")
        lines.append(f"| `{address}` | {clean_name} ({status}) | {size} | {coverage} | {resolved} | {unresolved} |")
    lines.extend(["", "> Structural acceptance does not establish semantic equivalence.",
                  "> Counts distinguish historical CSV statuses, new accepted checkpoints, and review cases.",
                  ""])
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    root = Path(__file__).resolve().parents[2]
    parser.add_argument("--inventory", type=Path, default=root / "docs/RE_FUNCTION_INVENTORY.csv")
    parser.add_argument("--results", type=Path, default=root / "docs/re-results")
    parser.add_argument("--binary", type=Path, default=root / "src/lib/armeabi/libgl2jni.so")
    args = parser.parse_args()
    report = render(summarize(args.inventory, args.results, args.binary))
    dest = args.results / "PROGRESS.md"
    tmp = dest.with_suffix(".md.tmp")
    tmp.write_text(report, encoding="utf-8")
    tmp.replace(dest)
    print(report.split("## Checkpoint status", 1)[0])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
