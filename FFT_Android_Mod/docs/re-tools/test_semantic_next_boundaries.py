"""Boundary inspection is observational: never label linear code semantic proof."""
import unittest
from unittest.mock import patch
from pathlib import Path

import semantic_next_boundaries as audit


class BoundaryAuditTests(unittest.TestCase):
    def test_elf_boundaries_aligned_and_nonoverlapping(self):
        self.assertEqual(len(audit.TARGETS), 2)
        self.assertEqual(audit.BYTES, 96)
        self.assertEqual(audit.SOUND, 0x2B2B7C)
        self.assertEqual(audit.ICON, 0x2B8928)

    def test_invalid_or_truncated_arm_region_fails_closed(self):
        with patch.object(audit.semantic_evidence, "read_function",
                          return_value=bytes.fromhex("0000a0e1")):
            with self.assertRaisesRegex(ValueError, "Unaligned or undecodable"):
                audit.inspect(Path("/missing"))

    def test_actual_elf_report_marks_uncertainty(self):
        binary = audit.semantic_evidence.ROOT / "src/lib/armeabi/libgl2jni.so"
        if not binary.is_file():
            self.skipTest("Original ELF not present")
        report = audit.inspect(binary)
        for token in ("0x2b2b7c","0x2b8928","not a demonstrated",
                      "Stop before an unmodeled", "ELF SHA-256"):
            self.assertIn(token, report)
        for start in (audit.SOUND, audit.ICON):
            self.assertIn(f"0x{start+92:x}", report)


if __name__=="__main__":
    unittest.main()
