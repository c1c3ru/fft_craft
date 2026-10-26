"""Tests for deterministic, read-only review sharding."""
import csv
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

spec = importlib.util.spec_from_file_location(
    "review_shards", Path(__file__).with_name("review_shards.py")
)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


class ReviewShardsTests(unittest.TestCase):
    def test_balanced_unique_deterministic(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            queue = root / "queue.csv"
            rows = [
                ("00000010", 100), ("00000020", 80),
                ("00000030", 70), ("00000040", 60),
                ("00000050", 50),
            ]
            with queue.open("w", newline="") as handle:
                writer = csv.DictWriter(handle, fieldnames=["address", "name"])
                writer.writeheader()
                for address, size in rows + [rows[0]]:
                    writer.writerow({"address": address, "name": address})
                    (root / (address + ".json")).write_text(json.dumps({
                        "address": address, "status": "needs_review",
                        "size": size, "binary_sha256": "a" * 64,
                    }))
            shards = mod.build_shards(queue, root, 3, 5)
            self.assertEqual(shards, mod.build_shards(queue, root, 3, 5))
            assigned = [task["address"] for shard in shards for task in shard]
            self.assertEqual(len(assigned), len(set(assigned)))
            self.assertEqual(set(assigned), {a for a, _ in rows})
            self.assertEqual(sorted(map(lambda s: sum(t["size"] for t in s), shards)),
                             [100, 110, 150])
            self.assertEqual(sum(map(len, mod.build_shards(queue, root, 5, 2))), 2)

    def test_rejects_stale_checkpoint(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "queue.csv").write_text("address,name\n00000010,target\n")
            (root / "00000010.json").write_text(json.dumps({
                "address": "00000010", "status": "auto_structural",
                "size": 10, "binary_sha256": "a" * 64,
            }))
            with self.assertRaises(ValueError):
                mod.build_shards(root / "queue.csv", root, 2, 1)


if __name__ == "__main__":
    unittest.main()
