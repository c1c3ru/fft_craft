#!/usr/bin/env python3
"""Export a deterministic, core-first manual review worklist from ARM checkpoints."""
import argparse
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path


def classify(r):
    if int(r.get("tables_unresolved") or 0):
        return "unresolved_jump_table"
    if int(r.get("tables_resolved") or 0):
        return "resolved_jump_table_check"
    coverage = float(r.get("coverage_pct") or 0)
    return "coverage_below_95" if coverage < 95 else "indirect_flow_or_manual_check"


def build(inventory, core, results, binary):
    with inventory.open(newline="", encoding="utf-8") as f:
        rows = {r["address"].lower(): r for r in csv.DictReader(f)}
    with core.open(newline="", encoding="utf-8") as f:
        priorities = {r["address"].lower() for r in csv.DictReader(f)}
    sha = hashlib.sha256(binary.read_bytes()).hexdigest()
    output = []
    for p in results.glob("*.json"):
        try:
            r = json.loads(p.read_text(encoding="utf-8"))
            addr = r.get("address", "").lower()
            inv = rows.get(addr)
            if (inv is None or r.get("status") != "needs_review"
                    or r.get("binary_sha256") != sha
                    or int(r.get("size", -1)) != int(inv["size"])
                    or r.get("pipeline_version") != 2):
                continue
            reason = classify(r)
            output.append({
                "address": addr, "name": inv["demangled"],
                "size": int(inv["size"]), "core_priority": int(addr in priorities),
                "coverage_pct": r.get("coverage_pct", ""),
                "review_reason": reason, "tables_resolved": r.get("tables_resolved", 0),
                "tables_unresolved": r.get("tables_unresolved", 0),
                "review_attempts": r.get("review_attempts", 1),
                "checkpoint_path": (Path("FFT_Android_Mod/docs/re-results") / p.name).as_posix(),
            })
        except (OSError, ValueError, TypeError):
            continue
    output.sort(key=lambda x: (-x["core_priority"], -x["size"], x["address"]))
    return output


def render_triage(rows):
    counts = Counter(r["review_reason"] for r in rows)
    core = Counter(r["review_reason"] for r in rows if r["core_priority"])
    lines = ["# ARM semantic review triage", "",
             f"Unverified checkpoints: **{len(rows)}**; core targets: **{sum(core.values())}**.", "",
             "These are structural observations, not semantic equivalence proofs.", "",
             "| Review reason | Total | Core |",
             "|---|---:|---:|"]
    for reason in sorted(counts):
        lines.append(f"| {reason} | {counts[reason]} | {core[reason]} |")
    lines += ["", "## Highest priority evidence collection", "",
              "| Address | Function | Coverage | Reason | Next check |",
              "|---|---|---:|---|---|"]
    checks = {
      "unresolved_jump_table": "Recover bounds and every indirect target",
      "resolved_jump_table_check": "Verify guard, all cases and default path",
      "coverage_below_95": "Disassemble uncovered blocks and side effects",
      "indirect_flow_or_manual_check": "Validate outputs, memory writes and return paths",
    }
    for r in rows[:30]:
        label = str(r["name"]).replace("|", "/")
        lines.append(f'| `{r["address"]}` | {label} | {r["coverage_pct"]}% | '
                     f'{r["review_reason"]} | {checks[r["review_reason"]]} |')
    lines += ["", "Approval requires instruction-level control-flow evidence, "
              "input/output invariants, and ideally differential tests or execution traces. "
              "Do not change needs_review solely from these summaries.", ""]
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser()
    root = Path(__file__).resolve().parents[2]
    parser.add_argument("--inventory", type=Path, default=root / "docs/RE_FUNCTION_INVENTORY.csv")
    parser.add_argument("--core", type=Path, default=root / "docs/alvos_prioritarios_nucleo.csv")
    parser.add_argument("--results", type=Path, default=root / "docs/re-results")
    parser.add_argument("--binary", type=Path, default=root / "src/lib/armeabi/libgl2jni.so")
    args = parser.parse_args()
    rows = build(args.inventory, args.core, args.results, args.binary)
    dest = args.results / "REVIEW_QUEUE.csv"
    fields = ["address", "name", "size", "core_priority", "coverage_pct",
              "review_reason", "tables_resolved", "tables_unresolved",
              "review_attempts", "checkpoint_path"]
    with dest.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    (args.results / "REVIEW_TRIAGE.md").write_text(render_triage(rows), encoding="utf-8")
    print(f"Review queue: {len(rows)} rows, {sum(x['core_priority'] for x in rows)} core")


if __name__ == "__main__":
    main()
