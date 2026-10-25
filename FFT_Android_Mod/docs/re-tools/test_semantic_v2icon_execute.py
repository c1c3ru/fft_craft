"""Isolated real-shape ARM getter microexecution and memory safety tests."""
import unittest

import semantic_v2icon_execute as getter
import semantic_callee_v2icon as audit
import semantic_branch_microexec as branch
from test_semantic_callee_v2icon import FAKE_BODY


class V2IconMachineTests(unittest.TestCase):
    def test_indexed_lookup_value_and_read_addresses(self):
        for index in getter.INDICES:
            for value in (0, 0x40, 0x12345678, 0xFFFFFFFF):
                with self.subTest(index=index, value=value):
                    result = getter.execute(FAKE_BODY, 0x1000, index, value,
                                            branch.CPSR_STATES[0])
                    self.assertEqual(result["result"], value)
                    self.assertEqual(result["slot"],
                                     audit.indexed_address(0x1000, index))
                    self.assertEqual(result["reads"], [
                        (audit.LITERAL_ADDR, 4), (result["slot"], 4)])

    def test_nzcv_seed_does_not_affect_getter(self):
        first = getter.execute(FAKE_BODY, 0x1000, 7, 0x80000000,
                               branch.CPSR_STATES[0])
        other = getter.execute(FAKE_BODY, 0x1000, 7, 0x80000000,
                               branch.CPSR_STATES[1])
        self.assertEqual(first, other)

    def test_changed_literal_or_opcode_rejected(self):
        with self.assertRaisesRegex(ValueError, "literal"):
            getter.execute(FAKE_BODY, 0x2000, 1, 7, branch.CPSR_STATES[0])
        changed = bytearray(FAKE_BODY)
        changed[0] ^= 1
        with self.assertRaisesRegex(ValueError, "no longer matches"):
            getter.execute(bytes(changed), 0x1000, 1, 7,
                           branch.CPSR_STATES[0])

    def test_out_of_scope_index_or_value_rejected(self):
        for idx, val in ((-1, 5), (0xFFFFFFFF, 5), (0, -1)):
            with self.subTest(index=idx, value=val):
                with self.assertRaisesRegex(ValueError, "Invalid sampled"):
                    getter.execute(FAKE_BODY, 0x1000, idx, val,
                                   branch.CPSR_STATES[0])


if __name__ == "__main__":
    unittest.main()
