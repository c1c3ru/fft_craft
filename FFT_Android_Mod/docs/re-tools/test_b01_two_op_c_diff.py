"""B01 candidate-xref section triage and independent C/Unicorn two-opcode gates."""
import ctypes
import tempfile
import unittest
from pathlib import Path

import b01_source_section_partition as partition
import b01_two_op_c_differential as diff
import b01_overlap_elf_evidence as baseline

HERE = Path(__file__).resolve().parent


def words(first, second):
    return first.to_bytes(4,"little") + second.to_bytes(4,"little")


class RegionPartitionTests(unittest.TestCase):
    def setUp(self):
        self.entries=[{"start":0x1000,"end":0x1020,"size":0x20},
                      {"start":0x1100,"end":0x1120,"size":0x20}]
        self.sections=[
            {"start":0x1000,"end":0x1200,"name":".text","elf_exec_flag":True},
            {"start":0x1200,"end":0x1250,"name":".rodata","elf_exec_flag":False}
        ]
        self.report={
            "source_elf_sha256":baseline.PINNED_ELF_SHA,
            "input_inventory_sha256":"c"*64,
            "confirmed_runtime_callers":0,
            "confirmed_executable_source_instructions":0,
            "all_linear_sweep_candidates":3,
            "tier_counts":{"no_inventory_owner":2,"unresolved_source":1},
            "sources_by_target":{
                "00002000":[
                    {"source":"00001004","target":"00002000","opcode":"000000ea","mnemonic":"b","tier":"unresolved_source","anchors":[{"owner":"00001000","tier":"no_v3_anchor"}]},
                    {"source":"00001060","target":"00002000","opcode":"000000ea","mnemonic":"b","tier":"no_inventory_owner","anchors":[]},
                    {"source":"00001210","target":"00002000","opcode":"000000ea","mnemonic":"b","tier":"no_inventory_owner","anchors":[]}
                ]
            }
        }

    def test_source_accounting_partition_and_no_promotion(self):
        x=partition.classify(self.report,self.sections,self.entries)
        self.assertEqual(x["xref_candidate_count"],3)
        self.assertEqual(x["partition_counts"]["inventory_gap_unproven"],2)
        self.assertEqual(x["partition_counts"]["owned_unresolved_not_confirmed"],1)
        self.assertEqual(x["elf_section_counts"]["non_exec_section"],1)
        self.assertEqual(x["elf_section_counts"]["exec_flagged_section"],2)
        self.assertFalse(any(v["source_instruction_confirmed"] for v in x["candidates"]))
        self.assertEqual(x["confirmed_call_edges"],0)

    def test_no_sections_are_not_necessarily_data(self):
        r=partition.section_for_address(self.sections,0x5000)
        self.assertIsNone(r)

    def test_section_chooses_most_specific(self):
        s=self.sections+[{"start":0x1000,"end":0x1010,
                          "name":".mini","elf_exec_flag":True}]
        self.assertEqual(partition.section_for_address(s,0x1004)["name"],".mini")

    def test_loss_and_duplicate_rejected(self):
        self.report["all_linear_sweep_candidates"]=4
        with self.assertRaises(ValueError):
            partition.classify(self.report,self.sections,self.entries)
        self.report["all_linear_sweep_candidates"]=3
        self.report["sources_by_target"]["00002000"][2]["source"]="00001060"
        with self.assertRaises(ValueError):
            partition.classify(self.report,self.sections,self.entries)

    def test_never_trust_proclaimed_runtime_confirmation(self):
        self.report["confirmed_runtime_callers"]=1
        with self.assertRaises(ValueError):
            partition.classify(self.report,self.sections,self.entries)


class TwoOpcodeDifferentialTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp=tempfile.TemporaryDirectory()
        cls.model=diff.build_c_model(
            HERE/"c-models/b01_two_op.c",Path(cls.tmp.name)/"b01_model.so")

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def gate(self,first,second):
        from capstone import Cs,CS_ARCH_ARM,CS_MODE_ARM
        c=diff.safe_pair(words(first,second),0x200000,
                         Cs(CS_ARCH_ARM,CS_MODE_ARM))
        return c

    def test_safe_alu_and_byte_or_word_memory(self):
        first=0xe2812003   # ADD R2, R1, #3
        for second,mnem in ((0xe5802008,"str"),(0xe590300c,"ldr"),
                            (0xe5c0200d,"strb"),(0xe5d0300f,"ldrb")):
            with self.subTest(opcode=hex(second)):
                pair=self.gate(first,second)
                self.assertIsNotNone(pair)
                self.assertEqual(pair["second"]["mnemonic"],mnem)
                for seed,flags in ((0,0),(1,0xf0000000),(0xffffffff,0)):
                    self.assertTrue(diff.differential_two(
                        0x200000,words(first,second),pair,
                        self.model,seed,flags))

    def test_model_rejects_invalid_memory_opcode_before_mutation(self):
        first=0xe2812003
        invalid=(0xe5812008,0xe5002008,0xe5802002,0xe5802600,
                 0xe5a02008,0xe5800008,0xe7802001)
        for second in invalid:
            with self.subTest(w=hex(second)):
                self.assertIsNone(self.gate(first,second))
                regs,mem=diff.sample_state(3)
                rb=(ctypes.c_uint32*13)(*regs)
                mb=(ctypes.c_uint8*diff.MEM_SIZE).from_buffer_copy(mem)
                code=self.model(first,second,rb,mb,len(mem))
                self.assertNotEqual(code,0)
                self.assertEqual(list(rb),regs)
                self.assertEqual(bytes(mb),bytes(mem))

    def test_unconditional_only_and_no_pc_stack_changes(self):
        second=0xe5802008
        for first in (0x12812003,0xe2912003,0xe281d003,0xe2800003,
                      0xe12fff1e,0xe5902004):
            with self.subTest(w=hex(first)):
                self.assertIsNone(self.gate(first,second))

    def test_boundary_offsets_and_c_model_bounds(self):
        first=0xe2812003
        for second in (0xe5802500,0xe5c02500):
            pair=self.gate(first,second)
            self.assertIsNotNone(pair)
            self.assertTrue(diff.differential_two(
                0x200000,words(first,second),pair,self.model,0x12345678,0))

    def test_c_canary_is_preserved(self):
        pair=self.gate(0xe2812003,0xe5802008)
        self.assertTrue(diff.differential_two(
            0x200000,words(0xe2812003,0xe5802008),pair,self.model,0xffffffff,0))


if __name__=="__main__":
    unittest.main()
