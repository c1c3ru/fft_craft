#!/usr/bin/env python3
"""Two-phase human review request for scoped A32 BX LR certificates.

Stage one publishes a review-only fingerprint manifest in a dedicated PR.
An independent human reviews that PR. Stage two promotes matching partial
ledger entries in a later PR. Approval is read from GitHub, never fabricated.
"""
import argparse
import hashlib
import json
import re
from pathlib import Path

import semantic_coverage
import semantic_evidence
import semantic_bxlr_contract_pilot as bxlr

PROTOCOL = "independent_github_review_request_v1"
REVIEW_PATH = "FFT_Android_Mod/docs/re-results/SEMANTIC_BXLR_REVIEW_REQUEST.json"
# A prior request was merged without an APPROVED review. Every new review round
# adds a fresh, immutable request file; do not rewrite the already merged one.
REVIEW_RETRY_PATH = "FFT_Android_Mod/docs/re-results/SEMANTIC_BXLR_REVIEW_REQUEST_R2.json"
REVIEW_PATHS = (REVIEW_PATH, REVIEW_RETRY_PATH)
REVIEW_BASE = "FFT_Android_Mod/docs/re-results/"
REVIEW_FILENAME = re.compile(r"SEMANTIC_BXLR_REVIEW_REQUEST(?:_R[2-9][0-9]*)?\.json\Z")


def is_review_request_path(path):
    """Accept only enumerated versioned immutable review requests."""
    return (isinstance(path, str) and path.startswith(REVIEW_BASE)
            and REVIEW_FILENAME.fullmatch(path[len(REVIEW_BASE):]) is not None)


def reviewed_request_paths(folder):
    folder = Path(folder)
    return sorted(p for p in folder.glob("SEMANTIC_BXLR_REVIEW_REQUEST*.json")
                  if is_review_request_path(REVIEW_BASE + p.name))


FIELDS = (
    "binary_sha256", "size", "proof_class", "scope",
    "instruction_encoding", "instruction_sha256", "contract",
    "preconditions", "postconditions", "control_flow", "memory_effects",
    "test_evidence",
)


