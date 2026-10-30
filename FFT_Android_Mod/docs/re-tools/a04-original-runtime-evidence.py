#!/usr/bin/env python3
"""Fail-closed structural validation for A04 *observational* runtime evidence.

A valid report does NOT attest its own provenance, certify semantic equivalence,
prove global path bounds, or authorize running the original unbounded strcpy.
No user-provided path contents or arbitrary input values are printed.
"""
import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

from jsonschema import Draft202012Validator

EXPECTED_ELF_SHA256 = "bf913415ab9458a83b14ac8c8a0fa3430d1f5d18bfbcd7c7472d6f5e8b4850bc"
SCHEMA_FILE = Path(__file__).with_name("a04-original-runtime-evidence.schema.json")
MAX_FILE_BYTES = 256 * 1024
MAX_EVENTS = 256
BOUND = 242


class EvidenceError(ValueError):
    """Rejected evidence; error messages must never contain path contents."""


def _unique_keys(pairs):
    obj = {}
    for key, value in pairs:
        if key in obj:
            raise EvidenceError("Duplicate JSON object key")
        obj[key] = value
    return obj


def _reject_constant(_value):
    raise EvidenceError("Non-finite JSON number")


def load_json(path):
    if path.stat().st_size > MAX_FILE_BYTES:
        raise EvidenceError("Input exceeds maximum evidence size")
    try:
        return json.loads(
            path.read_text(encoding="utf-8"),
            object_pairs_hook=_unique_keys,
            parse_constant=_reject_constant,
        )
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise EvidenceError("Malformed evidence JSON") from None


def validate_evidence(document, schema, expected_elf=EXPECTED_ELF_SHA256):
    # Format/shape validation uses the checked-in JSON Schema; cross-field
    # invariants below supplement JSON Schema without trusting the producer.
    if not re.fullmatch(r"[a-f0-9]{64}", expected_elf):
        raise EvidenceError("Invalid expected ELF digest")
    Draft202012Validator.check_schema(schema)
    if not Draft202012Validator(schema).is_valid(document):
        raise EvidenceError("Evidence JSON violates A04 schema")
    if document["elf_sha256"] != expected_elf:
        raise EvidenceError("Evidence ELF digest differs from pinned inventory")
    events = document["events"]
    if not events or len(events) > MAX_EVENTS:
        raise EvidenceError("Evidence event count is invalid")
    seen = set()
    outcomes = Counter()
    exceeds = 0
    correlated = 0
    verified_nul = 0
    for event in events:
        event_id = event["event_id"]
        if event_id in seen:
            raise EvidenceError("Repeated event identifier")
        seen.add(event_id)
        outcome = event["outcome"]
        outcomes[outcome] += 1
        is_correlated = event["jni_to_r1_correlated"]
        is_pre_copy = event["pre_copy_observed"]
        nul = event["r1_nul_termination"]
        if outcome == "present":
            byte_length = event["jni_byte_length"]
            within = event["within_242_bytes"]
            if within is not (byte_length <= BOUND):
                raise EvidenceError("Length and 242-byte budget flag disagree")
            if is_correlated and not is_pre_copy:
                raise EvidenceError("R1 correlation requires pre-copy observation")
            if nul == "not_applicable":
                if is_pre_copy or is_correlated:
                    raise EvidenceError("Observed R1 requires NUL disposition")
            elif nul == "verified_bounded":
                if not (is_pre_copy and is_correlated):
                    raise EvidenceError("NUL verification requires correlated pre-copy R1")
                verified_nul += 1
            if not within:
                exceeds += 1
            if is_correlated:
                correlated += 1
        else:
            if (event["jni_byte_length"] is not None
                    or event["within_242_bytes"] is not None
                    or is_correlated or is_pre_copy
                    or nul != "not_applicable"):
                raise EvidenceError("Absent or unresolved path cannot claim R1 evidence")
    return {
        "result": "format_validated_only",
        "schema_version": 1,
        "android_api": document["android_api"],
        "total_events": len(events),
        "outcomes": dict(sorted(outcomes.items())),
        "jni_r1_correlated_events": correlated,
        "bounded_nul_verified_events": verified_nul,
        "observed_length_exceedances": exceeds,
        "global_maximum_proven": False,
        "original_elf_semantic_equivalence_certified": False,
        "original_game_provenance_independently_attested": False,
        "semantic_certificates_issued": 0,
        "path_contents_retained": False,
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("evidence", type=Path)
    parser.add_argument("--expected-elf", default=EXPECTED_ELF_SHA256,
                        help="ELF SHA-256 from independent inventory")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)
    try:
        schema = load_json(SCHEMA_FILE)
        evidence = load_json(args.evidence)
        result = validate_evidence(evidence, schema, args.expected_elf)
    except (EvidenceError, OSError, ValueError) as exc:
        # Suppress parser exceptions and any untrusted JSON values.
        print("A04_EVIDENCE_REJECTED: " + (
            str(exc) if isinstance(exc, EvidenceError)
            else "Unable to validate evidence"), file=sys.stderr)
        return 2
    output = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(output, encoding="utf-8")
    else:
        print(output, end="")
    return 0


if __name__ == "__main__":
    sys.exit(main())
