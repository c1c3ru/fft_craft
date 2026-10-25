"""Regression tests for isolated real-ARM-style branch microexecution."""
import unittest
import semantic_branch_microexec as branch


# ARM little-endian words at the real function's instruction addresses.
SYNTHETIC_PAIRS = (
    bytes.fromhex("2b0052e3 3d0000ca"),  # cmp r2,#43; bgt 0x2443c8
    bytes.fromhex("010c53e3 1d00000a"),  # cmp r3,#256; beq 0x24438c
    bytes.fromhex("010c53e3 d5ffff1a"),  # cmp r3,#256; bne 0x2442e0
)


class ConditionalMicroexecTests(unittest.TestCase):
    def test_both_paths_and_seeded_nzcv_states(self):
        probes = (0, 42, 43, 44, 255, 256, 257, 0x7fffffff,
                  0x80000000, 0xffffffff)
        for case, data in zip(branch.BRANCHES, SYNTHETIC_PAIRS):
            branch.verify_pair(data, case)
            for value in probes:
                for cpsr in branch.CPSR_STATES:
                    with self.subTest(name=case["name"], value=value, cpsr=cpsr):
                        target = branch.execute_pair(data, case, value, cpsr)
                        expected = (case["taken"] if branch.expected_taken(case, value)
                                    else case["fallthrough"])
                        self.assertEqual(target, expected)

    def test_mutated_branch_target_is_rejected(self):
        case = branch.BRANCHES[0]
        bad = SYNTHETIC_PAIRS[0][:4] + bytes.fromhex("000000ca")
        with self.assertRaisesRegex(ValueError, "no longer matches"):
            branch.verify_pair(bad, case)

    def test_mutated_comparison_is_rejected(self):
        case = branch.BRANCHES[0]
        bad = bytes.fromhex("2a0052e3") + SYNTHETIC_PAIRS[0][4:]
        with self.assertRaisesRegex(ValueError, "no longer matches"):
            branch.verify_pair(bad, case)

    def test_32_bit_boundary_samples_repeat(self):
        self.assertEqual(len(branch.vectors()), 32)
        self.assertEqual(branch.vectors(), branch.vectors())
        self.assertIn(43, branch.vectors())
        self.assertIn(44, branch.vectors())
        self.assertIn(256, branch.vectors())
        self.assertIn(257, branch.vectors())
        self.assertIn(0x80000000, branch.vectors())
        self.assertFalse(branch.expected_taken(branch.BRANCHES[0], 0xffffffff))

    def test_invalid_cpsr_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "Invalid test state"):
            branch.execute_pair(SYNTHETIC_PAIRS[0], branch.BRANCHES[0], 43, 0x0)


if __name__ == "__main__":
    unittest.main()
