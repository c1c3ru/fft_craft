"""Isolated ARM instruction emulator tests (not whole-function tests)."""
import unittest

import semantic_microexec as micro


class ArmMicroexecutionTests(unittest.TestCase):
    def test_bit_clear_on_known_arm_words(self):
        # ldr r2,[r4]; bic r2,r2,#0x40; str r2,[r4]
        data = bytes.fromhex("002094e5 4020c2e3 002084e5")
        cases = [0, 1, 0x40, 0x41, 0x7f, 0xffffffff, 0x80000040]
        for initial in cases:
            with self.subTest(initial=initial):
                self.assertEqual(
                    micro.microexecute(data, 0x244254, initial),
                    initial & 0xFFFFFFBF)

    def test_nonmatching_arm_words_are_refused(self):
        bad = bytes.fromhex("002094e5 4020c2e3 002085e5")
        with self.assertRaisesRegex(ValueError, "Expected unconditional"):
            micro.check_instructions(bad, 0x244254)

    def test_deterministic_vectors_have_edge_cases(self):
        self.assertEqual(micro.inputs(), micro.inputs())
        self.assertIn(0, micro.inputs())
        self.assertIn(0x40, micro.inputs())
        self.assertIn(0xFFFFFFFF, micro.inputs())
        self.assertEqual(len(micro.inputs()), 32)


if __name__ == "__main__":
    unittest.main()
