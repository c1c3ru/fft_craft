"""Four-lane automation rejects absent proofs and never promotes certificates."""
import copy
import json
import tempfile
import unittest
from pathlib import Path

import re_four_track_automation as a


def sample(lane):
    if lane == "t06_t12":
        return {
            "original_elf_sha256": a.SHA, "wrapper_slices_tested": 2,
            "differential_scenarios_passed": 7, "new_semantic_certificates": 0,
            "new_structural_approvals": 0, "real_external_callees_untested": True,
            "T06_done": False, "wrappers": [
                {"scenarios": [{}] * 3, "unattributed_trailing_symbol_bytes": 0},
                {"scenarios": [{}] * 4, "unattributed_trailing_symbol_bytes": 12},
            ],
        }
    if lane == "b01":
        return {"elf_sha256": a.SHA, "unique_methods": 7,
                "original_elf_vs_named_cpp_differentials": 672,
                "new_semantic_certificates": 0, "B01_done": False,
                "cpp_class_layout_proven": False,
                "whole_program_call_context_proven": False,
                "entries": [{} for _ in range(7)]}
    if lane == "a04":
        return {"A04_JNI_HOST_CASES": 271,
                "A04_JNI_MODIFIED_UTF8_CONFIRMED": 1,
                "A04_JNI_REAL_ANDROID_PATH_SAMPLES": 0}
    if lane == "t14_t26":
        return {"format": "t14_t26_unittest_v1",
                "test_modules_count": 29, "tasks_with_tests": a.TASKS,
                "tests_run": 45, "tests_passed": True,
                "errors": 0, "failures": 0,
                "native_stage_ctest_passed": True}
    raise ValueError(lane)


class FourTrackTests(unittest.TestCase):
    def test_all_lanes_keep_unverified_flags(self):
        for name in a.LANES:
            with self.subTest(lane=name):
                item = a.evaluate(name, sample(name), 303)
                self.assertEqual(a.verify_lane(item), name)
                self.assertEqual(item["new_semantic_certificates"], 0)
                self.assertFalse(item["full_equivalence_proven"])
                self.assertFalse(item["task_states_changed"])
                self.assertFalse(item["original_android_app_verified"])

    def test_missing_or_different_original_elf_identity_is_rejected(self):
        for name in ("t06_t12", "b01"):
            x = sample(name)
            x["original_elf_sha256" if name == "t06_t12" else "elf_sha256"] = "0" * 64
            with self.assertRaisesRegex(ValueError, "Proof gate"):
                a.evaluate(name, x, 303)

    def test_missing_t06_scenarios_and_unattributed_tail(self):
        x = sample("t06_t12")
        x["wrappers"][1]["scenarios"] = [{}]
        with self.assertRaisesRegex(ValueError, "truncated"):
            a.evaluate("t06_t12", x, 303)
        x = sample("t06_t12")
        x["wrappers"][1]["unattributed_trailing_symbol_bytes"] = 0
        with self.assertRaisesRegex(ValueError, "unassigned"):
            a.evaluate("t06_t12", x, 303)

    def test_b01_missing_function_and_unearned_certificate(self):
        x = sample("b01")
        x["entries"] = [{}] * 6
        with self.assertRaisesRegex(ValueError, "incomplete"):
            a.evaluate("b01", x, 303)
        x = sample("b01")
        x["new_semantic_certificates"] = 1
        with self.assertRaisesRegex(ValueError, "Proof gate"):
            a.evaluate("b01", x, 303)

    def test_a04_host_log_is_not_original_game_trace(self):
        log = ("A04_JNI_HOST_CASES=271\n"
               "A04_JNI_MODIFIED_UTF8_CONFIRMED=1\n"
               "A04_JNI_REAL_ANDROID_PATH_SAMPLES=0\n")
        parsed = a.parse_a04(log)
        item = a.evaluate("a04", parsed, 303)
        self.assertEqual(item["observed"]["original_app_runtime_samples"], 0)
        self.assertFalse(item["original_android_app_verified"])

    def test_a04_fake_game_samples_rejected(self):
        x = sample("a04")
        x["A04_JNI_REAL_ANDROID_PATH_SAMPLES"] = 1
        with self.assertRaisesRegex(ValueError, "Proof gate"):
            a.evaluate("a04", x, 303)

    def test_a04_duplicate_or_untrusted_token_rejected(self):
        with self.assertRaisesRegex(ValueError, "Duplicate"):
            a.parse_a04("A04_JNI_HOST_CASES=271\nA04_JNI_HOST_CASES=271")
        with self.assertRaisesRegex(ValueError, "Invalid JNI"):
            a.parse_a04("A04_JNI_HOST_CASES=/home/user/private/path")

    def test_vertical_lost_task_or_failed_test_refused(self):
        x = sample("t14_t26")
        x["tasks_with_tests"] = a.TASKS[:-1]
        with self.assertRaisesRegex(ValueError, "incomplete"):
            a.evaluate("t14_t26", x, 303)
        x = sample("t14_t26")
        x["failures"] = 1
        with self.assertRaisesRegex(ValueError, "Proof gate"):
            a.evaluate("t14_t26", x, 303)

    def test_29_real_test_modules_exist_in_all_13_tasks(self):
        seen = []
        for n in a.TASKS:
            m = sorted(a.TOOLS.glob("test_" + n.lower() + "_*.py"))
            self.assertTrue(m, n)
            seen += m
        self.assertEqual(len(seen), 29)

    def test_combine_rejects_missing_lane(self):
        with tempfile.TemporaryDirectory() as folder:
            for name in a.LANES[:-1]:
                sub = Path(folder) / ("re-four-track-" + name)
                sub.mkdir()
                (sub / (name + ".json")).write_text(
                    json.dumps(a.evaluate(name, sample(name), 303)))
            with self.assertRaisesRegex(ValueError, "Four lane"):
                a.consolidate(folder, 303)

    def test_combine_four_with_zero_new_certificates(self):
        with tempfile.TemporaryDirectory() as folder:
            for name in a.LANES:
                sub = Path(folder) / ("re-four-track-" + name)
                sub.mkdir()
                (sub / (name + ".json")).write_text(
                    json.dumps(a.evaluate(name, sample(name), 303)))
            out = a.consolidate(folder, 303)
            self.assertEqual(out["lanes_tested"], 4)
            self.assertEqual(out["new_semantic_certificates"], 0)
            self.assertIn("host", a.markdown(out))
            self.assertFalse(out["full_app_reconstructed"])

    def test_combine_rejects_false_equivalence_and_foreign_baseline(self):
        with tempfile.TemporaryDirectory() as folder:
            for name in a.LANES:
                sub = Path(folder) / ("re-four-track-" + name)
                sub.mkdir()
                doc = a.evaluate(name, sample(name), 303)
                if name == "a04":
                    doc["full_equivalence_proven"] = True
                (sub / (name + ".json")).write_text(json.dumps(doc))
            with self.assertRaisesRegex(ValueError, "Proof gate"):
                a.consolidate(folder, 303)

    def test_verified_certificate_population_only(self):
        with tempfile.TemporaryDirectory() as folder:
            binary = Path(folder) / "original.so"
            ledger = Path(folder) / "ledger.json"
            binary.write_bytes(b"not-the-original-elf")
            ledger.write_text(json.dumps({"a": {"status": "certified"}}))
            with self.assertRaisesRegex(ValueError, "Original ELF"):
                a.source_count(binary, ledger)


if __name__ == "__main__":
    unittest.main()
