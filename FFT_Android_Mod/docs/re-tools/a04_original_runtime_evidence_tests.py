"""Host-only negative regression tests for A04 read-only runtime evidence.

Fixtures are SYNTHETIC: they are never evidence of executing the game APK/ELF.
"""
import copy
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

BASE = Path(__file__).parent
spec = importlib.util.spec_from_file_location(
    "a04_original_evidence", BASE / "a04-original-runtime-evidence.py"
)
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)


def event(event_id=0, getter="GetIntPath", outcome="present", length=242):
    present = outcome == "present"
    return {
        "event_id": event_id,
        "getter": getter,
        "outcome": outcome,
        "jni_to_r1_correlated": present,
        "pre_copy_observed": present,
        "r1_nul_termination": "verified_bounded" if present else "not_applicable",
        "jni_byte_length": length if present else None,
        "within_242_bytes": length <= 242 if present else None,
    }


def evidence(*events):
    return {
        "schema_version": 1,
        "source_kind": "authorized_original_game_observational_trace",
        "elf_sha256": validator.EXPECTED_ELF_SHA256,
        "apk_sha256": "a" * 64,
        "instrumentation_sha256": "b" * 64,
        "android_api": 29,
        "scenario": "normal_launch",
        "events": list(events) if events else [event()],
        "original_strcpy_executed": False,
        "contains_path_contents": False,
        "semantic_certificates_issued": 0,
    }


class EvidenceValidationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.schema = validator.load_json(validator.SCHEMA_FILE)

    def check(self, payload):
        return validator.validate_evidence(payload, self.schema)

    def rejects(self, payload):
        with self.assertRaises(validator.EvidenceError):
            self.check(payload)

    def test_boundary_and_reporting(self):
        data = self.check(evidence(event(1, length=242),
                                   event(2, "GetExt1Path", length=243)))
        self.assertEqual(data["total_events"], 2)
        self.assertEqual(data["jni_r1_correlated_events"], 2)
        self.assertEqual(data["observed_length_exceedances"], 1)
        self.assertEqual(data["result"], "format_validated_only")
        self.assertFalse(data["global_maximum_proven"])
        self.assertFalse(data["original_elf_semantic_equivalence_certified"])
        self.assertFalse(data["original_game_provenance_independently_attested"])
        self.assertEqual(data["semantic_certificates_issued"], 0)
        self.assertNotIn("a" * 64, json.dumps(data))
        self.assertNotIn("b" * 64, json.dumps(data))

    def test_absent_states_are_distinct(self):
        events = [event(i, outcome=o)
                  for i, o in enumerate(("null", "exception", "not_reached", "unresolved"))]
        data = self.check(evidence(*events))
        self.assertEqual(set(data["outcomes"]), {e["outcome"] for e in events})
        self.assertEqual(data["jni_r1_correlated_events"], 0)

    def test_uncorrelated_present_is_not_certified(self):
        row = event()
        row.update(jni_to_r1_correlated=False, pre_copy_observed=False,
                   r1_nul_termination="not_verified")
        data = self.check(evidence(row))
        self.assertEqual(data["bounded_nul_verified_events"], 0)
        self.assertEqual(data["jni_r1_correlated_events"], 0)

    def test_required_and_unknown_fields(self):
        item = evidence()
        del item["elf_sha256"]
        self.rejects(item)
        item = evidence()
        item["absolute_path"] = "/do-not-include-this"
        self.rejects(item)
        item = evidence()
        item["events"][0]["path_contents"] = "/private/path"
        self.rejects(item)

    def test_wrong_identity_or_hash(self):
        for key, bad in (
            ("elf_sha256", "c" * 64),
            ("apk_sha256", "bad"),
            ("instrumentation_sha256", "a" * 63 + "Z"),
            ("source_kind", "independent_diagnostic_apk"),
            ("schema_version", 2),
            ("scenario", "unverified_case"),
        ):
            with self.subTest(key=key):
                item = evidence()
                item[key] = bad
                self.rejects(item)
        with self.assertRaises(validator.EvidenceError):
            validator.validate_evidence(
                evidence(), self.schema, expected_elf="not-a-sha")

    def test_boolean_and_count_type_safety(self):
        for key, bad in (
            ("jni_byte_length", True),
            ("within_242_bytes", 1),
            ("event_id", True),
            ("pre_copy_observed", 1),
            ("jni_to_r1_correlated", "true"),
        ):
            with self.subTest(key=key):
                item = evidence()
                item["events"][0][key] = bad
                self.rejects(item)

    def test_budget_disagreement(self):
        for n, flag in ((242, False), (243, True), (0, False)):
            with self.subTest(length=n, flag=flag):
                item = evidence(event(length=n))
                item["events"][0]["within_242_bytes"] = flag
                self.rejects(item)

    def test_nonpresent_cannot_claim_effects(self):
        for field, bad in (
            ("jni_byte_length", 0),
            ("within_242_bytes", False),
            ("jni_to_r1_correlated", True),
            ("pre_copy_observed", True),
            ("r1_nul_termination", "verified_bounded"),
        ):
            with self.subTest(field=field):
                item = evidence(event(outcome="null"))
                item["events"][0][field] = bad
                self.rejects(item)

    def test_correlated_event_needs_pre_copy(self):
        item = evidence()
        item["events"][0]["pre_copy_observed"] = False
        self.rejects(item)

    def test_verified_nul_requires_correlated_r1(self):
        item = evidence()
        item["events"][0]["jni_to_r1_correlated"] = False
        self.rejects(item)

    def test_not_applicable_nul_requires_no_r1_observation(self):
        item = evidence()
        item["events"][0]["r1_nul_termination"] = "not_applicable"
        self.rejects(item)

    def test_duplicates_and_empty_events(self):
        self.rejects(evidence(event(7), event(7, "GetExt1Path")))
        item = evidence()
        item["events"] = []
        self.rejects(item)
        item = evidence()
        item["events"] = [event(i) for i in range(validator.MAX_EVENTS + 1)]
        self.rejects(item)

    def test_forbidden_claims(self):
        for key, bad in (
            ("original_strcpy_executed", True),
            ("contains_path_contents", True),
            ("semantic_certificates_issued", 1),
        ):
            with self.subTest(key=key):
                item = evidence()
                item[key] = bad
                self.rejects(item)

    def test_invalid_getter_and_api(self):
        item = evidence()
        item["events"][0]["getter"] = "GetUnsafePath"
        self.rejects(item)
        item = evidence()
        item["android_api"] = True
        self.rejects(item)

    def test_duplicate_json_object_keys_are_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "evidence.json"
            path.write_text('{"a": 1, "a": 2}', encoding="utf-8")
            with self.assertRaises(validator.EvidenceError):
                validator.load_json(path)

    def test_nonfinite_and_oversized_file_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "evidence.json"
            path.write_text('{"number": NaN}', encoding="utf-8")
            with self.assertRaises(validator.EvidenceError):
                validator.load_json(path)
            path.write_text("x" * (validator.MAX_FILE_BYTES + 1), encoding="utf-8")
            with self.assertRaises(validator.EvidenceError):
                validator.load_json(path)

    def test_cli_does_not_echo_untrusted_values(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "evidence.json"
            item = evidence()
            item["secret_path"] = "/users/sensitive/sentinel"
            path.write_text(json.dumps(item), encoding="utf-8")
            self.assertEqual(validator.main([str(path)]), 2)

    def test_schema_is_valid_2020_12(self):
        from jsonschema import Draft202012Validator
        Draft202012Validator.check_schema(self.schema)


if __name__ == "__main__":
    unittest.main()
