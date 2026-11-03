"""Offline T27/T29 inventory checks; tests never read game content."""
import tempfile
import unittest
from pathlib import Path

import t27_t29_android_inventory as inventory


class AndroidHandoffTests(unittest.TestCase):
    def test_jni_invocations_include_exact_descriptor(self):
        with tempfile.TemporaryDirectory() as folder:
            src = Path(folder) / "src"
            cls = src / "com" / "example"
            cls.mkdir(parents=True)
            (cls / "Caller.smali").write_text(
                '.class public Lcom/example/Caller;\n'
                'invoke-static {}, Lcom/square_enix/FFT_Android/GL2JNILib;->step()V\n'
                'invoke-static {v0}, Lcom/square_enix/FFT_Android/GL2JNILib;->init(I)V\n'
                'invoke-static {v0, v1}, Lcom/square_enix/FFT_Android/GL2JNILib;->init(II)V\n',
                encoding="utf-8",
            )
            methods = [
                {"class": inventory.GL_CLASS, "method": "step", "descriptor": "()V"},
                {"class": inventory.GL_CLASS, "method": "init", "descriptor": "(II)V"},
            ]
            actual = inventory.invocations(src, methods)
            self.assertEqual(len(actual[(inventory.GL_CLASS, "step", "()V")]), 1)
            self.assertEqual(actual[(inventory.GL_CLASS, "init", "(II)V")][0]["line"], 4)
            self.assertEqual(sum(len(x) for x in actual.values()), 2)

    def test_manifest_component_mapping_keeps_runtime_unproven(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "AndroidManifest.xml"
            path.write_text(
                '<manifest xmlns:android="http://schemas.android.com/apk/res/android" '
                'package="com.sample"><application><activity android:name=".Main"/>'
                '<service android:name="com.sample.Background"/></application></manifest>',
                encoding="utf-8",
            )
            report = inventory.manifest_inventory(path, {"Lcom/sample/Main;"})
            self.assertEqual(len(report["components"]), 2)
            self.assertEqual(sorted(c["smali_class_declared"] for c in report["components"]),
                             [False, True])
            self.assertTrue(all(not c["runtime_component_invoked"]
                                for c in report["components"]))

    def test_pointer_identity_does_not_prove_obb_bytes(self):
        data = inventory.obb_handoff({
            "state": "git_lfs_pointer_only",
            "lfs_declared_size_bytes": inventory.OBB_SIZE,
            "lfs_declared_sha256": inventory.OBB_SHA,
        })
        self.assertFalse(data["materialized_sha256_verified"])
        self.assertFalse(data["t29_done"])
        self.assertEqual(data["assets_classified"], 0)

    def test_wrong_obb_identity_rejected(self):
        with self.assertRaisesRegex(ValueError, "Unexpected"):
            inventory.obb_handoff({
                "state": "git_lfs_pointer_only",
                "lfs_declared_size_bytes": inventory.OBB_SIZE,
                "lfs_declared_sha256": "0" * 64,
            })

    def test_missing_obb_rejected_without_download(self):
        with self.assertRaisesRegex(ValueError, "Expected OBB pointer"):
            inventory.obb_handoff({"state": "missing"})

    def test_no_fake_t27_completion(self):
        natives = [
            {"class": inventory.GL_CLASS, "method": x, "descriptor": "()V",
             "jni_export_candidates": []}
            for x in inventory.EXPECTED_GL_METHODS
        ]
        s = {"native_methods": natives, "native_method_count": 12,
             "smali_files_scanned": 1, "smali_classes_declared": 1,
             "jni_onload_exported": False}
        map_ = inventory.summarize(
            s, {}, {"package": "com.sample", "components": [
                {"kind":"activity","declared_name":"Main","smali_class_declared": True}
            ]},
            inventory.obb_handoff({"state":"git_lfs_pointer_only",
                                  "lfs_declared_size_bytes": inventory.OBB_SIZE,
                                  "lfs_declared_sha256": inventory.OBB_SHA}))
        self.assertFalse(map_["t27_done"])
        self.assertFalse(map_["t29_done"])
        self.assertEqual(map_["new_semantic_certificates"], 0)
        self.assertFalse(map_["bidirectional_behavioral_jni_mapping_complete"])


if __name__ == "__main__":
    unittest.main()
