"""A01: strict decoding plus actual Unicorn with synthetic (never certified) opcodes."""
import unittest
from unittest import mock

import semantic_a01_memory_21 as a01
import semantic_evidence
import semantic_loop_250 as prior


def words(*opcodes):
    return b"".join(w.to_bytes(4, "little") for w in opcodes)


class A01Tests(unittest.TestCase):
    def test_all_ten_original_instruction_words_have_narrow_local_contract(self):
        # Hex bytes transcribed from the verified 34-entry original ELF artifact.
        cases = {
            "000a9404": ("4010c0e51eff2fe1", "strb_r1"),
            "000b1ad4": ("0410c0e51eff2fe1", "strb_r1"),
            "000b1acc": ("0400d0e51eff2fe1", "ldrb_r0"),
            "000ad8d0": ("540090e51eff2fe1", "ldr_large_r0"),
            "000ae088": ("680090e51eff2fe1", "ldr_large_r0"),
            "000af110": ("840590e51eff2fe1", "ldr_large_r0"),
            "000af118": ("880590e51eff2fe1", "ldr_large_r0"),
            "000b67b0": ("080190e51eff2fe1", "ldr_large_r0"),
            "000b682c": ("040190e51eff2fe1", "ldr_large_r0"),
            "000b6ac4": ("280190e51eff2fe1", "ldr_large_r0"),
        }
        for address, (opcode, operation) in cases.items():
            with self.subTest(address=address):
                decoded = a01.decode(bytes.fromhex(opcode), int(address, 16))
                self.assertIsNotNone(decoded)
                self.assertEqual(decoded["op"], operation)
                self.assertEqual(decoded["opcode"], opcode)

    def test_reject_conditional_writeback_negative_pc_and_unknown(self):
        valid = 0xe5c01040  # STRB r1,[r0,#0x40] + BX LR
        for word in (
            valid & 0x0fffffff | 0x10000000,  # NE condition
            valid | (1 << 21),                # writeback
            valid & ~(1 << 24),               # post-indexed
            valid & ~(1 << 23),               # negative offset
            valid | (1 << 25),                # register/shifted offset
            valid | (15 << 16),               # PC base
            valid & ~(15 << 12) | (15 << 12),  # PC source
            0xe5c02040,                       # unknown source
            0xe5d01040,                       # load to R1
            0xe5900040,                       # already handled by earlier loop
            0xea000000,                       # branch
        ):
            with self.subTest(opcode=hex(word)):
                self.assertIsNone(a01.decode(words(word, prior.BX_LR), 0x1000))
        self.assertIsNone(a01.decode(words(valid, 0xe12fff10), 0x1000))
        self.assertIsNone(a01.decode(words(valid), 0x1000))
        self.assertIsNone(a01.decode(words(valid, prior.BX_LR), 0x1002))
        self.assertIsNone(a01.decode(words(0xe5900601, prior.BX_LR), 0x1000))

    def test_strb_masks_low_byte_and_preserves_neighboring_bytes(self):
        spec = a01.decode(words(0xe5c01040, prior.BX_LR), 0x1000)
        regs, before, after, reads, writes = a01.expected_effect(spec, 0xdeadbeef)
        self.assertEqual(reads, [])
        self.assertEqual(writes, [(a01.BASE + 64, 1, regs[1] & 255)])
        self.assertEqual(after[:64], before[:64])
        self.assertEqual(after[65:], before[65:])
        self.assertEqual(after[0x900:0x908], a01.CANARY)

    def test_ldrb_zero_extends_and_ldr_preserves_memory(self):
        for word, width in ((0xe5d00004, 1), (0xe5900584, 4)):
            with self.subTest(word=hex(word)):
                spec = a01.decode(words(word, prior.BX_LR), 0x1000)
                regs, before, after, reads, writes = a01.expected_effect(spec, 0xa5a5a5a5)
                self.assertEqual(before, after)
                self.assertEqual(writes, [])
                self.assertEqual(reads, [(a01.BASE + spec["offset"], width)])
                self.assertLess(regs[0], 1 << (width * 8))

    def test_actual_unicorn_strb_ldrb_ldr_machine_regression(self):
        for word in (0xe5c01040, 0xe5c01004, 0xe5d00004,
                     0xe5900054, 0xe5900584, 0xe5900588):
            address = 0xa1000
            raw = words(word, prior.BX_LR)
            entry = {"address": f"{address:08x}", "size": 8, "raw_hex": raw.hex(),
                     "contract": a01.decode(raw, address)}
            self.assertIsNotNone(entry["contract"])
            with self.subTest(opcode=hex(word)):
                def reader(binary, addr, size):
                    if (addr, size) != (address, 8):
                        raise ValueError("Unlisted synthetic opcode read")
                    return raw

                with mock.patch.object(semantic_evidence, "read_function", side_effect=reader):
                    for seed in (0, 0x12345678, 0xffffffff):
                        for flags in (0, 0x20000000, 0x40000000, 0x90000000):
                            a01.execute(None, entry, seed, flags)

    def test_refuse_untested_jumps_and_require_checkpoint_identity(self):
        row = {"address": "002a1268", "size": 4, "raw_hex": "feffffea",
               "assembly": ["b #0x2a1268"], "contract": None,
               "status": "unmodeled_not_executed"}
        self.assertIsNone(a01.decode(bytes.fromhex(row["raw_hex"]), int(row["address"], 16)))
        with self.assertRaisesRegex(ValueError, "Refusing"):
            a01.execute(None, row, 0, 0)
        state = a01.checkpoint("a" * 64, "b" * 64, "c" * 64, [row], [])
        self.assertEqual(state["new_certificates"], 0)
        self.assertIn("não são executados", a01.render(state))


if __name__ == "__main__":
    unittest.main()
