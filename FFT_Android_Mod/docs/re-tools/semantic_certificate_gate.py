#!/usr/bin/env python3
"""Fail-closed validation gate for *approved*, scoped semantic certificates.

This gate never produces approvals, nor converts a machine-test PASS to a
human-reviewed certificate. Initial supported contract class: exact original
A32 BX LR one-instruction function, under normal valid-return preconditions.
For every approved record, CI checks ELF bytes and reruns differential
Unicorn against an independent normal-instruction-state model.
"""
import argparse
import datetime
import hashlib
import os
import subprocess
import json
import re
from pathlib import Path

import semantic_coverage
import semantic_evidence
import semantic_bxlr_contract_pilot as bxlr

SCOPE = "original_a32_bxlr_normal_return_v1"
PR_RE = re.compile(r"^https://github\.com/c1c3ru/fft_craft/pull/[1-9][0-9]*$")
PRECONDITIONS = (
    "ARM state at entry", "executable mapped 4-byte instruction",
    "valid mapped LR destination", "normal execution context",
)
POSTCONDITIONS = (
    "PC=LR & ~1", "CPSR.T=LR & 1",
    "other CPSR bits preserved", "R0-R14 preserved",
)
MEMORY_EFFECTS = ("none in the decoded function body",)
CONTROL_FLOW = ("only unconditional BX LR; no internal callees",)
REQUIRED_EVIDENCE = (
    "original ELF instruction", "Capstone exact opcode",
    "independent pure A32 BX LR transition model",
    "Unicorn PC/CPSR/general-register/memory differential",
)

REVIEW_REQUIRED = (
    "type", "name", "github_login", "decision", "approval_pr",
    "approved_at", "notes",
)


def verify_one(record, row, binary, digest, reader=None, executor=None):
    if record.get("status") != "certified":
        raise ValueError("gate only validates explicitly certified records")
    if (record.get("proof_class") != SCOPE
            or row["size"] != 4
            or record.get("size") != 4
            or record.get("binary_sha256") != digest
            or record.get("scope") != "normal_a32_valid_abi_return"
            or record.get("instruction_encoding") != "1eff2fe1"):
        raise ValueError("unsupported semantic proof class or invalid ELF binding")
    review = record.get("reviewer")
    if not isinstance(review, dict) or any(
            not isinstance(review.get(k), str) or not review[k].strip()
            for k in REVIEW_REQUIRED):
        raise ValueError("independent reviewer metadata is missing")
    if (review["type"] != "human" or review["decision"] != "approved"
            or not PR_RE.fullmatch(review["approval_pr"])
            or review["github_login"].strip().lower().endswith("[bot]")
            or review["github_login"].strip().lower() in
            {"bot", "ci", "automated", "pending", "unknown"}):
        raise ValueError("not an explicit recorded human review")
    if (record.get("preconditions") != list(PRECONDITIONS)
            or record.get("postconditions") != list(POSTCONDITIONS)
            or record.get("memory_effects") != list(MEMORY_EFFECTS)
            or record.get("control_flow") != list(CONTROL_FLOW)
            or record.get("test_evidence") != list(REQUIRED_EVIDENCE)):
        raise ValueError("approved BX LR proof must match full scoped contract")
    reader = reader or semantic_evidence.read_function
    executor = executor or bxlr.verify_interworking
    address = int(row["address"], 16)
    original = reader(binary, address, 4)
    if original.hex() != "1eff2fe1":
        raise ValueError("ELF no longer contains a full A32 BX LR body")
    if record.get("instruction_sha256") != hashlib.sha256(original).hexdigest():
        raise ValueError("instruction digest does not match original ELF")
    if record["contract"] != bxlr.isa_contract(original):
        raise ValueError("contract specification differs from actual instruction")
    # Machine observations are deliberately checked live, never trusted from
    # an arbitrary JSON count or old artifact alone.
    count = executor(address, original)
    if count != 32:
        raise ValueError("insufficient independent ARM/Thumb differential tests")
    return True



