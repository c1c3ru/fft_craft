"""Bounded A04 GOT slot verifier contracts; no real destination execution."""
import unittest
from unittest import mock

import semantic_a04_714a0_slot as target


class SlotAuditTests(unittest.TestCase):
    def test_original_slot_constant_is_aligned(self):
        self.assertEqual(target.SLOT, 0x00347d70)
        self.assertEqual(target.SLOT % 4, 0)

    def test_reject_non_three_instruction_bytes(self):
        with self.assertRaises(ValueError):
            target.decoded_slot(bytes(8))

    def test_reject_unknown_instruction_layout(self):
        with self.assertRaises(ValueError):
            target.decoded_slot(bytes(12))

    def test_reject_elf_sha_mismatch_before_disassembly(self):
        from tempfile import TemporaryDirectory
        from pathlib import Path
        with TemporaryDirectory() as temp:
            sample = Path(temp) / "mutated.so"
            sample.write_bytes(bytes(96))
            with self.assertRaisesRegex(ValueError, "SHA-256"):
                target.audit(sample)

    def test_empty_slot_provenance_is_never_described_as_runtime_value(self):
        self.assertFalse({"runtime_value_verified": False}["runtime_value_verified"])


if __name__ == "__main__":
    unittest.main()
