"""Regression tests use synthetic A32 instruction words, NOT the original ELF."""
import unittest

import semantic_loop_250 as loop


def words(*values):
    return b"".join(value.to_bytes(4, "little") for value in values)


class SemanticLoopTests(unittest.TestCase):
    def test_unconditional_arm_branch_to_unexecuted_destination(self):
        spec = loop.decode(words(0xea000000), 0x1000)
        self.assertEqual(spec["target"], 0x1008)
        self.assertEqual(spec["kind"], "branch_prefix")
        self.assertIsNone(loop.decode(words(0xeafffffe), 0x1000))

    def test_8_byte_arithmetic_return_contracts(self):
        for word, operation, expected in (
            (0xe3a00005, "mov", 5),
            (0xe2800001, "add", 8),
            (0xe2400001, "sub", 6),
            (0xe2000003, "and", 3),
            (0xe3800003, "orr", 7),
            (0xe2200003, "eor", 4),
        ):
            with self.subTest(operation=operation):
                spec = loop.decode(words(word, loop.BX_LR), 0x2000)
                self.assertEqual(spec["kind"], "leaf_return")
                self.assertEqual(spec["op"], operation)
                self.assertEqual(loop.model(spec, 7, 8, 9), expected)

    def test_register_move_and_controlled_load(self):
        move = loop.decode(words(0xe1a00001, loop.BX_LR), 0x2000)
        self.assertEqual(loop.model(move, 1, 0x87654321, 0), 0x87654321)
        load = loop.decode(words(0xe5900000, loop.BX_LR), 0x2000)
        self.assertEqual((load["op"], load["base"], load["offset"]), ("ldr", 0, 0))
        self.assertEqual(loop.model(load, 1, 2, 0x12345678), 0x12345678)

    def test_no_unsafe_flow_memory_writes_or_conditional_words(self):
        for word in (0xe5801000, 0x1a000000, 0xeb000000, 0xe12fff10,
                     0xe3b00001):
            with self.subTest(opcode=hex(word)):
                self.assertIsNone(loop.decode(words(word), 0x1000))
                self.assertIsNone(loop.decode(words(word, loop.BX_LR), 0x1000))

    def test_alignment_and_contract_outputs_are_bounded(self):
        self.assertIsNone(loop.decode(words(0xe3a00001, loop.BX_LR), 0x1002))
        d = loop.state("a" * 64, "b" * 64, [], {"unsafe": 250}, 0, [])
        self.assertEqual(d["new_certificates"], 0)
        report = loop.render(d)
        self.assertIn("Nenhum callee", report)
        self.assertIn("303 certificados", report)

    def test_unicorn_register_bank_regression(self):
        """Original bug: installing LR before selecting user CPSR bank jumped to zero."""
        from unittest import mock
        import semantic_evidence
        cases = (
            (0x823e4, words(0xe3a00055, loop.BX_LR)),
            (0x8300c, words(0xe5900008, loop.BX_LR)),
            (0xa8210, words(0xe280001c, loop.BX_LR)),
            (0x92000, words(0xea000000)),
        )
        for address, raw in cases:
            with self.subTest(address=hex(address)):
                spec = {**loop.decode(raw, address),
                        "address": f"{address:08x}", "size": len(raw)}
                def read_fixture(binary, start, size):
                    if start == address and size == len(raw):
                        return raw
                    if spec["kind"] == "branch_prefix" and start == address + 8:
                        return words(loop.BX_LR)
                    raise ValueError("unexpected binary read in synthetic test")
                with mock.patch.object(semantic_evidence, "read_function",
                                       side_effect=read_fixture):
                    for flags in (0, 0x40000000, 0x90000000):
                        loop.execute(None, spec, 0x12345678, flags)

    def test_rotated_immediate(self):
        # MOV r0, #0x80000000 (imm8 0x80 rotated right 8).
        spec = loop.decode(words(0xe3a00480, loop.BX_LR), 0x2000)
        self.assertEqual(spec["imm"], 0x80000000)
        self.assertEqual(loop.model(spec, 0, 0, 0), 0x80000000)


if __name__ == "__main__":
    unittest.main()
