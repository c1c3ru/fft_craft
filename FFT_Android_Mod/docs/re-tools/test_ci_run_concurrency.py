"""Guard against redundant PR CI and accidental main batch cancellation."""
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
WORKFLOWS = ROOT / ".github" / "workflows"
PR_WORKFLOWS = (
    "re-pipeline.yml",
    "re-semantic-queue.yml",
    "re-semantic-real-elf-250.yml",
)

class CiConcurrencyTests(unittest.TestCase):
    def test_old_pr_revisions_are_cancelled_per_workflow_only(self):
        for name in PR_WORKFLOWS:
            with self.subTest(workflow=name):
                source = (WORKFLOWS / name).read_text(encoding="utf-8")
                self.assertIn("pull_request:", source)
                self.assertEqual(source.count("\nconcurrency:\n"), 1)
                self.assertIn(
                    "group: ${{ github.workflow }}-${{ github.event.pull_request.number || github.ref }}",
                    source)
                self.assertIn(
                    "cancel-in-progress: ${{ github.event_name == 'pull_request' }}",
                    source)
                self.assertIn("workflow_dispatch:", source)

    def test_main_batch_processing_must_not_be_cancelled(self):
        source = (WORKFLOWS / "re-batches.yml").read_text(encoding="utf-8")
        self.assertIn("group: re-automated-batches", source)
        self.assertIn("cancel-in-progress: false", source)

if __name__ == "__main__":
    unittest.main()
