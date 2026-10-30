"""B01 original ARM recursive CFG candidates and three-opcode C11 differential."""
import ctypes
import io
import tempfile
import unittest
from pathlib import Path

from capstone import Cs,CS_ARCH_ARM,CS_MODE_ARM

import b01_recursive_group_paths as paths
import b01_three_op_c_differential as triple
import b01_two_op_c_differential as two


class FakeELF:
    def __init__(self,size,start=0x1000):
        self.size=size
        self.start=start

    def iter_segments(self):
        return [{"p_type":"PT_LOAD","p_flags":5,
                 "p_vaddr":self.start,"p_offset":0,
                 "p_filesz":self.size}]


def words(*ops):
    return b"".join(x.to_bytes(4,"little") for x in ops)


class RecursiveGroupTests(unittest.TestCase):
    def setUp(self):
        self.md=Cs(CS_ARCH_ARM,CS_MODE_ARM)
        self.md.detail=True

    def test_unconditional_branch_skips_inline_words_before_bx_lr(self):
        # B 0x100c; three words not all reachable from 0x1000.
        data=words(0xea000001,0xe3a00001,0xe3a00002,0xe12fff1e)
        state=paths.walk(FakeELF(len(data)),io.BytesIO(data),
                         0x1000,0x1010,0x1000,self.md,set())
        self.assertEqual(state["candidate_decoded_slots"],2)
        self.assertEqual([e["pc"] for e in state["decoded"]],["00001000","0000100c"])
        self.assertEqual(len(state["candidate_returns"]),1)
        self.assertFalse(state["all_edges_proven"])

    def test_bx_reg_is_held_as_unresolved_indirect(self):
        data=words(0xe12fff13) # BX R3
        state=paths.walk(FakeELF(len(data)),io.BytesIO(data),
                         0x1000,0x1004,0x1000,self.md,set())
        self.assertEqual(state["unresolved_boundaries"][0]["reason"],
                         "bx_indirect_unresolved")
        self.assertEqual(state["candidate_returns"],[])

    def test_ldr_pc_literal_cannot_claim_runtime_resolution(self):
        data=words(0xe59ff000,0xe3a00002,0x100f) # LDR PC,[PC,#0] -> 0x1008
        elf=FakeELF(len(data))
        state=paths.walk(elf,io.BytesIO(data),0x1000,0x100c,0x1000,self.md,set())
        detail=state["unresolved_boundaries"][0]["detail"]
        self.assertEqual(detail["classification"],"unrelocated_literal_target_candidate")
        self.assertTrue(detail["thumb_bit"])
        self.assertFalse(detail["runtime_target_verified"])
        relocated=paths.resolve_ldr_pc_slot(0xe59ff000,0x1000,elf,
                                           io.BytesIO(data),{0x1008})
        self.assertEqual(relocated["classification"],"relocation_dependent_literal_slot")

    def test_outside_group_direct_target_is_explicitly_unknown(self):
        data=words(0xea000006)
        state=paths.walk(FakeELF(len(data)),io.BytesIO(data),
                         0x1000,0x1004,0x1000,self.md,set())
        self.assertEqual(state["unresolved_boundaries"][0]["reason"],
                         "out_of_group_direct_edge")

    def test_cfg_summary_does_not_promote_reachability(self):
        data=words(0xe1a00001,0xe12fff1e)
        state=paths.walk(FakeELF(len(data)),io.BytesIO(data),
                         0x1000,0x1008,0x1000,self.md,set())
        self.assertFalse(state["runtime_reachable"])
        self.assertFalse(state["semantically_certified"])
        self.assertEqual(len(state["candidate_returns"]),1)


class ThreeOpDifferentialTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp=tempfile.TemporaryDirectory()
        root=Path(__file__).resolve().parent
        cls.fn=triple.build_model(root/"c-models/b01_two_op.c",
                                  root/"c-models/b01_three_op.c",
                                  Path(cls.temp.name)/"triple.so")
        cls.md=Cs(CS_ARCH_ARM,CS_MODE_ARM)

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def test_alu_memory_alu_with_register_dependency(self):
        # ADD R2,R1,#3; LDR R3,[R0,#0xC]; ADD R3,R3,#1
        raw=words(0xe2812003,0xe590300c,0xe2833001)
        c=triple.eligible_three(raw,0x200000,self.md)
        self.assertEqual(c["third_kind"],"alu")
        for seed in (0,1,0xffffffff):
            for flags in (0,0xf0000000):
                self.assertTrue(triple.run_case(0x200000,raw,c,self.fn,seed,flags))

    def test_alu_memory_store_then_bx_lr(self):
        raw=words(0xe2812003,0xe5802008,0xe12fff1e)
        c=triple.eligible_three(raw,0x200000,self.md)
        self.assertEqual(c["third_kind"],"bx_lr")
        for seed in (0,0xffffffff):
            self.assertTrue(triple.run_case(0x200000,raw,c,self.fn,seed,0))

    def test_byte_store_and_register_dependency(self):
        raw=words(0xe2812003,0xe5c0200d,0xe2824001)
        c=triple.eligible_three(raw,0x200000,self.md)
        self.assertIsNotNone(c)
        self.assertTrue(triple.run_case(0x200000,raw,c,self.fn,1,0xf0000000))

    def test_non_whitelisted_third_op_rejected(self):
        prefix=(0xe2812003,0xe5802008)
        for third in (0xe12fff13,0x12833001,0xe2800001,0xe590300c):
            with self.subTest(last=hex(third)):
                raw=words(*prefix,third)
                self.assertIsNone(triple.eligible_three(raw,0x200000,self.md))

    def test_model_fails_closed_without_altering_state(self):
        first,second,invalid=0xe2812003,0xe5802008,0xe12fff13
        registers,mem=two.sample_state(0)
        rr=(ctypes.c_uint32*13)(*registers)
        mm=(ctypes.c_uint8*two.MEM_SIZE).from_buffer_copy(mem)
        pc=ctypes.c_uint32()
        ret=ctypes.c_int()
        rc=self.fn(first,second,invalid,rr,mm,two.MEM_SIZE,
                   0x200000,triple.LR_SENTINEL,ctypes.byref(pc),ctypes.byref(ret))
        self.assertNotEqual(rc,0)
        self.assertEqual(list(rr),registers)
        self.assertEqual(bytes(mm),bytes(mem))


if __name__=="__main__":
    unittest.main()