def github_json(path):
    """Fetch authenticated GitHub PR evidence; reject unavailable API."""
    if not os.environ.get("GH_TOKEN"):
        raise ValueError("GH_TOKEN required to authenticate human PR approval")
    proc = subprocess.run(["gh", "api", path], capture_output=True,
                          text=True, check=False)
    if proc.returncode:
        raise ValueError("GitHub reviewer evidence unavailable: " + proc.stderr[:300])
    return json.loads(proc.stdout)


def verify_remote_review(record, address, provider=github_json):
    """Tie approval to the exact PR head and an added certificate entry."""
    review = record["reviewer"]
    number = int(review["approval_pr"].rsplit("/", 1)[-1])
    prefix = f"repos/c1c3ru/fft_craft/pulls/{number}"
    pr = provider(prefix)
    reviews = provider(prefix + "/reviews?per_page=100")
    files = provider(prefix + "/files?per_page=100")
    if (not isinstance(pr, dict) or not isinstance(reviews, list)
            or not isinstance(files, list) or not pr.get("head", {}).get("sha")):
        raise ValueError("malformed external PR review evidence")
    certificate_diffs = [
        file for file in files if
        file.get("filename") ==
        "FFT_Android_Mod/docs/re-results/semantic-certificates.json"
        and isinstance(file.get("patch"), str)]
    if not certificate_diffs or not any(
            any(line.startswith("+") and not line.startswith("+++")
                and f'"{address}"' in line
                for line in entry["patch"].splitlines())
            for entry in certificate_diffs):
        raise ValueError("approval PR does not introduce this certificate entry")
    reviewer_login = review["github_login"].lower()
    effective = sorted(
        (item for item in reviews if
         item.get("user", {}).get("login", "").lower() == reviewer_login
         and item.get("submitted_at")), key=lambda item: item["submitted_at"])
    if not effective:
        raise ValueError("no GitHub review by declared reviewer")
    approved = effective[-1]
    if (approved.get("state") != "APPROVED"
            or approved.get("commit_id") != pr["head"]["sha"]
            or approved.get("user", {}).get("type") == "Bot"):
        raise ValueError("last review is not a valid human approval of PR head")
    try:
        declared_date = datetime.date.fromisoformat(review["approved_at"])
        actual_date = datetime.datetime.fromisoformat(
            approved["submitted_at"].replace("Z", "+00:00")).date()
    except (ValueError, TypeError) as exc:
        raise ValueError("invalid approval date") from exc
    if declared_date != actual_date:
        raise ValueError("declared approval date differs from GitHub")
    return True

def gate(binary, inventory, certificates_path):
    binary, inventory = Path(binary), Path(inventory)
    digest = hashlib.sha256(binary.read_bytes()).hexdigest()
    certificates = (json.loads(Path(certificates_path).read_text(encoding="utf-8"))
                    if Path(certificates_path).is_file() else {})
    rows = semantic_coverage.ledger(inventory, digest, certificates)
    by_addr = {r["address"]: r for r in rows}
    certified = []
    review_cache = {}

    def cached_github(path):
        if path not in review_cache:
            review_cache[path] = github_json(path)
        return review_cache[path]

    for address in sorted(certificates):
        record = certificates[address]
        if record.get("status") != "certified":
            continue
        verify_one(record, by_addr[address], binary, digest)
        # A string in reviewer metadata is never treated as proof of consent:
        # GitHub must show an APPROVED review for the affected PR and head.
        verify_remote_review(record, address, provider=cached_github)
        certified.append(address)
    print(f"SEMANTIC_APPROVED_CERTIFICATES_VERIFIED={len(certified)}")
    print(f"SEMANTIC_APPROVED_CERTIFICATE_BYTES={sum(by_addr[a]['size'] for a in certified)}")
    return certified


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--binary", type=Path, default=semantic_coverage.BINARY)
    p.add_argument("--inventory", type=Path, default=semantic_coverage.INVENTORY)
    p.add_argument("--certificates", type=Path,
                   default=semantic_coverage.RESULTS / "semantic-certificates.json")
    a = p.parse_args()
    gate(a.binary, a.inventory, a.certificates)


if __name__ == "__main__":
    main()
