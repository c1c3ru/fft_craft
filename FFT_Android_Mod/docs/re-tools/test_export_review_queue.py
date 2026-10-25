"""Tests for core-first review worklist classification."""
import importlib.util
import unittest
from pathlib import Path

p = Path(__file__).with_name("export_review_queue.py")
spec = importlib.util.spec_from_file_location("export_review_queue", p)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class ReviewQueueTests(unittest.TestCase):
    def test_checkpoint_path_is_portable(self):
        import csv
        import json
        import tempfile
        from unittest.mock import patch
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            inv = root / "inventory.csv"
            inv.write_text("address,size,mangled,demangled,status,section_ref\n"
                           "00000010,8,a,example(),unread,\n")
            core = root / "core.csv"
            core.write_text("address\n00000010\n")
            binary = root / "bin.so"
            binary.write_bytes(b"sample")
            import hashlib
            results = root / "results"
            results.mkdir()
            (results / "00000010.json").write_text(json.dumps({
                "address": "00000010", "size": 8,
                "status": "needs_review", "pipeline_version": 2,
                "binary_sha256": hashlib.sha256(b"sample").hexdigest(),
                "coverage_pct": 90
            }))
            rows = module.build(inv, core, results, binary)
            self.assertEqual(rows[0]["checkpoint_path"],
                             "FFT_Android_Mod/docs/re-results/00000010.json")

    def test_unresolved_table_takes_precedence(self):
        self.assertEqual(module.classify({"tables_unresolved": 1, "coverage_pct": 10}),
                         "unresolved_jump_table")

    def test_resolved_table_still_requires_review(self):
        self.assertEqual(module.classify({"tables_resolved": 1, "coverage_pct": 99}),
                         "resolved_jump_table_check")

    def test_low_coverage(self):
        self.assertEqual(module.classify({"coverage_pct": 94.9}), "coverage_below_95")

    def test_high_coverage_stays_manual(self):
        self.assertEqual(module.classify({"coverage_pct": 100}),
                         "indirect_flow_or_manual_check")


if __name__ == "__main__":
    unittest.main()
