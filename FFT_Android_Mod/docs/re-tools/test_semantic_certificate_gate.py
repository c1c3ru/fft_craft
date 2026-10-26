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
        "preconditions": ["ARM mode and mapped aligned return target"],
        "postconditions": ["PC from LR", "CPSR.T selected from LR"],
        "memory_effects": ["none"], "control_flow": ["BX LR"],
        "test_evidence": ["original ELF", "differential model", "Unicorn"],
        "reviewer": {
            "type": "human", "name": "Independent Reviewer",
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
        with self.assertRaisesRegex(ValueError, "original ELF"):
            gate.verify_one(approved(), {"address": ADDRESS, "size": 4},
                            None, DIGEST, reader=lambda *_: b"\x00" * 4,
                            executor=lambda *_: 32)
        with self.assertRaisesRegex(ValueError, "insufficient"):
            gate.verify_one(approved(), {"address": ADDRESS, "size": 4},
                            None, DIGEST, reader=lambda *_: WORD,
                            executor=lambda *_: 31)


if __name__ == "__main__":
    unittest.main()
