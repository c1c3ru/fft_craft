"""Fail-closed tests for the two newly identified ARM call targets."""
import unittest
from unittest.mock import patch
from pathlib import Path
import tempfile
import csv

import semantic_sound_dispatch_audit as audit


class SoundDispatchAuditTests(unittest.TestCase):
    def test_expected_function_boundaries(self):
        self.assertEqual(audit.SOUND_DISPATCH, (
            0x2B2CF8, 12, "SysSE_PlayDef(int)"))
        self.assertEqual(audit.ICON_POSITION[0], 0x2B8900)
        self.assertEqual(audit.ICON_PREFIX_BYTES % 4, 0)

    def test_non_arm_word_rejected(self):
        with patch.object(audit.semantic_evidence, "read_function",
                          return_value=bytes.fromhex("0100a0e3") * 2):
            with self.assertRaisesRegex(ValueError, "not fully ARM"):
                audit.disassemble(Path("/unused"), 0x1000, 12)

    def test_inventory_mismatch_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "inventory.csv"
            with path.open("w", newline="") as stream:
                writer = csv.DictWriter(
                    stream, fieldnames=("address", "size", "demangled"))
                writer.writeheader()
                writer.writerow({
                    "address": "002b2cf8", "size": 16,
                    "demangled": "SysSE_PlayDef(int)"})
            with self.assertRaisesRegex(ValueError, "Inventory mismatch"):
                audit.matching_symbol(path, audit.SOUND_DISPATCH)

    def test_real_elf_sound_and_icon_addresses_are_readable(self):
        binary = audit.semantic_evidence.ROOT / "src/lib/armeabi/libgl2jni.so"
        if not binary.is_file():
            self.skipTest("Bundled ELF not available")
        _, sound = audit.disassemble(binary, 0x2B2CF8, 12)
        _, icon = audit.disassemble(binary, 0x2B8900, 96)
        self.assertEqual(len(sound), 3)
        self.assertEqual(len(icon), 24)


if __name__ == "__main__":
    unittest.main()
