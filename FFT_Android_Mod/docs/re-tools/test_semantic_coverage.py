"""Semantic coverage must never infer full equivalence from structural checks."""
import csv
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

spec = importlib.util.spec_from_file_location("semantic_coverage", Path(__file__).with_name("semantic_coverage.py"))
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


class SemanticCoverageTests(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.dir.cleanup)
        self.path = Path(self.dir.name) / "inventory.csv"
        with self.path.open("w", newline="") as stream:
            writer = csv.DictWriter(stream, fieldnames=["address", "size", "demangled"])
            writer.writeheader()
            writer.writerow({"address": "00000010", "size": 120, "demangled": "a"})
            writer.writerow({"address": "00000020", "size": 80, "demangled": "b"})

    def test_unknown_not_promoted(self):
        rows = mod.ledger(self.path, "a" * 64, {})
        self.assertEqual([x["semantic_status"] for x in rows], ["unknown", "unknown"])
        report = mod.report(rows, "a" * 64)
        self.assertIn("Funções inventariadas | 2", report)
        self.assertIn("Semântica integral certificada por registro | 0", report)

    def test_partial_is_not_certified(self):
        rows = mod.ledger(self.path, "a" * 64, {
            "00000010": {"status": "partial", "binary_sha256": "a" * 64, "size": 120,
                         "test_evidence": ["microexec"]}
        })
        self.assertEqual(rows[0]["semantic_status"], "partial")

    def test_requires_certificate_fields_and_hash(self):
        with self.assertRaises(ValueError):
            mod.ledger(self.path, "a" * 64, {"00000010": {
                "status": "certified", "binary_sha256": "a" * 64, "size": 120,
                "test_evidence": ["microexec"]}})
        with self.assertRaises(ValueError):
            mod.ledger(self.path, "a" * 64, {"00000010": {
                "status": "partial", "binary_sha256": "b" * 64, "size": 120}})

    def test_rejects_outside_inventory(self):
        with self.assertRaises(ValueError):
            mod.ledger(self.path, "a" * 64, {"deadbeef": {}})


if __name__ == "__main__":
    unittest.main()
