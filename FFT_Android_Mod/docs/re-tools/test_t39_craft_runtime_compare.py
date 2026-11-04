"""Third-party ARM disassembly must be compared without raw evidence leakage."""
import hashlib
import struct
import tempfile
import unittest
from pathlib import Path

import t39_craft_runtime_compare as compare


def h(value):
    return hashlib.sha256(bytes.fromhex(value)).hexdigest()


def target():
    return {
        "name": "control", "task": "B01", "declared_entry": "0x000b9f7c",
        "physical_entry": "0x000b9f7c", "entry_isa": "arm",
        "requested_bytes": 8,
        "first_instructions": [
            {"address": "0x000b9f7c", "size": 4, "mnemonic": "mov",
             "instruction_bytes_sha256": h("0220a0e3")},
            {"address": "0x000b9f80", "size": 4, "mnemonic": "str",
             "instruction_bytes_sha256": h("142080e5")},
        ]
    }


def output():
    return {
        "operation": "native_function_instructions_list",
        "result": {
            "entry": "0xb9f7c",
            "instructions": [
                {"address": "0xb9f7c", "length": 4, "bytes": "0220a0e3",
                 "mnemonic": "mov", "flow": "Next"},
                {"address": "0xb9f80", "length": 4, "bytes": "142080e5",
                 "mnemonic": "str", "flow": "Next"},
            ],
        }
    }


