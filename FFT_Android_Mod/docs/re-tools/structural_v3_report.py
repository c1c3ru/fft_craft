#!/usr/bin/env python3
"""Report v2 preservation, v3 upgrades, code/literal gaps and verified tables."""
import argparse
from collections import Counter
import json
from pathlib import Path


def render(results):
    counts = Counter()
    findings = []
    for file in sorted(results.glob("*.json")):
        try:
            row = json.loads(file.read_text(encoding="utf-8"))
        except (ValueError, OSError):
            continue
        if row.get("structural_version") != 3:
            counts["legacy"] += 1
            continue
        counts["v3"] += 1
        counts[row.get("status", "unknown")] += 1
        fact = row.get("structural_v3", {})
        counts["literal_slots"] += len(fact.get("literal_slots", []))
        counts["unexplained_slots"] += fact.get("unexplained_count", 0)
        counts["safe_tables"] += sum(t.get("safe", False) for t in fact.get("tables", []))
        counts["unsafe_tables"] += sum(not t.get("safe", False)
                                       for t in fact.get("tables", []))
        if row.get("archived_previous_checkpoint"):
            counts["archives"] += 1
        if row.get("status") == "needs_review":
            findings.append((row.get("address"), fact.get("unexplained_count", 0),
                             fact.get("reason", "unknown")))
    lines = [
        "# Structural analyzer v3 — migration and coverage", "",
        "Automatic structural acceptance checks all ARM instruction slots, "
        "candidate PC-relative data words, unresolved flow and jump-table "
        "bounds/targets. It is **not semantic equivalence**.", "",
        "| Metric | Count |", "|---|---:|",
        f'| v3 checkpoints | {counts["v3"]} |',
        f'| Legacy checkpoint records unchanged | {counts["legacy"]} |',
        f'| v3 structurally accepted | {counts["auto_structural"]} |',
        f'| v3 still under review | {counts["needs_review"]} |',
        f'| Archived v2 originals | {counts["archives"]} |',
        f'| Referenced candidate literal words | {counts["literal_slots"]} |',
        f'| Unexplained instruction slots | {counts["unexplained_slots"]} |',
        f'| Independently checked jump tables | {counts["safe_tables"]} |',
        f'| Unsafe / unresolved checked tables | {counts["unsafe_tables"]} |',
        "", "## Remaining v3 review examples", "",
        "| Address | Unexplained slots | Reason |", "|---|---:|---|",
    ]
    for address, gaps, reason in findings[:30]:
        lines.append(f"| `{address}` | {gaps} | {reason} |")
    lines.extend(["", "## Migration contract", "",
                  "Original v2 JSON checkpoints are archived in "
                  "`structural-v2/` on first upgrade; unprocessed "
                  "checkpoints remain untouched.",
                  "A ruleset fingerprint prevents repeating unchanged v3 "
                  "checkpoints, but changed rules trigger selective reruns.",
                  "Missing instructions, ambiguous literal words and unsafe "
                  "table targets remain in review.", ""])
    return "\n".join(lines)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--results", type=Path,
                   default=Path(__file__).resolve().parents[2] / "docs/re-results")
    args = p.parse_args()
    dest = args.results / "STRUCTURAL_V3_REPORT.md"
    dest.write_text(render(args.results), encoding="utf-8")
    print(f"Wrote structural v3 report: {dest}")


if __name__ == "__main__":
    main()
