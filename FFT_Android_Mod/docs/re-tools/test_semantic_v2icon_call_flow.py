"""Regression for actual ARM BL/BX LR and return-based three-way dispatch."""
import unittest

import semantic_v2icon_call_flow as flow
import semantic_branch_microexec as branch
from test_semantic_callee_v2icon import FAKE_BODY, bl_word

CALLER = (
    bl_word(flow.CALLSITE, flow.getter.CALLEE)
    + bytes.fromhex(
        "010050e3 "  # cmp r0,#1
        "0800000a "  # beq 0x25a2c8
        "020050e3 "  # cmp r0,#2
        "1200001a "  # bne 0x25a2f8
    )
)


class V2IconReturnBranchesTests(unittest.TestCase):
    def test_five_exact_caller_opcodes(self):
        self.assertEqual(flow.verify(CALLER, FAKE_BODY), 0x1000)

    def test_three_branches_and_exact_getter_reads(self):
        for ret, expected in ((1, flow.DEST_ONE), (2, flow.DEST_TWO),
                              (0, flow.DEST_OTHER),
                              (0xFFFFFFFF, flow.DEST_OTHER),
                              (0x80000000, flow.DEST_OTHER)):
            with self.subTest(result=ret):
                outcome = flow.execute(CALLER, FAKE_BODY, ret,
                                       branch.CPSR_STATES[0])
                self.assertEqual(outcome["destination"], expected)
                self.assertEqual(outcome["reads"], [
                    (flow.getter.LITERAL_ADDR, 4), (outcome["slot"], 4)])
                self.assertEqual(outcome["writes"], [])

    def test_seeded_flags_and_neighbors_not_changed(self):
        x = flow.execute(CALLER, FAKE_BODY, 2, branch.CPSR_STATES[0],
                         flow.NEIGHBOR_SEEDS[0])
        y = flow.execute(CALLER, FAKE_BODY, 2, branch.CPSR_STATES[1],
                         flow.NEIGHBOR_SEEDS[1])
        self.assertEqual(x["destination"], y["destination"])
        self.assertEqual(x["trace"], y["trace"])

    def test_reject_wrong_BL_and_changed_postcall_compare(self):
        wrong_call = bl_word(flow.CALLSITE, flow.getter.CALLEE + 4) + CALLER[4:]
        with self.assertRaisesRegex(ValueError, "Caller return-value"):
            flow.verify(wrong_call, FAKE_BODY)
        wrong_cmp = CALLER[:4] + bytes.fromhex("030050e3") + CALLER[8:]
        with self.assertRaisesRegex(ValueError, "Caller return-value"):
            flow.verify(wrong_cmp, FAKE_BODY)

    def test_refuse_unmodelled_return_value(self):
        with self.assertRaisesRegex(ValueError, "Controlled return value"):
            flow.execute(CALLER, FAKE_BODY, 0xDEADBEEF,
                         branch.CPSR_STATES[0])


if __name__ == "__main__":
    unittest.main()
