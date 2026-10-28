"""Fail-closed original ELF sound global slot audit and controlled LDR tests."""
import unittest

import semantic_evidence
import semantic_sound_global_slot as m
import semantic_sound_three_entry_exec as inputs


class SoundGlobalSlotTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.binary = semantic_evidence.ROOT / "src/lib/armeabi/libgl2jni.so"
        cls.code, cls.slot, cls.literal = m.provenance(cls.binary)

    def test_original_elf_slot_and_relocation_metadata(self):
        self.assertEqual(self.slot, 0x34615C)
        self.assertEqual(self.literal, 0x935C4)
        self.assertEqual(self.code, m.ORIGINAL_CODE)
        backing, relocs = m.elf_slot_metadata(self.binary, self.slot)
        self.assertIn("file_backed", backing)
        self.assertIn("flags", backing)
        self.assertIsInstance(relocs, list)

    def test_controlled_original_ldr_all_512_cases(self):
        count = 0
        for arg in inputs.R0_STATES:
            for flags in range(16):
                for value in m.VALUES:
                    with self.subTest(arg=arg, flags=flags, value=value):
                        result = m.execute(self.code, self.slot,
                                           self.literal, arg, flags, value)
                        self.assertEqual(result["pc"], m.NEXT)
                        self.assertEqual(result["r0"], value)
                        self.assertEqual(result["reads"], ((self.slot, 4),))
                        self.assertEqual(result["writes"], ())
                        self.assertFalse(result["actual_runtime_value_proven"])
                        self.assertFalse(result["new_certificate"])
                        count += 1
        self.assertEqual(count, 512)

    def test_changed_code_address_or_fixture_rejected(self):
        for code, addr, word in (
            (b"\x00"*4 + self.code[4:], self.slot, 0),
            (self.code, self.slot + 4, 0),
            (self.code, self.slot, 0xDEADBEEF),
        ):
            with self.assertRaisesRegex(ValueError, "Unsupported original"):
                m.execute(code, addr, self.literal, 0, 0, word)

    def test_report_distinguishes_elf_file_from_runtime_global(self):
        report = m.render(self.binary)
        self.assertIn("0x34615c", report)
        self.assertIn("0x000935c4", report)
        self.assertIn("512 execuções Unicorn", report)
        self.assertIn("SINTÉTICOS", report)
        self.assertIn("Nenhum valor de memória do processo original", report)
        self.assertIn("Novos certificados semânticos: 0", report)


if __name__ == "__main__":
    unittest.main()
