"""Original ELF regression checks for the sound destination 0x271314 audit."""
import unittest

import semantic_evidence
import semantic_sound_destination_271314 as target


class SoundDestinationAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.binary = semantic_evidence.ROOT / "src/lib/armeabi/libgl2jni.so"

    def test_original_branch_entries_are_distinct(self):
        digest, code, incoming, insns = target.inspect(self.binary)
        self.assertEqual(digest, target.prior.ELF_SHA256)
        self.assertEqual(len(code), 96)
        self.assertEqual(len(insns), 24)
        self.assertEqual([i[1] for i in incoming[1:]], list(target.ENTRIES)[::2] +
                         [target.ENTRIES[1]])
        self.assertEqual(len(set(target.ENTRIES)), 3)

    def test_original_window_is_not_misrepresented_as_execution(self):
        text = target.render(self.binary)
        self.assertIn("Novas certificacoes: 0", text)
        self.assertIn("Ainda NAO executado", text)
        self.assertIn("0x271314 (entry)", text)
        self.assertIn("0x271318 (entry)", text)
        self.assertIn("0x27131c (entry)", text)
        self.assertIn("0x2168e0", text)

    def test_fails_closed_on_mutated_branch(self):
        original = target.semantic_evidence.read_function
        def swapped(binary, addr, size):
            if addr == 0x2168E0:
                return bytes.fromhex("0000a0e1")
            return original(binary, addr, size)
        from unittest.mock import patch
        with patch.object(target.semantic_evidence, "read_function",
                          side_effect=swapped):
            with self.assertRaisesRegex(ValueError, "Changed ARM branch"):
                target.inspect(self.binary)


if __name__ == "__main__":
    unittest.main()
