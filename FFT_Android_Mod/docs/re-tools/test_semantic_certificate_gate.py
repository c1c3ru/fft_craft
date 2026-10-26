"""Regression: certification requires human approval plus fresh exact ELF execution."""
import hashlib
import unittest

import semantic_bxlr_contract_pilot as pilot
import semantic_certificate_gate as gate

WORD = bytes.fromhex("1eff2fe1")
DIGEST = "a" * 64
ADDRESS = "00002010"


def approved():
    return {
        "status": "certified",
        "proof_class": gate.SCOPE,
        "scope": "normal_a32_valid_abi_return",
        "binary_sha256": DIGEST,
        "size": 4,
        "instruction_encoding": WORD.hex(),
        "instruction_sha256": hashlib.sha256(WORD).hexdigest(),
        "contract": pilot.isa_contract(WORD),
        "preconditions": list(gate.PRECONDITIONS),
        "postconditions": list(gate.POSTCONDITIONS),
        "memory_effects": list(gate.MEMORY_EFFECTS),
        "control_flow": list(gate.CONTROL_FLOW),
        "test_evidence": list(gate.REQUIRED_EVIDENCE),
        "reviewer": {
            "type": "human", "name": "Independent Reviewer",
            "github_login": "independent-reviewer",
            "decision": "approved", "approval_pr":
                "https://github.com/c1c3ru/fft_craft/pull/325",
            "approved_at": "2026-10-26", "notes": "Signed human-scoped review",
        },
    }


class CertificateGateTests(unittest.TestCase):
    def test_checked_certificate_with_exact_original_arm_word(self):
        checked = []
        def read(binary, address, size):
            self.assertEqual((address, size), (0x2010, 4))
            return WORD
        def execute(address, word):
            checked.append((address, word))
            return 32
        self.assertTrue(gate.verify_one(
            approved(), {"address": ADDRESS, "size": 4},
            None, DIGEST, reader=read, executor=execute))
        self.assertEqual(checked, [(0x2010, WORD)])

    def test_requires_explicit_human_review(self):
        for reviewer in (
            None, "CI", {"type": "bot", "name": "CI",
                         "github_login": "ci[bot]",
                         "decision": "approved", "approval_pr":
                             "https://github.com/c1c3ru/fft_craft/pull/325",
                         "approved_at": "2026-10-26", "notes": "not human"},
            dict(approved()["reviewer"], decision="pending"),
            dict(approved()["reviewer"], approval_pr="https://attacker.test/1"),
        ):
            cert = approved()
            cert["reviewer"] = reviewer
            with self.subTest(reviewer=reviewer):
                with self.assertRaises(ValueError):
                    gate.verify_one(cert, {"address": ADDRESS, "size": 4},
                                    None, DIGEST)

    def test_remote_approval_tied_to_entry_and_head_commit(self):
        cert = approved()
        # The local fixture never claims that this PR is *actually* approved;
        # the mocked GitHub data only exercises the gate contract.
        expected_prefix = "repos/c1c3ru/fft_craft/pulls/325"
        def provider(path):
            self.assertTrue(path.startswith(expected_prefix))
            if path == expected_prefix:
                return {"head": {"sha": "commit-abc"}}
            if path.endswith("/reviews?per_page=100"):
                return [{"user": {"login": "independent-reviewer",
                                  "type": "User"},
                         "state": "APPROVED", "commit_id": "commit-abc",
                         "submitted_at": "2026-10-26T15:00:00Z"}]
            return [{"filename": "FFT_Android_Mod/docs/re-results/"
                                  "semantic-certificates.json",
                     "patch": ('@@ -1,9 +1,9 @@\n'
                               ' {\n'
                               '   "00002010": {\n'
                               '-    "status": "partial",\n'
                               '+    "status": "certified",\n'
                               '     "size": 4,')}]
        self.assertTrue(gate.verify_remote_review(cert, ADDRESS, provider))
        with self.assertRaisesRegex(ValueError, "specific certificate"):
            gate.verify_remote_review(cert, "00002014", provider)
        def wrong_commit(path):
            value = provider(path)
            if path == expected_prefix:
                return {"head": {"sha": "different-head"}}
            return value
        with self.assertRaisesRegex(ValueError, "valid human approval"):
            gate.verify_remote_review(cert, ADDRESS, wrong_commit)

    def test_unified_diff_partial_promotion_scoped_per_address(self):
        patch = (
            "@@ -1,11 +1,11 @@\n"
            " {\n"
            '   "00002010": {\n'
            '-    "status": "partial",\n'
            '+    "status": "certified",\n'
            '   "00002014": {\n'
            '     "status": "partial",\n'
        )
        self.assertTrue(gate.patch_promotes_address(patch, "00002010"))
        self.assertFalse(gate.patch_promotes_address(patch, "00002014"))
        self.assertFalse(gate.patch_promotes_address(patch, "00002018"))
        forged = (
            "@@ -1,9 +1,9 @@\n"
            '   "00002010": {\n'
            '+    "status": "partial",\n'
            '   "00002014": {\n'
            '+    "status": "certified",\n'
        )
        self.assertFalse(gate.patch_promotes_address(forged, "00002010"))
        self.assertTrue(gate.patch_promotes_address(forged, "00002014"))

    def test_reject_wrong_binary_opcode_or_unverified_tests(self):
        for change in (
            {"binary_sha256": "b" * 64},
            {"instruction_sha256": "b" * 64},
            {"size": 8},
            {"scope": "whole_program_equivalence"},
            {"contract": "imaginary function"},
        ):
            cert = dict(approved(), **change)
            with self.subTest(change=change):
                with self.assertRaises(ValueError):
                    gate.verify_one(cert, {"address": ADDRESS, "size": 4},
                                    None, DIGEST, reader=lambda *_: WORD,
                                    executor=lambda *_: 32)
        with self.assertRaisesRegex(ValueError, "ELF no longer"):
            gate.verify_one(approved(), {"address": ADDRESS, "size": 4},
                            None, DIGEST, reader=lambda *_: b"\x00" * 4,
                            executor=lambda *_: 32)
        with self.assertRaisesRegex(ValueError, "insufficient"):
            gate.verify_one(approved(), {"address": ADDRESS, "size": 4},
                            None, DIGEST, reader=lambda *_: WORD,
                            executor=lambda *_: 31)


if __name__ == "__main__":
    unittest.main()
