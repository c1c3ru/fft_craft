"""Regression tests for ARM evidence, not semantic verification."""
import importlib.util
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
spec = importlib.util.spec_from_file_location("semantic_evidence", HERE / "semantic_evidence.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class EvidenceTests(unittest.TestCase):
    def test_reachability_and_possible_memory_write(self):
        # mov r0, #1; str r0, [sp]; bx lr; trailing literal word
        data = bytes.fromhex("0100a0e3 00008de5 1eff2fe1 78563412")
        found, tables, unresolved = module.collect(data, 0x1000)
        self.assertIn(0x1000, found)
        self.assertIn(0x1004, found)
        self.assertIn(0x1008, found)
        self.assertNotIn(0x100c, found)
        self.assertFalse(tables)
        self.assertFalse(unresolved)
        report = module.evidence({
            "address": "00001000", "name": "synthetic()",
            "status": "needs_review",
        }, data)
        self.assertIn("str r0, [sp]", report)
        self.assertIn("0x100c", report)
        self.assertIn("No semantic equivalence is proved", report)

    def test_pc_relative_literal_not_misreported_as_unexplained_code(self):
        # ldr r0, [pc]; bx lr; .word 0x12345678
        data = bytes.fromhex("00009fe5 1eff2fe1 78563412")
        found, _, _ = module.collect(data, 0x1000)
        literals = module.pc_relative_literals(found, 0x1000, data)
        self.assertEqual(literals[0x1008]["value"], 0x12345678)
        report = module.evidence({
            "address": "00001000", "name": "literal_test()",
            "status": "needs_review",
        }, data)
        self.assertIn("Unvisited slots referenced by PC-relative LDR: 1", report)
        self.assertIn("Other unvisited slots: 0", report)
        self.assertIn("0x1008", report)

    def test_progressive_rotation_skips_existing_evidence(self):
        import csv
        import hashlib
        import json
        import tempfile
        from unittest.mock import patch
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            binary = root / "fake.so"
            binary.write_bytes(b"synthetic")
            digest = hashlib.sha256(b"synthetic").hexdigest()
            results = root / "results"
            results.mkdir()
            output = results / "semantic-evidence"
            output.mkdir()
            rows = []
            for i in (0x1000, 0x2000, 0x3000):
                addr = f"{i:08x}"
                rows.append({"address": addr, "name": f"f_{addr}"})
                (results / f"{addr}.json").write_text(json.dumps({
                    "address": addr, "name": f"f_{addr}", "size": 8,
                    "status": "needs_review", "pipeline_version": 2,
                    "binary_sha256": digest,
                }))
            with (results / "REVIEW_QUEUE.csv").open("w", newline="") as stream:
                writer = csv.DictWriter(stream, fieldnames=["address", "name"])
                writer.writeheader()
                writer.writerows(rows)
            # The first address has valid existing evidence.
            (output / "00001000.md").write_text(f"ELF SHA-256: `{digest}`")
            data = bytes.fromhex("0100a0e3 1eff2fe1")
            with patch.object(module, "read_function", return_value=data) as reader:
                module.run(binary, results, output, 2)
                self.assertEqual(reader.call_count, 2)
                self.assertTrue((output / "00002000.md").exists())
                self.assertTrue((output / "00003000.md").exists())
                module.run(binary, results, output, 2)
                self.assertEqual(reader.call_count, 2)
            index = (results / "SEMANTIC_EVIDENCE_INDEX.md").read_text()
            self.assertIn("Evidence collected: **3/3**", index)

    def test_reject_invalid_executable_range(self):
        with self.assertRaisesRegex(ValueError, "halfword aligned"):
            module.read_function(Path("/nonexistent"), 0x1001, 8)
        with self.assertRaisesRegex(ValueError, "size positive"):
            module.read_function(Path("/nonexistent"), 0x1000, 0)
        # A short non-word-multiple symbol is valid input to the reader.
        with self.assertRaises(FileNotFoundError):
            module.read_function(Path("/nonexistent"), 0x1000, 7)

    def test_thumb_tagged_symbol_is_decoded_in_thumb_mode(self):
        # Thumb: movs r0, #1; bx lr; .word data
        data = bytes.fromhex("0120 7047 78563412")
        report = module.evidence({
            "address": "00001001", "name": "__gxx_personality_v0",
            "status": "needs_review",
        }, data)
        self.assertIn("Instruction set: Thumb (tagged symbol address)", report)
        self.assertIn("0x00001000: movs r0, #1", report)
        self.assertIn("Thumb jump-table analysis was not performed", report)
        self.assertIn("Other unvisited slots", report)
        self.assertIn("linear, stops at first recognized return; NOT a CFG", report)

    def test_thumb_literal_reference_uses_thumb_pc_offset(self):
        data = bytes.fromhex("0048 7047 78563412")
        found, _, _ = module.collect_thumb(data, 0x1000)
        refs = module.pc_relative_literals(found, 0x1000, data, thumb=True)
        self.assertEqual(refs[0x1004]["value"], 0x12345678)

    def test_markdown_contains_real_newlines(self):
        spec = importlib.util.spec_from_file_location(
            "export_review_queue", HERE / "export_review_queue.py")
        other = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(other)
        report = other.render_triage([])
        self.assertIn("# ARM semantic review triage\n\n", report)
        self.assertNotIn("\\n", report)


if __name__ == "__main__":
    unittest.main()
