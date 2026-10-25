"""Tests for structural v3 coverage classification, jump-table safety and retries."""
import unittest
from unittest.mock import patch

from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
import structural_v3
import parallel_loop


def arm(data, start=0x1000, exclude=()):
    md = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    md.detail = True
    return {ins.address: ins for ins in md.disasm(data, start)
            if ins.address not in exclude}


class StructuralV3Tests(unittest.TestCase):
    def test_pc_relative_literal_removes_only_referenced_gap(self):
        # LDR r0,[pc] -> PC+8; BX LR; .word literal
        data = bytes.fromhex("00009fe5 1eff2fe1 78563412")
        result = structural_v3.inspect(data, 0x1000)
        self.assertEqual(result["status"], "auto_structural")
        self.assertEqual(result["code_slots"], 2)
        self.assertEqual(result["literal_slots"], ["0x1008"])
        self.assertEqual(result["unexplained_count"], 0)
        self.assertEqual(result["code_coverage_pct"], 100.0)
        self.assertTrue(result["candidate_literal_data_not_proven"])

    def test_unknown_gap_stays_under_review(self):
        data = bytes.fromhex("0100a0e3 1eff2fe1 78563412")
        result = structural_v3.inspect(data, 0x1000)
        self.assertEqual(result["status"], "needs_review")
        self.assertEqual(result["unexplained_slots"], ["0x1008"])
        self.assertEqual(result["literal_slots"], [])

    def test_unaligned_arm_never_passes(self):
        for start, code in ((0x1001, b"abcd"), (0x1000, b"abc")):
            with self.subTest(start=start):
                self.assertEqual(structural_v3.inspect(code, start)["status"],
                                 "needs_review")

    def test_verified_dispatch_entries_count_as_executable_slots(self):
        data = bytes.fromhex(
            "010050e3 "  # 0x1000 cmp r0,#1
            "00f08fe0 "  # 0x1004 add pc,pc,r0,lsl#2
            "0110a0e1 "  # 0x1008 mov r1,r1 (artificial decoded entry)
            "000000ea "  # 0x100c b #0x1014
            "000000ea "  # 0x1010 b #0x1018
            "1eff2fe1 "  # 0x1014 bx lr
            "1eff2fe1 "  # 0x1018 bx lr
        )
        decoded = arm(data, exclude=(0x100c, 0x1010))
        with patch.object(structural_v3.semantic_evidence, "collect",
                          return_value=(decoded, [(0x1000, 0x1004,
                                                   [0x1014, 0x1018])], [])):
            result = structural_v3.inspect(data, 0x1000)
        self.assertEqual(result["status"], "auto_structural")
        self.assertEqual(result["table_entry_slots"], 2)
        self.assertEqual(result["code_slots"], 7)
        self.assertEqual(result["tables"][0]["cases"], 2)
        self.assertTrue(result["tables_safe"])

        # Reject dispatches with a target not observed as executable code.
        with patch.object(structural_v3.semantic_evidence, "collect",
                          return_value=(decoded, [(0x1000, 0x1004,
                                                   [0x1014, 0x2000])], [])):
            result = structural_v3.inspect(data, 0x1000)
        self.assertEqual(result["status"], "needs_review")
        self.assertFalse(result["tables_safe"])

    def test_stale_rules_only_reprocess_review_of_same_binary(self):
        current = {"status": "needs_review", "binary_sha256": "sha",
                   "pipeline_version": 2, "size": 12,
                   "structural_version": 3, "structural_fingerprint": "abc"}
        self.assertFalse(parallel_loop.needs_v3_upgrade(current, "sha", 12, "abc"))
        self.assertTrue(parallel_loop.needs_v3_upgrade(current, "sha", 12, "def"))
        old = {**current, "structural_version": 2}
        self.assertTrue(parallel_loop.needs_v3_upgrade(old, "sha", 12, "abc"))
        for different in ({**old, "status": "auto_structural"},
                          {**old, "size": 16},
                          {**old, "binary_sha256": "other"}):
            self.assertFalse(parallel_loop.needs_v3_upgrade(
                different, "sha", 12, "abc"))


if __name__ == "__main__":
    unittest.main()
