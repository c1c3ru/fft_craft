"""Regression tests for review-queue consistency during structural-v3 migration."""
import csv
import json
import tempfile
import unittest
from pathlib import Path

import semantic_path_report


class StaleReviewQueueTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.results = Path(self.temp.name)
        rows = [
            {"address": "00001000", "name": "promoted()", "size": "12"},
            {"address": "0000100c", "name": "pending_a()", "size": "12"},
            {"address": "00001018", "name": "pending_b()", "size": "12"},
        ]
        with (self.results / "REVIEW_QUEUE.csv").open("w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=rows[0])
            w.writeheader()
            w.writerows(rows)
        for row in rows:
            record = {
                "address": row["address"],
                "size": int(row["size"]),
                "status": "needs_review",
                "binary_sha256": "digest",
                "pipeline_version": 2,
            }
            (self.results / f'{row["address"]}.json').write_text(
                json.dumps(record), encoding="utf-8")

    def tearDown(self):
        self.temp.cleanup()

    def set_status(self, address, status):
        p = self.results / f"{address}.json"
        data = json.loads(p.read_text())
        data["status"] = status
        p.write_text(json.dumps(data))

    def test_promoted_checkpoint_is_skipped_and_limit_refilled(self):
        self.set_status("00001000", "auto_structural")
        selected = semantic_path_report.active_review_rows(
            self.results, "digest", 2)
        self.assertEqual([row["address"] for row, _ in selected],
                         ["0000100c", "00001018"])

    def test_stale_or_unknown_status_still_fails(self):
        self.set_status("00001000", "error")
        with self.assertRaisesRegex(ValueError, "Invalid review status"):
            semantic_path_report.active_review_rows(self.results, "digest", 2)

    def test_mismatched_binary_is_not_silently_skipped(self):
        self.set_status("00001000", "auto_structural")
        with self.assertRaisesRegex(ValueError, "Invalid review checkpoint"):
            semantic_path_report.active_review_rows(self.results, "other", 2)

    def test_same_binary_promotion_does_not_skip_corrupt_size(self):
        self.set_status("00001000", "auto_structural")
        p = self.results / "00001000.json"
        record = json.loads(p.read_text())
        record["size"] = 16
        p.write_text(json.dumps(record))
        with self.assertRaisesRegex(ValueError, "Invalid review checkpoint"):
            semantic_path_report.active_review_rows(self.results, "digest", 2)


if __name__ == "__main__":
    unittest.main()
