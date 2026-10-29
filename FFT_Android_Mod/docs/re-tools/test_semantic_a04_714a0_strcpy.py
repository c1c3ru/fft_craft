"""Strcpy relocation contract cannot silently accept different imports."""
import unittest
import semantic_a04_714a0_strcpy as checks

def sample():
    return {"exact_relocations": [{"offset": "00347d70", "rel_section": ".rel.plt",
             "type_id": 22, "type": "R_ARM_JUMP_SLOT",
             "symbol": {"name": "strcpy", "shndx": "SHN_UNDEF", "kind": "STT_FUNC"}}],
            "needed_libraries": ["libc.so"], "sections": [{"name": ".got"}],
            "file_word": {"le32": "00071468"}}


class ImportAuditTests(unittest.TestCase):
    def test_original_import_is_accepted_only_as_runtime_candidate(self):
        result = checks.verify_strcpy_provenance(sample())
        self.assertEqual(result["symbol"], "strcpy")
        self.assertIsNone(result["resolved_android_runtime_address"])

    def test_wrong_import_fails_closed(self):
        a = sample()
        a["exact_relocations"][0]["symbol"]["name"] = "strcat"
        with self.assertRaises(ValueError):
            checks.verify_strcpy_provenance(a)

    def test_missing_relocation_fails_closed(self):
        a = sample()
        a["exact_relocations"] = []
        with self.assertRaises(ValueError):
            checks.verify_strcpy_provenance(a)

    def test_wrong_elf_slot_fails_closed(self):
        a = sample()
        a["file_word"]["le32"] = "00000000"
        with self.assertRaises(ValueError):
            checks.verify_strcpy_provenance(a)

    def test_missing_libc_dependency_fails_closed(self):
        a = sample()
        a["needed_libraries"] = []
        with self.assertRaises(ValueError):
            checks.verify_strcpy_provenance(a)

if __name__ == "__main__":
    unittest.main()
