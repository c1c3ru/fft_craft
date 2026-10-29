"""Fail closed on A04 source-lineage overclaims, call clobbers and unproven NUL."""
import unittest
from semantic_a04_r1_sources import (last_derived_definition, split_operands,
                                      lane_for, opcode_base, is_reg)


def ins(pc, mnemonic, operands):
    return {"pc":f"{pc:08x}","mnemonic":mnemonic,
            "operands":operands,"hex":"00000000"}


class R1LineageTests(unittest.TestCase):
    def test_arm_memory_operand_not_broken_by_comma(self):
        self.assertEqual(split_operands("r1, [sp, #0x18]"),
                         ["r1","[sp, #0x18]"])

    def test_conditional_move_not_unconditional_reaching_def(self):
        result=last_derived_definition([ins(0x1000,"movne","r1, r7")])
        self.assertEqual(result["kind"],"conditional_definition_unknown")
        self.assertTrue(result["no_length_or_nul_proof"])

    def test_preserved_register_crosses_bl_but_r1_does_not(self):
        rows=[ins(0x1000,"mov","r5, r1"),
              ins(0x1004,"bl","#0x2cdf6c"),
              ins(0x1008,"mov","r1, r5")]
        result=last_derived_definition(rows)
        self.assertEqual(result["kind"],"incoming_abi_argument_candidate")
        self.assertEqual(result["terminal"],"r1")
        self.assertTrue(result["no_length_or_nul_proof"])
        clobbered=last_derived_definition([ins(0x1000,"mov","r1, r2"),
                                           ins(0x1004,"bl","#0x71494")])
        self.assertEqual(clobbered["kind"],"volatile_across_call_unknown")

    def test_stack_spill_is_only_candidate(self):
        result=last_derived_definition([ins(0x1000,"ldr","r1, [sp, #4]")])
        self.assertEqual(result["kind"],"stack_slot_candidate")
        self.assertFalse("bounded" in result["kind"])
        self.assertTrue(result["no_length_or_nul_proof"])

    def test_explicit_null_branch_is_only_syntactic(self):
        result=last_derived_definition([ins(0x1000,"mov","r1, #0")])
        self.assertEqual(result["kind"],"syntactic_null_constant")
        self.assertTrue(result["no_length_or_nul_proof"])

    def test_untracked_arithmetic_is_not_proof(self):
        result=last_derived_definition([ins(0x1000,"add","r1, r3, r5")])
        self.assertEqual(result["kind"],"arithmetic_or_computed_pointer_candidate")

    def test_abi_aliases(self):
        self.assertTrue(is_reg("sb"))
        result=last_derived_definition([ins(0x1000,"mov","r1, sb")])
        self.assertEqual(result["terminal"],"r9")

    def test_lanes_are_disjoint_by_symbol(self):
        self.assertEqual(lane_for({"symbol_owners":[{"name":"CEGL2_SHADER::Load"}]}),"shader")
        self.assertEqual(lane_for({"symbol_owners":[{"name":"CFILE_TXT::Save"}]}),"file-io")
        self.assertEqual(lane_for({"symbol_owners":[{"name":"_Zother"}]}),"other")

    def test_unknown_opcode_not_safe(self):
        result=last_derived_definition([ins(0x1000,"mul","r1, r2, r3")])
        self.assertEqual(result["kind"],"unsupported_register_def")
        self.assertTrue(result["no_length_or_nul_proof"])


if __name__=="__main__":
    unittest.main()
