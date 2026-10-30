"""B01 candidate-source gate and ALU one-step differential regressions.

All fixtures are synthetic, not proof of function-level equivalence.
"""
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent


def read_module(filename, name):
    spec = importlib.util.spec_from_file_location(name, HERE / filename)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


source = read_module("b01_source_evidence_filter.py", "b01_source_filter")
alu = read_module("b01_safe_alu_differential.py", "b01_safe_alu")


class B01SourceFilterTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.results = Path(self.temp.name)

    def tearDown(self):
        self.temp.cleanup()

    def checkpoint(self, status="auto_structural", unknown=None,
                   digest=source.PINNED):
        obj = {"address": "00001000", "size": 32,
               "binary_sha256": digest, "pipeline_version": 2,
               "structural_version": 3,
               "structural_v3": {"status": status,
                                 "unexplained_slots": unknown or [],
                                 "literal_slots": []}}
        (self.results / "00001000.json").write_text(json.dumps(obj))
        return {"start": 0x1000, "size": 32, "end": 0x1020}

    def test_owner_index_does_not_assume_nonoverlap(self):
        entries = [{"start": 0x1000,"end":0x1100},
                   {"start": 0x1004,"end":0x1020},
                   {"start": 0x2000,"end":0x2020}]
        starts = [x["start"] for x in entries]
        max_end_prefix = [0x1100, 0x1100, 0x2020]
        got = source.candidate_owners(entries, 0x1008, starts, max_end_prefix)
        self.assertEqual([x["start"] for x in got], [0x1004, 0x1000])
        self.assertEqual(source.candidate_owners(entries, 0x1800, starts,max_end_prefix), [])

    def test_same_elf_v3_can_only_make_a_structural_candidate(self):
        owner = self.checkpoint()
        tier, anchors = source.evidence_tier(0x1004,[owner],self.results)
        self.assertEqual(tier,"structurally_anchored_candidate")
        self.assertEqual(anchors[0]["tier"],"v3_structurally_approved_candidate")

    def test_unexplained_slot_prevents_structural_upgrade(self):
        owner=self.checkpoint(status="needs_review", unknown=["0x00001004"])
        tier, anchors=source.evidence_tier(0x1004,[owner],self.results)
        self.assertEqual(tier,"explicitly_unresolved_source")
        self.assertEqual(anchors[0]["tier"],"v3_explicitly_unexplained_or_literal_slot")

    def test_wrong_sha_or_unverified_checkpoint_fails_closed(self):
        owner=self.checkpoint(digest="a"*64)
        tier, anchors=source.evidence_tier(0x1004,[owner],self.results)
        self.assertEqual(tier,"unresolved_source")
        self.assertEqual(anchors[0]["tier"],"stale_or_non_v3_checkpoint")

    def test_unattributed_entry_has_no_code_proof(self):
        tier, anchors=source.evidence_tier(0x1004,[],self.results)
        self.assertEqual(tier,"no_inventory_owner")
        self.assertEqual(anchors,[])


class B01ALUOneStepTests(unittest.TestCase):
    def test_decode_safe_immediate_and_register(self):
        for w, name in ((0xe3a0002a, "mov"), (0xe2812003,"add"),
                        (0xe2434001,"sub"),(0xe1a00001,"mov"),
                        (0xe1800001,"orr")):
            with self.subTest(opcode=hex(w)):
                decoded=alu.decode_safe(w.to_bytes(4,"little"))
                self.assertEqual(decoded["opcode"],name)

    def test_unsafe_effects_or_control_flow_rejected(self):
        for w in (0x13a0002a,0xe2900001,0xe5900000,
                  0xe1a0d000,0xe12fff1e,0xe1a00060,0xe080000f):
            with self.subTest(opcode=hex(w)):
                self.assertIsNone(alu.decode_safe(w.to_bytes(4,"little")))

    def test_python_model_wraps_and_no_mutation_of_inputs(self):
        regs = [0]*13
        regs[1]=0xffffffff
        spec=alu.decode_safe((0xe2812003).to_bytes(4,"little"))
        result=alu.expected_result(spec,regs)
        self.assertEqual(result[2],2)
        self.assertEqual(regs[2],0)

    def test_unicorn_differential_uses_real_opcode_bytes(self):
        for w in (0xe3a0002a,0xe2812003,0xe2434001,
                  0xe1a00001,0xe1800001):
            raw=w.to_bytes(4,"little")
            spec=alu.decode_safe(raw)
            for seed in (0,1,0xffffffff):
                for flags in (0,0xf0000000):
                    self.assertTrue(alu.execute_one(0x201000,raw,spec,seed,flags))

    def test_rotate_by_zero_and_nonzero(self):
        self.assertEqual(alu.ror(0x80,0),0x80)
        self.assertEqual(alu.ror(0x80,2),0x20)


if __name__ == "__main__":
    unittest.main()
