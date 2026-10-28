"""Fail PR CI if the workflow acquires duplicated YAML job blocks."""
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
WORKFLOW = ROOT / ".github/workflows/re-pipeline.yml"


class RePipelineIntegrityTests(unittest.TestCase):
    def test_exactly_one_pipeline_job_of_each_type(self):
        source = WORKFLOW.read_text(encoding="utf-8")
        self.assertEqual(len(re.findall(r"(?m)^jobs:$", source)), 1)
        for job in ("unit-tests", "structural-smoke"):
            self.assertEqual(len(re.findall(r"(?m)^  " + job + r":$", source)), 1,
                             f"Duplicated or missing {job} job")
        self.assertEqual(source.count("      - name: Validate roadmap tracker"), 1)
        self.assertEqual(source.count("      - name: Validate central project dashboard"), 1)

    def test_roadmap_may_grow_without_breaking_CI(self):
        source = WORKFLOW.read_text(encoding="utf-8")
        self.assertNotIn("RE_COMPLETION_TRACKER_TASKS=16", source)
        self.assertIn("RE_COMPLETION_TRACKER_TASKS=//p", source)
        self.assertIn("RE_COMPLETION_TRACKER_VALID=1", source)

    def test_pipeline_is_not_wholesale_repeated(self):
        source = WORKFLOW.read_text(encoding="utf-8")
        # Historical breakage duplicated almost every job and ~20k characters.
        self.assertLess(source.count("      - uses: actions/checkout@v4"), 6)
        self.assertEqual(source.count("name: Reverse engineering pipeline"), 1)


if __name__ == "__main__":
    unittest.main()
