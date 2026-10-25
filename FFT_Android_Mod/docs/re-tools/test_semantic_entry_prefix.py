"""Regression tests for real ARM entry prologue, indexed globals and guards."""
import unittest

import semantic_entry_prefix as entry
import semantic_two_guards as guards
import semantic_branch_microexec as branches
from test_semantic_two_guards import SLICE

# Encoded ARM words for the 9-instruction entry preparation:
# push, ldr, two LDR literals, mov, PC-relative add, mul, indexed ldr, mov.
PREFIX = bytes.fromhex(
    "38402de9 "  # push {r3,r4,r5,lr}
    "043090e5 "  # ldr r3,[r0,#4]
    "cc419fe5 "  # ldr r4,[pc,#0x1cc]
    "cc219fe5 "  # ldr r2,[pc,#0x1cc]
    "3810a0e3 "  # mov r1,#0x38
    "04408fe0 "  # add r4,pc,r4
    "910303e0 "  # mul r3,r1,r3
    "022094e7 "  # ldr r2,[r4,r2]
    "0050a0e1 "  # mov r5,r0
)
CODE = PREFIX + SLICE


class EntryPrefixTests(unittest.TestCase):
    def test_all_opcodes_and_pc_literals(self):
        self.assertEqual(len(entry.verify(CODE, entry.LITERAL_VALUES)), 21)
        self.assertEqual(entry.GLOBAL_ANCHOR, 0x347D58)
        self.assertEqual(entry.STATUS_SLOT, 0x3479B0)
        self.assertEqual(entry.FLAG_SLOT, 0x3479CC)

    def test_early_status_uses_index_and_preserves_fields(self):
        for index in entry.INDICES:
            for field in (0, 1, 0xFFFFFFFF):
                with self.subTest(index=index, field=field):
                    result = entry.simulate(CODE, entry.LITERAL_VALUES, index,
                                            0x100, field, 0xA5A50000,
                                            branches.CPSR_STATES[1])
                    self.assertEqual(result["path"], "early_status")
                    self.assertEqual(result["trace"][-1], entry.EARLY_EXIT)

    def test_nonpositive_controls_do_not_modify_global_state(self):
        for control in (0, 0x80000000, 0xFFFFFFFF):
            for index in (0, 3):
                result = entry.simulate(CODE, entry.LITERAL_VALUES, index,
                                        0x80, control, 0,
                                        branches.CPSR_STATES[0])
                self.assertEqual(result["path"], "nonpositive")

    def test_positive_controls_modify_only_two_state_fields(self):
        for index in entry.INDICES:
            for seed in (0, 0xFFFFFFFF):
                result = entry.simulate(CODE, entry.LITERAL_VALUES, index,
                                        0, 43, seed, branches.CPSR_STATES[0])
                self.assertEqual(result["path"], "writes")
                self.assertIn((entry.FLAG_BASE, 4, seed | 0x40), result["writes"])

    def test_literal_and_opcode_change_rejected(self):
        bad_literals = list(entry.LITERAL_VALUES)
        bad_literals[1] ^= 4
        with self.assertRaisesRegex(ValueError, "literal"):
            entry.verify(CODE, bad_literals)
        bad = bytearray(CODE)
        bad[4] ^= 1
        with self.assertRaisesRegex(ValueError, "opcode signature"):
            entry.verify(bytes(bad), entry.LITERAL_VALUES)

    def test_invalid_index_rejected(self):
        with self.assertRaisesRegex(ValueError, "Invalid controlled"):
            entry.simulate(CODE, entry.LITERAL_VALUES, 99, 0, 0, 0,
                           branches.CPSR_STATES[0])

    def test_flags_seed_independence(self):
        args = (CODE, entry.LITERAL_VALUES, 2, 0, 256, 0)
        a = entry.simulate(*args, branches.CPSR_STATES[0])
        b = entry.simulate(*args, branches.CPSR_STATES[1])
        self.assertEqual(a["path"], b["path"])
        self.assertEqual(a["writes"], b["writes"])
        self.assertEqual(a["trace"], b["trace"])


if __name__ == "__main__":
    unittest.main()