class RuntimeCompareTests(unittest.TestCase):
    def test_exact_bytes_size_and_mnemonic(self):
        rows = compare.parse_tool(output(), "native_function_instructions_list")
        report = compare.compare_target(target(), rows, {}, "success")
        self.assertEqual(report["matched_instruction_boundaries_and_bytes"], 2)
        self.assertEqual(report["differences_or_not_reported"], [])
        self.assertFalse(report["semantic_equivalence_proven"])

    def test_bad_byte_sequence_is_reported_without_copying_raw(self):
        data = output()
        data["result"]["instructions"][0]["bytes"] = "0000a0e1"
        rows = compare.parse_tool(data, "native_function_instructions_list")
        report = compare.compare_target(target(), rows, {}, "success")
        self.assertEqual(report["matched_instruction_boundaries_and_bytes"], 1)
        self.assertEqual(report["differences_or_not_reported"][0]["reason"],
                         "instruction_mismatch")
        self.assertNotIn("0000a0e1", str(report))

    def test_untrusted_string_not_a_valid_instruction(self):
        data = output()
        data["result"]["instructions"][0]["mnemonic"] = '<script>alert(1)</script>'
        rows = compare.parse_tool(data, "native_function_instructions_list")
        self.assertEqual(rows[0]["mnemonic"], "unknown")
        report = compare.compare_target(target(), rows, {}, "success")
        self.assertEqual(report["matched_instruction_boundaries_and_bytes"], 1)

    def test_foreign_operation_rejected(self):
        with self.assertRaisesRegex(ValueError, "requested evidence"):
            compare.parse_tool(output(), "native_instruction_show")

    def test_overlong_or_malformed_instruction_bytes_rejected(self):
        data = output()
        data["result"]["instructions"][0]["bytes"] = "bad"
        with self.assertRaisesRegex(ValueError, "instruction bytes"):
            compare.parse_tool(data, "native_function_instructions_list")
        data["result"]["instructions"][0]["bytes"] = "e3a02002"
        data["result"]["instructions"][0]["length"] = 2
        with self.assertRaisesRegex(ValueError, "instruction bytes"):
            compare.parse_tool(data, "native_function_instructions_list")

    def test_single_instruction_fallback_evidence(self):
        doc = {
            "operation": "native_instruction_show",
            "result": {"kind": "instruction", "address": "0xb9f7c",
                       "length": 4, "bytes": "0220a0e3",
                       "mnemonic": "mov", "flow": "Next"}
        }
        rows = compare.parse_tool(doc, "native_instruction_show")
        self.assertEqual(len(rows), 1)
        report = compare.compare_target(target(), rows, {}, "first_instruction_only")
        self.assertEqual(report["matched_instruction_boundaries_and_bytes"], 1)
        self.assertEqual(report["differences_or_not_reported"][0]["reason"],
                         "instruction_not_reported")

    def test_target_mismatch_is_not_accepted(self):
        self.assertEqual(compare.external_branch_target({"Call":{"target":"0x0000abcd"}}),
                         0xabcd)
        self.assertIsNone(compare.external_branch_target({"Call":{"target":"invalid"}}))
        self.assertIsNone(compare.external_branch_target("Unknown"))
        self.assertEqual(compare.external_branch_target({"Cond":{"target":0x100}}), 0x100)

    def test_branch_compared_only_if_target_available(self):
        data=output()
        data["result"]["instructions"][0]["flow"] = {"Call":{"target":"0x1000"}}
        rows=compare.parse_tool(data, "native_function_instructions_list")
        result=compare.compare_target(target(), rows, {0xb9f7c:0x2000}, "success")
        self.assertFalse(result["branch_target_comparison"][0]["targets_match"])
        rows[0]["flow"] = {"Call":{"target":"bad"}}
        result=compare.compare_target(target(), rows, {0xb9f7c:0x2000}, "success")
        self.assertIsNone(result["branch_target_comparison"][0]["targets_match"])

    def test_duplicate_third_party_addresses_rejected(self):
        rows=compare.parse_tool(output(), "native_function_instructions_list")
        with self.assertRaisesRegex(ValueError, "Overlapping"):
            compare.compare_target(target(), rows+rows[:1], {}, "success")

    def test_external_addresses_must_be_arm32(self):
        with self.assertRaisesRegex(ValueError, "Untrusted address"):
            compare.address("../../../etc/passwd")
        with self.assertRaisesRegex(ValueError, "Untrusted address"):
            compare.address(1<<40)
        with self.assertRaisesRegex(ValueError, "Untrusted address"):
            compare.address(True)

    def test_partial_no_evidence_not_misreported_as_agreement(self):
        report=compare.compare_target(target(), [], {}, "unavailable_tool_error")
        self.assertEqual(report["matched_instruction_boundaries_and_bytes"],0)
        self.assertEqual(len(report["differences_or_not_reported"]),2)
        self.assertFalse(report["original_function_reachability_proven"])

    def test_sanitized_md_does_not_insert_third_party_text(self):
        data={"elf_sha256":"a"*64,"craft_anything_version":"0.3.0","targets":[
            compare.compare_target(target(), [], {}, "unavailable_tool_error")]}
        rendered=compare.render_md(data)
        self.assertIn("Sem certificados novos", rendered)
        self.assertNotIn("0220a0e3", rendered)


    def test_derived_thumb_probe_only_rewrites_elf_header_entry(self):
        binary = compare.pilot.ROOT / "src/lib/armeabi/libgl2jni.so"
        baseline = binary.read_bytes()
        with tempfile.TemporaryDirectory() as tmp:
            alt = compare.make_thumb_mode_probe(binary, 0x002c9115, Path(tmp))
            new = alt.read_bytes()
        self.assertEqual(len(new), len(baseline))
        self.assertEqual(baseline[:24], new[:24])
        self.assertEqual(baseline[28:], new[28:])
        self.assertEqual(struct.unpack_from("<I", new, 24)[0], 0x002c9115)
        self.assertNotEqual(hashlib.sha256(new).digest(),
                            hashlib.sha256(baseline).digest())

    def test_derived_thumb_probe_rejects_even_entry(self):
        binary = compare.pilot.ROOT / "src/lib/armeabi/libgl2jni.so"
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaisesRegex(ValueError, "Thumb entry"):
                compare.make_thumb_mode_probe(binary, 0x002c9114, Path(tmp))


if __name__ == "__main__":
    unittest.main()
