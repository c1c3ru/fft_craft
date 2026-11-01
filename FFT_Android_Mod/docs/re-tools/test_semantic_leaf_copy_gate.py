"""T12 (RE_COMPLETUDE_TASKS.md): verify_leaf_copy, the second supported
proof class in semantic_certificate_gate.py, alongside the pre-existing
BX LR one. Mirrors test_semantic_certificate_gate.py's style (synthetic
digest, injected reader/differ -- no real binary or network needed).

Required by T12's acceptance criterion: the gate must reject a BX LR
proof misapplied here, an incomplete certificate, a function with a
relevant (unknown or otherwise) callee, and evidence bound to another
ELF -- each has its own test below.
"""
import hashlib
import unittest

import semantic_certificate_gate as gate
import semantic_review_protocol as protocol

DIGEST = "b" * 64
ADDRESS = "001d9ee0"
SIZE = 120

# push {r4,lr}; nop*? ... real shape doesn't matter here, only that it
# decodes as a clean, branch-free, call-free ARM block ending in bx lr.
PURE_COPY_BODY = bytes.fromhex(
    "04402de5"      # str r4, [sp, #-4]!
    "04409de4"      # ldr r4, [sp], #4
    "1eff2fe1"       # bx lr
)
BRANCHY_BODY = bytes.fromhex(
    "0100008b"       # bl #0x10 (a relevant callee -- disqualifies this class)
    "1eff2fe1"
)


def approved(**overrides):
    record = {
        "status": "certified",
        "proof_class": gate.LEAF_COPY_SCOPE,
        "scope": gate.LEAF_COPY_SCOPE,
        "binary_sha256": DIGEST,
        "size": SIZE,
        "instruction_sha256": hashlib.sha256(PURE_COPY_BODY).hexdigest(),
        "preconditions": ["BWORK/EDATA pointers valid and mapped"],
        "postconditions": ["BWORK fields updated per contract"],
        "memory_effects": ["writes fixed offsets of BWORK from EDATA"],
        "control_flow": list(gate.LEAF_COPY_CONTROL_FLOW),
        "test_evidence": ["Unicorn differential vs. independent Python reference"],
        "reviewer": {
            "type": "human", "name": "Independent Reviewer",
            "github_login": "independent-reviewer",
            "decision": "approved",
            "approval_pr": "https://github.com/c1c3ru/fft_craft/pull/900",
            "approved_at": "2026-10-31", "notes": "Signed human-scoped review",
            "review_protocol": protocol.PROTOCOL,
        },
    }
    record.update(overrides)
    return record


def make_reader(body=PURE_COPY_BODY):
    def read(binary, address, size):
        return body
    return read


def make_differ(match=True):
    def differ(binary, address, size, record):
        return {"match": match}
    return differ


class LeafCopyGateTests(unittest.TestCase):
    def test_well_formed_certificate_passes(self):
        self.assertTrue(gate.verify_leaf_copy(
            approved(), {"address": ADDRESS, "size": SIZE}, None, DIGEST,
            reader=make_reader(), differ=make_differ(True)))

    def test_rejects_bxlr_proof_class_misapplied_here(self):
        record = approved(proof_class=gate.SCOPE, scope=gate.SCOPE)
        with self.assertRaises(ValueError):
            gate.verify_leaf_copy(
                record, {"address": ADDRESS, "size": SIZE}, None, DIGEST,
                reader=make_reader(), differ=make_differ(True))

    def test_rejects_incomplete_certificate(self):
        for missing in ("preconditions", "postconditions", "memory_effects",
                        "control_flow", "test_evidence"):
            with self.subTest(missing=missing):
                record = approved()
                del record[missing]
                with self.assertRaises(ValueError):
                    gate.verify_leaf_copy(
                        record, {"address": ADDRESS, "size": SIZE}, None, DIGEST,
                        reader=make_reader(), differ=make_differ(True))

    def test_rejects_function_with_a_relevant_callee(self):
        # The record CLAIMS a pure leaf copy, but the actual ELF bytes (as
        # the live reader returns them) contain a bl -- the gate must
        # catch this from the real bytes, not trust the claim.
        record = approved(instruction_sha256=hashlib.sha256(BRANCHY_BODY).hexdigest())
        with self.assertRaises(ValueError):
            gate.verify_leaf_copy(
                record, {"address": ADDRESS, "size": len(BRANCHY_BODY)}, None, DIGEST,
                reader=make_reader(BRANCHY_BODY), differ=make_differ(True))

    def test_rejects_evidence_bound_to_a_different_elf(self):
        record = approved(binary_sha256="c" * 64)  # does not match `digest` below
        with self.assertRaises(ValueError):
            gate.verify_leaf_copy(
                record, {"address": ADDRESS, "size": SIZE}, None, DIGEST,
                reader=make_reader(), differ=make_differ(True))

    def test_rejects_failed_live_differential(self):
        with self.assertRaises(ValueError):
            gate.verify_leaf_copy(
                approved(), {"address": ADDRESS, "size": SIZE}, None, DIGEST,
                reader=make_reader(), differ=make_differ(False))

    def test_rejects_missing_or_bot_reviewer(self):
        for reviewer in (None, {"type": "bot", "github_login": "ci[bot]",
                                "decision": "approved",
                                "approval_pr": "https://github.com/c1c3ru/fft_craft/pull/1",
                                "name": "x", "approved_at": "2026-10-31",
                                "notes": "x", "review_protocol": protocol.PROTOCOL}):
            with self.subTest(reviewer=reviewer):
                record = approved(reviewer=reviewer)
                with self.assertRaises(ValueError):
                    gate.verify_leaf_copy(
                        record, {"address": ADDRESS, "size": SIZE}, None, DIGEST,
                        reader=make_reader(), differ=make_differ(True))

    def test_default_differ_is_not_silently_permissive(self):
        # No `differ` injected -- the gate must not fall back to a
        # default that quietly accepts an arbitrary function.
        with self.assertRaises(NotImplementedError):
            gate.verify_leaf_copy(
                approved(), {"address": ADDRESS, "size": SIZE}, None, DIGEST,
                reader=make_reader())


if __name__ == "__main__":
    unittest.main()
