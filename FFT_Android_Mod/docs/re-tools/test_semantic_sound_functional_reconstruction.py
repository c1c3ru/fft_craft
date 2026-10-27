"""Fail-closed regression tests: original A32 sound prefix vs independent C model."""
import unittest

import semantic_evidence
import semantic_sound_functional_reconstruction as m
import semantic_sound_three_entry_exec as upstream


class SoundFunctionalReconstructionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.binary = semantic_evidence.ROOT / "src/lib/armeabi/libgl2jni.so"
        cls.sites, cls.prefix = m.original(cls.binary)

    def test_original_instruction_provenance(self):
        self.assertTrue(m.validate(self.prefix))
        self.assertEqual(self.prefix.hex(), m.PREFIX_HEX)
        self.assertEqual(m.TRACE[-1], 0x2B2B7C)
        self.assertEqual(len(m.TRACE), 7)

    def test_mutated_opcode_must_fail_closed(self):
        changed = bytes.fromhex("0000a0e1") + self.prefix[4:]
        with self.assertRaisesRegex(ValueError, "signature drift"):
            m.validate(changed)

    def test_original_arm_execution_preserves_non_outputs(self):
        result = m.execute(self.sites, self.prefix, 0xFFFFFFFF, 0xF0000010)
        self.assertEqual(result, (0x2B2B7C, 0, 0xFFFFFFFF))
        with self.assertRaisesRegex(ValueError, "Unsupported differential sample"):
            m.execute(self.sites, self.prefix, 5, upstream.CPSR_STATES[0])

    def test_real_elf_differential_against_c_128_cases(self):
        count, code = m.verify(self.binary)
        self.assertEqual(count, len(upstream.R0_STATES) * len(upstream.CPSR_STATES))
        self.assertEqual(code, self.prefix)

    def test_report_preserves_full_function_unknowns(self):
        report = m.render(self.binary)
        self.assertIn("128/128", report)
        self.assertIn("0x2b2b7c", report)
        self.assertIn("Nenhum certificado novo", report)
        self.assertIn("não se demonstrou equivalência integral", report)


if __name__ == "__main__":
    unittest.main()
