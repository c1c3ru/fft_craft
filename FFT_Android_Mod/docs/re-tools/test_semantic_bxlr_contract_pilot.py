"""Regression: interworking, opcode drift and malformed contract preconditions."""
import importlib.util
import unittest
from pathlib import Path

spec = importlib.util.spec_from_file_location(
    "semantic_bxlr_contract_pilot",
    Path(__file__).with_name("semantic_bxlr_contract_pilot.py"))
pilot = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pilot)


class BXLrContractPilotTests(unittest.TestCase):
    def test_original_arm_encoding_and_unique_instruction(self):
        self.assertIn("CPSR.T", pilot.isa_contract(bytes.fromhex("1eff2fe1")))
        for wrong in (bytes.fromhex("0000a0e1"),
                      bytes.fromhex("1eff2f11"), b"", b"\x1e\xff\x2f"):
            with self.assertRaises(ValueError):
                pilot.isa_contract(wrong)

    def test_even_and_odd_return_preserve_state(self):
        self.assertEqual(len(pilot.FLAGS), 16)
        self.assertEqual(pilot.verify_interworking(
            0x2020, bytes.fromhex("1eff2fe1")), 32)

    def test_reject_invalid_elf_entry_location(self):
        with self.assertRaises(ValueError):
            pilot.verify_interworking(0x2021, bytes.fromhex("1eff2fe1"))
        with self.assertRaises(ValueError):
            pilot.verify_interworking(pilot.RETURN, bytes.fromhex("1eff2fe1"))


if __name__ == "__main__":
    unittest.main()
