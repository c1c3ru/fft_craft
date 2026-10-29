"""Batch classifier must expand A04 candidates without certifying buffers."""
import unittest
from semantic_a04_xrefs_batch import classify


def row(pc="000a2ecc",middle=None):
    if middle is None:
        middle = [("000a2ec4","mov","r1, r7"),
                  ("000a2ec8","mov","r5, r0")]
    rows=[{"pc":"000a2ebc","mnemonic":"mov","operands":"r0, #0x10c"},
          {"pc":"000a2ec0","mnemonic":"bl","operands":"#0x2cdf6c"}]
    rows += [{"pc":a,"mnemonic":b,"operands":c} for a,b,c in middle]
    rows += [{"pc":pc,"mnemonic":"bl","operands":"#0xb6620"}]
    return {"callsite":pc,"target":"000b6620",
            "context_linear_not_cfg":rows}


class CallerBatchTests(unittest.TestCase):
    def test_old_strict_caller_remains(self):
        r=classify(row())
        self.assertEqual(r["class"],"new_0x10c_candidate")
        self.assertTrue(r["strict_old_rule"])
        self.assertFalse(r["actual_allocated_capacity_proven"])

    def test_ldr_r1_and_str_r0_allowed(self):
        r=classify(row(middle=[
            ("000a2ec4","ldr","r1, [sp, #4]"),
            ("000a2ec8","str","r0, [sp, #0xc]")]))
        self.assertEqual(r["class"],"new_0x10c_candidate")
        self.assertFalse(r["strict_old_rule"])
        self.assertFalse(r["source_length_proven"])

    def test_intervening_r0_clobber_refused(self):
        r=classify(row(middle=[
            ("000a2ec4","mov","r1, r7"),
            ("000a2ec8","mov","r0, #0")]))
        self.assertNotEqual(r["class"],"new_0x10c_candidate")

    def test_missing_source_assignment_refused(self):
        r=classify(row(middle=[
            ("000a2ec4","str","r1, [sp]"),
            ("000a2ec8","mov","r5, r0")]))
        self.assertNotEqual(r["class"],"new_0x10c_candidate")

    def test_shader_stack_case_stays_unproven(self):
        r=row("000ab6cc",middle=[("000a2ec4","mov","r1, sb"),
                                    ("000a2ec8","add","r6, sp, #0x120")])
        r["context_linear_not_cfg"] = r["context_linear_not_cfg"][2:]
        self.assertEqual(classify(r)["class"],"shader_stack_pointer_candidate")

    def test_shader_carried_pointer_stays_unproven(self):
        r=row("000ab6a4",middle=[])
        r["context_linear_not_cfg"] = [r["context_linear_not_cfg"][-1]]
        self.assertEqual(classify(r)["class"],"shader_carried_pointer_candidate")


if __name__ == "__main__":
    unittest.main()