def fingerprint(address, record):
    """Canonical binding to the exact address, original instruction and scope."""
    if not isinstance(record, dict) or not isinstance(address, str):
        raise ValueError("invalid semantic contract")
    if len(address) != 8 or any(c not in "0123456789abcdef" for c in address):
        raise ValueError("address must be eight lowercase hex digits")
    if any(field not in record for field in FIELDS):
        raise ValueError("missing field in contract fingerprint")
    content = {"address": address, **{name: record[name] for name in FIELDS}}
    raw = json.dumps(content, sort_keys=True, ensure_ascii=True,
                     separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def make_request(binary, inventory, ledger_path, limit=5):
    if type(limit) is not int or not 1 <= limit <= 20:
        raise ValueError("review request limit must be between 1 and 20")
    binary = Path(binary)
    digest = hashlib.sha256(binary.read_bytes()).hexdigest()
    records = json.loads(Path(ledger_path).read_text(encoding="utf-8"))
    rows = semantic_coverage.ledger(Path(inventory), digest, records)
    addresses = {r["address"]: r for r in rows}
    import semantic_certificate_gate as gate
    selected = []
    for address in sorted(records):
        record = records[address]
        if record["status"] != "partial" or record.get("proof_class") != gate.SCOPE:
            continue
        if (address not in addresses or addresses[address]["size"] != 4
                or record.get("scope") != "normal_a32_valid_abi_return"
                or record.get("reviewer") is not None
                or record.get("instruction_encoding") != "1eff2fe1"
                or record.get("machine_samples_passed") != 32
                or record.get("preconditions") != list(gate.PRECONDITIONS)
                or record.get("postconditions") != list(gate.POSTCONDITIONS)
                or record.get("control_flow") != list(gate.CONTROL_FLOW)
                or record.get("memory_effects") != list(gate.MEMORY_EFFECTS)
                or record.get("test_evidence") != list(gate.REQUIRED_EVIDENCE)):
            raise ValueError(f"review candidate lacks exact local proof: {address}")
        code = semantic_evidence.read_function(binary, int(address, 16), 4)
        if (code.hex() != "1eff2fe1"
                or hashlib.sha256(code).hexdigest() !=
                   record.get("instruction_sha256")
                or record.get("contract") != bxlr.isa_contract(code)):
            raise ValueError(f"original ELF mismatch for {address}")
        # Fresh live execution, not just a passing count copied into a JSON.
        if bxlr.verify_interworking(int(address, 16), code) != 32:
            raise ValueError(f"failed independent original-ELF differential proof: {address}")
        selected.append((address, record))
    if len(selected) < limit:
        raise ValueError("not enough verified partial contracts to request review")
    selected = selected[:limit]
    return {
        "schema": 1, "review_protocol": PROTOCOL,
        "elf_sha256": digest,
        "status": "human_review_requested",
        "certified": False,
        "certificate_fingerprints": {
            address: fingerprint(address, record) for address, record in selected
        },
        "instructions_to_reviewer": (
            "Review exact original ELF, ARM/Thumb return normal-state scope, "
            "exceptions excluded, address and each contract fingerprint. "
            "Approve this PR only if all requested contracts are independently accepted."
        ),
    }



def verify_request(binary, inventory, ledger_path, request_path):
    """Revalidate a historical review request before AND after certification.

    An approved request stays immutable while corresponding ledger statuses
    transition from partial to certified. Its fingerprint binds the original
    contract (but deliberately excludes the mutable approval metadata).
    """
    import semantic_certificate_gate as gate
    binary, inventory, ledger_path, request_path = map(
        Path, (binary, inventory, ledger_path, request_path))
    digest = hashlib.sha256(binary.read_bytes()).hexdigest()
    request = json.loads(request_path.read_text(encoding="utf-8"))
    expected_keys = {
        "schema", "review_protocol", "elf_sha256", "status",
        "certified", "certificate_fingerprints", "instructions_to_reviewer",
    }
    if (not isinstance(request, dict) or set(request) != expected_keys
            or request["schema"] != 1 or request["review_protocol"] != PROTOCOL
            or request["elf_sha256"] != digest
            or request["status"] != "human_review_requested"
            or request["certified"] is not False
            or not isinstance(request["instructions_to_reviewer"], str)
            or not request["instructions_to_reviewer"].strip()):
        raise ValueError("invalid original ELF review request")
    fingerprints = request["certificate_fingerprints"]
    if (not isinstance(fingerprints, dict)
            or not 1 <= len(fingerprints) <= 20):
        raise ValueError("invalid reviewed address set")
    records = json.loads(ledger_path.read_text(encoding="utf-8"))
    rows = semantic_coverage.ledger(inventory, digest, records)
    mapped = {r["address"]: r for r in rows}
    for address, approved_hash in sorted(fingerprints.items()):
        record = records.get(address)
        if (not isinstance(record, dict) or address not in mapped
                or mapped[address]["size"] != 4
                or record.get("status") not in ("partial", "certified")
                or record.get("proof_class") != gate.SCOPE
                or record.get("scope") != "normal_a32_valid_abi_return"
                or record.get("size") != 4
                or record.get("binary_sha256") != digest
                or record.get("instruction_encoding") != "1eff2fe1"
                or record.get("preconditions") != list(gate.PRECONDITIONS)
                or record.get("postconditions") != list(gate.POSTCONDITIONS)
                or record.get("control_flow") != list(gate.CONTROL_FLOW)
                or record.get("memory_effects") != list(gate.MEMORY_EFFECTS)
                or record.get("test_evidence") != list(gate.REQUIRED_EVIDENCE)):
            raise ValueError(f"review proof mismatch at {address}")
        code = semantic_evidence.read_function(binary, int(address, 16), 4)
        if (code.hex() != "1eff2fe1"
                or record.get("instruction_sha256") !=
                   hashlib.sha256(code).hexdigest()
                or record.get("contract") != bxlr.isa_contract(code)
                or fingerprint(address, record) != approved_hash):
            raise ValueError(f"reviewed fingerprint or original ELF mismatch at {address}")
        if bxlr.verify_interworking(int(address, 16), code) != 32:
            raise ValueError(f"reviewed differential execution failed at {address}")
    print(f"SEMANTIC_REVIEW_REQUEST_REVERIFIED={len(fingerprints)}")
    print("SEMANTIC_REVIEW_REQUEST_NEW_CERTIFICATIONS=0")
    return len(fingerprints)

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--binary", type=Path, default=semantic_coverage.BINARY)
    p.add_argument("--inventory", type=Path, default=semantic_coverage.INVENTORY)
    p.add_argument("--ledger", type=Path,
                   default=semantic_coverage.RESULTS / "semantic-certificates.json")
    p.add_argument("--output", type=Path)
    p.add_argument("--verify-request", type=Path)
    p.add_argument("--verify-all", action="store_true")
    p.add_argument("--limit", type=int, default=5)
    args = p.parse_args()
    if args.verify_all:
        if args.output is not None or args.verify_request is not None:
            p.error("--verify-all conflicts with --output/--verify-request")
        paths = reviewed_request_paths(semantic_coverage.RESULTS)
        if not paths:
            p.error("no immutable review requests found")
        for request_path in paths:
            verify_request(args.binary, args.inventory, args.ledger, request_path)
        print(f"SEMANTIC_REVIEW_REQUEST_FILES_REVERIFIED={len(paths)}")
        return
    if args.verify_request is not None:
        if args.output is not None:
            p.error("--verify-request cannot be used with --output")
        verify_request(args.binary, args.inventory, args.ledger, args.verify_request)
        return
    if args.output is None:
        p.error("--output is required when creating a new review request")
    request = make_request(args.binary, args.inventory, args.ledger, args.limit)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(request, indent=2, ensure_ascii=False) + "\n",
                           encoding="utf-8")
    print(f"SEMANTIC_HUMAN_REVIEW_REQUESTED={len(request['certificate_fingerprints'])}")
    print("SEMANTIC_HUMAN_REVIEW_CERTIFIED=0")


if __name__ == "__main__":
    main()
