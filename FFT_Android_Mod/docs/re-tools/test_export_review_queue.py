"""Tests for core-first review worklist classification."""
import importlib.util
import unittest
from pathlib import Path

p = Path(__file__).with_name("export_review_queue.py")
spec = importlib.util.spec_from_file_location("export_review_queue", p)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class ReviewQueueTests(unittest.TestCase):
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
