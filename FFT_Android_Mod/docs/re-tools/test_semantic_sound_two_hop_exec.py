"""Original ELF two-hop sound_request branch microexecution regressions."""
import unittest

import semantic_evidence
import semantic_sound_two_hop_exec as relay


class SoundTwoHopTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.binary = semantic_evidence.ROOT / "src/lib/armeabi/libgl2jni.so"
        cls.code = relay.original_code(cls.binary)

    def test_original_a32_branch_signatures(self):
        self.assertTrue(relay.validate(self.code))
        self.assertEqual((relay.SOUND, relay.RELAY, relay.UNKNOWN),
                         (0x26B374, 0x2168E0, 0x271314))

    def test_bounded_unicorn_branch_chain_preserves_state(self):
        for r0 in relay.R0_STATES:
            for cpsr in relay.CPSR_STATES:
                with self.subTest(r0=r0, cpsr=cpsr):
                    result = relay.execute(self.code, r0, cpsr)
                    self.assertEqual(result["trace"],
                                     (relay.SOUND, relay.RELAY, relay.UNKNOWN))
                    self.assertEqual(result["reads"], ())
                    self.assertEqual(result["writes"], ())
                    self.assertFalse(result["normal_return_verified"])

    def test_reject_mutated_opcode_and_unapproved_states(self):
        for modified in ((b"\x00"*4, self.code[1]),
                         (self.code[0], b"\x00"*4)):
            with self.assertRaisesRegex(ValueError, "signature changed"):
                relay.validate(modified)
        with self.assertRaisesRegex(ValueError, "Unapproved initial"):
            relay.execute(self.code, 0x12345678, relay.CPSR_STATES[0])
        with self.assertRaisesRegex(ValueError, "Unapproved CPSR"):
            relay.execute(self.code, 0, 0xABCDEF10)

    def test_report_is_explicit_about_unknown_destination(self):
        report = relay.render(self.binary)
        self.assertIn("Microexecucoes Unicorn verificadas: 8", report)
        self.assertIn("ANTES da instrucao", report)
        self.assertIn("Nenhuma equivalencia de funcao", report)


if __name__ == "__main__":
    unittest.main()
