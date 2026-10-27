"""Fail-closed Unicorn tests on three original A32 sound-dispatcher entry paths."""
import unittest

import semantic_evidence
import semantic_sound_three_entry_exec as m


class SoundThreeEntryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.binary = semantic_evidence.ROOT / "src/lib/armeabi/libgl2jni.so"
        cls.words = m.original_words(cls.binary)

    def test_exact_original_opcode_signatures_and_destinations(self):
        self.assertTrue(m.validate(self.words))
        self.assertEqual(m.PATHS["sound_request"][1][-1], 0x2B2CF8)
        self.assertEqual(m.PATHS["relay_f4"][1][-1], 0x2B2448)
        self.assertEqual(m.PATHS["relay_e4"][1][-1], 0x2B2814)
        self.assertEqual(len(m.DESTINATIONS), 3)

    def test_all_384_original_arm_microexecutions(self):
        cases = 0
        for name, (_, trace, decrement) in m.PATHS.items():
            for r0 in m.R0_STATES:
                for cpsr in m.CPSR_STATES:
                    with self.subTest(mode=name, r0=r0, nzcv=cpsr):
                        result = m.execute(self.words, name, r0, cpsr)
                        self.assertEqual(result["trace"], trace)
                        self.assertEqual(result["destination"], trace[-1])
                        self.assertEqual(result["r0"],
                                         ((r0 - 1) & 0xFFFFFFFF)
                                         if decrement else r0)
                        self.assertEqual(result["data_reads"], ())
                        self.assertEqual(result["data_writes"], ())
                        self.assertFalse(result["fully_certified"])
                        self.assertFalse(result["destination_executed"])
                        cases += 1
        self.assertEqual(cases, 384)

    def test_reject_changed_original_word_or_unapproved_input(self):
        for site in (0x271314, 0x27131C, 0x2168E4):
            copy = dict(self.words)
            copy[site] = bytes.fromhex("0000a0e1")
            with self.subTest(site=site), self.assertRaisesRegex(
                    ValueError, "Changed original ARM sound opcode"):
                m.validate(copy)
        with self.assertRaisesRegex(ValueError, "Unsupported R0"):
            m.execute(self.words, "relay_e4", 0x55555555, m.CPSR_STATES[0])
        with self.assertRaisesRegex(ValueError, "Unsupported ARM mode"):
            m.execute(self.words, "relay_e4", 0, 0x4000001F)

    def test_report_explains_reachability_and_certification_boundaries(self):
        text = m.render(self.binary)
        self.assertIn("Microexecucoes Unicorn verificadas: 384", text)
        self.assertIn("0x2b2cf8", text)
        self.assertIn("0x2b2448", text)
        self.assertIn("0x2b2814", text)
        self.assertIn("nao foi provado", text)
        self.assertIn("Novos certificados neste relatorio: 0", text)


if __name__ == "__main__":
    unittest.main()
