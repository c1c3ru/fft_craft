#!/usr/bin/env python3
"""Verify real-ELF smoke evidence against known stable ARM functions."""
import argparse
import json
from pathlib import Path

# Observed from the successful GitHub Actions ARM smoke run (PR #6).
BASELINE = {
    "002cdb20": {"min_coverage": 99.0, "tables": 0, "status": "auto_structural"},
    "000736ac": {"min_coverage": 98.0, "tables": 0, "status": "auto_structural"},
    "002cd594": {"min_coverage": 95.0, "tables": 1, "status": "needs_review"},
}


def verify(folder: Path) -> list[str]:
    failures = []
    for address, expected in BASELINE.items():
        path = folder / f"{address}.json"
        if not path.is_file():
            failures.append(f"{address}: missing smoke artifact")
            continue
        try:
            record = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError) as exc:
            failures.append(f"{address}: invalid result ({exc})")
            continue
        # The old baseline contains a table-review case. A v3 result may
        # advance it only if its table and every non-literal slot are verified.
        upgraded = record.get("structural_v3", {})
        safe_v3_acceptance = (
            expected["status"] == "needs_review"
            and record.get("status") == "auto_structural"
            and record.get("structural_version") == 3
            and upgraded.get("status") == "auto_structural"
            and upgraded.get("reason") == "all_slots_accounted"
            and upgraded.get("tables_safe") is True
            and upgraded.get("unexplained_count") == 0)
        for key, value in (("status", expected["status"]),
                           ("tables_resolved", expected["tables"])):
            if record.get(key) != value and not (key == "status" and safe_v3_acceptance):
                failures.append(f"{address}: {key}={record.get(key)!r}, expected {value!r}")
        if float(record.get("coverage_pct", 0)) < expected["min_coverage"]:
            failures.append(f"{address}: coverage below {expected['min_coverage']}%")
        if not record.get("binary_sha256") or record.get("pipeline_version") is None:
            failures.append(f"{address}: provenance missing")
    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("folder", type=Path)
    args = parser.parse_args()
    failures = verify(args.folder)
    if failures:
        for item in failures:
            print("FAIL:", item)
        return 1
    print("PASS: 3 ARM golden smoke checks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
