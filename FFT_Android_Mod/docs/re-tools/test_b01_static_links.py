"""Host-only regression tests for the B01 ELF overlap/JNI/OBB gates.

Synthetic fixtures never imply actual original game code was executed.
"""
import importlib.util
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).parent


def load(name, module_name):
    spec = importlib.util.spec_from_file_location(module_name, ROOT / name)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


overlap = load("b01_overlap_elf_evidence.py", "b01_overlap")
smali = load("b01_smali_jni_obb_audit.py", "b01_jni_obb")


class B01StaticLinkTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def test_co_terminal_pairs_are_all_enumerated(self):
        entries = [
            {"start": 0x1000, "size": 0x40, "end": 0x1040},
            {"start": 0x1004, "size": 0x3c, "end": 0x1040},
            {"start": 0x1008, "size": 0x38, "end": 0x1040},
            {"start": 0x1100, "size": 0x10, "end": 0x1110},
        ]
        pairs = overlap.get_pairs(entries)
        self.assertEqual(len(pairs), 3)
        self.assertTrue(all(a["end"] == b["end"] for a,b in pairs))

    def test_non_coterminal_overlap_is_not_silently_ignored(self):
        entries = [
            {"start": 0x1000, "end": 0x1040},
            {"start": 0x1004, "end": 0x1020},
        ]
        pairs = overlap.get_pairs(entries)
        self.assertEqual(len(pairs), 1)
        self.assertNotEqual(pairs[0][0]["end"], pairs[0][1]["end"])

    def test_inventory_rejects_changed_size_for_same_address(self):
        inp = self.root / "inventory.csv"
        inp.write_text(
            "address,size,mangled,demangled,status,section_ref\n"
            "00001000,16,f,foo,read_structural,fixture\n"
            "00001000,20,g,bar,read_structural,fixture\n",
            encoding="utf-8")
        with self.assertRaises(ValueError):
            overlap.get_entries(inp)

    def test_jni_symbol_escaping(self):
        self.assertEqual(smali.jni_encode("com/example/A_B"), "com_example_A_1B")
        self.assertEqual(smali.jni_encode("[I"), "_3I")
        self.assertEqual(smali.jni_encode(";"), "_2")

    def test_smali_native_methods_and_loadlibrary_reference(self):
        path = self.root / "com/example/GL2JNILib.smali"
        path.parent.mkdir(parents=True)
        path.write_text(
            ".class public Lcom/example/GL2JNILib;\n"
            '.method public static native init(II)V\n.end method\n'
            '.method static constructor <clinit>()V\n'
            'const-string v0, "gl2jni"\n'
            'invoke-static {v0}, Ljava/lang/System;->loadLibrary(Ljava/lang/String;)V\n'
            '.end method\n', encoding="utf-8")
        data = smali.scan_smali(self.root)
        self.assertEqual(data["smali_files_scanned"], 1)
        self.assertEqual(data["native_methods"][0]["descriptor"], "(II)V")
        self.assertEqual(data["native_methods"][0]["method"], "init")
        self.assertEqual(len(data["gl2jni_literal_references"]), 1)
        linked = smali.link_methods(data["native_methods"], {
            "Java_com_example_GL2JNILib_init"})
        self.assertTrue(linked[0]["static_export_candidate"])
        self.assertFalse(linked[0]["runtime_binding_proven"])

    def test_unresolved_native_binding_stays_unresolved(self):
        entry={"class":"Lcom/example/GL2JNILib;","method":"init",
               "descriptor":"(II)V","source":"GL2JNILib.smali"}
        rows = smali.link_methods([entry], {"JNI_OnLoad"})
        self.assertEqual(rows[0]["jni_export_candidates"], [])
        self.assertFalse(rows[0]["runtime_binding_proven"])

    def test_lfs_pointer_does_not_count_as_obb_asset(self):
        path = self.root / "main.obb"
        path.write_text("version https://git-lfs.github.com/spec/v1\n"
                        "oid sha256:" + "a"*64 + "\nsize 123456\n")
        result = smali.inspect_obb(path)
        self.assertEqual(result["state"], "git_lfs_pointer_only")
        self.assertFalse(result["materialized_bytes_verified"])
        self.assertEqual(result["lfs_declared_size_bytes"], 123456)

    def test_materialized_nonzip_obb_not_assumed_complete(self):
        path = self.root / "main.obb"
        path.write_bytes(b"private-test-not-zip")
        result = smali.inspect_obb(path)
        self.assertEqual(result["state"], "materialized_non_pointer")
        self.assertEqual(result["archive_format"], "unknown_not_zip")
        self.assertFalse(result["entries_verified"])

    def test_zip_obb_directory_is_not_contents_or_crc_proof(self):
        import zipfile
        path = self.root / "main.obb"
        with zipfile.ZipFile(path, "w") as z:
            z.writestr("path-not-to-publish.dat", "data")
        result = smali.inspect_obb(path)
        self.assertEqual(result["archive_format"], "zip_directory_only")
        self.assertEqual(result["archive_entry_count"], 1)
        self.assertFalse(result["member_crc_or_data_verified"])
        self.assertNotIn("path-not-to-publish.dat", str(result))

    def test_empty_smali_tree_rejected(self):
        with self.assertRaises(ValueError):
            smali.scan_smali(self.root)

    def test_no_file_not_materialized(self):
        self.assertEqual(smali.inspect_obb(self.root / "absent.obb")["state"], "missing")


if __name__ == "__main__":
    unittest.main()
