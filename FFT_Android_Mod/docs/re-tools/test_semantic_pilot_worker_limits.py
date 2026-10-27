"""Regression for manifest count > Unicorn/static worker thread cap.

Tests execution orchestration only; fake inspect_task avoids claiming ARM
evidence from synthetic fixtures. No semantic certificates are generated.
"""
import contextlib
import hashlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import semantic_pilot as pilot


class SemanticPilotManyManifestsTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.binary = self.root / "test.elf"
        self.binary.write_bytes(b"fixture, not original ARM ELF")
        self.digest = hashlib.sha256(self.binary.read_bytes()).hexdigest()
        self.manifests = self.root / "manifests"
        self.manifests.mkdir()
        for shard in range(1, 26):
            rows = []
            for task in range(10):
                address = f"{0x1000 + ((shard - 1) * 10 + task) * 4:08x}"
                rows.append({"address": address, "size": 4, "name": "fixture",
                             "binary_sha256": self.digest})
            (self.manifests / f"semantic-worker-{shard:02d}.json").write_text(
                json.dumps({"elf_sha256": self.digest, "tasks": rows}))
        self.output = self.root / "output"

    def run_main(self, workers):
        argv = ["semantic_pilot.py", "--binary", str(self.binary),
                "--manifests", str(self.manifests), "--output",
                str(self.output), "--workers", str(workers)]
        observed = []
        original_pool = pilot.futures.ThreadPoolExecutor

        def audited_pool(*args, **kwargs):
            observed.append(kwargs.get("max_workers"))
            return original_pool(*args, **kwargs)

        def fake_inspect(task, binary, digest):
            if digest != self.digest or task["binary_sha256"] != digest:
                raise ValueError("wrong ELF binding")
            return {"address": task["address"], "semantic_status": "partial",
                    "binary_sha256": digest, "evidence_class": "fixture_only"}

        stream = io.StringIO()
        with (mock.patch.object(sys, "argv", argv),
              mock.patch.object(pilot.futures, "ThreadPoolExecutor",
                                side_effect=audited_pool),
              mock.patch.object(pilot, "inspect_task",
                                side_effect=fake_inspect),
              contextlib.redirect_stdout(stream)):
            pilot.main()
        return observed, stream.getvalue()

    def test_25_manifests_250_tasks_use_at_most_16_threads(self):
        observed, output = self.run_main(25)
        self.assertEqual(observed, [16])
        self.assertIn("PILOT_MANIFEST_SHARDS=25", output)
        self.assertIn("PILOT_CONCURRENT_THREADS=16", output)
        self.assertIn("PILOT_PARTIAL=250", output)
        self.assertIn("PILOT_FAILED=0", output)
        results = list(self.output.glob("*.json"))
        self.assertEqual(len(results), 250)
        self.assertEqual(len(set(p.stem for p in results)), 250)

    def test_5_manifests_cannot_overparallelize(self):
        observed, _ = self.run_main(5)
        self.assertEqual(observed, [5])
        self.assertEqual(len(list(self.output.glob("*.json"))), 250)

    def test_workers_outside_range_are_rejected(self):
        for value in (0, 33):
            with self.subTest(value=value), self.assertRaises(SystemExit) as exc:
                self.run_main(value)
            self.assertEqual(exc.exception.code, 2)


if __name__ == "__main__":
    unittest.main()
