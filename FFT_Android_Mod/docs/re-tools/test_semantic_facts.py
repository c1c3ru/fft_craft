"""Synthetic Capstone tests for instruction-local semantic facts."""
import importlib.util
import sys
import unittest
from pathlib import Path

from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
spec = importlib.util.spec_from_file_location("semantic_facts", HERE / "semantic_facts.py")
facts = importlib.util.module_from_spec(spec)
spec.loader.exec_module(facts)


def disasm(hex_words, start=0x1000):
    md = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    md.detail = True
    instructions = list(md.disasm(bytes.fromhex(hex_words), start))
    return {ins.address: ins for ins in instructions}


class SemanticFactsTests(unittest.TestCase):
    def test_bl_and_blx_only_not_conditional_ble_blt(self):
        # BLE, BLT, BL, BX LR
        insns = disasm("000000da 000000ba 000000eb 1eff2fe1")
        self.assertEqual([address for address, _ in facts.calls(insns)], [0x1008])

    def test_unconditional_bic_field_clear(self):
        # LDR R2,[R4]; BIC R2,R2,#0x40; STR R2,[R4]
        insns = disasm("002094e5 4020c2e3 002084e5")
        result = facts.bitmask_effects(insns)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["kind"], "clear_bits")
        self.assertEqual(result[0]["mask"], 0x40)
        self.assertEqual(result[0]["memory"], "[r4]")
        self.assertEqual(result[0]["condition"], "always")
        self.assertEqual(result[0]["addresses"], [0x1000, 0x1004, 0x1008])

    def test_guarded_orr_field_set(self):
        # LDR R3,[R4]; TST R3,#0x20; ORREQ R3,R3,#0x20; STREQ R3,[R4]
        insns = disasm("003094e5 200013e3 20308303 00308405")
        result = facts.bitmask_effects(insns)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["kind"], "set_bits")
        self.assertEqual(result[0]["mask"], 0x20)
        self.assertEqual(result[0]["test_mask"], 0x20)
        self.assertEqual(result[0]["condition"], "eq")

    def test_different_memory_base_is_not_an_effect(self):
        insns = disasm("002094e5 4020c2e3 002085e5")
        self.assertEqual(facts.bitmask_effects(insns), [])

    def test_conditional_store_without_matching_op_is_not_an_effect(self):
        # LDR R2,[R4]; BIC R2,R2,#0x40; STREQ R2,[R4]
        insns = disasm("002094e5 4020c2e3 00208405")
        self.assertEqual(facts.bitmask_effects(insns), [])


if __name__ == "__main__":
    unittest.main()
