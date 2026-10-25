#!/usr/bin/env python3
"""Parallel, resumable structural-analysis loop for the ARM FFT library.

Workers never edit shared files. The coordinator alone writes JSON and reports.
Similarity is a triage decision, not proof of semantic equivalence.
"""
from __future__ import annotations

import argparse
import concurrent.futures as cf
import csv
import hashlib
import json
import re
import subprocess
import sys
import shutil
from pathlib import Path

import structural_v3

ROOT = Path(__file__).resolve().parents[2]
TOOLS = Path(__file__).resolve().parent
DEFAULT_SO = ROOT / "src/lib/armeabi/libgl2jni.so"
DEFAULT_CSV = ROOT / "docs/RE_FUNCTION_INVENTORY.csv"
DEFAULT_PRIORITY_CSV = ROOT / "docs/alvos_prioritarios_nucleo.csv"
CONFIRMED = {"read_structural", "read_full", "confirmed_by_similarity"}
RETRYABLE = {"error", "needs_review"}
PIPELINE_VERSION = 2  # Checkpoint JSON schema; structural analyzer uses its own version.
FAMILY_PATTERNS = (
    ("Mdl", re.compile(r"^Mdl\d+")),
    ("personalwindow", re.compile(r"^(?:[WACDE])?disp_personalwindow")),
)
COVERAGE = re.compile(r"coverage:\s*(\d+) of ~?(\d+) instruction slots \((\d+)%\)")
UNRESOLVED = re.compile(r"\[WARN\] jump table")
BL = re.compile(r"^\s*0x([0-9a-f]+) x\d+\s+", re.M)
TABLES = re.compile(r"-- jump tables resolved: (\d+) --")


def family(name: str) -> str | None:
    for label, pattern in FAMILY_PATTERNS:
        if pattern.search(name):
            return label
    return None


def addr(value: str) -> int:
    return int(value, 16)


