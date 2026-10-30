"""B01 independent named-C++ method and candidate prologue linkage tests."""
import tempfile
import unittest
from pathlib import Path

from capstone import Cs,CS_ARCH_ARM,CS_MODE_ARM

import b01_named_cpp_differential as cpp
import b01_prologue_external_audit as link
import b01_overlap_elf_evidence as base

HERE=Path(__file__).resolve().parent


def raw(*words):
    return b"".join(x.to_bytes(4,"little") for x in words)


class CppReconstructionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp=tempfile.TemporaryDirectory()
        cls.model=cpp.build_cpp(HERE/"c-models/b01_named_cpp_methods.cpp",
                                Path(cls.temp.name)/"reimpl.so")
        cls.disassembler=Cs(CS_ARCH_ARM,CS_MODE_ARM)

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def test_original_shape_and_cpp_store_return(self):
        # MOV R2,#2; STR R2,[R0,#20]; BX LR.
        address=0x000b9f7c
        inst=raw(0xe3a02002,0xe5802014,0xe12fff1e)
        spec=cpp.check_opcode_contract(address,inst,self.disassembler)
        self.assertEqual(spec["third_kind"],"bx_lr")
        for shift in (0,0x100,0x200):
            for flags in (0,0xf0000000):
                self.assertTrue(cpp.compare_case(address,inst,0x14,2,
                    self.model,shift,0xffffffff,flags,0x710000))

    def test_invalid_object_null_and_unknown_method_are_fail_closed(self):
        self.assertEqual(cpp.reject_invalid_object_buffers(self.model),43)

    def test_mismatch_original_opcode_rejected(self):
        with self.assertRaises(ValueError):
            cpp.check_opcode_contract(0x000b9f7c,
                raw(0xe3a02008,0xe5802014,0xe12fff1e),self.disassembler)
        with self.assertRaises(ValueError):
            cpp.check_opcode_contract(0x000b9f7c,
                raw(0xe3a02002,0xe5802020,0xe12fff1e),self.disassembler)

    def test_exact_seven_methods_not_nine_aliased_names(self):
        self.assertEqual(len(cpp.EXPECTED),7)
        self.assertEqual(set(cpp.EXPECTED),set(cpp.abi.SEVEN))


class PrologueCandidateTests(unittest.TestCase):
    def test_push_pop_mask_with_lr_to_pc_and_no_runtime_promotion(self):
        # PUSH {r4,lr}; POP {r4,pc}.
        steps=[{"pc":"00001000","bytes":raw(0xe92d4010).hex()},
               {"pc":"00001004","bytes":raw(0xe1a00000).hex()},
               {"pc":"00001008","bytes":raw(0xe8bd8010).hex()}]
        cases=link.paired_prologue_candidates(steps,0x1008,0x8010)
        self.assertEqual(len(cases),1)
        self.assertTrue(cases[0]["same_saved_registers_except_lr_to_pc"])
        self.assertFalse(cases[0]["path_sensitive_and_stack_aliasing_proven"])

    def test_pop_condition_and_mismatched_register_mask(self):
        self.assertEqual(link.pop_mask(0x18bd8010),0x8010)
        self.assertIsNone(link.pop_mask(0xe8bd2010))
        self.assertIsNone(link.push_mask(0xe92d8000))
        cases=link.paired_prologue_candidates(
            [{"pc":"00001000","bytes":raw(0xe92d4000).hex()}],0x1008,0x8010)
        self.assertFalse(cases[0]["same_saved_registers_except_lr_to_pc"])

    def test_inventory_target_remains_unproven(self):
        paths=[{
            "entry":"00001000",
            "decoded":[{"pc":"00001000","bytes":raw(0xe92d4010).hex()},
                       {"pc":"00001008","bytes":raw(0xe8bd8010).hex()}],
            "unresolved_boundaries":[
                {"at":"00001008","reason":"return_via_stack_not_modeled"},
                {"at":"00001004","reason":"callee_effects_and_return_unknown","target":"00002000"}]
        }]
        state={
            "elf_sha256":base.PINNED_ELF_SHA,
            "groups":[{"common_end":"0000100c","entry_witnesses":paths}],
            "group_count":1,
            "boundary_reason_counts":{
                "return_via_stack_not_modeled":1,
                "callee_effects_and_return_unknown":1,
                "out_of_group_direct_edge":0}}
        # A synthetic group can't meet the exact original 28/14/10 gate;
        # fail closed instead of silently skipping the missing occurrences.
        with self.assertRaises(ValueError):
            link.classify(state,[{"start":0x2000,"end":0x2010}])


if __name__=="__main__":
    unittest.main()
