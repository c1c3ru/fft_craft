"""Roadmap integrity and render tests: never confuse planning with ARM coverage."""
import copy
import unittest

import re_completion_tracker as roadmap

SHA = "a" * 64


def fixture():
    return {
        "schema": 1,
        "project": "Test app",
        "scope": "end_to_end_android_app",
        "elf_sha256": SHA,
        "phases": [
            {"id": f"F{i}", "title": f"Phase {i}", "exit_gate": f"Evidence gate {i}"}
            for i in range(7)
        ],
        "tasks": [
            {"id": "A01", "phase": "F0", "status": "in_progress",
             "priority": 1, "title": "Original ELF",
             "next_action": "Trace real functions", "acceptance": "CI check",
             "depends_on": [], "evidence": []},
            {"id": "B01", "phase": "F1", "status": "planned", "priority": 1,
             "title": "ARM contract", "next_action": "Extend byte loads",
             "acceptance": "Compare original and model",
             "depends_on": ["A01"], "evidence": []},
            {"id": "C01", "phase": "F1", "status": "planned", "priority": 2,
             "title": "Ready work", "next_action": "Run isolated STR",
             "acceptance": "Bounded trace",
             "depends_on": [], "evidence": []},
        ]
    }


class CompletionTrackerTests(unittest.TestCase):
    def test_validated_queue_uses_dependencies(self):
        obj = roadmap.validate(fixture(), SHA)
        result = roadmap.render(obj)
        self.assertIn("3 totais", result)
        self.assertIn("1 em andamento", result)
        self.assertIn("1 prontas para iniciar", result)
        self.assertIn("A01", result)
        self.assertIn("C01", result)
        self.assertIn("B01", result)
        self.assertIn("aguarda A01", result)
        self.assertIn("APK/OBB", result)
        self.assertIn("0 concluídas com evidência", result)

    def test_wrong_binary_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "ELF"):
            roadmap.validate(fixture(), "b" * 64)

    def test_completed_without_proof_or_dependency_is_rejected(self):
        obj = fixture()
        obj["tasks"][0]["status"] = "done"
        with self.assertRaisesRegex(ValueError, "without evidence"):
            roadmap.validate(obj, SHA)
        obj["tasks"][0]["evidence"] = ["https://github.com/example/issue/1"]
        roadmap.validate(obj, SHA)
        obj["tasks"][1]["status"] = "done"
        obj["tasks"][1]["evidence"] = ["run#11"]
        roadmap.validate(obj, SHA)
        obj["tasks"][0]["status"] = "in_progress"
        with self.assertRaisesRegex(ValueError, "before dependency"):
            roadmap.validate(obj, SHA)

    def test_cycle_duplicate_and_unknown_dependencies(self):
        obj = fixture()
        obj["tasks"][0]["depends_on"] = ["B01"]
        with self.assertRaisesRegex(ValueError, "Cyclic"):
            roadmap.validate(obj, SHA)
        obj = fixture()
        obj["tasks"][0]["depends_on"] = ["Q99"]
        with self.assertRaisesRegex(ValueError, "Unknown"):
            roadmap.validate(obj, SHA)
        obj = fixture()
        obj["tasks"].append(copy.deepcopy(obj["tasks"][0]))
        with self.assertRaisesRegex(ValueError, "Duplicate"):
            roadmap.validate(obj, SHA)

    def test_invalid_status_stage_and_scope(self):
        obj = fixture()
        obj["tasks"][0]["status"] = "certified"
        with self.assertRaisesRegex(ValueError, "status"):
            roadmap.validate(obj, SHA)
        obj = fixture()
        obj["scope"] = "only_static"
        with self.assertRaisesRegex(ValueError, "scope"):
            roadmap.validate(obj, SHA)
        obj = fixture()
        obj["phases"][1]["exit_gate"] = ""
        with self.assertRaisesRegex(ValueError, "F0-F6"):
            roadmap.validate(obj, SHA)


if __name__ == "__main__":
    unittest.main()
