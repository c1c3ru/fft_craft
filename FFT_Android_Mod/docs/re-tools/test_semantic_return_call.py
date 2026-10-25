"""Regression tests for early ARM POP and conditional state before first BL."""
import unittest

import semantic_return_call as bounded
import semantic_entry_prefix as entry
import semantic_branch_microexec as branches
from test_semantic_entry_prefix import CODE

# The seven ARM instructions following 0x25a27c, before BL at 0x25a298.
CONTINUATION = bytes.fromhex(
    "8c319fe5 3400a0e3 03308fe0 002093e5 "
    "000052e3 0020a013 00208315"
)
EARLY_POP = bytes.fromhex("3880bde8")
BYTES = CODE + CONTINUATION
LITERALS = entry.LITERAL_VALUES + (bounded.NEXT_LITERAL,)


class ReturnCallBoundaryTests(unittest.TestCase):
    def test_fixture_exactly_matches_prefix_continuation_and_pop(self):
        instructions = bounded.validate(BYTES, EARLY_POP, LITERALS)
        self.assertEqual(len(instructions), 28)
        self.assertEqual(bounded.NEXT_SLOT, 0x67B2F8)

    def test_true_pop_restores_registers_and_returns(self):
        for index in (0, 3):
            for next_value in bounded.NEXT_VALUES:
                result = bounded.emulate(
                    BYTES, EARLY_POP, LITERALS,
                    index, 0x100, 43, 0, next_value, branches.CPSR_STATES[1])
                self.assertEqual(result["path"], "early_return")
                self.assertEqual(result["endpoint"], bounded.RETURN_PC)
                self.assertFalse(result["next_slot_zeroed"])

    def test_nonpositive_continuation_stops_at_call_boundary(self):
        for field in (0, 0x80000000, 0xFFFFFFFF):
            for next_value in bounded.NEXT_VALUES:
                result = bounded.emulate(
                    BYTES, EARLY_POP, LITERALS,
                    2, 0x80, field, 0, next_value, branches.CPSR_STATES[0])
                self.assertEqual(result["path"], "nonpositive")
                self.assertEqual(result["endpoint"], bounded.FIRST_CALL)
                self.assertEqual(result["next_slot_zeroed"], bool(next_value))

    def test_positive_control_writes_object_flag_and_optional_slot_reset(self):
        for flag in (0, 0x40, 0xFFFFFFFF):
            for next_value in bounded.NEXT_VALUES:
                result = bounded.emulate(
                    BYTES, EARLY_POP, LITERALS,
                    1, 0, 43, flag, next_value, branches.CPSR_STATES[1])
                self.assertEqual(result["path"], "writes")
                self.assertEqual(result["endpoint"], bounded.FIRST_CALL)
                self.assertEqual(result["next_slot_zeroed"], bool(next_value))
                self.assertIn((entry.FLAG_BASE, 4, flag | 0x40), result["writes"])

    def test_cpsr_seed_does_not_impact_guarded_path(self):
        args = (BYTES, EARLY_POP, LITERALS, 3, 0, 1, 0, 0x9ABCDEF0)
        a = bounded.emulate(*args, branches.CPSR_STATES[0])
        b = bounded.emulate(*args, branches.CPSR_STATES[1])
        self.assertEqual(a["trace"], b["trace"])
        self.assertEqual(a["writes"], b["writes"])

    def test_mutated_literal_pop_or_code_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "literal"):
            bounded.validate(BYTES, EARLY_POP, LITERALS[:-1] + (0,))
        with self.assertRaisesRegex(ValueError, "opcode"):
            bounded.validate(BYTES, bytes.fromhex("1eff2fe1"), LITERALS)
        mutated = bytearray(BYTES)
        mutated[-4] ^= 1
        with self.assertRaisesRegex(ValueError, "opcode"):
            bounded.validate(bytes(mutated), EARLY_POP, LITERALS)

    def test_bad_control_input_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "Controlled inputs"):
            bounded.emulate(
                BYTES, EARLY_POP, LITERALS, 1, 0, 1, -1, 0,
                branches.CPSR_STATES[0])


if __name__ == "__main__":
    unittest.main()
