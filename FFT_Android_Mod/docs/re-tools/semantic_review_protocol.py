#!/usr/bin/env python3
"""Two-phase human review request for scoped A32 BX LR certificates.

Stage one publishes a review-only fingerprint manifest in a dedicated PR.
An independent human reviews that PR. Stage two promotes matching partial
ledger entries in a later PR. Approval is read from GitHub, never fabricated.
"""
import argparse
import hashlib
import json
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


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--binary", type=Path, default=semantic_coverage.BINARY)
    p.add_argument("--inventory", type=Path, default=semantic_coverage.INVENTORY)
    p.add_argument("--ledger", type=Path,
                   default=semantic_coverage.RESULTS / "semantic-certificates.json")
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--limit", type=int, default=5)
    args = p.parse_args()
    request = make_request(args.binary, args.inventory, args.ledger, args.limit)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(request, indent=2, ensure_ascii=False) + "\n",
                           encoding="utf-8")
    print(f"SEMANTIC_HUMAN_REVIEW_REQUESTED={len(request['certificate_fingerprints'])}")
    print("SEMANTIC_HUMAN_REVIEW_CERTIFIED=0")


if __name__ == "__main__":
    main()
