"""Two-guard ARM slice regression tests: early return, BLE and writes."""
import unittest

import semantic_two_guards as twoguard
import semantic_branch_microexec as branches
import semantic_guarded_block as prior
from test_semantic_guarded_block import BLOCK

# LDR r3,[r2,r3]; ANDS r3,r3,#0x100; BNE 0x25a2f4;
# LDR r2,[r0,#0x14]; followed by the previously proven CMP/BLE/ORR/STR slice.
SLICE = bytes.fromhex("033092e7 013c13e2 2600001a 142090e5") + BLOCK


class TwoGuardsTests(unittest.TestCase):
    def test_opcode_fixture_disassembles_all_twelve(self):
        decoded = twoguard.validate(SLICE, twoguard.LITERAL_WORD)
        self.assertEqual(len(decoded), 12)

    def test_status_bit_halts_early_and_preserves_memory(self):
        for status in (0x100, 0x101, 0xFFFFFFFF):
            for field in (0, 1, 0xFFFFFFFF):
                with self.subTest(status=status, field=field):
                    result = twoguard.simulate(
                        SLICE, twoguard.LITERAL_WORD, status, field,
                        0xFFFFFFFF, branches.CPSR_STATES[1])
                    self.assertEqual(result["path"], "early_status")
                    self.assertEqual(result["writes"], [])
                    self.assertEqual(result["trace"][-1], twoguard.EARLY_EXIT)

    def test_second_guard_skips_nonpositive_field(self):
        for field in (0, 0xFFFFFFFF, 0x80000000):
            result = twoguard.simulate(
                SLICE, twoguard.LITERAL_WORD, 0, field,
                0, branches.CPSR_STATES[0])
            self.assertEqual(result["path"], "nonpositive")
            self.assertEqual(result["writes"], [])
            self.assertEqual(result["trace"][-1], twoguard.END)

    def test_write_path_updates_two_words_only(self):
        for status in (0, 0x80):
            for field in (1, 43, 0x7FFFFFFF):
                for initial in prior.FLAGS:
                    with self.subTest(status=status, field=field, initial=initial):
                        result = twoguard.simulate(
                            SLICE, twoguard.LITERAL_WORD, status, field,
                            initial, branches.CPSR_STATES[0])
                        self.assertEqual(result["path"], "writes")
                        self.assertEqual(
                            result["writes"],
                            [(twoguard.OBJECT_BASE + 0x14, 4, 0),
                             (twoguard.GLOBAL_FLAG_BASE, 4, initial | 0x40)])

    def test_seed_flags_do_not_change_two_guard_decisions(self):
        def run(seed):
            return twoguard.simulate(
                SLICE, twoguard.LITERAL_WORD, 0x80, 1, 0, seed)
        a, b = (run(c) for c in branches.CPSR_STATES)
        self.assertEqual(a["trace"], b["trace"])
        self.assertEqual(a["writes"], b["writes"])

    def test_byte_and_literal_mutations_fail_closed(self):
        with self.assertRaisesRegex(ValueError, "literal"):
            twoguard.validate(SLICE, twoguard.LITERAL_WORD ^ 1)
        with self.assertRaisesRegex(ValueError, "Expected 12"):
            twoguard.validate(bytes.fromhex("033092e7 013c13e2 0000001a 142090e5") +
                              BLOCK, twoguard.LITERAL_WORD)

    def test_invalid_state_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "unsigned"):
            twoguard.simulate(SLICE, twoguard.LITERAL_WORD,
                              -1, 1, 0, branches.CPSR_STATES[0])


if __name__ == "__main__":
    unittest.main()
