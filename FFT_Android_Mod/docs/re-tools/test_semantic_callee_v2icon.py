"""Regression tests for external BL target identity and bounded ARM decode."""
import csv
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import semantic_callee_v2icon as callee


def bl_word(source, target):
    delta = target - (source + 8)
    if delta % 4 or not -(1 << 25) <= delta < (1 << 25):
        raise ValueError("Unrepresentable ARM BL")
    return (0xEB000000 | ((delta >> 2) & 0x00FFFFFF)).to_bytes(4, "little")


FAKE_BODY = bytes.fromhex(
    "0c309fe5 03308fe0 000183e0 040d90e5 1eff2fe1 00100000"
)


class V2IconTargetTests(unittest.TestCase):
    def test_bl_target_matches_six_word_callee(self):
        target = bl_word(callee.CALLSITE, callee.CALLEE)

        def get_data(binary, address, length):
            if address == callee.CALLSITE:
                return target
            if address == callee.CALLEE:
                return FAKE_BODY
            raise ValueError("unexpected address")

        with patch.object(callee.semantic_evidence, "read_function",
                          side_effect=get_data):
            instruction, body, literal = callee.decode(Path("/nonexistent"))
        self.assertEqual(instruction.mnemonic, "bl")
        self.assertEqual(len(body), 5)
        self.assertEqual(literal, 0x1000)
        self.assertEqual(body[0].address, callee.CALLEE)
        self.assertEqual(body[-1].op_str, "lr")

    def test_wrong_bl_target_rejected(self):
        with patch.object(callee.semantic_evidence, "read_function",
                          return_value=bl_word(callee.CALLSITE, callee.CALLEE+4)):
            with self.assertRaisesRegex(ValueError, "not BL to expected"):
                callee.decode(Path("/nonexistent"))

    def test_truncated_callee_rejected(self):
        def get_data(binary, address, length):
            return (bl_word(callee.CALLSITE, callee.CALLEE)
                    if address == callee.CALLSITE else FAKE_BODY[:-4])
        with patch.object(callee.semantic_evidence, "read_function",
                          side_effect=get_data):
            with self.assertRaisesRegex(ValueError, "truncated"):
                callee.decode(Path("/nonexistent"))

    def test_literal_is_data_and_table_has_word_stride(self):
        self.assertEqual(callee.LITERAL_ADDR, callee.CALLEE + 20)
        base = callee.indexed_address(0x1000, 0)
        self.assertEqual(callee.indexed_address(0x1000, 7), base + 28)
        with self.assertRaisesRegex(ValueError, "32-bit"):
            callee.indexed_address(0, -1)

    def test_inventory_requires_exact_symbol_size_address(self):
        with tempfile.TemporaryDirectory() as temp:
            inventory = Path(temp) / "inventory.csv"
            def save(name, size):
                with inventory.open("w", newline="") as stream:
                    writer = csv.DictWriter(
                        stream, fieldnames=("address", "size", "demangled"))
                    writer.writeheader()
                    writer.writerow({
                        "address": f"{callee.CALLEE:08x}",
                        "size": str(size), "demangled": name,
                    })
            save(callee.EXPECTED_SYMBOL, callee.CALLEE_SIZE)
            self.assertEqual(
                callee.inventory_match(inventory)["demangled"],
                callee.EXPECTED_SYMBOL)
            save("unexpected()", callee.CALLEE_SIZE)
            with self.assertRaisesRegex(ValueError, "inventory"):
                callee.inventory_match(inventory)
            save(callee.EXPECTED_SYMBOL, callee.CALLEE_SIZE+4)
            with self.assertRaisesRegex(ValueError, "inventory"):
                callee.inventory_match(inventory)


if __name__ == "__main__":
    unittest.main()
