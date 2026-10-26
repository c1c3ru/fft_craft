#!/usr/bin/env python3
"""Persist same-run semantic observations without turning them into certificates.

CI artifacts are short-lived and running the dashboard without --*-dir must
not erase already verified metrics. A snapshot is bound to the exact ELF,
certificate-ledger contents and original CI run. It never stores or promotes
certified counts; those are recalculated from the actual ledger.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path

import semantic_coverage
import central_semantic_summary

METRICS = (
    "partial_evidence_unique", "static_reports", "unicorn_reports",
    "dynamic_samples", "leaf_candidates", "checked_local_contracts",
    "contract_samples", "assigned",
)


def ledger_digest(certificates):
    raw = json.dumps(certificates, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


def make_snapshot(summary, digest, certificates, run_id, folders):
    if len(digest) != 64 or any(ch not in "0123456789abcdef" for ch in digest):
        raise ValueError("ELF SHA-256 required")
    addresses = {}
    for name, folder, pattern in (
        ("static", folders["static"], "*.json"),
        ("unicorn", folders["unicorn"], "*.json"),
        ("contracts", folders["contracts"], "*.json"),
    ):
        addresses[name] = sorted(p.stem.lower() for p in Path(folder).glob(pattern))
        if len(set(addresses[name])) != len(addresses[name]):
            raise ValueError("duplicate address in snapshot folder")
    snapshot = {
        "schema": 1,
        "elf_sha256": digest,
        "certificates_sha256": ledger_digest(certificates),
        "run_id": str(run_id),
        "inventory_addresses": summary["unique"],
        "metrics": {key: summary[key] for key in METRICS},
        "addresses": addresses,
    }
    validate(snapshot, digest, certificates, summary["unique"])
    return snapshot


def validate(snapshot, digest, certificates, inventory_addresses):
    if (not isinstance(snapshot, dict) or snapshot.get("schema") != 1
            or snapshot.get("elf_sha256") != digest
            or snapshot.get("certificates_sha256") != ledger_digest(certificates)
            or snapshot.get("inventory_addresses") != inventory_addresses
            or not str(snapshot.get("run_id", "")).strip()):
        raise ValueError("snapshot stale or not bound to current ELF/ledger")
    metrics = snapshot.get("metrics")
    addresses = snapshot.get("addresses")
    if not isinstance(metrics, dict) or set(metrics) != set(METRICS):
        raise ValueError("invalid snapshot metrics")
    if (not isinstance(addresses, dict)
            or set(addresses) != {"static", "unicorn", "contracts"}):
        raise ValueError("invalid snapshot address sets")
    for name, values in addresses.items():
        if (not isinstance(values, list) or len(set(values)) != len(values)
                or any(not isinstance(a, str) or len(a) != 8 or
                       any(ch not in "0123456789abcdef" for ch in a)
                       for a in values)):
            raise ValueError(f"invalid snapshot {name} addresses")
    if any(type(metrics[key]) is not int or metrics[key] < 0 for key in METRICS):
        raise ValueError("invalid snapshot count")
    certified_addresses = {
        address for address, record in certificates.items()
        if isinstance(record, dict) and record.get("status") == "certified"
    }
    uncertified_evidence = (
        set(addresses["static"]) | set(addresses["unicorn"])
    ) - certified_addresses
    if (metrics["static_reports"] != len(addresses["static"])
            or metrics["unicorn_reports"] != len(addresses["unicorn"])
            or metrics["checked_local_contracts"] != len(addresses["contracts"])
            or metrics["contract_samples"] != 32 * len(addresses["contracts"])
            or metrics["leaf_candidates"] > metrics["unicorn_reports"]
            or metrics["checked_local_contracts"] > metrics["leaf_candidates"]
            or metrics["partial_evidence_unique"] > inventory_addresses
            or metrics["partial_evidence_unique"] <
               len(uncertified_evidence)
            or not set(addresses["contracts"]).issubset(set(addresses["unicorn"]))):
        raise ValueError("contradictory snapshot counts")
    return metrics


def load(path, digest, certificates, unique):
    path = Path(path)
    if not path.is_file():
        return None
    snapshot = json.loads(path.read_text(encoding="utf-8"))
    validate(snapshot, digest, certificates, unique)
    return snapshot


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--binary", type=Path, default=semantic_coverage.BINARY)
    parser.add_argument("--inventory", type=Path, default=semantic_coverage.INVENTORY)
    parser.add_argument("--certificates", type=Path,
                        default=semantic_coverage.RESULTS / "semantic-certificates.json")
    parser.add_argument("--results", type=Path, default=semantic_coverage.RESULTS)
    parser.add_argument("--pilot-dir", type=Path, required=True)
    parser.add_argument("--dynamic-dir", type=Path, required=True)
    parser.add_argument("--contracts-dir", type=Path, required=True)
    parser.add_argument("--manifests-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path,
                        default=semantic_coverage.RESULTS / "SEMANTIC_RUN_SNAPSHOT.json")
    args = parser.parse_args()
    binary_digest = hashlib.sha256(args.binary.read_bytes()).hexdigest()
    certificates = (json.loads(args.certificates.read_text(encoding="utf-8"))
                    if args.certificates.is_file() else {})
    summary = central_semantic_summary.summarize(
        args.inventory, binary_digest, args.certificates,
        args.pilot_dir, args.dynamic_dir, args.manifests_dir,
        history_dir=args.results, contracts_dir=args.contracts_dir,
        binary=args.binary)
    snapshot = make_snapshot(summary, binary_digest, certificates,
                             os.environ.get("GITHUB_RUN_ID", "local"),
                             {"static": args.pilot_dir, "unicorn": args.dynamic_dir,
                              "contracts": args.contracts_dir})
    args.output.parent.mkdir(parents=True, exist_ok=True)
    temporary = args.output.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(snapshot, indent=2) + "\n", encoding="utf-8")
    temporary.replace(args.output)
    print(f"SEMANTIC_SNAPSHOT_EVIDENCE={summary['partial_evidence_unique']}")
    print(f"SEMANTIC_SNAPSHOT_RUN_ID={snapshot['run_id']}")
    print(f"SEMANTIC_SNAPSHOT_CERTIFIED_BY_THIS_STEP=0")


if __name__ == "__main__":
    main()
