"""Tests for strictly local ARM conditional edge observations."""
import unittest
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
import semantic_paths


def decode(hex_words, start=0x1000):
    md = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    md.detail = True
    return {i.address: i for i in md.disasm(bytes.fromhex(hex_words), start)}


class BranchConditionsTests(unittest.TestCase):
    def test_eq_branch_has_both_edges(self):
        # CMP r0,#0; BEQ 0x1018; LDR/BIC/STR ... (fallthrough)
        instructions = decode(
            "000050e3 0300000a 002094e5 4020c2e3 002084e5")
        guards = semantic_paths.branch_guards(instructions)
        self.assertEqual(len(guards), 1)
        guard = guards[0]
        self.assertEqual(guard["compare"], 0x1000)
        self.assertEqual(guard["branch"], 0x1004)
        self.assertEqual(guard["taken_target"], 0x1018)
        self.assertEqual(guard["fallthrough_target"], 0x1008)
        self.assertEqual(guard["taken_predicate"], "r0 == 0x0")
        self.assertEqual(guard["fallthrough_predicate"], "r0 != 0x0")
        from semantic_facts import bitmask_effects
        effects = semantic_paths.incoming_guard_edges(bitmask_effects(instructions), guards)
        self.assertEqual(effects[0]["incoming_guard_edges"][0]["edge"], "fallthrough")
        self.assertEqual(effects[0]["incoming_guard_edges"][0]["predicate"], "r0 != 0x0")

    def test_no_comparison_yields_no_global_guards(self):
        # LDR/BIC/STR by themselves cannot prove predecessor flags.
        instructions = decode("002094e5 4020c2e3 002084e5")
        self.assertEqual(semantic_paths.branch_guards(instructions), [])

    def test_tst_ne_branch_yields_bit_conditions(self):
        # TST r2, #0x20; BNE 0x1018
        instructions = decode("200012e3 0300001a")
        found = semantic_paths.branch_guards(instructions)
        self.assertEqual(len(found), 1)
        self.assertEqual(found[0]["taken_predicate"], "(r2 & 0x20) != 0")
        self.assertEqual(found[0]["fallthrough_predicate"], "(r2 & 0x20) == 0")

    def test_non_adjacent_compare_not_assumed(self):
        # CMP; MOVS (changes flags); BEQ; no accepted pair
        instructions = decode("000050e3 0000b0e3 0000000a")
        self.assertEqual(semantic_paths.branch_guards(instructions), [])


if __name__ == "__main__":
    unittest.main()
