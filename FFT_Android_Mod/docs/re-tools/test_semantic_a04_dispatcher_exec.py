"""Safety and differential regression for original ARM A04 integrated dispatcher."""
import unittest
from unittest import mock

import semantic_a02_branch_11 as a02
import semantic_a04_dispatcher_exec as a04
import semantic_evidence


class A04DispatcherTests(unittest.TestCase):
    def test_independent_row_col_word_address(self):
        for seed in (0, 0x12345678, 0xffffffff):
            for column in range(4):
                for row in range(4):
                    regs, memory, table, reads = a04.reference(seed, column, row, "dispatcher")
                    index = column + 4*row
                    self.assertEqual(regs[2], index)
                    self.assertEqual(regs[3], a04.ARRAY)
                    self.assertEqual(reads, [(a04.BASE+8, 4), (a04.ARRAY+index*4, 4)])
                    self.assertEqual(regs[0], int.from_bytes(table[index*4:index*4+4], "little"))
                    self.assertEqual(int.from_bytes(memory[8:12], "little"), a04.ARRAY)

    def test_leaf_getter_read_only(self):
        regs, before, table, reads = a04.reference(0xdecafbad, 0, 0, "getter")
        self.assertEqual(regs[0], a04.ARRAY)
        self.assertEqual(reads, [(a04.BASE+8, 4)])

    def test_original_opcode_constants_and_four_a02_branch_sources(self):
        self.assertEqual(len(a04.CALLERS), 4)
        for addr, idx in a04.CALLERS.items():
            decoded = a02.decode(bytes.fromhex(a02.EXPECTED[f"{addr:08x}"][0]), addr)
            self.assertEqual(decoded["target"], a04.DISPATCHER)
            self.assertEqual(decoded["op"], ("mov_r2_zero", "mov_r2_one",
                                              "mov_r2_two", "mov_r2_three")[idx])
        self.assertEqual(a04.DISPATCHER_HEX, "083090e5012182e0020193e71eff2fe1")
        self.assertEqual(a04.GETTER_HEX, "080090e51eff2fe1")

    def test_unicorn_enters_only_exact_modeled_original_blobs(self):
        chunks = {
            a04.DISPATCHER: bytes.fromhex(a04.DISPATCHER_HEX),
            a04.GETTER: bytes.fromhex(a04.GETTER_HEX)
        }
        for address in a04.CALLERS:
            chunks[address] = bytes.fromhex(a02.EXPECTED[f"{address:08x}"][0])
        def original(binary, address, size):
            if address not in chunks or len(chunks[address]) != size:
                raise ValueError("Wrong or unlisted executable range")
            return chunks[address]
        with mock.patch.object(semantic_evidence, "read_function", side_effect=original):
            a04.assert_original(None)
            for address in a04.CALLERS:
                for seed in (0, 0xffffffff, 0x12345678):
                    for row in range(4):
                        for flags in (0, 0x90000000):
                            with self.subTest(address=hex(address), row=row, flags=flags):
                                a04.execute(None, "dispatcher", address, seed, row, flags)
            for seed in (0, 0x12345678, 0xffffffff):
                for flags in (0, 0x40000000):
                    a04.execute(None, "getter", a04.GETTER, seed, 0, flags)
            with self.assertRaisesRegex(ValueError, "Unlisted"):
                a04.execute(None, "dispatcher", 0xb6c58, 0, 0, 0)
        chunks[a04.DISPATCHER] = bytes(len(chunks[a04.DISPATCHER]))
        with mock.patch.object(semantic_evidence, "read_function", side_effect=original):
            with self.assertRaisesRegex(ValueError, "Unexpected ELF ARM bytes"):
                a04.assert_original(None)

    def test_checkpoint_does_not_add_certificates(self):
        state = a04.snapshot("a"*64, "b"*64, [{"name": "test", "cases": 32}])
        self.assertEqual(state["new_certificates"], 0)
        self.assertIn("Unknown", a04.report(state).replace("unverified", "Unknown"))


if __name__ == "__main__":
    unittest.main()
