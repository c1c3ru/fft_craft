"""B01 inventory audit: synthetic host-only tests (no Android/ARM execution)."""
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).with_name("b01_inventory_audit.py")
spec = importlib.util.spec_from_file_location("b01audit", SCRIPT)
audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)

HEADER = "address,size,mangled,demangled,status,section_ref\n"


def row(address, size, name="test"):
    return "%s,%s,%s,%s,read_structural,fixture\n" % (
        address, size, name, name)


class B01InventoryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.docs = self.root / "FFT_Android_Mod/docs"
        self.docs.mkdir(parents=True)
        self.canonical = self.docs / "RE_FUNCTION_INVENTORY.csv"
        self.priority = self.docs / "alvos_prioritarios_nucleo.csv"

    def tearDown(self):
        self.temp.cleanup()

    def put(self, path, contents):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(contents, encoding="utf-8")

    def fixtures(self, inv=None, priority=None):
        if inv is None:
            inv = (row("00001000", 32, "a")
                   + row("00001000", 32, "alias")
                   + row("00001004", 8, "internal")
                   + row("00002000", 12, "separate"))
        if priority is None:
            priority = row("00001000", 32, "a")
        self.put(self.canonical, HEADER + inv)
        self.put(self.priority, HEADER + priority)

    def test_reproducible_dedup_and_overlap(self):
        self.fixtures()
        output, canonical = audit.canonicalize(audit.csv_rows(self.canonical))
        self.assertEqual(output["declared_entries"], 4)
        self.assertEqual(output["unique_entrypoints"], 3)
        self.assertEqual(output["duplicate_address_entries"], 1)
        self.assertEqual(output["overlap_pair_count"], 1)
        self.assertEqual(output["overlap_pairs"][0]["overlap_bytes"], 8)
        self.assertEqual(output["declared_interval_union_bytes_not_executable_coverage"], 44)
        self.assertTrue(output["not_semantic_equivalence"])
        self.assertTrue(audit.validate_priority(
            audit.csv_rows(self.priority), canonical)["sizes_agree"])

    def test_nested_overlap_pairs_not_undercounted(self):
        rows = [
            {"address": "00001000", "start": 4096, "size": 64},
            {"address": "00001004", "start": 4100, "size": 32},
            {"address": "00001008", "start": 4104, "size": 8},
        ]
        counts, _ = audit.canonicalize(rows)
        self.assertEqual(counts["overlap_pair_count"], 3)
        self.assertEqual(counts["declared_interval_union_bytes_not_executable_coverage"], 64)

    def test_same_address_different_size_rejected(self):
        self.fixtures(inv=row("00001000", 4) + row("00001000", 8))
        with self.assertRaises(audit.InventoryError):
            audit.canonicalize(audit.csv_rows(self.canonical))

    def test_invalid_schema_and_addresses_rejected(self):
        self.put(self.canonical, "address,size\n00001000,20\n")
        with self.assertRaises(audit.InventoryError):
            audit.csv_rows(self.canonical)
        self.put(self.canonical, HEADER + row("ffffffff", 4))
        with self.assertRaises(audit.InventoryError):
            audit.csv_rows(self.canonical)
        self.put(self.canonical, HEADER + row("0x000100", 4))
        with self.assertRaises(audit.InventoryError):
            audit.csv_rows(self.canonical)

    def test_invalid_size_and_blank_csv_rejected(self):
        for size in ("0", "-5", "foo", "4294967296"):
            with self.subTest(size=size):
                self.put(self.canonical, HEADER + row("00001000", size))
                with self.assertRaises(audit.InventoryError):
                    audit.csv_rows(self.canonical)
        self.put(self.canonical, HEADER)
        with self.assertRaises(audit.InventoryError):
            audit.csv_rows(self.canonical)

    def test_priority_must_be_subset_with_equal_sizes(self):
        self.fixtures(priority=row("00003000", 32))
        with self.assertRaises(audit.InventoryError):
            audit.validate_priority(
                audit.csv_rows(self.priority),
                audit.canonicalize(audit.csv_rows(self.canonical))[1])
        self.fixtures(priority=row("00001000", 31))
        with self.assertRaises(audit.InventoryError):
            audit.validate_priority(
                audit.csv_rows(self.priority),
                audit.canonicalize(audit.csv_rows(self.canonical))[1])
        self.fixtures(priority=row("00001000", 32) + row("00001000", 32))
        with self.assertRaises(audit.InventoryError):
            audit.validate_priority(
                audit.csv_rows(self.priority),
                audit.canonicalize(audit.csv_rows(self.canonical))[1])

    def test_lfs_pointer_is_not_a_materialized_obb(self):
        p = self.root / "FFT_Android_Mod/obb-data/game.obb"
        self.put(p, "version https://git-lfs.github.com/spec/v1\n"
                 "oid sha256:" + "a" * 64 + "\nsize 123456789\n")
        state = audit.file_state(p)
        self.assertEqual(state["status"], "lfs_pointer_not_asset")
        self.assertNotIn("sha256", state)

    def test_missing_file_is_not_verified(self):
        self.assertEqual(audit.file_state(self.root / "no/file")["status"], "missing")

    def test_elf_not_falsely_verified_by_header(self):
        p = self.root / "FFT_Android_Mod/src/lib/armeabi/libgl2jni.so"
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(b"\x7fELF\x01\x01" + b"\0" * 12 + (40).to_bytes(2, "little") + b"\0" * 64)
        tracked = ["FFT_Android_Mod/src/lib/armeabi/libgl2jni.so"]
        output = audit.asset_inventory(self.root, tracked)
        self.assertFalse(output["native_elf"]["matches_expected_sha256"])
        self.assertTrue(output["native_elf"]["valid_arm_elf32_le_header"])
        self.assertFalse(output["android_artifact_inventory_complete"])

    def test_report_keeps_B01_in_progress_and_no_certificates(self):
        self.fixtures()
        tracked = ["FFT_Android_Mod/src/lib/armeabi/libgl2jni.so",
                   "FFT_Android_Mod/obb-data/game.obb",
                   "FFT_Android_Mod/original/game.apk",
                   "FFT_Android_Mod/src/smali/com/example/StorageUtil.smali"]
        report = audit.build_report(self.root, tracked_paths=tracked)
        self.assertFalse(report["ready_to_mark_B01_done"])
        self.assertEqual(report["task_state"], "in_progress")
        self.assertEqual(report["semantic_certificates_added"], 0)
        self.assertIn("reference_arm_elf_not_sha_verified", report["blockers"])
        self.assertEqual(report["elf_function_inventory"]["overlap_pair_count"], 1)
        self.assertIn("jni_smali_class_to_native_symbol_mapping_not_validated", report["blockers"])
        self.assertNotIn("semantic_certificate", json.dumps(report["elf_function_inventory"]))

    def test_git_manifest_is_required(self):
        with self.assertRaises(audit.InventoryError):
            audit.git_tracked_paths(self.root)


if __name__ == "__main__":
    unittest.main()
