"""Fail-closed tests for A04 post-strcpy original ARM callsite."""
import unittest
from semantic_a04_714a0_postcopy import verify_sequence

class PostCopyTests(unittest.TestCase):
    def test_missing_continuation_is_rejected(self):
        with self.assertRaises(ValueError):
            verify_sequence([])

    def test_missing_second_call_is_rejected(self):
        rows = [{"pc": f"{pc:08x}", "mnemonic": name, "bytes": "0000a0e1"}
                for pc, name in ((0xb6634, "mov"), (0xb6638, "mov"),
                                 (0xb663c, "mov"), (0xb6644, "mov"),
                                 (0xb6648, "str"), (0xb664c, "mov"),
                                 (0xb6650, "pop"))]
        with self.assertRaises(ValueError):
            verify_sequence(rows)

    def test_wrong_original_call_target_is_rejected(self):
        rows = [{"pc": f"{pc:08x}", "mnemonic": name, "bytes": "0000a0e1"}
                for pc, name in ((0xb6634, "mov"), (0xb6638, "mov"),
                                 (0xb663c, "mov"), (0xb6640, "bl"),
                                 (0xb6644, "mov"), (0xb6648, "str"),
                                 (0xb664c, "mov"), (0xb6650, "pop"))]
        with self.assertRaises(ValueError):
            verify_sequence(rows)

if __name__ == "__main__":
    unittest.main()
