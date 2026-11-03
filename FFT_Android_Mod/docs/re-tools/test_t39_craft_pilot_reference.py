"""The independent pilot must preserve ARM/Thumb ISA and reject false proof."""
import copy
import unittest

import t39_craft_pilot_reference as pilot


def queue():
    return {
        "schema": 1, "task_count": 40,
        "elf_sha256": pilot.original.PINNED_ELF_SHA,
        "t04": {"interval_count": 1, "candidates": [
            {"address": "0x71c50", "size": 2144},
        ]},
        "t06": {"current_review_count": 2, "candidates": [
            {"address": "002c9115"}, {"address": "002c9a25"},
        ]}
    }


class PilotReferenceTests(unittest.TestCase):
    def test_pinned_targets_have_two_thumb_one_gap_and_cpp_control(self):
        self.assertEqual(len(pilot.TARGETS), 4)
        self.assertEqual([t["isa"] for t in pilot.TARGETS],
                         ["thumb", "thumb", "arm", "arm"])
        self.assertTrue(pilot.check_targets(queue()))

    def test_t04_missing_interval_refused(self):
        q = queue()
        q["t04"]["candidates"][0]["address"] = "0x9000"
        with self.assertRaisesRegex(ValueError, "T04 target absent"):
            pilot.check_targets(q)

    def test_t06_missing_odd_entry_refused(self):
        q = queue()
        q["t06"]["candidates"][0]["address"] = "002c9114"
        with self.assertRaisesRegex(ValueError, "T06 Thumb target absent"):
            pilot.check_targets(q)

    def test_queue_elf_changed_refused(self):
        q = queue()
        q["elf_sha256"] = "0" * 64
        with self.assertRaisesRegex(ValueError, "pinned"):
            pilot.check_targets(q)

    def test_queue_dropped_review_refused(self):
        q = queue()
        q["t06"]["current_review_count"] = 3
        with self.assertRaisesRegex(ValueError, "truncated"):
            pilot.check_targets(q)

    def test_thumb_bit_removed_for_memory_but_not_entry(self):
        result = pilot.analyze_window(bytes.fromhex("7047"), 0x2c9115, "thumb")
        self.assertEqual(result["physical_entry"], "0x002c9114")
        self.assertEqual(result["entry_isa"], "thumb")
        self.assertEqual(result["first_instructions"][0]["mnemonic"], "bx")
        self.assertEqual(result["decoded_prefix_bytes"], 2)

    def test_bad_a32_alignment_refused(self):
        with self.assertRaisesRegex(ValueError, "word aligned"):
            pilot.analyze_window(bytes.fromhex("1eff2fe1"), 0x1001, "arm")

    def test_zero_length_and_unknown_isa_refused(self):
        with self.assertRaisesRegex(ValueError, "Invalid disassembly"):
            pilot.analyze_window(b"", 0x1000, "arm")
        with self.assertRaisesRegex(ValueError, "Invalid disassembly"):
            pilot.analyze_window(b"abcd", 0x1000, "aarch64")

    def test_known_12_byte_cpp_control_pattern(self):
        b = bytes.fromhex("0220a0e3142080e51eff2fe1")
        result = pilot.analyze_window(b, 0xb9f7c, "arm")
        pilot.check_control(result)
        self.assertEqual(result["decoded_prefix_bytes"], 12)
        self.assertEqual([x["mnemonic"] for x in result["first_instructions"]],
                         ["mov", "str", "bx"])

    def test_false_cpp_control_refused(self):
        b = bytes.fromhex("0220a0e3142080e50000a0e1")
        with self.assertRaisesRegex(ValueError, "pattern changed"):
            pilot.check_control(pilot.analyze_window(b, 0xb9f7c, "arm"))

    def test_optional_bundle_does_not_auto_promote(self):
        q = queue()
        old = copy.deepcopy(q)
        # Only test source matching; no original game execution / C++ claim.
        from t39_craft_anything_bridge import reconcile
        e = {"id": "ev_" + "1" * 64,
             "subject": {"kind": "native",
                         "sha256": pilot.original.PINNED_ELF_SHA},
             "operation": "native_instruction_show",
             "locations": [{"kind": "address", "value": "0x2c9115"}]}
        matched = reconcile(q, {"format": "craft-anything-evidence-bundle",
                                "version": 1, "records": [e]})
        self.assertEqual(matched["queue_matches"], 1)
        self.assertEqual(q, old)
        self.assertEqual(matched["new_semantic_certificates"], 0)

    def test_render_has_explicit_no_upstream_run(self):
        report = {"elf_sha256": pilot.original.PINNED_ELF_SHA,
                  "capstone_reference_targets": []}
        result = pilot.markdown(report)
        self.assertIn("Não foi executado o Craft Anything", result)


if __name__ == "__main__":
    unittest.main()
