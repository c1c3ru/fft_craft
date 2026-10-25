"""Bounded ARM CMP/BLE/LDR/ORR/STR tests with synthetic encoded instructions."""
import unittest
import semantic_guarded_block as guarded
import semantic_branch_microexec as branch

# Encodings of the eight ARM instructions at 0x25a25c..0x25a278.
# Real ELF byte equality is NOT assumed here; CI independently disassembles it.
BLOCK = bytes.fromhex(
    "000052e3 "     # cmp r2, #0
    "050000da "     # ble 0x25a27c
    "a0219fe5 "     # ldr r2, [pc, #0x1a0]
    "143080e5 "     # str r3, [r0, #0x14]
    "023094e7 "     # ldr r3, [r4, r2]
    "002093e5 "     # ldr r2, [r3]
    "402082e3 "     # orr r2, r2, #0x40
    "002083e5 "     # str r2, [r3]
)


class GuardedBlockTests(unittest.TestCase):
    def test_fixture_matches_expected_assembly(self):
        self.assertEqual(len(guarded.verify_original_code(BLOCK, guarded.LITERAL_WORD)), 8)

    def test_positive_controls_update_object_and_flag(self):
        for control in (1, 2, 43, 256, 0x7fffffff):
            for flags in guarded.FLAGS:
                with self.subTest(control=control, flags=flags):
                    r = guarded.execute(BLOCK, guarded.LITERAL_WORD, control,
                                        flags, branch.CPSR_STATES[0])
                    self.assertFalse(r["taken"])
                    self.assertEqual(r["flag"], flags | 0x40)
                    self.assertEqual(len(r["writes"]), 2)

    def test_zero_and_negative_controls_bypass_all_writes(self):
        for control in (0, 0xffffffff, 0x80000000, 0xfffffffe):
            for cpsr in branch.CPSR_STATES:
                with self.subTest(control=control, cpsr=cpsr):
                    r = guarded.execute(BLOCK, guarded.LITERAL_WORD, control,
                                        0xA5A50000, cpsr)
                    self.assertTrue(r["taken"])
                    self.assertEqual(r["writes"], [])
                    self.assertEqual(r["flag"], 0xA5A50000)

    def test_flag_result_does_not_depend_on_seeded_nzcv(self):
        a = guarded.execute(BLOCK, guarded.LITERAL_WORD, 1, 0,
                            branch.CPSR_STATES[0])
        b = guarded.execute(BLOCK, guarded.LITERAL_WORD, 1, 0,
                            branch.CPSR_STATES[1])
        self.assertEqual(a["trace"], b["trace"])
        self.assertEqual(a["writes"], b["writes"])

    def test_mutated_block_or_literal_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "literal pool"):
            guarded.verify_original_code(BLOCK, guarded.LITERAL_WORD + 1)
        bad = BLOCK[:28] + bytes.fromhex("002084e5")
        with self.assertRaisesRegex(ValueError, "Unexpected ARM"):
            guarded.verify_original_code(bad, guarded.LITERAL_WORD)

    def test_inputs_must_fit_u32(self):
        with self.assertRaisesRegex(ValueError, "outside its allowed range"):
            guarded.execute(BLOCK, guarded.LITERAL_WORD, -1, 0,
                            branch.CPSR_STATES[0])


if __name__ == "__main__":
    unittest.main()
