"""Regression: semantic snapshot must not enter structural checkpoint accounting."""
import json
import tempfile
import unittest
from pathlib import Path

import checkpoint_files as cp
import structural_v3_report as v3


class CheckpointFileTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)

    def write(self, name, value):
        (self.root / name).write_text(json.dumps(value), encoding="utf-8")

    def test_only_eight_hex_digit_checkpoint_names(self):
        self.write("00244200.json", {"address": "00244200", "status": "needs_review"})
        self.write("00244204.json", {"address": "00244204", "status": "auto_structural"})
        self.write("SEMANTIC_RUN_SNAPSHOT.json",
                   {"elf_sha256": "a"*64, "schema": 1, "metrics": {}})
        self.write("semantic-certificates.json", {"00244200": {"status": "partial"}})
        self.write("other.json", {"status": "error"})
        self.assertEqual(len(cp.checkpoint_paths(self.root)), 2)
        count, statuses = cp.summarize(self.root)
        self.assertEqual(count, 2)
        self.assertEqual(statuses["needs_review"], 1)
        self.assertEqual(statuses["auto_structural"], 1)

    def test_v3_report_never_counts_snapshot_as_legacy_checkpoint(self):
        self.write("00244200.json", {"address": "00244200",
                                    "status": "needs_review"})
        self.write("00244204.json", {"address": "00244204",
                                    "status": "auto_structural",
                                    "structural_version": 3})
        self.write("SEMANTIC_RUN_SNAPSHOT.json",
                   {"schema": 1, "elf_sha256": "a"*64})
        report = v3.render(self.root)
        self.assertIn("v3 checkpoints | 1", report)
        self.assertIn("Legacy checkpoint records unchanged | 1", report)

    def test_checkpoint_errors_and_address_mismatch_remain_fatal(self):
        self.write("00244200.json", {"address": "00244200", "status": "error"})
        with self.assertRaisesRegex(ValueError, "Errors in checkpoints"):
            cp.summarize(self.root)
        self.write("00244200.json", {"address": "deadbeef", "status": "needs_review"})
        with self.assertRaisesRegex(ValueError, "checkpoint address mismatch"):
            cp.summarize(self.root)
        self.write("00244200.json", {"address": "00244200"})
        with self.assertRaisesRegex(ValueError, "invalid checkpoint metadata"):
            cp.summarize(self.root)


if __name__ == "__main__":
    unittest.main()
