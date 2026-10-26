"""Bounded machine evidence must never be upgraded to full certification."""
import importlib.util
import unittest
from pathlib import Path

spec = importlib.util.spec_from_file_location(
    "semantic_dynamic_evidence",
    Path(__file__).with_name("semantic_dynamic_evidence.py"),
)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


class DynamicEvidenceTests(unittest.TestCase):
    def test_accepted_report_remains_partial(self):
        digest = "a" * 64
        report = "\n".join([
            f"ELF SHA-256: `{digest}`",
            mod.TOTAL_MARKER,
            *(case[3] for case in mod.CASES),
        ])
        rows = mod.verified_records(report, digest)
        self.assertEqual(len(rows), 2)
        self.assertEqual(sum(r["machine_samples_passed"] for r in rows), 96)
        self.assertTrue(all(r["semantic_status"] == "partial"
                            and r["certified"] is False
                            and r["unverified"] for r in rows))

    def test_callee_evidence_is_partial_and_not_double_counted(self):
        digest = "a" * 64
        report = f"ELF SHA-256: `{digest}`\\n{mod.CALLEE_MARKER}"
        rows = mod.verified_callee_records(report, digest)
        self.assertEqual(len(rows), 4)
        self.assertEqual(len({r["address"] for r in rows}), 4)
        self.assertTrue(all(r["certified"] is False and
                            r["semantic_status"] == "partial" for r in rows))
        self.assertTrue(all(r["suite_samples_passed"] == 72 for r in rows))
        self.assertTrue(all("do not sum" in r["suite_sample_count_scope"]
                            for r in rows))

    def test_callee_wrong_binary_rejected(self):
        with self.assertRaises(ValueError):
            mod.verified_callee_records(
                f"ELF SHA-256: `{'b'*64}`\\n{mod.CALLEE_MARKER}", "a"*64)

    def test_missing_machine_test_count_fails_closed(self):
        digest = "a" * 64
        with self.assertRaises(ValueError):
            mod.verified_records(f"ELF SHA-256: `{digest}`", digest)

    def test_wrong_binary_fails_closed(self):
        digest = "a" * 64
        report = "\n".join([
            f"ELF SHA-256: `{'b'*64}`",
            mod.TOTAL_MARKER,
            *(case[3] for case in mod.CASES),
        ])
        with self.assertRaises(ValueError):
            mod.verified_records(report, digest)

    def test_missing_individual_suite_fails_closed(self):
        digest = "a" * 64
        report = f"ELF SHA-256: `{digest}`\n{mod.TOTAL_MARKER}\n{mod.CASES[0][3]}"
        with self.assertRaises(ValueError):
            mod.verified_records(report, digest)


if __name__ == "__main__":
    unittest.main()
