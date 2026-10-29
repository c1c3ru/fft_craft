"""Fail-closed original A04 callsite assertions."""
import unittest
from unittest import mock
import semantic_a04_714a0_audit as target
import semantic_evidence

class ExternalCalleeAuditTests(unittest.TestCase):
    def test_callsite_opcode_and_target_are_exact(self):
        # A32 BL with PC+8 relative displacement.
        displacement = (target.TARGET - (target.CALLSITE + 8)) >> 2
        raw = (0xeb000000 | (displacement & 0xffffff)).to_bytes(4, "little")
        with mock.patch.object(semantic_evidence, "read_function", return_value=raw):
            self.assertEqual(target.verify_bl(None), raw.hex())

    def test_mutated_opcode_is_rejected(self):
        with mock.patch.object(semantic_evidence, "read_function", return_value=bytes(4)):
            with self.assertRaises(ValueError):
                target.verify_bl(None)

    def test_wrong_call_target_is_rejected(self):
        with mock.patch.object(semantic_evidence, "read_function",
                               return_value=bytes.fromhex("000000eb")):
            with self.assertRaises(ValueError):
                target.verify_bl(None)

    def test_reports_do_not_promise_semantic_equivalence(self):
        row = {"candidate_cfg": {"instructions": [], "edges": [],
                "memory_candidates": [], "calls": [], "unresolved": []}}
        report = target.report(row)
        self.assertIn("primeiro efeito desconhecido", report)
        self.assertIn("nem certificar automaticamente", report)

if __name__ == "__main__":
    unittest.main()
