"""Fail closed on changed operator-new ARM-to-Thumb veneer contract."""
import copy
import unittest
from semantic_a04_new_veneer import verify_target


def original():
    return {"first_veneer_verified":True,"literal_word_le":"ffffba3d",
            "literal_addr":"002cdf78","computed_destination":"002c99b5",
            "thumb_state":True,
            "matching_function_symbols":[{"name":"_Znwj","start":"002c99b4",
                                          "size":76,"kind":"STT_FUNC"}]}

class NativeNewVeneerTests(unittest.TestCase):
    def test_mangled_operator_new_symbol_is_required(self):
        self.assertEqual(verify_target(original())["mangled_symbol"],"_Znwj")

    def test_wrong_symbol_rejected(self):
        row=original()
        row["matching_function_symbols"][0]["name"]="_ZdlPv"
        with self.assertRaises(ValueError):
            verify_target(row)

    def test_thumb_flag_rejected(self):
        row=original()
        row["thumb_state"]=False
        with self.assertRaises(ValueError):
            verify_target(row)

    def test_mutated_literal_rejected(self):
        row=original()
        row["literal_word_le"]="00000000"
        with self.assertRaises(ValueError):
            verify_target(row)

if __name__=="__main__":
    unittest.main()
