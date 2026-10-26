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
