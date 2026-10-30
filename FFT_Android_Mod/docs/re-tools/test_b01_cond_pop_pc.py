"""B01 conditional ARM POP PC: true/false return with synthetic stack.

Independent C model and Unicorn must agree for all sixteen NZCV states.
"""
import ctypes
import tempfile
import unittest
from pathlib import Path

import b01_cond_pop_pc_differential as conditional
import b01_pop_pc_differential as prior

DIR=Path(__file__).resolve().parent


class ConditionalPopTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp=tempfile.TemporaryDirectory()
        cls.model=conditional.model_fn(
            DIR/"c-models/b01_pop_pc.c",
            DIR/"c-models/b01_cond_pop_pc.c",
            Path(cls.temp.name)/"model.so")

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def test_four_real_encoding_shapes_both_branches(self):
        # These A32 opcodes have conditions HI, GE, NE and CC.
        for word in (0x88bd8030,0xa8bd8030,0x18bd8030,0x38bd8030):
            with self.subTest(word=hex(word)):
                raw=word.to_bytes(4,"little")
                self.assertTrue(conditional.is_conditional_pop(raw))
                both={conditional.test_one(0x200000,raw,self.model,1,flags)
                      for flags in conditional.NZCV_STATES}
                self.assertEqual(both,{True,False})

    def test_c_rejects_invalid_encoding_without_mutation(self):
        regs=[0]*16
        regs[13]=prior.STACK
        rc=(ctypes.c_uint32*16)(*regs)
        stack=(ctypes.c_uint8*prior.STORAGE)()
        dest=ctypes.c_uint32()
        took=ctypes.c_int()
        for opcode in (0xf8bd8030,0xe8bd2000,0x18bd2010,0x18bd0010):
            with self.subTest(word=hex(opcode)):
                self.assertFalse(conditional.is_conditional_pop(opcode.to_bytes(4,"little")))
                result=self.model(opcode,rc,stack,prior.STORAGE,0x10,
                                  0x200000,ctypes.byref(dest),ctypes.byref(took))
                self.assertNotEqual(result,0)
                self.assertEqual(list(rc),regs)

    def test_true_branch_restores_sp_false_branch_does_not(self):
        raw=(0x18bd8030).to_bytes(4,"little") # NE
        # Z=0 -> condition true; Z=1 -> condition false
        self.assertTrue(conditional.test_one(0x200000,raw,self.model,0,0))
        self.assertFalse(conditional.test_one(0x200000,raw,self.model,0,0x40000000))


if __name__=="__main__":
    unittest.main()
