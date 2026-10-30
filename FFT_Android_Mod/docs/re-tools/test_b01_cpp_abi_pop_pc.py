"""B01 full-declared-body ABI hypotheses and isolated stack returns.

Synthetic test bytes validate the testing harness, not original-game proofs.
"""
import ctypes
import tempfile
import unittest
from pathlib import Path
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM

import b01_seven_cpp_contracts as contracts
import b01_pop_pc_differential as stack
import b01_three_op_c_differential as triple

BASE=Path(__file__).resolve().parent


def opcodes(*ops):
    return b"".join(i.to_bytes(4,"little") for i in ops)


class MemberBodyContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp=tempfile.TemporaryDirectory()
        cls.model=triple.build_model(
            BASE/"c-models/b01_two_op.c",BASE/"c-models/b01_three_op.c",
            Path(cls.temp.name)/"three.so")
        cls.md=Cs(CS_ARCH_ARM,CS_MODE_ARM)

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def test_abi_this_shifts_flags_lr_and_canaries(self):
        raw=opcodes(0xe2812003,0xe5802008,0xe12fff1e)
        spec=triple.eligible_three(raw,0x200000,self.md)
        self.assertEqual(spec["third_kind"],"bx_lr")
        for shift in contracts.SHIFTS:
            for lr in contracts.LRS:
                for flags in contracts.FLAGS:
                    self.assertTrue(contracts.compare_full_declared_body(
                        0x200000,raw,spec,self.model,
                        seed=0x80000000,flags=flags,shift=shift,lr=lr))

    def test_load_byte_and_word_are_modeled(self):
        for second in (0xe590300c,0xe5d0300f,0xe5c0200d):
            raw=opcodes(0xe2812003,second,0xe12fff1e)
            spec=triple.eligible_three(raw,0x200000,self.md)
            self.assertIsNotNone(spec)
            self.assertTrue(contracts.compare_full_declared_body(
                0x200000,raw,spec,self.model,
                seed=1,flags=0,shift=0x100,lr=0x720000))

    def test_invalid_synthetic_object_scenario_rejected(self):
        raw=opcodes(0xe2812003,0xe5802008,0xe12fff1e)
        spec=triple.eligible_three(raw,0x200000,self.md)
        with self.assertRaises(ValueError):
            contracts.compare_full_declared_body(
                0x200000,raw,spec,self.model,0,0,0x123,0x710000)
        with self.assertRaises(ValueError):
            contracts.compare_full_declared_body(
                0x200000,raw,spec,self.model,0,0,0,0x799999)

    def test_seven_addresses_are_unique_and_reproducible(self):
        self.assertEqual(len(set(contracts.SEVEN)),7)
        self.assertEqual(contracts.REPETITIONS,96)

    def test_size_and_cpp_aliases_do_not_multiply_functions(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/"inventory.csv"
            header="address,size,mangled,demangled,status,section_ref\n"
            lines=[]
            for a in contracts.SEVEN:
                lines.append(f"{a:08x},12,_foo,Class::func(),read_structural,\n")
            lines.append(f"{contracts.SEVEN[0]:08x},12,_alias,Class::alias(),read_structural,\n")
            p.write_text(header+"".join(lines),encoding="utf-8")
            groups=contracts.names_by_entry(p)
            self.assertEqual(len(groups),7)
            self.assertEqual(len(groups[contracts.SEVEN[0]]),2)
            p.write_text((header+"".join(lines)).replace("000b3518,12,","000b3518,16,",1))
            with self.assertRaises(ValueError):
                contracts.names_by_entry(p)


class PopPcIsolatedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp=tempfile.TemporaryDirectory()
        cls.model=stack.c_model(
            BASE/"c-models/b01_pop_pc.c",
            Path(cls.temp.name)/"pop.so")

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def test_pop_registers_and_pc_return(self):
        for word in (0xe8bd8010,0xe8bd8ff0,0xe8bd8001,0xe8bdc010):
            with self.subTest(instruction=hex(word)):
                raw=word.to_bytes(4,"little")
                self.assertTrue(stack.is_safe_pop(raw))
                for flag in stack.FLAGS:
                    self.assertTrue(stack.compare_one(
                        0x200000,raw,self.model,0x12345678,flag))

    def test_disallow_non_al_and_sp_restore_and_non_pop(self):
        for word in (0x08bd8010,0xe8bd2010,0xe8bd0010,0xe12fff1e,0xe92d8010):
            with self.subTest(word=hex(word)):
                self.assertFalse(stack.is_safe_pop(word.to_bytes(4,"little")))

    def test_c_rejects_invalid_without_mutation(self):
        values=[1]*16
        values[13]=stack.STACK
        rb=(ctypes.c_uint32*16)(*values)
        mem=(ctypes.c_uint8*stack.STORAGE)(*([0]*stack.STORAGE))
        ret=ctypes.c_uint32()
        status=self.model(0xe8bd2001,rb,mem,stack.STORAGE,ctypes.byref(ret))
        self.assertNotEqual(status,0)
        self.assertEqual(list(rb),values)

    def test_c_stack_bounds_checked(self):
        values=[1]*16
        values[13]=stack.STACK
        rb=(ctypes.c_uint32*16)(*values)
        mem=(ctypes.c_uint8*4)(0,0,0,0)
        ret=ctypes.c_uint32()
        code=self.model(0xe8bd8010,rb,mem,4,ctypes.byref(ret))
        self.assertNotEqual(code,0)


if __name__=="__main__":
    unittest.main()
