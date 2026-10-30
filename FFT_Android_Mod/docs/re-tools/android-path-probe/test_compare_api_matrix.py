"""Regression fixtures for the Android JNI path matrix result aggregator."""
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

MODULE_PATH=Path(__file__).with_name("compare-api-matrix.py")
spec=importlib.util.spec_from_file_location("a04_android_matrix",MODULE_PATH)
module=importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def measurement(api, internal=61, external=81):
    def row(n):
        return {"present":n is not None,
                "jni_mutf8_byte_length":n,
                "within_242_bytes":n<=242 if n is not None else None,
                "bounded_c_model_accepted":n<=242 if n is not None else None,
                "path_contents":"sensitive-do-not-retain"}
    return {"schema":1,"android_sdk":api,"package_identity":module.PACKAGE,
            "status":"sampled_not_a_global_bound",
            "running_original_game_apk":False,
            "original_strcpy_executed":False,
            "same_package_name_as_original_game":True,
            "native_method":"JNI GetStringUTFLength",
            "native_ascii_242":242,"native_ascii_243":243,
            "bounded_c_ascii_242":1,"bounded_c_ascii_243":0,
            "bounded_c_nul_java":1,"bounded_c_emoji_one":1,
            "native_nul_utf_bytes_hex":"61c08062",
            "native_emoji_utf_bytes_hex":"f09f9880",
            "GetIntPath":row(internal),"GetExt1Path":row(external)}


class AggregationTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.root=Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def files(self, *records):
        files=[]
        for i,record in enumerate(records):
            p=self.root/f"sample{i}.json"
            p.write_text(json.dumps(record),encoding="utf-8")
            files.append(p)
        return files

    def test_three_api_samples_are_observations_not_universal_bound(self):
        data=module.consolidate(self.files(
            measurement(23,59,79),measurement(29,61,81),
            measurement(35,63,83)),[23,29,35])
        self.assertEqual(data["diagnostic_apk_path_samples"],3)
        self.assertEqual([r["android_api"] for r in data["api_observations"]],[23,29,35])
        self.assertFalse(data["global_maximum_proven"])
        self.assertFalse(data["original_game_apk_executed"])
        self.assertNotIn("sensitive-do-not-retain",json.dumps(data))

    def test_missing_external_is_not_a_validated_string(self):
        data=module.consolidate(self.files(measurement(29,61,None)),[29])
        external=data["api_observations"][0]["methods"]["GetExt1Path"]
        self.assertFalse(external["present"])
        self.assertIsNone(external["observed_within_budget"])

    def test_over_242_is_recorded_as_observed_risk_not_false_certificate(self):
        data=module.consolidate(self.files(measurement(35,243,81)),[35])
        self.assertTrue(data["observed_violation_of_layout_precondition"])
        self.assertEqual(data["api_observations"][0]["methods"]["GetIntPath"]
                         ["remaining_budget_bytes"],-1)
        self.assertFalse(data["global_maximum_proven"])

    def test_duplicate_api_is_rejected(self):
        with self.assertRaises(ValueError):
            module.consolidate(self.files(measurement(29),measurement(29)),[23,29])

    def test_unlabeled_or_inconsistent_sample_is_rejected(self):
        wrong=measurement(29)
        wrong["original_strcpy_executed"]=True
        with self.assertRaises(ValueError):
            module.consolidate(self.files(wrong),[29])
        wrong=measurement(29)
        wrong["GetIntPath"]["within_242_bytes"]=False
        with self.assertRaises(ValueError):
            module.consolidate(self.files(wrong),[29])

    def test_emulator_script_supplies_expected_sdk_to_python(self):
        source=Path(__file__).with_name("run-emulator.sh").read_text(encoding="utf-8")
        self.assertIn('python3 - "$OUT" "$EXPECTED_API" <<', source)
        self.assertIn("expected_api=sys.argv[2]", source)

    def test_missing_api_is_rejected(self):
        with self.assertRaises(ValueError):
            module.consolidate(self.files(measurement(29)),[23,29])


if __name__=="__main__":
    unittest.main()
