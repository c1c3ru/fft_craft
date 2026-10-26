"""Checks that only exact original ELF return opcodes become review candidates."""
import importlib.util
import unittest
from pathlib import Path

spec = importlib.util.spec_from_file_location(
    "semantic_leaf_bxlr", Path(__file__).with_name("semantic_leaf_bxlr.py"))
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


class LeafBXLRTests(unittest.TestCase):
    def test_candidate_selection_requires_exact_arm_word(self):
        rows = [
            {"address": "00002010", "name": "ret", "size": 4},
            {"address": "00002014", "name": "branch", "size": 4},
            {"address": "00002018", "name": "long", "size": 8},
            {"address": "0000201c", "name": "ret2", "size": 4},
        ]
        words = {0x2010: mod.BX_LR, 0x2014: bytes.fromhex("000000ea"),
                 0x201c: mod.BX_LR}
        def reader(binary, address, size):
            return words[address]
        checked, found = mod.find_candidates(rows, None, reader)
        self.assertEqual(checked, 3)
        self.assertEqual([r["address"] for r in found], ["00002010", "0000201c"])

    def test_real_unicorn_opcode_register_and_memory_contract(self):
        self.assertEqual(mod.verify_execution(0x2010, mod.BX_LR),
                         len(mod.STATES))

    def test_reject_changed_opcode_and_alignment(self):
        with self.assertRaises(ValueError):
            mod.verify_execution(0x2010, bytes.fromhex("0000a0e1"))
        with self.assertRaises(ValueError):
            mod.verify_execution(0x2011, mod.BX_LR)


if __name__ == "__main__":
    unittest.main()
