"""Regression checks for independent, exact-ELF review request generation."""
import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import semantic_bxlr_contract_pilot as bxlr
import semantic_certificate_gate as gate
import semantic_review_protocol as protocol

WORD = bytes.fromhex("1eff2fe1")


class SemanticReviewProtocolTests(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.dir.cleanup)
        self.root = Path(self.dir.name)
        self.elf = self.root / "test-arm.so"
        self.elf.write_bytes(b"this fixture hashes binary, mocked read checks ELF word")
        self.digest = hashlib.sha256(self.elf.read_bytes()).hexdigest()
        self.inventory = self.root / "inventory.csv"
        self.inventory.write_text(
            "address,size,demangled\n00002010,4,first\n"
            "00002014,4,second\n00002020,100,nonleaf\n",
            encoding="utf-8")
        self.ledger = self.root / "certificates.json"
        self.records = {}
        for address in ("00002010", "00002014"):
            self.records[address] = {
                "status": "partial",
                "size": 4, "binary_sha256": self.digest,
                "proof_class": gate.SCOPE,
                "scope": "normal_a32_valid_abi_return",
                "instruction_encoding": WORD.hex(),
                "instruction_sha256": hashlib.sha256(WORD).hexdigest(),
                "contract": bxlr.isa_contract(WORD),
                "preconditions": list(gate.PRECONDITIONS),
                "postconditions": list(gate.POSTCONDITIONS),
                "control_flow": list(gate.CONTROL_FLOW),
                "memory_effects": list(gate.MEMORY_EFFECTS),
                "test_evidence": list(gate.REQUIRED_EVIDENCE),
                "reviewer": None,
                "machine_samples_passed": 32,
            }
        self.save()
    def save(self):
        self.ledger.write_text(json.dumps(self.records), encoding="utf-8")
    def build(self, limit=2):
        with mock.patch.object(protocol.semantic_evidence, "read_function",
                               return_value=WORD), mock.patch.object(
                protocol.bxlr, "verify_interworking", return_value=32):
            return protocol.make_request(self.elf, self.inventory,
                                         self.ledger, limit=limit)

    def test_two_distinct_original_elf_review_fingerprints(self):
        request = self.build()
        self.assertEqual(request["review_protocol"], protocol.PROTOCOL)
        self.assertEqual(request["status"], "human_review_requested")
        self.assertIs(request["certified"], False)
        self.assertEqual(request["elf_sha256"], self.digest)
        self.assertEqual(sorted(request["certificate_fingerprints"]),
                         ["00002010", "00002014"])
        self.assertNotEqual(request["certificate_fingerprints"]["00002010"],
                            request["certificate_fingerprints"]["00002014"])

    def test_fingerprint_detects_any_changed_contract_field(self):
        r = self.records["00002010"]
        original = protocol.fingerprint("00002010", r)
        for key, replacement in (
            ("contract", "something else"),
            ("scope", "whole_program"),
            ("binary_sha256", "b" * 64),
            ("instruction_sha256", "c" * 64),
            ("postconditions", ["changes memory"]),
        ):
            modified = dict(r, **{key: replacement})
            with self.subTest(key=key):
                self.assertNotEqual(protocol.fingerprint("00002010", modified),
                                    original)

    def test_fail_closed_on_unproven_candidate_or_changed_elf_word(self):
        record = self.records["00002010"]
        record["machine_samples_passed"] = 31
        self.save()
        with self.assertRaisesRegex(ValueError, "exact local proof"):
            self.build()
        record["machine_samples_passed"] = 32
        self.save()
        with mock.patch.object(protocol.semantic_evidence, "read_function",
                               return_value=b"\0\0\0\0"):
            with self.assertRaisesRegex(ValueError, "original ELF mismatch"):
                protocol.make_request(self.elf, self.inventory, self.ledger, 1)

    def test_review_request_requires_live_differential_execution(self):
        with mock.patch.object(protocol.semantic_evidence, "read_function",
                               return_value=WORD), mock.patch.object(
                protocol.bxlr, "verify_interworking", return_value=31):
            with self.assertRaisesRegex(ValueError, "differential proof"):
                protocol.make_request(self.elf, self.inventory, self.ledger, 1)

    def test_reject_any_already_approved_record_as_unreviewed(self):
        self.records["00002010"]["status"] = "certified"
        self.records["00002010"]["reviewer"] = {"type": "human"}
        self.save()
        with self.assertRaisesRegex(ValueError, "not enough"):
            self.build(limit=2)

    def test_immutable_request_remains_valid_after_five_certifications(self):
        original = self.build()
        request_path = self.root / "review-request.json"
        request_path.write_text(json.dumps(original), encoding="utf-8")
        with mock.patch.object(protocol.semantic_evidence, "read_function",
                               return_value=WORD), mock.patch.object(
                protocol.bxlr, "verify_interworking", return_value=32):
            self.assertEqual(protocol.verify_request(
                self.elf, self.inventory, self.ledger, request_path), 2)
        for record in self.records.values():
            record["status"] = "certified"
            record["reviewer"] = {
                "type": "human", "name": "Independent reviewer",
                "github_login": "independent-reviewer", "decision": "approved",
                "approval_pr": "https://github.com/c1c3ru/fft_craft/pull/338",
                "review_protocol": protocol.PROTOCOL,
                "approved_at": "2026-10-26", "notes": "Mocked test review",
            }
        self.save()
        with mock.patch.object(protocol.semantic_evidence, "read_function",
                               return_value=WORD), mock.patch.object(
                protocol.bxlr, "verify_interworking", return_value=32):
            self.assertEqual(protocol.verify_request(
                self.elf, self.inventory, self.ledger, request_path), 2)
        self.assertIs(original["certified"], False)

    def test_fails_closed_when_reviewed_fingerprint_changes(self):
        original = self.build()
        request_path = self.root / "review-request.json"
        original["certificate_fingerprints"]["00002010"] = "f" * 64
        request_path.write_text(json.dumps(original), encoding="utf-8")
        with mock.patch.object(protocol.semantic_evidence, "read_function",
                               return_value=WORD), mock.patch.object(
                protocol.bxlr, "verify_interworking", return_value=32):
            with self.assertRaisesRegex(ValueError, "reviewed fingerprint"):
                protocol.verify_request(self.elf, self.inventory, self.ledger,
                                        request_path)

    def test_fail_closed_for_wrong_binary_or_live_reexecution(self):
        original = self.build()
        request_path = self.root / "review-request.json"
        request_path.write_text(json.dumps(original), encoding="utf-8")
        with mock.patch.object(protocol.semantic_evidence, "read_function",
                               return_value=b"\x00" * 4):
            with self.assertRaisesRegex(ValueError, "original ELF"):
                protocol.verify_request(self.elf, self.inventory, self.ledger,
                                        request_path)
        with mock.patch.object(protocol.semantic_evidence, "read_function",
                               return_value=WORD), mock.patch.object(
                protocol.bxlr, "verify_interworking", return_value=31):
            with self.assertRaisesRegex(ValueError, "differential execution"):
                protocol.verify_request(self.elf, self.inventory, self.ledger,
                                        request_path)

    def test_accepts_versioned_review_requests_but_not_unrelated_paths(self):
        accepted = [
            protocol.REVIEW_PATH, protocol.REVIEW_RETRY_PATH,
            protocol.REVIEW_BASE + "SEMANTIC_BXLR_REVIEW_REQUEST_R3.json",
            protocol.REVIEW_BASE + "SEMANTIC_BXLR_REVIEW_REQUEST_R100.json",
        ]
        rejected = [
            protocol.REVIEW_BASE + "SEMANTIC_BXLR_REVIEW_REQUEST_R1.json",
            protocol.REVIEW_BASE + "SEMANTIC_BXLR_REVIEW_REQUEST_R0.json",
            protocol.REVIEW_BASE + "SEMANTIC_BXLR_REVIEW_REQUEST_R3.json.bak",
            protocol.REVIEW_BASE + "../SEMANTIC_BXLR_REVIEW_REQUEST_R3.json",
            "FFT_Android_Mod/docs/re-results/arbitrary.json",
            None, "", "SEMANTIC_BXLR_REVIEW_REQUEST_R3.json"
        ]
        for value in accepted:
            with self.subTest(value=value):
                self.assertTrue(protocol.is_review_request_path(value))
        for value in rejected:
            with self.subTest(value=value):
                self.assertFalse(protocol.is_review_request_path(value))
        review_dir = self.root / "requests"
        review_dir.mkdir()
        for filename in (
            "SEMANTIC_BXLR_REVIEW_REQUEST.json",
            "SEMANTIC_BXLR_REVIEW_REQUEST_R2.json",
            "SEMANTIC_BXLR_REVIEW_REQUEST_R3.json",
            "SEMANTIC_BXLR_REVIEW_REQUEST_R4.json.bak",
            "OTHER.json",
        ):
            (review_dir / filename).write_text("{}")
        self.assertEqual(
            [p.name for p in protocol.reviewed_request_paths(review_dir)],
            ["SEMANTIC_BXLR_REVIEW_REQUEST.json",
             "SEMANTIC_BXLR_REVIEW_REQUEST_R2.json",
             "SEMANTIC_BXLR_REVIEW_REQUEST_R3.json"],
        )

    def test_small_valid_limit(self):
        with self.assertRaises(ValueError):
            self.build(0)
        with self.assertRaises(ValueError):
            self.build(304)
        self.assertEqual(len(self.build(1)["certificate_fingerprints"]), 1)
        # The larger batch cap must not silently accept missing evidence.
        with self.assertRaisesRegex(ValueError, "not enough"):
            self.build(100)


if __name__ == "__main__":
    unittest.main()
