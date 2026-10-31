"""B01 bounds: original BL destination and synthetic C++ object contract."""
import unittest

import b01_bounded_caller_execution as execution


class CallsiteTests(unittest.TestCase):
    def test_exact_reviewed_arm_bl(self):
        self.assertTrue(execution.verify_callsite(
            bytes.fromhex("f9ffffeb"), 0xb9f90, 0xb9f7c, "f9ffffeb"))
        self.assertTrue(execution.verify_callsite(
            bytes.fromhex("f9ffffeb"), 0xbe1f0, 0xbe1dc, "f9ffffeb"))

    def test_wrong_elf_bytes_refused(self):
        with self.assertRaisesRegex(ValueError, "opcode"):
            execution.verify_callsite(
                bytes.fromhex("000000ea"), 0xb9f90, 0xb9f7c, "f9ffffeb")

    def test_wrong_destination_refused(self):
        with self.assertRaisesRegex(ValueError, "destination"):
            execution.verify_callsite(
                bytes.fromhex("f9ffffeb"), 0xb9f90, 0xb9f80, "f9ffffeb")

    def test_unconditional_call_required(self):
        with self.assertRaisesRegex(ValueError, "unconditional"):
            execution.verify_callsite(
                bytes.fromhex("000000ea"), 0xb9f90, 0xb9f98, "000000ea")

    def test_object_bounds(self):
        self.assertTrue(execution.valid_this(execution.DATA+0x1000, 0x20))
        self.assertTrue(execution.valid_this(execution.DATA+execution.DATA_SIZE-4, 0))
        self.assertFalse(execution.valid_this(execution.DATA+execution.DATA_SIZE-4, 0x20))
        self.assertFalse(execution.valid_this(execution.DATA-4, 0))
        self.assertFalse(execution.valid_this(execution.DATA+1, 0))
        self.assertFalse(execution.valid_this(None, 0))

    def test_only_two_audited_small_callers(self):
        self.assertEqual(len(execution.CASES), 2)
        for case in execution.CASES:
            self.assertIn(case["callee"], execution.cpp.EXPECTED)
            self.assertLess(case["caller"], case["site"])
            self.assertNotEqual(case["caller"], case["callee"])


if __name__ == "__main__":
    unittest.main()
