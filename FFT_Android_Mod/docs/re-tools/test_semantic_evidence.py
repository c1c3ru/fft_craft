"""Regression tests for ARM evidence, not semantic verification."""
import importlib.util
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
spec = importlib.util.spec_from_file_location("semantic_evidence", HERE / "semantic_evidence.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class EvidenceTests(unittest.TestCase):
    def test_reachability_and_possible_memory_write(self):
        # mov r0, #1; str r0, [sp]; bx lr; trailing literal word
        data = bytes.fromhex("0100a0e3 00008de5 1eff2fe1 78563412")
        found, tables, unresolved = module.collect(data, 0x1000)
        self.assertIn(0x1000, found)
        self.assertIn(0x1004, found)
        self.assertIn(0x1008, found)
        self.assertNotIn(0x100c, found)
        self.assertFalse(tables)
        self.assertFalse(unresolved)
        report = module.evidence({
            "address": "00001000", "name": "synthetic()",
            "status": "needs_review",
        }, data)
        self.assertIn("str r0, [sp]", report)
        self.assertIn("0x100c", report)
        self.assertIn("No semantic equivalence is proved", report)

    def test_reject_unaligned_arm_ranges(self):
        with self.assertRaisesRegex(ValueError, "multiples of four"):
            module.read_function(Path("/nonexistent"), 0x1001, 8)
        with self.assertRaisesRegex(ValueError, "multiples of four"):
            module.read_function(Path("/nonexistent"), 0x1000, 7)

    def test_markdown_contains_real_newlines(self):
        spec = importlib.util.spec_from_file_location(
            "export_review_queue", HERE / "export_review_queue.py")
        other = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(other)
        report = other.render_triage([])
        self.assertIn("# ARM semantic review triage\\n\\n", report)
        self.assertNotIn("\\\\n", report)


if __name__ == "__main__":
    unittest.main()
