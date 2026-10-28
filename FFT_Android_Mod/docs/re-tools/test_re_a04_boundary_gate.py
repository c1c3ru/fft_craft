"""Regression tests for fail-closed A04 tracker consistency."""
import copy
import json
import unittest
from pathlib import Path

import re_a04_boundary_gate as gate


class A04BoundaryGateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.state = json.loads(gate.TRACKER.read_text(encoding="utf-8"))

    def test_repository_tracker_still_has_unresolved_contracts(self):
        result = gate.audit(self.state)
        self.assertEqual(result["status"], "in_progress")
        self.assertEqual(result["semantic_certificates_created"], 0)
        self.assertEqual(len(result["bl_pairs"]), 2)

    def test_disallows_premature_completion(self):
        state = copy.deepcopy(self.state)
        next(t for t in state["tasks"] if t["id"] == "A04")["status"] = "done"
        with self.assertRaisesRegex(ValueError, "in_progress"):
            gate.audit(state)

    def test_detects_lost_boundary(self):
        state = copy.deepcopy(self.state)
        task = next(t for t in state["tasks"] if t["id"] == "A04")
        task["next_action"] = task["next_action"].replace("0x002b1bb8", "fallthrough")
        with self.assertRaisesRegex(ValueError, "0x002b1bb8"):
            gate.audit(state)

    def test_detects_changed_elf(self):
        state = copy.deepcopy(self.state)
        state["elf_sha256"] = "0" * 64
        with self.assertRaisesRegex(ValueError, "baseline"):
            gate.audit(state)

    def test_detects_duplicated_task(self):
        state = copy.deepcopy(self.state)
        state["tasks"].append(copy.deepcopy(next(t for t in state["tasks"] if t["id"] == "A04")))
        with self.assertRaisesRegex(ValueError, "exactly once"):
            gate.audit(state)


if __name__ == "__main__":
    unittest.main()
