"""Regression tests of ARM post-getter destinations, writes and boundaries."""
import unittest

import semantic_evidence
import semantic_v2icon_destinations as nextstep
import semantic_v2icon_call_flow as flow
import semantic_callee_v2icon as getter
import semantic_branch_microexec as branches


class PostGetterDestinationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        binary = semantic_evidence.ROOT / "src/lib/armeabi/libgl2jni.so"
        cls.caller = semantic_evidence.read_function(
            binary, nextstep.START, nextstep.MAIN_END - nextstep.START)
        cls.body = semantic_evidence.read_function(
            binary, getter.CALLEE, getter.CALLEE_SIZE)
        cls.followup = semantic_evidence.read_function(
            binary, nextstep.EXTRA_CALL, 4)
        cls.literal = int.from_bytes(
            semantic_evidence.read_function(
                binary, nextstep.CALLER_LITERAL_ADDR, 4), "little")

    def test_exact_original_opcode_signatures(self):
        literal = nextstep.validate(
            self.caller, self.body, self.followup, self.literal)
        self.assertEqual(literal, 0x01723FA8)

    def test_all_branch_types_are_distinct(self):
        scenarios = [
            (2, 0, "setter_call", nextstep.CALL_SETTER),
            (1, 0, "followup_call", nextstep.CALL_FOLLOWUP),
            (1, 0x40, "status_call", nextstep.CALL_STATUS),
            (0, 0, "pop_return", nextstep.RETURN_PC),
            (0, 0x20, "followup_call", nextstep.CALL_FOLLOWUP),
            (0, 0x40, "status_call", nextstep.CALL_STATUS),
            (0xFFFFFFFF, 0x60, "status_call", nextstep.CALL_STATUS),
        ]
        for value, flag, kind, address in scenarios:
            with self.subTest(value=value, flag=flag):
                self.assertEqual(nextstep.route(value, flag), (kind, address))
                r = nextstep.execute(
                    self.caller, self.body, self.followup, self.literal,
                    value, flag, branches.CPSR_STATES[0])
                self.assertEqual(r["kind"], kind)
                self.assertEqual(r["endpoint"], address)
                self.assertEqual(r["trace"], nextstep.expected_trace(value, flag))

    def test_flags_are_not_taken_from_prior_nzcv(self):
        for val, flag in ((1, 0), (1, 0x40), (0, 0x20), (0, 0), (2, 0)):
            with self.subTest(value=val, flag=flag):
                args = (self.caller, self.body, self.followup, self.literal,
                        val, flag)
                a = nextstep.execute(*args, branches.CPSR_STATES[0])
                b = nextstep.execute(*args, branches.CPSR_STATES[1])
                self.assertEqual(a["trace"], b["trace"])
                self.assertEqual(a["writes"], b["writes"])

    def test_mutation_rejected_before_execution(self):
        code = bytearray(self.caller)
        code[-4] ^= 1
        with self.assertRaisesRegex(ValueError, "destination instructions"):
            nextstep.validate(bytes(code), self.body, self.followup, self.literal)
        with self.assertRaisesRegex(ValueError, "literal changed"):
            nextstep.validate(self.caller, self.body, self.followup,
                              self.literal ^ 0x10)

    def test_bad_input_rejected(self):
        with self.assertRaisesRegex(ValueError, "Unexpected sampled"):
            nextstep.execute(
                self.caller, self.body, self.followup, self.literal,
                0xDEADBEEF, 0, branches.CPSR_STATES[0])


if __name__ == "__main__":
    unittest.main()
