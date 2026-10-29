"""Fail closed when the second A04 import is not the original strlen."""
import unittest
from semantic_a04_b942c_strlen import check_import, veneer_slot

def candidate():
    return ({"slot": "00347d6c"},
            {"offset": "00347d6c", "section": ".rel.plt", "type": 22,
             "name": "strlen", "shndx": "SHN_UNDEF", "kind": "STT_FUNC"})

class SecondImportTests(unittest.TestCase):
    def test_exact_strlen_import(self):
        v, r = candidate()
        self.assertEqual(check_import(v, r)["import"], "strlen")

    def test_wrong_symbol_refused(self):
        v, r = candidate()
        r["name"] = "strcpy"
        with self.assertRaises(ValueError):
            check_import(v, r)

    def test_wrong_slot_refused(self):
        v, r = candidate()
        v["slot"] = "00347d70"
        with self.assertRaises(ValueError):
            check_import(v, r)

    def test_wrong_relocation_refused(self):
        v, r = candidate()
        r["type"] = 21
        with self.assertRaises(ValueError):
            check_import(v, r)

    def test_wrong_veneer_bytes_refused(self):
        from unittest.mock import patch
        import semantic_evidence
        with patch.object(semantic_evidence, "read_function", return_value=bytes(12)):
            with self.assertRaises(ValueError):
                veneer_slot(None)


if __name__ == "__main__":
    unittest.main()
