"""Review packets are byte-bound and never certify or double-count tests."""
import hashlib
import json
import tempfile
import unittest
from pathlib import Path

import semantic_bxlr_review_batch as batch
import semantic_bxlr_contract_pilot as local
import semantic_certificate_gate as gate

CODE = bytes.fromhex("1eff2fe1")


class ReviewBatchTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.binary = self.root / "libtest.so"
        self.binary.write_bytes(b"ELF fixture for digest, not execution")
        self.digest = hashlib.sha256(self.binary.read_bytes()).hexdigest()
        self.inventory = self.root / "inventory.csv"
        self.inventory.write_text(
            "address,size,demangled\n00002010,4,return_one\n"
            "00002014,4,return_alias\n00002020,32,large_function\n",
            encoding="utf-8")
        self.contracts = self.root / "contracts"
        self.contracts.mkdir()
        for address in ("00002010", "00002014"):
            record = {
                "address": address, "name": "test", "size": 4,
                "binary_sha256": self.digest,
                "instruction_word": CODE.hex(),
                "instruction_sha256": hashlib.sha256(CODE).hexdigest(),
                "semantic_status": "partial", "certified": False,
                "reviewer": None,
                "contract_stage": "local_isa_contract_checked_review_pending",
                "machine_samples_passed": 32, "machine_samples_failed": 0,
                "verified_return_modes": ["ARM", "Thumb"],
                "contract": local.isa_contract(CODE),
                "preconditions": list(gate.PRECONDITIONS),
                "postconditions": list(gate.POSTCONDITIONS),
                "memory_effects": list(gate.MEMORY_EFFECTS),
                "control_flow": list(gate.CONTROL_FLOW),
                "test_evidence": list(gate.REQUIRED_EVIDENCE),
            }
            (self.contracts / (address + ".json")).write_text(
                json.dumps(record), encoding="utf-8")

    def prepare(self, limit=2, reader=None):
        return batch.build(self.binary, self.inventory, self.contracts,
                           limit=limit, reader=reader or
                           (lambda binary, address, size: CODE),
                           run_id="456")

    def test_reuses_verified_contracts_with_no_new_certification(self):
        proof = self.prepare()
        self.assertEqual(len(proof["candidates"]), 2)
        self.assertEqual(proof["source_ci_run_id"], "456")
        self.assertEqual(proof["certified_functions"], 0)
        self.assertEqual(proof["sample_accounting"],
                         "reuses previous 32 samples per function; adds zero")
        self.assertEqual([p["address"] for p in proof["candidates"]],
                         ["00002010", "00002014"])
        self.assertTrue(all(p["status"] == "partial" and
                            p["certified"] is False and
                            p["reviewer"] is None and
                            p["new_machine_samples_in_this_step"] == 0
                            for p in proof["candidates"]))
        self.assertEqual(proof["candidates"][0]["proof_class"], gate.SCOPE)
        self.assertIn("revisão pendente", batch.render(proof))
        output = self.root / "manifest.json"
        report = self.root / "review.md"
        batch.write(proof, output, report)
        self.assertEqual(json.loads(output.read_text())["certified_functions"], 0)
        self.assertIn("Nenhuma função está certificada", report.read_text())

    def test_seeded_partial_ledger_must_match_proven_contract(self):
        import semantic_coverage
        certfile = self.root / "certificates.json"
        proof = self.prepare(limit=1)["candidates"][0]
        record = {k: v for k, v in proof.items() if
                  k in ("status", "binary_sha256", "size", "proof_class",
                        "scope", "instruction_encoding", "instruction_sha256",
                        "contract", "preconditions", "postconditions",
                        "control_flow", "memory_effects", "test_evidence",
                        "reviewer")}
        certfile.write_text(json.dumps({"00002010": record}))
        approved = batch.build(
            self.binary, self.inventory, self.contracts, limit=2,
            reader=lambda binary, address, size: CODE,
            certificates_path=certfile)
        self.assertEqual(len(approved["candidates"]), 2)
        record["contract"] = "forged"
        certfile.write_text(json.dumps({"00002010": record}))
        with self.assertRaisesRegex(ValueError, "ledger and same-run"):
            batch.build(self.binary, self.inventory, self.contracts,
                        reader=lambda binary, address, size: CODE,
                        certificates_path=certfile)

    def test_stale_opcode_or_digest_is_blocking(self):
        with self.assertRaisesRegex(ValueError, "ELF bytes changed"):
            self.prepare(reader=lambda binary, address, size: b"\x00" * 4)
        path = self.contracts / "00002010.json"
        record = json.loads(path.read_text())
        record["binary_sha256"] = "a" * 64
        path.write_text(json.dumps(record))
        with self.assertRaisesRegex(ValueError, "unverified or stale"):
            self.prepare()

    def test_reviewer_cannot_be_forged_by_candidate_file(self):
        path = self.contracts / "00002010.json"
        record = json.loads(path.read_text())
        record["reviewer"] = {"type": "human", "decision": "approved"}
        path.write_text(json.dumps(record))
        with self.assertRaisesRegex(ValueError, "unverified or stale"):
            self.prepare()

    def test_capped_review_batch_with_fewer_remaining_candidates(self):
        result = batch.build(
            self.binary, self.inventory, self.contracts, limit=100,
            reader=lambda binary, address, size: CODE,
            up_to=True)
        self.assertEqual(len(result["candidates"]), 2)
        self.assertEqual(result["certified_functions"], 0)
        self.assertEqual(result["candidates"][0]["new_machine_samples_in_this_step"], 0)

    def test_missing_or_few_valid_candidates_is_fatal(self):
        with self.assertRaises(ValueError):
            self.prepare(limit=304)
        with self.assertRaisesRegex(ValueError, "insufficient"):
            self.prepare(limit=3)
        for path in self.contracts.glob("*.json"):
            path.unlink()
        with self.assertRaisesRegex(ValueError, "no same-run"):
            self.prepare()


if __name__ == "__main__":
    unittest.main()
