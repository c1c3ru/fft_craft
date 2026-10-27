"""Regression tests for SysSE_PlayDef original ELF entry audit."""
import hashlib
import unittest
from unittest.mock import patch

import semantic_evidence
import semantic_sound_playdef_entry as m


class SoundPlayDefEntryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.binary = semantic_evidence.ROOT / "src/lib/armeabi/libgl2jni.so"

    def test_original_entry_disassembles_and_reports_original_bytes(self):
        code, instructions = m.inspect(self.binary)
        self.assertEqual(len(code), 128)
        self.assertEqual(len(instructions), 32)
        self.assertEqual(instructions[0].address, 0x2B2CF8)
        text = m.render(self.binary)
        self.assertIn(hashlib.sha256(code).hexdigest(), text)
        self.assertIn("Nenhuma instrução de SysSE_PlayDef foi executada", text)
        self.assertIn("Nenhuma função adicional é certificada", text)

    def test_fails_closed_on_binary_identity_drift(self):
        with patch.object(m.hashlib, "sha256") as digest:
            digest.return_value.hexdigest.return_value = "bad"
            with self.assertRaisesRegex(ValueError, "SHA-256 mismatch"):
                m.inspect(self.binary)

    def test_predecessor_must_be_verified(self):
        with patch.object(m.upstream, "original_words", side_effect=ValueError("drift")):
            with self.assertRaisesRegex(ValueError, "drift"):
                m.inspect(self.binary)


if __name__ == "__main__":
    unittest.main()
