#!/usr/bin/env python3
"""Fail-closed validation gate for *approved*, scoped semantic certificates.

This gate never produces approvals, nor converts a machine-test PASS to a
human-reviewed certificate. Initial supported contract class: exact original
A32 BX LR one-instruction function, under normal valid-return preconditions.
For every approved record, CI checks ELF bytes and reruns differential
Unicorn against an independent normal-instruction-state model.
"""
import argparse
import base64
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
    "review_protocol",
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
    import semantic_review_protocol as protocol
    if review["review_protocol"] != protocol.PROTOCOL:
        raise ValueError("unsupported independent human review protocol")
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


def patch_promotes_address(patch, address):
    """Recognize a reviewable promotion of this precise ledger key in a PR diff."""
    if not isinstance(patch, str):
        return False
    current = None
    for line in patch.splitlines():
        if line.startswith("@@"):
            current = None
            continue
        if not line or line[0] not in "+- " or line.startswith(("+++", "---")):
            continue
        body = line[1:]
        key = re.match(r'^\s*"([0-9a-f]{8})"\s*:\s*\{', body)
        if key:
            current = key.group(1)
        if (line.startswith("+") and current == address
                and re.fullmatch(r'\s*"status"\s*:\s*"certified"\s*,?\s*', body)):
            return True
    return False

def verify_remote_review(record, address, provider=github_json):
    """Verify prior independent approval of an immutable scoped proof request.

    The approved PR must contain an exact contract fingerprint, not the later
    partial->certified promotion. This avoids the unsatisfiable CI cycle where
    the reviewer identity/date would be needed before the PR could be approved.
    """
    import semantic_review_protocol as protocol
    review = record["reviewer"]
    if review.get("review_protocol") != protocol.PROTOCOL:
        raise ValueError("unsupported independent human review protocol")
    number = int(review["approval_pr"].rsplit("/", 1)[-1])
    prefix = f"repos/c1c3ru/fft_craft/pulls/{number}"
    pr = provider(prefix)
    reviews = provider(prefix + "/reviews?per_page=100")
    files = provider(prefix + "/files?per_page=100")
    if (not isinstance(pr, dict) or not isinstance(reviews, list)
            or not isinstance(files, list)
            or not isinstance(pr.get("head"), dict)
            or not isinstance(pr["head"].get("sha"), str)
            or not isinstance(pr.get("user"), dict)):
        raise ValueError("malformed external review PR evidence")
    head_sha = pr["head"]["sha"]
    reviewer_login = review["github_login"].strip().lower()
    if reviewer_login == pr["user"].get("login", "").strip().lower():
        raise ValueError("review author cannot independently approve their own request")
    effective = sorted(
        (item for item in reviews if
         item.get("user", {}).get("login", "").lower() == reviewer_login
         and item.get("submitted_at")), key=lambda item: item["submitted_at"])
    if not effective:
        raise ValueError("no GitHub review by declared reviewer")
    approved = effective[-1]
    if (approved.get("state") != "APPROVED"
            or approved.get("commit_id") != head_sha
            or approved.get("user", {}).get("type") != "User"):
        raise ValueError("last review is not human APPROVED on exact request head")
    try:
        declared_date = datetime.date.fromisoformat(review["approved_at"])
        actual_date = datetime.datetime.fromisoformat(
            approved["submitted_at"].replace("Z", "+00:00")).date()
    except (ValueError, TypeError) as exc:
        raise ValueError("invalid approval date") from exc
    if declared_date != actual_date:
        raise ValueError("declared approval date differs from GitHub")
    fingerprint = protocol.fingerprint(address, record)
    changed = [file for file in files if
               protocol.is_review_request_path(file.get("filename"))
               and isinstance(file.get("patch"), str)]
    def includes_approved_fingerprint(patch):
        for line in patch.splitlines():
            if not line.startswith("+") or line.startswith("+++"):
                continue
            matched = re.fullmatch(
                r'\s*"([0-9a-f]{8})"\s*:\s*"([0-9a-f]{64})"\s*,?\s*',
                line[1:])
            if matched and matched.group(1) == address and matched.group(2) == fingerprint:
                return True
        return False
    # GitHub can truncate large unified diffs. A newly ADDED file is a
    # reliable PR-file fact; its entire content is fetched from the exact
    # reviewer-approved commit below and the fingerprint checked there.
    approved_sources = [item for item in changed if
                        item.get("status") == "added"
                        or includes_approved_fingerprint(item["patch"])]
    if len(approved_sources) != 1:
        raise ValueError("review PR must add the exact scoped fingerprint in one review request")
    approved_path = approved_sources[0]["filename"]
    ref = f"repos/c1c3ru/fft_craft/contents/{approved_path}?ref={head_sha}"
    document = provider(ref)
    if (not isinstance(document, dict)
            or document.get("encoding") != "base64"
            or not isinstance(document.get("content"), str)):
        raise ValueError("review request content unavailable at approved commit")
    try:
        payload = json.loads(base64.b64decode(
            document["content"], validate=False).decode("utf-8"))
    except (ValueError, TypeError, UnicodeError) as exc:
        raise ValueError("invalid reviewed request payload") from exc
    if (payload.get("schema") != 1
            or payload.get("review_protocol") != protocol.PROTOCOL
            or payload.get("elf_sha256") != record["binary_sha256"]
            or payload.get("status") != "human_review_requested"
            or payload.get("certified") is not False
            or payload.get("certificate_fingerprints", {}).get(address) != fingerprint):
        raise ValueError("approved request differs from proposed certificate")
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
