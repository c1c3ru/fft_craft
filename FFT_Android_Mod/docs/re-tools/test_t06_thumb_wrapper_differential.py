"""Original-ELF isolated Thumb wrapper flow, stack and C++ contract tests."""
import tempfile
import unittest
from pathlib import Path

from elftools.elf.elffile import ELFFile

import b01_overlap_elf_evidence as original
import t06_thumb_wrapper_differential as contracts

ELF = contracts.ROOT / "src/lib/armeabi/libgl2jni.so"


class OriginalWrapperTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if original.sha256(ELF) != original.PINNED_ELF_SHA:
            raise AssertionError("Wrong ELF file in T06 tests")
        cls.source = ELF.open("rb")
        cls.elf = ELFFile(cls.source)

    @classmethod
    def tearDownClass(cls):
        cls.source.close()

    def test_exact_original_thumb_sequences_and_branch_destinations(self):
        for item in contracts.SLICES:
            with self.subTest(name=item["id"]):
                code, insns = contracts.read_slice(self.elf, self.source, item)
                self.assertEqual(len(code), item["bytes"])
                self.assertEqual([x.mnemonic for x in insns], list(item["mnemonics"]))
                self.assertEqual(sum(x.size for x in insns), item["bytes"])

    def test_delete_guard_has_typed_taken_and_fallthrough_edges(self):
        item = contracts.SLICES[0]
        _, decoded = contracts.read_slice(self.elf, self.source, item)
        edges = contracts.static_edges(item, decoded)
        self.assertEqual(
            [edge["kind"] for edge in edges].count("taken_Z_equals_1"), 1)
        self.assertEqual(
            [edge["kind"] for edge in edges].count("fallthrough_Z_equals_0"), 1)
        self.assertEqual(
            [edge["kind"] for edge in edges].count("return_via_stack"), 1)
        self.assertEqual(
            [edge["kind"] for edge in edges].count("external_callee_unmodeled"), 1)

    def test_new_array_has_unclaimed_symbol_tail(self):
        item = contracts.SLICES[1]
        self.assertEqual(item["bytes"], 8)
        self.assertEqual(item["symbol_bytes"], 20)
        self.assertEqual(item["symbol_bytes"] - item["bytes"], 12)

    def test_delete_null_returns_without_external_call(self):
        item = contracts.SLICES[0]
        code, _ = contracts.read_slice(self.elf, self.source, item)
        value = contracts.execute_wrapper(item, code, 0, 0)
        self.assertEqual(value["external_call_count"], 0)
        self.assertIsNone(value["external_r0_argument"])
        self.assertTrue(value["original_stack_and_r3_restored"])

    def test_delete_non_null_passes_argument_once(self):
        item = contracts.SLICES[0]
        code, _ = contracts.read_slice(self.elf, self.source, item)
        value = contracts.execute_wrapper(item, code, 0x12345678, 0)
        self.assertEqual(value["external_call_count"], 1)
        self.assertEqual(value["external_r0_argument"], 0x12345678)
        self.assertEqual(value["external_callee"], "0x002ce07c")
        self.assertTrue(value["returned_to_controlled_sentinel"])

    def test_new_array_forwards_input_and_mock_return(self):
        item = contracts.SLICES[1]
        code, _ = contracts.read_slice(self.elf, self.source, item)
        value = contracts.execute_wrapper(item, code, 64, 0xABCDEF00)
        self.assertEqual(value["external_call_count"], 1)
        self.assertEqual(value["external_r0_argument"], 64)
        self.assertEqual(value["returned_r0"], 0xABCDEF00)
        self.assertEqual(value["external_callee"], "0x002c99b4")

    def test_fault_injection_invalid_opcode_is_rejected(self):
        item = contracts.SLICES[0]
        code, _ = contracts.read_slice(self.elf, self.source, item)
        changed = bytearray(code)
        changed[:2] = b"\x00\xbf"  # Thumb NOP no longer saves SP/LR
        with self.assertRaisesRegex(ValueError, "instruction boundaries"):
            # Mock the file-backed read so validation cannot trust altered bytes.
            from unittest.mock import patch
            with patch.object(contracts.original, "read_executable",
                              return_value=(bytes(changed), 0)):
                contracts.read_slice(self.elf, self.source, item)

    def test_injected_bad_arguments_never_executed(self):
        item = contracts.SLICES[1]
        code, _ = contracts.read_slice(self.elf, self.source, item)
        with self.assertRaisesRegex(ValueError, "uint32"):
            contracts.execute_wrapper(item, code, -1, 0)
        with self.assertRaisesRegex(ValueError, "uint32"):
            contracts.execute_wrapper(item, code, 0, 1 << 40)

    def test_truncated_input_not_accepted(self):
        item = contracts.SLICES[0]
        with self.assertRaisesRegex(ValueError, "not in executable ELF segment"):
            from unittest.mock import patch
            with patch.object(contracts.original, "read_executable",
                              return_value=(b"\x00", 0)):
                contracts.read_slice(self.elf, self.source, item)


if __name__ == "__main__":
    unittest.main()
