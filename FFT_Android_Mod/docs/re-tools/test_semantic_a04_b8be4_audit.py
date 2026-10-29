"""Nested A04 callsite validation must reject changed original instructions."""
import unittest
from unittest.mock import patch
import semantic_evidence
import semantic_a04_b8be4_audit as m

class NestedCallTests(unittest.TestCase):
    def test_direct_bl_target(self):
        off = ((m.CALLEE - (m.CALLSITE + 8)) >> 2) & 0xffffff
        raw = (0xeb000000 | off).to_bytes(4, "little")
        with patch.object(semantic_evidence, "read_function", return_value=raw):
            self.assertEqual(m.verify_original_callsite(None), raw.hex())

    def test_wrong_opcode(self):
        with patch.object(semantic_evidence, "read_function", return_value=bytes(4)):
            with self.assertRaises(ValueError):
                m.verify_original_callsite(None)

    def test_wrong_target(self):
        with patch.object(semantic_evidence, "read_function", return_value=(0xeb000000).to_bytes(4, "little")):
            with self.assertRaises(ValueError):
                m.verify_original_callsite(None)

if __name__ == "__main__":
    unittest.main()