def load_inventory(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    for row in rows:
        row["size"] = int(row["size"])
    return sorted(rows, key=lambda row: -row["size"])


def prioritize(rows: list[dict], priority_csv: Path | None) -> list[dict]:
    """Core addresses first, then remaining inventory by descending byte size.

    The canonical inventory owns status and size; the priority file only
    supplies a rank. Missing or already reviewed addresses are harmless.
    """
    if priority_csv is None:
        return rows
    with priority_csv.open(newline="", encoding="utf-8") as handle:
        priority_addresses = {row["address"].strip().lower()
                              for row in csv.DictReader(handle)}
    core = [row for row in rows if row["address"].lower() in priority_addresses]
    other = [row for row in rows if row["address"].lower() not in priority_addresses]
    return core + other


def signature(row: dict) -> str:
    return f"{row['address']}:{row['size']}"


def run_script(script: str, so: Path, row: dict, timeout: int) -> str:
    cmd = [sys.executable, str(TOOLS / script), str(so),
           row["address"], f"+{row['size']}"]
    proc = subprocess.run(cmd, text=True, capture_output=True, timeout=timeout,
                          check=False)
    if proc.returncode:
        raise RuntimeError(f"{script} exited {proc.returncode}: {proc.stderr[-600:]}")
    return proc.stdout


def analyze_one(row: dict, so: Path, timeout: int, references: dict,
                min_targets: int, threshold: float, enable_v3: bool = False) -> dict:
    result = {"address": row["address"], "name": row["demangled"],
              "size": row["size"], "previous_status": row["status"]}
    label = family(row["demangled"])
    reference = references.get(label) if label else None
    if reference and reference["address"] != row["address"]:
        try:
            cmd = [sys.executable, str(TOOLS / "family_sim.py"), str(so),
                   reference["address"], f"+{reference['size']}",
                   f"candidate:{row['address']}:+{row['size']}"]
            proc = subprocess.run(cmd, text=True, capture_output=True,
                                  timeout=timeout, check=False)
            if proc.returncode:
                raise RuntimeError(proc.stderr[-600:])
            match = re.search(
                r"candidate .*?\((\d+)%\), (\d+) bl targets, "
                r"jaccard=([\d.]+), jt_unresolved=(\d+)", proc.stdout)
            refmatch = re.search(r"reference .*?\((\d+)%\), (\d+) distinct "
                                 r"bl targets, (\d+) unresolved", proc.stdout)
            if match and refmatch:
                cov, count, similarity, jumps = match.groups()
                result["similarity"] = float(similarity)
                result["reference_address"] = reference["address"]
                # Guard against empty/tiny catalogs and weak reference analysis.
                if (float(similarity) >= threshold and int(jumps) == 0
                        and int(count) >= min_targets
                        and int(refmatch.group(2)) >= min_targets
                        and int(refmatch.group(3)) == 0
                        and int(refmatch.group(1)) >= 95
                        and int(cov) >= 95):
                    result.update(status="confirmed_by_similarity",
                                  coverage_pct=int(cov), distinct_bl=int(count),
                                  tables_resolved=0, tables_unresolved=0)
                    return result
            else:
                result["similarity_warning"] = "Unrecognized similarity output"
        except (OSError, subprocess.TimeoutExpired, RuntimeError) as error:
            result["similarity_warning"] = str(error)
    output = run_script("jtable.py", so, row, timeout)
    cov = COVERAGE.search(output)
    tables = TABLES.search(output)
    unresolved = len(UNRESOLVED.findall(output))
    targets_section = output.split("-- bl targets:", 1)[-1].split("-- branches:", 1)[0]
    targets = set(BL.findall(targets_section))
    if not cov or not tables:
        raise ValueError("Could not parse jtable.py output; leave for manual review")
    coverage_pct = 100 * int(cov.group(1)) / max(1, int(cov.group(2)))
    resolved = int(tables.group(1))
    status = ("auto_structural" if coverage_pct >= 95 and unresolved == 0
              and resolved == 0 else "needs_review")
    result.update(status=status, coverage_pct=round(coverage_pct, 2),
                  distinct_bl=len(targets), tables_resolved=resolved,
                  tables_unresolved=unresolved,
                  bl_targets=sorted(targets), log=output)
    if enable_v3:
        # V3 does not trust jtable's raw 95% score or blanket reject all
        # resolved tables. A separate byte-level check must pass first.
        diagnostic = structural_v3.inspect_binary(
            so, int(row["address"], 16), row["size"])
        result["v2_structural_status"] = status
        result["status"] = diagnostic["status"]
        result["structural_v3"] = diagnostic
        result["structural_version"] = structural_v3.VERSION
        result["structural_fingerprint"] = structural_v3.fingerprint()
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--so", type=Path, default=DEFAULT_SO)
    parser.add_argument("--inventory", type=Path, default=DEFAULT_CSV)
    parser.add_argument("--priority-csv", type=Path, default=DEFAULT_PRIORITY_CSV,
                        help="Prioritize core targets; use --no-priority to disable")
    parser.add_argument("--no-priority", action="store_true")
    parser.add_argument("--output", type=Path, default=ROOT / "docs/re-results")
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--limit", type=int, default=25)
    parser.add_argument("--timeout", type=int, default=180)
    parser.add_argument("--similarity", type=float, default=0.90)
    parser.add_argument("--min-bl", type=int, default=5)
    parser.add_argument("--include-reviewed", action="store_true")
    parser.add_argument("--review-only", action="store_true",
                        help="Process only existing needs_review checkpoints; requires --retry-review")
    parser.add_argument("--max-review-attempts", type=int, default=2,
                        help="Maximum total review passes per unchanged binary (default 2)")
    parser.add_argument("--retry-review", action="store_true",
                        help="Reprocess results flagged for manual review")
    parser.add_argument("--upgrade-v3", action="store_true",
                        help="Only upgrade stale needs_review checkpoints to structural v3")
    args = parser.parse_args()
    if not (1 <= args.workers <= 16 and args.limit >= 1 and
            0 < args.similarity <= 1 and args.min_bl >= 1):
        parser.error("invalid worker/limit/similarity/min-bl setting")
    if args.review_only and not args.retry_review:
        parser.error("--review-only requires --retry-review")
    if args.upgrade_v3 and not (args.review_only and args.retry_review):
        parser.error("--upgrade-v3 requires --review-only --retry-review")
    if args.max_review_attempts < 1:
        parser.error("--max-review-attempts must be positive")
    if args.timeout < 1:
        parser.error("timeout must be positive")
    if not args.so.is_file():
        parser.error(f"library missing: {args.so}")
    rows = prioritize(load_inventory(args.inventory),
                      None if args.no_priority else args.priority_csv)
    references = {}
    for row in sorted(rows, key=lambda item: -item["size"]):
        label = family(row["demangled"])
        if label and row["status"] in {"read_structural", "read_full"}:
            references.setdefault(label, row)
    args.output.mkdir(parents=True, exist_ok=True)
    binary_hash = hashlib.sha256(args.so.read_bytes()).hexdigest()
    queue = []
    review_attempts = {}
    current_fingerprint = structural_v3.fingerprint()
    for row in rows:
        if not args.include_reviewed and row["status"] in CONFIRMED:
            continue
        destination = args.output / (row["address"] + ".json")
        if args.review_only:
            try:
                prior = json.loads(destination.read_text(encoding="utf-8"))
                if not (prior.get("status") == "needs_review"
                        and prior.get("binary_sha256") == binary_hash
                        and prior.get("pipeline_version") == PIPELINE_VERSION
                        and prior.get("size") == row["size"]):
                    continue
            except (OSError, ValueError):
                continue
        if destination.exists():
            try:
                previous = json.loads(destination.read_text(encoding="utf-8"))
                if args.upgrade_v3:
                    # Reanalyze only when the binary/size is unchanged,
                    # structural rules differ, and review is still pending.
                    if not (previous.get("status") == "needs_review"
                            and previous.get("binary_sha256") == binary_hash
                            and previous.get("size") == row["size"]
                            and previous.get("pipeline_version") == PIPELINE_VERSION
                            and (previous.get("structural_version") != structural_v3.VERSION
                                 or previous.get("structural_fingerprint") != current_fingerprint)):
                        continue
                    queue.append(row)
                    if len(queue) >= args.limit:
                        break
                    continue
                if (args.retry_review and previous.get("status") == "needs_review"
                        and previous.get("binary_sha256") == binary_hash
                        and previous.get("pipeline_version") == PIPELINE_VERSION):
                    attempts = max(1, int(previous.get("review_attempts", 1)))
                    if attempts >= args.max_review_attempts:
                        continue
                    review_attempts[row["address"]] = attempts
                if (previous.get("binary_sha256") == binary_hash
                        and previous.get("size") == row["size"]
                        and previous.get("pipeline_version") == PIPELINE_VERSION
                        and previous.get("status") != "error"
                        and not (args.retry_review and previous.get("status") == "needs_review")):
                    continue
            except (ValueError, OSError):
                pass
        queue.append(row)
        if len(queue) >= args.limit:
            break
    completed = []
    with cf.ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = {executor.submit(analyze_one, row, args.so, args.timeout,
                                   {} if args.upgrade_v3 else references,
                                   args.min_bl, args.similarity, True): row
                   for row in queue}
        for future in cf.as_completed(futures):
            row = futures[future]
            try:
                result = future.result()
            except Exception as error:
                result = {"address": row["address"], "size": row["size"],
                          "name": row["demangled"], "status": "error",
                          "error": str(error)}
            if row["address"] in review_attempts:
                result["review_attempts"] = review_attempts[row["address"]] + 1
            elif result.get("status") == "needs_review":
                result["review_attempts"] = 1
            result["binary_sha256"] = binary_hash
            result["pipeline_version"] = PIPELINE_VERSION
            completed.append(result)
            target = args.output / (row["address"] + ".json")
            if args.upgrade_v3 and target.is_file():
                original = json.loads(target.read_text(encoding="utf-8"))
                if original.get("structural_version") != structural_v3.VERSION:
                    archive = args.output / "structural-v2" / target.name
                    archive.parent.mkdir(parents=True, exist_ok=True)
                    if not archive.exists():
                        shutil.copyfile(target, archive)
                    result["archived_previous_checkpoint"] = (
                        "FFT_Android_Mod/docs/re-results/structural-v2/" + target.name)
            temp = target.with_suffix(".json.tmp")
            temp.write_text(json.dumps(result, ensure_ascii=False, indent=2),
                            encoding="utf-8")
            temp.replace(target)
            print(f"{row['address']} {result['status']} ({row['size']} B)", flush=True)
    recorded = []
    for path in args.output.glob("*.json"):
        try:
            record = json.loads(path.read_text(encoding="utf-8"))
            if (record.get("binary_sha256") == binary_hash
                    and record.get("pipeline_version") == PIPELINE_VERSION):
                recorded.append(record)
        except (ValueError, OSError):
            continue
    recorded.sort(key=lambda r: (-r["size"], r["address"]))
    total_bytes = sum(row["size"] for row in rows)
    accepted = {"auto_structural", "confirmed_by_similarity"}
    validated_bytes = sum(r["size"] for r in recorded if r["status"] in accepted)
    lines = ["# Parallel reverse-engineering loop", "",
             f"Binary SHA-256: `{binary_hash}`", "",
             f"Analyzed in current binary: {len(recorded)}",
             f"Automatically triaged: {validated_bytes:,} bytes / "
             f"{total_bytes:,} inventory bytes "
             f"({validated_bytes / max(total_bytes, 1):.2%}); "
             "**this is newly triaged coverage, not total project coverage**.", "",
             "| Address | Function | Size (B) | Coverage | Status |",
             "|---|---|---:|---:|---|"]
    for item in recorded:
        name = item["name"].replace("|", "\|")
        lines.append(f"| `{item['address']}` | {name} | {item['size']} | "
                     f"{item.get('coverage_pct', '—')}% | {item['status']} |")
    summary = args.output / "SUMMARY.md"
    summary_tmp = summary.with_suffix(".md.tmp")
    summary_tmp.write_text("\n".join(lines) + "\n", encoding="utf-8")
    summary_tmp.replace(summary)
    if args.upgrade_v3:
        print(f"V3_UPGRADED={len(completed)}", flush=True)
    return 1 if any(item["status"] == "error" for item in completed) else 0


if __name__ == "__main__":
    raise SystemExit(main())
