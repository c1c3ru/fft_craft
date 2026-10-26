"""Fail-fast regression checks for all three reverse-engineering workflows.

Prevents CI trigger gaps when new RE tool files are introduced, and keeps a
single complete regression entry point. Uses only Python's standard library.
"""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3] / ".github" / "workflows"
WORKFLOWS = {
    "pipeline": ROOT / "re-pipeline.yml",
    "semantic": ROOT / "re-semantic-queue.yml",
    "batches": ROOT / "re-batches.yml",
}
TOOLS = "FFT_Android_Mod/docs/re-tools/**"
LEDGER = "FFT_Android_Mod/docs/re-results/semantic-certificates.json"
INVENTORY = "FFT_Android_Mod/docs/RE_FUNCTION_INVENTORY.csv"
ELF = "FFT_Android_Mod/src/lib/armeabi/libgl2jni.so"
COMMAND = "python3 -m unittest discover -s FFT_Android_Mod/docs/re-tools -p 'test_*.py' -v"
SYNTAX = "python3 -m compileall -q FFT_Android_Mod/docs/re-tools"


def event_paths(content, event):
    """Extract a workflow event's paths block, not unrelated job steps."""
    header = re.search(r"(?m)^  " + re.escape(event) + r":\s*$", content)
    if not header:
        raise AssertionError(f"missing event {event}")
    later = re.search(r"(?m)^  [a-z][a-z_-]*:\s*(?:$|\[)",
                      content[header.end():])
    section = content[header.end():header.end() + later.start()] if later else content[header.end():]
    paths = re.search(r"(?m)^    paths:\s*$", section)
    if not paths:
        raise AssertionError(f"missing {event}.paths")
    values = re.findall(r"(?m)^      - '([^']+)'\s*$", section[paths.end():])
    if len(values) != len(set(values)):
        raise AssertionError(f"duplicate paths in {event}")
    return set(values)


class CIWorkflowIntegrity(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.workflows = {name: path.read_text(encoding="utf-8")
                         for name, path in WORKFLOWS.items()}

    def test_all_tool_changes_trigger_all_relevant_checks(self):
        for name in ("pipeline", "semantic"):
            paths = event_paths(self.workflows[name], "pull_request")
            with self.subTest(workflow=name):
                self.assertTrue(
                    {TOOLS, LEDGER, INVENTORY, ELF}.issubset(paths),
                    paths)
        batch_paths = event_paths(self.workflows["batches"], "push")
        self.assertTrue({TOOLS, LEDGER, INVENTORY, ELF}.issubset(batch_paths))

    def test_workflow_changes_trigger_regression_ci(self):
        pipeline = event_paths(self.workflows["pipeline"], "pull_request")
        semantic = event_paths(self.workflows["semantic"], "pull_request")
        self.assertIn(".github/workflows/re-pipeline.yml", pipeline)
        self.assertIn(".github/workflows/re-batches.yml", pipeline)
        self.assertIn(".github/workflows/re-semantic-queue.yml", pipeline)
        self.assertIn(".github/workflows/re-semantic-queue.yml", semantic)
        self.assertIn(".github/workflows/re-batches.yml",
                      event_paths(self.workflows["batches"], "push"))

    def test_every_workflow_compiles_all_scripts_and_tests_full_suite(self):
        for name, content in self.workflows.items():
            with self.subTest(workflow=name):
                self.assertIn(COMMAND, content)
                self.assertIn(SYNTAX, content)
                self.assertLess(content.index(SYNTAX), content.index(COMMAND))
                self.assertLess(content.index(COMMAND),
                                content.index("semantic_certificate_gate.py")
                                if name == "batches"
                                else content.index("python3 FFT_Android_Mod/docs/re-tools/semantic_certificate_gate.py")
                                if name == "semantic"
                                else content.index("      - name: Structural batch"))

    def test_batch_keeps_no_recursion_on_generated_snapshots(self):
        source = self.workflows["batches"]
        triggers = event_paths(source, "push")
        self.assertNotIn("FFT_Android_Mod/docs/re-results/**", triggers)
        self.assertNotIn("FFT_Android_Mod/docs/re-results/*.json", triggers)
        self.assertIn("  workflow_dispatch:", source)
        self.assertIn("  schedule:", source)
        self.assertLess(source.index("semantic_run_snapshot.py"),
                        source.index("- name: Update central FFT Craft dashboard"))
        self.assertIn("checkpoint_files.py --verify", source)

    def test_semantic_generation_uses_original_elf_and_same_run_contracts(self):
        source = self.workflows["semantic"]
        stages = (
            "semantic_dynamic_evidence.py",
            "semantic_bxlr_contract_pilot.py",
            "semantic_bxlr_review_batch.py",
            "semantic_run_snapshot.py",
            "status_geral.py",
        )
        points = [source.index(f"python3 FFT_Android_Mod/docs/re-tools/{step}")
                  for step in stages]
        self.assertEqual(points, sorted(points))
        self.assertIn("--contracts-dir /tmp/fft-semantic/contract-pilot", source)
        self.assertIn("SEMANTIC_BXLR_REVIEW_BATCH.json", source)


if __name__ == "__main__":
    unittest.main()
