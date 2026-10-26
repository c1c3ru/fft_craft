#!/usr/bin/env python3
"""Export reproducible bounded Unicorn observations for two audited ARM getters.

Runs the EXISTING original-ELF machine tests before writing any evidence.
This is not a complete-function semantic-equivalence certification.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import semantic_evidence
import semantic_getparam_getscale_exec as suite
import semantic_three_callees_exec as callees

CASES = (
    ("GetParam", suite.GET_PARAM, 64, "GetParam microexecutions: 64/64 PASS"),
    ("GetScale", suite.GET_SCALE, 32, "GetScale microexecutions: 32/32 PASS"),
)
TOTAL_MARKER = "Combined GetParam/GetScale microexecutions: 96/96 PASS"


def verified_records(report: str, digest: str) -> list[dict]:
    """Fail closed if the executed suite's expected summary changes."""
    if f"ELF SHA-256: `{digest}`" not in report:
        raise ValueError("Machine-test report not bound to the current ELF")
    if TOTAL_MARKER not in report:
        raise ValueError("Required 96 original-ELF microexecutions not reported")
    results = []
    for name, address, tests, marker in CASES:
        if marker not in report:
            raise ValueError(f"Missing successful {name} execution count")
        results.append({
            "address": f"{address:08x}",
            "name": name,
            "binary_sha256": digest,
            "semantic_status": "partial",
            "evidence_class": "unicorn_bounded_machine_execution",
            "machine_samples_passed": tests,
            "machine_samples_failed": 0,
            "invocation_modes": ["standalone_synthetic_lr", "original_caller_bl"],
            "verified_local_effects": (
                ["indexed_read", "return_register", "neighboring_canaries"]
                if name == "GetParam" else
                ["conditional_load_store", "NZCV", "neighboring_canaries"]
            ),
            "unverified": [
                "complete_input_domain", "full_caller_continuation",
                "aliasing_and_environment", "whole_program_semantic_equivalence",
            ],
            "certified": False,
        })
    return results


CALLEE_MARKER = "**Three-callee and caller tests: 72/72 PASS.**"
CALLEE_ROUTES = (
    ("iOS_setV2Icon", callees.SETTER, ["setter"]),
    ("iOS_clearOkNg", callees.CLEAR, ["clear"]),
    ("sound_request", callees.SOUND, ["sound"]),
    ("houkoku_okng", 0x25A228, ["caller_setter", "caller_clear_sound"]),
)


def verified_callee_records(report: str, digest: str) -> list[dict]:
    if f"ELF SHA-256: `{digest}`" not in report:
        raise ValueError("Callee execution report not bound to current ELF")
    if CALLEE_MARKER not in report:
        raise ValueError("Required 72 callee/caller microexecutions not reported")
    return [{
        "address": f"{address:08x}", "name": name,
        "binary_sha256": digest, "semantic_status": "partial",
        "evidence_class": "unicorn_bounded_machine_execution",
        "suite_samples_passed": 72,
        "suite_sample_count_scope": "shared across 5 routes; do not sum per address",
        "routes_exercised": routes,
        "verified_local_effects": [
            "arm_pc_traces", "memory_hooks", "canary_boundaries",
            "registers_and_return_boundary"
        ],
        "unverified": [
            "complete_function_body", "all_input_domains",
            "unresolved_external_branch_targets", "full_caller_continuations",
            "whole_program_semantic_equivalence"
        ],
        "certified": False,
    } for name, address, routes in CALLEE_ROUTES]


def run(binary: Path, output: Path):
    digest = hashlib.sha256(binary.read_bytes()).hexdigest()
    # Existing suite asserts each trace, memory effect and return value, and
    # raises on any failing test before a report is returned.
    report = suite.run(binary)
    records = verified_records(report, digest)
    callee_report = callees.run(binary, semantic_evidence.ROOT / "docs/RE_FUNCTION_INVENTORY.csv")
    records.extend(verified_callee_records(callee_report, digest))
    output.mkdir(parents=True, exist_ok=True)
    for record in records:
        destination = output / f"{record['address']}.json"
        destination.write_text(
            json.dumps(record, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
    (output / "GETTER_MACHINE_EXECUTIONS.md").write_text(report, encoding="utf-8")
    (output / "CALLEE_MACHINE_EXECUTIONS.md").write_text(callee_report, encoding="utf-8")
    print("DYNAMIC_SAMPLES_PASSED=168")
    print(f"DYNAMIC_PARTIAL_FUNCTIONS={len(records)}")
    print("DYNAMIC_CERTIFIED_FUNCTIONS=0")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--binary", type=Path,
                        default=semantic_evidence.ROOT / "src/lib/armeabi/libgl2jni.so")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    run(args.binary, args.output)


if __name__ == "__main__":
    main()
