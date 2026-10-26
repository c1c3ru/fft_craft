"""Regression checks for centralized exact-ELF semantic accounting."""
import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
sys.path.insert(0, str(TOOLS))
spec = importlib.util.spec_from_file_location(
    "central_semantic_summary", TOOLS / "central_semantic_summary.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


class CentralSemanticSummaryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.inventory = self.root / "inventory.csv"
        self.inventory.write_text(
            "address,size,demangled\n00000010,120,foo\n"
            "00000010,120,foo_alias\n00000020,80,bar\n", encoding="utf-8")
        self.digest = "a" * 64
        self.pilot = self.root / "pilot"
        self.dynamic = self.root / "dynamic"
        self.manifests = self.root / "manifests"
        for directory in (self.pilot, self.dynamic, self.manifests):
            directory.mkdir()

    def write(self, folder, name, data):
        (folder / name).write_text(json.dumps(data), encoding="utf-8")

    def test_unique_bytes_and_partial_evidence(self):
        self.write(self.pilot, "00000010.json",
                   {"address": "00000010", "binary_sha256": self.digest,
                    "semantic_status": "partial"})
        self.write(self.dynamic, "00000020.json",
                   {"address": "00000020", "binary_sha256": self.digest,
                    "semantic_status": "partial", "certified": False,
                    "machine_samples_passed": 32})
        self.write(self.manifests, "semantic-worker-01.json",
                   {"elf_sha256": self.digest, "tasks": [
                       {"address": "00000010", "size": 120,
                        "binary_sha256": self.digest}]})
        s = mod.summarize(self.inventory, self.digest, self.root / "none.json",
                          self.pilot, self.dynamic, self.manifests)
        self.assertEqual((s["symbols"], s["unique"], s["total_bytes"]), (3, 2, 200))
        self.assertEqual((s["partial_evidence_unique"], s["certified"]), (2, 0))
        self.assertEqual((s["assigned"], s["static_reports"], s["unicorn_reports"]),
                         (1, 1, 1))
        self.assertIn("0.00%", mod.render(s))
        self.assertEqual(s["dynamic_samples"], 32)

    def test_shared_unicorn_suite_counted_once(self):
        for address in ("00000010", "00000020"):
            self.write(self.dynamic, address + ".json",
                       {"address": address, "binary_sha256": self.digest,
                        "semantic_status": "partial", "certified": False,
                        "suite_samples_passed": 72,
                        "suite_sample_count_scope": "shared across callee routes"})
        result = mod.summarize(self.inventory, self.digest,
                               self.root / "none.json", dynamic_dir=self.dynamic)
        self.assertEqual(result["dynamic_samples"], 72)
        self.assertEqual(result["unicorn_reports"], 2)
        self.assertIn("Microexecuções Unicorn verificadas", mod.render(result))

    def test_local_contracts_are_counted_without_certification(self):
        self.inventory.write_text("address,size,demangled\n00000010,4,foo\n00000010,4,foo_alias\n00000020,80,bar\n", encoding="utf-8")
        contracts = self.root / "contracts"
        contracts.mkdir()
        self.write(contracts, "00000010.json", {
            "address": "00000010", "binary_sha256": self.digest,
            "instruction_word": "1eff2fe1", "contract_stage":
                "local_isa_contract_checked_review_pending",
            "semantic_status": "partial", "certified": False,
            "machine_samples_passed": 32, "machine_samples_failed": 0,
            "reviewer": None
        })
        report = mod.summarize(self.inventory, self.digest,
                               self.root / "missing.json",
                               contracts_dir=contracts)
        self.assertEqual(report["checked_local_contracts"], 1)
        self.assertEqual(report["contract_samples"], 32)
        self.assertEqual(report["certified"], 0)
        self.assertIn("Contratos locais BX LR", mod.render(report))
        self.write(contracts, "00000010.json", {
            "address": "00000010", "binary_sha256": self.digest,
            "instruction_word": "1eff2fe1", "contract_stage":
                "local_isa_contract_checked_review_pending",
            "semantic_status": "partial", "certified": True,
            "machine_samples_passed": 32, "machine_samples_failed": 0,
            "reviewer": None
        })
        with self.assertRaises(ValueError):
            mod.summarize(self.inventory, self.digest,
                          self.root / "missing.json",
                          contracts_dir=contracts)

    def test_certified_record_requires_original_binary_gate(self):
        certpath = self.root / "certs.json"
        certpath.write_text(json.dumps({
            "00000020": {
                "status": "certified", "binary_sha256": self.digest,
                "size": 80, "contract": "claimed",
                "preconditions": ["a"], "postconditions": ["b"],
                "control_flow": ["c"], "memory_effects": ["d"],
                "test_evidence": ["e"], "reviewer": "somebody"
            }
        }))
        with self.assertRaisesRegex(ValueError, "original ELF proof validation"):
            mod.summarize(self.inventory, self.digest, certpath)

    def test_review_batch_is_not_counted_as_certification(self):
        self.inventory.write_text(
            "address,size,demangled\n00000010,4,return_leaf\n"
            "00000020,80,other\n", encoding="utf-8")
        review_file = self.root / "review.json"
        review_file.write_text(json.dumps({
            "schema": 1, "elf_sha256": self.digest,
            "status": "review_pending", "certified_functions": 0,
            "candidates": [{
                "address": "00000010", "binary_sha256": self.digest,
                "size": 4, "status": "partial", "certified": False,
                "instruction_encoding": "1eff2fe1", "reviewer": None,
                "review_stage": "independent_human_review_pending",
                "same_run_machine_samples": 32,
                "new_machine_samples_in_this_step": 0
            }]
        }), encoding="utf-8")
        summary = mod.summarize(
            self.inventory, self.digest, self.root / "none.json",
            review_batch_path=review_file)
        self.assertEqual(summary["review_batch_candidates"], 1)
        self.assertEqual(summary["certified"], 0)
        self.assertEqual(summary["contract_samples"], 0)
        self.assertIn("preparados para revisão humana", mod.render(summary))
        document = json.loads(review_file.read_text(encoding="utf-8"))
        document["candidates"][0]["certified"] = True
        review_file.write_text(json.dumps(document), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "invalid review candidate"):
            mod.summarize(self.inventory, self.digest, self.root / "none.json",
                          review_batch_path=review_file)

    def test_stale_evidence_rejected(self):
        self.write(self.dynamic, "00000010.json",
                   {"address": "00000010", "binary_sha256": "b"*64,
                    "semantic_status": "partial"})
        with self.assertRaises(ValueError):
            mod.summarize(self.inventory, self.digest, self.root / "none.json",
                          dynamic_dir=self.dynamic)

    def test_duplicate_worker_assignments_rejected(self):
        manifest = {"elf_sha256": self.digest, "tasks": [
            {"address": "00000010", "size": 120, "binary_sha256": self.digest}]}
        self.write(self.manifests, "semantic-worker-01.json", manifest)
        self.write(self.manifests, "semantic-worker-02.json", manifest)
        with self.assertRaises(ValueError):
            mod.summarize(self.inventory, self.digest, self.root / "none.json",
                          manifests_dir=self.manifests)


if __name__ == "__main__":
    unittest.main()
