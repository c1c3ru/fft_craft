"""Test semantic task partitioning without claiming equivalence."""
import importlib.util
import unittest
from pathlib import Path

spec = importlib.util.spec_from_file_location(
    "semantic_work_queue", Path(__file__).with_name("semantic_work_queue.py"))
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class SemanticWorkQueueTests(unittest.TestCase):
    def setUp(self):
        self.rows = [
            {"address": f"{n:08x}", "size": size, "name": f"f{n}",
             "semantic_status": status}
            for n, size, status in (
                (1, 200, "unknown"), (2, 150, "certified"),
                (3, 120, "partial"), (4, 80, "unknown"),
                (5, 40, "unknown"))
        ]

    def test_partition_excludes_certified_and_no_duplicates(self):
        shards = module.partition(self.rows, "a" * 64, 3, 10)
        tasks = [task for shard in shards for task in shard]
        self.assertEqual(len(tasks), 4)
        self.assertEqual({x["address"] for x in tasks},
                         {"00000001", "00000003", "00000004", "00000005"})
        self.assertTrue(all(t["binary_sha256"] == "a" * 64 for t in tasks))
        self.assertTrue(all("unresolved_paths" in t["required_evidence"] for t in tasks))
        self.assertEqual(shards, module.partition(self.rows, "a" * 64, 3, 10))

    def test_prioritize_existing_leaf_proof_candidates(self):
        shards = module.partition(self.rows, "a"*64, 2, 2,
                                  priority_addresses={"00000005", "00000004"})
        tasks = [task["address"] for shard in shards for task in shard]
        self.assertEqual(set(tasks), {"00000005", "00000004"})
        # Without a candidate, re-use partial evidence before unknown entries.
        plain = module.partition(self.rows, "a"*64, 2, 1)
        self.assertEqual(
            [t["address"] for group in plain for t in group], ["00000003"])

    def test_limit_and_bad_workers(self):
        self.assertEqual(sum(map(len, module.partition(self.rows, "a"*64, 2, 2))), 2)
        for workers, limit in ((0, 2), (33, 2), (3, 0)):
            with self.assertRaises(ValueError):
                module.partition(self.rows, "a"*64, workers, limit)


if __name__ == "__main__":
    unittest.main()
