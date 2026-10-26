"""Real ARM GetParam and GetScale individual + linked callsite tests."""
import unittest

import semantic_getparam_getscale_exec as machines
import semantic_branch_microexec as branch
from test_semantic_callee_v2icon import bl_word

PARAM = bytes.fromhex("0e1081e2 010190e7 1eff2fe1")
SCALE = bytes.fromhex("000051e3 04309015 00308115 1eff2fe1")
PARAM_BL = bl_word(machines.PARAM_CALLSITE,machines.GET_PARAM)
SCALE_BL = bl_word(machines.SCALE_CALLSITE,machines.GET_SCALE)


class GetterMachineTests(unittest.TestCase):
    def test_exact_original_signatures(self):
        machines.exact_opcode(PARAM,machines.GET_PARAM,machines.PARAM_SIG)
        machines.exact_opcode(SCALE,machines.GET_SCALE,machines.SCALE_SIG)
        machines.exact_bl(PARAM_BL,machines.PARAM_CALLSITE,machines.GET_PARAM)
        machines.exact_bl(SCALE_BL,machines.SCALE_CALLSITE,machines.GET_SCALE)

    def test_param_indexed_load_and_linked_return(self):
        for mode in machines.MODES:
            for idx in machines.INDICES:
                for word in machines.WORDS:
                    with self.subTest(mode=mode,index=idx,word=word):
                        result=machines.getparam(
                            PARAM,PARAM_BL,idx,word,branch.CPSR_STATES[0],mode)
                        self.assertEqual(result["value"],word)
                        self.assertEqual(result["slot"],machines.TABLE+4*(idx+14))

    def test_scale_null_is_noop_nonnull_is_conditional_copy(self):
        for mode in machines.MODES:
            for value in machines.WORDS:
                for nonnull in (False,True):
                    with self.subTest(mode=mode,value=value,nonnull=nonnull):
                        r=machines.getscale(SCALE,SCALE_BL,value,nonnull,
                                            branch.CPSR_STATES[1],mode)
                        self.assertEqual(r["written"],nonnull)

    def test_initial_flags_do_not_change_postconditions(self):
        for mode in machines.MODES:
            for seed in branch.CPSR_STATES:
                self.assertEqual(
                    machines.getparam(PARAM,PARAM_BL,0x28,0x12345678,seed,mode)
                    ["value"],0x12345678)
                self.assertTrue(
                    machines.getscale(SCALE,SCALE_BL,0x40,True,seed,mode)
                    ["written"])

    def test_mutation_and_unmodeled_input_rejected(self):
        changed=bytearray(SCALE)
        changed[8]^=1
        with self.assertRaisesRegex(ValueError,"opcode signature changed"):
            machines.getscale(bytes(changed),SCALE_BL,1,True,
                              branch.CPSR_STATES[0],"standalone")
        wrong_bl=bl_word(machines.SCALE_CALLSITE,machines.GET_SCALE+4)
        with self.assertRaisesRegex(ValueError,"Original BL target changed"):
            machines.getscale(SCALE,wrong_bl,1,True,
                              branch.CPSR_STATES[0],"standalone")
        with self.assertRaisesRegex(ValueError,"Unmodeled GetParam"):
            machines.getparam(PARAM,PARAM_BL,999,0,
                              branch.CPSR_STATES[0],"standalone")

    def test_exact_elf_machine_words(self):
        elf=machines.semantic_evidence.ROOT/"src/lib/armeabi/libgl2jni.so"
        if not elf.is_file():
            self.skipTest("Original ELF absent in checkout")
        self.assertEqual(machines.semantic_evidence.read_function(
            elf,machines.GET_PARAM,12),PARAM)
        self.assertEqual(machines.semantic_evidence.read_function(
            elf,machines.GET_SCALE,16),SCALE)


if __name__=="__main__":
    unittest.main()
