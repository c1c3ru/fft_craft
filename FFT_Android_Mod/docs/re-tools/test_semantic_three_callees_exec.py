"""Real-ELF tests for all three callees and two caller continuations."""
import unittest
import semantic_evidence
import semantic_three_callees_exec as m
import semantic_branch_microexec as branches


class ThreeCalleeMachineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        binary = semantic_evidence.ROOT / "src/lib/armeabi/libgl2jni.so"
        cls.code = m.read_code(binary)

    def test_all_opcode_signatures_and_target_addresses(self):
        self.assertTrue(m.validate(self.code))
        self.assertEqual(m.table_slot(37), 0x19DCA18)
        self.assertEqual(m.table_slot(49), 0x19DCA48)
        self.assertEqual(m.table_slot(52), 0x19DCA54)

    def test_setter_index_special_and_normal(self):
        for index in (37,49,52):
            for value in m.VALUES:
                with self.subTest(index=index, value=value):
                    r=m.execute(self.code,"setter",index,value,branches.CPSR_STATES[0])
                    self.assertEqual(r["writes"],[(m.table_slot(index),4,value)])
                    self.assertEqual(r["end"],m.SPECIAL_TARGET if index==37 else m.RETURN_PC)

    def test_clear_routes_into_setter_without_new_stack_frame(self):
        for value in m.VALUES:
            with self.subTest(seed=value):
                r=m.execute(self.code,"clear",37,value,branches.CPSR_STATES[0])
                self.assertEqual(r["writes"],[(m.table_slot(49),4,0)])
                self.assertEqual(r["end"],m.RETURN_PC)

    def test_sound_is_redirect_not_synthetic_sound_effect(self):
        r=m.execute(self.code,"sound",52,0x40,branches.CPSR_STATES[1])
        self.assertEqual(r["writes"],[])
        self.assertEqual(r["reads"],[])
        self.assertEqual(r["end"],m.SOUND_TARGET)

    def test_caller_setter_executes_write_then_pop(self):
        for state in (0,0xffffffff):
            r=m.execute(self.code,"caller_setter",49,state,branches.CPSR_STATES[0])
            self.assertEqual(r["writes"],[(m.OBJECT+8,4,1),
                                            (m.table_slot(52),4,0),
                                            (m.OBJECT+0x14,4,1)])
            self.assertEqual(r["end"],m.RETURN_PC)

    def test_caller_clear_then_sound_redirect(self):
        r=m.execute(self.code,"caller_clear_sound",52,0x40,branches.CPSR_STATES[0])
        self.assertEqual(r["writes"],[(m.table_slot(49),4,0)])
        self.assertEqual(r["end"],m.SOUND_TARGET)

    def test_mutation_and_invalid_index_refused(self):
        changed=dict(self.code)
        altered=bytearray(changed["clear"])
        altered[0]^=1
        changed["clear"]=bytes(altered)
        with self.assertRaisesRegex(ValueError, "signature changed"):
            m.validate(changed)
        with self.assertRaisesRegex(ValueError, "Unexpected sampled"):
            m.execute(self.code,"setter",100,0,branches.CPSR_STATES[0])


if __name__=="__main__":
    unittest.main()
