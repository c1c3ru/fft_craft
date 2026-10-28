"""Original A32 stack-and-literal sound common prologue vs C model."""
import unittest
from unittest.mock import patch

import semantic_evidence
import semantic_sound_common_prologue as m
import semantic_sound_three_entry_exec as samples


class SoundCommonPrologueTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.binary = semantic_evidence.ROOT / "src/lib/armeabi/libgl2jni.so"
        cls.code, cls.literal = m.original(cls.binary)

    def test_exact_original_arm_words_and_literal(self):
        self.assertTrue(m.validate(self.code))
        self.assertEqual(self.code.hex(), m.PREFIX_HEX + m.STOP_HEX)
        self.assertEqual(len(self.literal), 4)
        self.assertEqual(m.LITERAL_ADDR, 0x2B2CE8)

    def test_all_128_states_have_real_stack_literal_register_evidence(self):
        counted = 0
        for arg in samples.R0_STATES:
            for nzcv in range(16):
                with self.subTest(arg=arg, nzcv=nzcv):
                    result = m.arm_execute(self.code, self.literal, arg, nzcv)
                    self.assertEqual(result[0], 0x2B2B90)
                    self.assertEqual(result[1], m.STACK_TOP - 64)
                    self.assertEqual(result[2], 0)
                    self.assertEqual(result[3], arg)
                    self.assertEqual(result[4],
                                     int.from_bytes(self.literal, "little"))
                    self.assertEqual(result[5], arg)
                    self.assertEqual(result[6], 0)
                    self.assertEqual(len(result[7]), 8)
                    counted += 1
        self.assertEqual(counted, 128)

    def test_compiled_independent_c_model_agrees_with_original_arm(self):
        count, literal = m.verify(self.binary)
        self.assertEqual(count, 128)
        self.assertEqual(literal, self.literal)

    def test_fails_closed_for_mutated_binary_or_input(self):
        mutated = b"\x00" * 4 + self.code[4:]
        with self.assertRaisesRegex(ValueError, "signature changed"):
            m.validate(mutated)
        with self.assertRaisesRegex(ValueError, "Unsupported input"):
            m.arm_execute(self.code, self.literal, 0xBADC0DE, 0)
        with self.assertRaisesRegex(ValueError, "Invalid original literal"):
            m.arm_execute(self.code, b"\x00", 0, 0)
        with patch.object(m.hashlib, "sha256") as mocked:
            mocked.return_value.hexdigest.return_value = "0" * 64
            with self.assertRaisesRegex(ValueError, "Wrong original ELF"):
                m.original(self.binary)

    def test_report_is_partial_and_stops_before_global_load(self):
        report = m.render(self.binary)
        self.assertIn("128/128 PASS", report)
        self.assertIn("640", report)
        self.assertIn("ANTES de 0x2b2b90", report)
        self.assertIn("Nenhuma função adicional certificada", report)


if __name__ == "__main__":
    unittest.main()
