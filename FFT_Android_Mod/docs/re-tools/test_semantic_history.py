"""The history panel must retain old work but never turn it into certification."""
import importlib.util
import tempfile
import unittest
from pathlib import Path

spec = importlib.util.spec_from_file_location(
    "semantic_history", Path(__file__).with_name("semantic_history.py"))
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


class HistoryTests(unittest.TestCase):
    def test_valid_digest_and_sample_claims(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            digest = "a" * 64
            (folder / "SEMANTIC_EXEC.md").write_text(
                f"# Original tested contract\nELF SHA-256: `{digest}`\n"
                "**Microexecutions: 8/8 PASS.**\n")
            (folder / "SEMANTIC_AUDIT.md").write_text(
                f"# Audit\nELF SHA-256: `{digest}`\n")
            (folder / "SEMANTIC_STALE.md").write_text(
                f"# Stale\nELF SHA-256: `{'b'*64}`\n")
            (folder / "SEMANTIC_UNBOUND.md").write_text("# Unbound\n")
            (folder / "SEMANTIC_HISTORY_INDEX.md").write_text(
                f"ELF SHA-256: `{digest}`\n")
            records, stale = mod.discover(folder, digest)
            self.assertEqual((len(records), stale), (2, 1))
            self.assertEqual(sum(x["kind"] == "microexecution_report"
                                 for x in records), 1)
            report = mod.render(records, stale, digest)
            self.assertIn("Original tested contract", report)
            self.assertIn("não são somadas", report)
            self.assertNotIn("SEMANTIC_STALE.md", report)
            self.assertNotIn("SEMANTIC_UNBOUND.md", report)


if __name__ == "__main__":
    unittest.main()
