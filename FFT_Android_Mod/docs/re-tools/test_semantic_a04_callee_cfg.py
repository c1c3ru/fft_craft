"""Bounded structural A04 callee inventory regressions (synthetic instruction bytes)."""
import unittest
from semantic_a04_callee_cfg import inventory

def words(*items):
    return b"".join(x.to_bytes(4, "little") for x in items)

class CalleeCfgTests(unittest.TestCase):
    def test_direct_call_stops_before_unknown_callee(self):
        # mov r0,r1; bl target; bx lr
        state = inventory(words(0xe1a00001, 0xeb000000, 0xe12fff1e), 0x1000)
        self.assertEqual(len(state["calls"]), 1)
        self.assertEqual(state["calls"][0]["target"], "0000100c")
        self.assertEqual(len(state["instructions"]), 2)
        self.assertFalse(state["reimplementation_ready"])
        self.assertTrue(any(x["reason"] == "callee_effects_unresolved" for x in state["unresolved"]))

    def test_stack_write_candidate_and_return(self):
        state = inventory(words(0xe92d4010, 0xe8bd8010), 0x2000)
        self.assertEqual(len(state["calls"]), 0)
        self.assertTrue(state["memory_candidates"])
        self.assertTrue(any(x["reason"] == "indirect_pc_transfer_or_return" for x in state["unresolved"]))

    def test_unconditional_branch_is_bounded(self):
        state = inventory(words(0xea000000, 0xe1a00000, 0xe12fff1e), 0x3000)
        self.assertEqual(state["edges"][0]["to"], "00003008")
        self.assertNotIn("00003004", [x["pc"] for x in state["instructions"]])

    def test_budget_never_inflates_semantic_coverage(self):
        state = inventory(words(*([0xe1a00000]*20)), 0x4000, max_instructions=2)
        self.assertEqual(len(state["instructions"]), 2)
        self.assertTrue(any(x["reason"] == "instruction_budget" for x in state["unresolved"]))

    def test_blt_is_conditional_branch_not_link_call(self):
        # A32 BLT +0, next PC+8 (same encoded displacement as BL).
        state = inventory(words(0xba000000, 0xe1a00000, 0xe12fff1e), 0x5000)
        self.assertEqual(state["calls"], [])
        self.assertTrue(any(x["type"] == "fallthrough_candidate" for x in state["edges"]))

    def test_rejects_bad_alignment(self):
        with self.assertRaises(ValueError):
            inventory(b"abcd", 0x1002)
        with self.assertRaises(ValueError):
            inventory(b"abc", 0x1000)

if __name__ == "__main__":
    unittest.main()
