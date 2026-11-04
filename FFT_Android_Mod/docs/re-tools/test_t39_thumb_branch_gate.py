"""T06 Thumb PC-relative target verification against original ARM ELF."""
import tempfile
import unittest
from pathlib import Path

import t39_thumb_branch_gate as gate


class ThumbBranchGateTests(unittest.TestCase):
    def test_original_elf_microexecutions_have_no_certificate(self):
        path = gate.ROOT / "src/lib/armeabi/libgl2jni.so"
        result = gate.audit(path)
        self.assertEqual(result["thumb_branch_scenarios"], 4)
        self.assertEqual(result["new_semantic_certificates"], 0)
        self.assertFalse(result["T06_done"])
        for item in result["results"]:
            self.assertEqual(item["expected_pc"], item["unicorn_pc"])
            self.assertEqual(item["expected_lr"], item["unicorn_lr"])
            self.assertTrue(item["one_original_instruction_executed"])

    def test_beq_both_flags_produce_distinct_destination(self):
        result = gate.audit(gate.ROOT / "src/lib/armeabi/libgl2jni.so")
        beq = [x for x in result["results"] if x["site"] == "0x002c9118"]
        self.assertEqual(len(beq), 2)
        self.assertEqual({x["unicorn_pc"] for x in beq},
                         {"0x002c911e", "0x002c911a"})

    def test_malformed_unaligned_thumb_inputs_rejected(self):
        with self.assertRaisesRegex(ValueError, "Invalid aligned"):
            gate.execute_case(0x1001, b"\x00\xbf", 0x1002, False, "beq")
        with self.assertRaisesRegex(ValueError, "Invalid aligned"):
            gate.execute_case(0x1000, b"\x00", 0x1002, False, "beq")
        with self.assertRaisesRegex(ValueError, "Invalid aligned"):
            gate.execute_case(0x1000, b"\x00\xbf", 0x1003, False, "beq")

    def test_wrong_elf_digest_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            bad = Path(d) / "libgl2jni.so"
            bad.write_bytes(b"invalid")
            with self.assertRaisesRegex(ValueError, "Unrecognized"):
                gate.audit(bad)


if __name__ == "__main__":
    unittest.main()
