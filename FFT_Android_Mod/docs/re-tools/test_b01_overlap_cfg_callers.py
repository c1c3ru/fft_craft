"""Negative and bounded A32 fixtures for B01 incoming-edge triage.

These tests model instruction bytes; they are NOT evidence of executing ARM.
"""
import importlib.util
import io
import tempfile
import unittest
from pathlib import Path

from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM

BASE = Path(__file__).parent
spec = importlib.util.spec_from_file_location("b01_cfg_callers", BASE / "b01_overlap_cfg_callers.py")
# Scripts in docs/re-tools are importable when unittest discovery runs there.
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class FakeELF:
    def __init__(self, size, start=0x1000):
        self.size = size
        self.start = start

    def iter_segments(self):
        return [{"p_type": "PT_LOAD", "p_flags": 5,
                 "p_vaddr": self.start, "p_offset": 0,
                 "p_filesz": self.size}]


def assembler_fixture():
    # B 0x100c; BL 0x2000; MOV R0,#0; BX LR.
    return b"".join(x.to_bytes(4, "little") for x in (
        0xea000001, 0xeb0003fd, 0xe3a00000, 0xe12fff1e))


class B01CFGCallerTests(unittest.TestCase):
    def setUp(self):
        self.raw = assembler_fixture()
        self.elf = FakeELF(len(self.raw))
        self.md = Cs(CS_ARCH_ARM, CS_MODE_ARM)
        self.md.detail = True

    def test_b_and_bl_targets_are_immediate_and_distinct(self):
        insn = list(self.md.disasm(self.raw, 0x1000))
        self.assertEqual(module.direct_target(insn[0]), 0x100c)
        self.assertEqual(module.direct_target(insn[1]), 0x2000)
        self.assertIsNone(module.direct_target(insn[2]))
        self.assertIsNone(module.direct_target(insn[3]))

    def test_candidate_global_incoming_witnesses(self):
        incoming, scanned = module.candidate_callers(
            self.elf, io.BytesIO(self.raw), {0x100c, 0x2000}, self.md)
        self.assertEqual(scanned, 16)
        self.assertEqual(incoming[0x100c]["total"], 1)
        self.assertEqual(incoming[0x2000]["total"], 1)
        self.assertEqual(incoming[0x100c]["witnesses"][0]["source"], "00001000")
        self.assertTrue(incoming[0x100c]["witnesses"][0]["candidate_only"])

    def test_cfg_entry_1000_reaches_return_but_skip_bl(self):
        incoming, _ = module.candidate_callers(
            self.elf, io.BytesIO(self.raw), {0x1000, 0x1004}, self.md)
        self.md.skipdata = False
        item = module.analyze_group(self.elf, io.BytesIO(self.raw), self.md,
                                    "00001010", ["00001000", "00001004"], incoming)
        self.assertEqual(item["a32_decoded_slots"], 4)
        self.assertTrue(item["entrypoint_routes"][0]["modeled_reaches_common_end_last_slot"])
        self.assertTrue(item["entrypoint_routes"][1]["modeled_reaches_common_end_last_slot"])
        self.assertFalse(item["all_edges_executed_or_verified"])
        self.assertFalse(item["all_entrypoints_reachability_proven"])
        self.assertEqual(item["direct_internal_branch_candidates"][0]["target"], "0000100c")
        self.assertEqual(item["direct_external_branch_call_candidates"][0]["target"], "00002000")

    def test_missing_executable_segment_rejected(self):
        with self.assertRaises(ValueError):
            module.analyze_group(FakeELF(4), io.BytesIO(self.raw[:4]), self.md,
                                 "00001010", ["00001000", "00001004"], {
                                    0x1000: {"total": 0, "witnesses": []},
                                    0x1004: {"total": 0, "witnesses": []}})

    def test_misaligned_group_rejected(self):
        with self.assertRaises(ValueError):
            module.analyze_group(self.elf, io.BytesIO(self.raw), self.md,
                                 "00001010", ["00001002"], {})

    def test_cfg_reachable_does_not_invent_external_nodes(self):
        edges = {0x1000: [(0x1004, "not_taken")], 0x1004: []}
        self.assertEqual(module.bounded_reachable(edges, 0x1000), {0x1000, 0x1004})
        self.assertEqual(module.bounded_reachable(edges, 0x2000), set())

    def test_truncated_executable_file_rejected(self):
        with self.assertRaises(ValueError):
            module.candidate_callers(FakeELF(16), io.BytesIO(b"\0" * 4),
                                     {0x1000}, self.md)

    def test_executable_scan_budget_enforced(self):
        with self.assertRaises(ValueError):
            module.candidate_callers(FakeELF(module.MAX_EXEC_SCAN_BYTES + 1),
                                     io.BytesIO(b""), {0x1000}, self.md)


if __name__ == "__main__":
    unittest.main()
