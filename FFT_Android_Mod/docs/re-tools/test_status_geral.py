"""Central status report must never equate ARM coverage and semantic proof."""
import json
import tempfile
import unittest
from pathlib import Path

import status_geral as status


SHA = "a" * 64


def metrics(**overrides):
    data = {
        "digest": SHA, "rows": 6455, "checkpoints": 3002,
        "accepted_count": 2913, "review_count": 89,
        "pending_count": 0, "core_review": 73,
        "core_checkpointed": 2345, "historical_count": 5932,
    }
    data.update(overrides)
    return data


class StatusGeralTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.results = Path(self.temp.name)
        (self.results / "SEMANTIC_EVIDENCE_INDEX.md").write_text(
            f"ELF SHA-256: `{SHA}`\nEvidence collected: **89/89** pending functions.\n",
            encoding="utf-8")
        (self.results / "SEMANTIC_SOUND_ICON_MICROEXEC.md").write_text(
            "Sound dispatcher microexecutions: 10/10 PASS.", encoding="utf-8")
        (self.results / "REVIEW_QUEUE.csv").write_text(
            "address,name,coverage_pct,review_reason\n"
            "0025a228,houkoku_okng(CTLINFO*),93.7,coverage_below_95\n",
            encoding="utf-8")
        for name, value in (("00001000", {
            "address": "00001000", "binary_sha256": SHA,
            "pipeline_version": 2, "status": "auto_structural",
            "structural_version": 3}),
            ("00001004", {
                "address": "00001004", "binary_sha256": SHA,
                "pipeline_version": 2, "status": "needs_review",
                "structural_version": 3}),
            ("00001008", {
                "address": "00001008", "binary_sha256": "f" * 64,
                "pipeline_version": 2, "status": "auto_structural",
                "structural_version": 3})):
            (self.results / f"{name}.json").write_text(json.dumps(value))

    def tearDown(self):
        self.temp.cleanup()

    def test_structural_percent_is_not_semantic_percent(self):
        report = status.render(metrics(), self.results)
        self.assertIn("2,913", report)
        self.assertIn("**97.0%**", report)
        self.assertIn("89", report)
        self.assertIn("não mensurado", report)
        self.assertIn("Não somamos esses conjuntos", report)
        self.assertIn("89/89 relatórios estáticos", report)
        self.assertIn("0025a228", report)

    def test_v3_only_accepts_same_binary_records(self):
        counts = status.current_v3(self.results, SHA)
        self.assertEqual(counts["v3"], 2)
        self.assertEqual(counts["auto_structural"], 1)
        self.assertEqual(counts["needs_review"], 1)

    def test_stale_evidence_is_flagged(self):
        report = status.render(metrics(review_count=88), self.results)
        self.assertIn("desatualizado perante 88", report)
        (self.results / "SEMANTIC_EVIDENCE_INDEX.md").write_text(
            "ELF SHA-256: `" + ("b" * 64) +
            "`\nEvidence collected: **89/89** pending functions.\n")
        self.assertIn("outro binário", status.render(metrics(), self.results))

    def test_only_github_merged_prs_are_displayed(self):
        pull_metadata = [
            {"number": 291, "title": "Análise ARM", "merged_at": "2026-10-25T23:20:00Z"},
            {"number": 293, "title": "Relatório", "merged_at": "2026-10-25T23:30:00Z"},
            {"number": 299, "title": "Ainda aberto", "merged_at": None},
        ]
        report = status.render(metrics(), self.results, pull_metadata)
        self.assertIn("PR #293", report)
        self.assertIn("PR #291", report)
        self.assertNotIn("PR #299", report)
        self.assertLess(report.index("PR #293"), report.index("PR #291"))
        self.assertIn("/pull/293", report)
        self.assertIn("Metadados dos PRs", status.render(metrics(), self.results))

    def test_impossible_checkpoint_count_is_error(self):
        with self.assertRaisesRegex(ValueError, "status accounting"):
            status.render(metrics(review_count=100), self.results)

    def test_optional_metrics_source_is_robust(self):
        self.assertEqual(status.percent(0, 0), "não mensurável")
        self.assertEqual(status.percent(2913, 3002), "97.0%")


if __name__ == "__main__":
    unittest.main()
