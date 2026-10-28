"""A04 original ELF BL entry boundaries: never execute unknown callees."""
import unittest
from unittest import mock

import semantic_a04_bl_boundaries as target
import semantic_a02_branch_11 as a02
import semantic_evidence


class BlBoundaryTests(unittest.TestCase):
    def test_original_sources_and_destinations_are_exact(self):
        self.assertEqual(target.SOURCE, 0xb4700)
        self.assertEqual(a02.decode(
            bytes.fromhex(a02.EXPECTED["000b4700"][0]), target.SOURCE)["target"],
            target.SIMPLE_TARGET)
        self.assertEqual(target.PAIR, ((0xab674, 0xb6620), (0xb461c, 0xb45d0)))

    def test_a32_bl_decode_rejects_unknown_call(self):
        # BL 0xb45d0 located at 0xb4628 = signed A32 imm24.
        pc = 0xb4628
        displacement = 0xb45d0 - (pc + 8)
        word = 0xeb000000 | ((displacement >> 2) & 0xffffff)
        self.assertEqual(word >> 24, 0xeb)
        self.assertEqual(
            (pc + 8 + ((word & 0xffffff) << 2) - (1 << 26)) & target.MASK,
            0xb45d0)

    def test_independent_model_preserves_stack_order_and_neighboring_memory(self):
        for seed in (0, 1, 0xdeadbeef, 0xffffffff):
            registers, writes = target.oracle(seed)
            start = [(seed ^ (i*0x11111111)) & target.MASK for i in range(13)]
            self.assertEqual(registers[1], 0)
            self.assertEqual(registers[5], start[0])
            self.assertEqual(registers[4], 0)
            self.assertEqual(writes, [
                (target.SP-16, 4, start[4]), (target.SP-12, 4, start[5]),
                (target.SP-8, 4, start[6]), (target.SP-4, 4, target.RETURN),
            ])

    def test_synthetic_bytes_execute_only_up_to_original_bl(self):
        caller = bytes.fromhex(a02.EXPECTED["000b4700"][0])
        # A32: push {r4,r5,r6,lr}; mov r5,r0; mov r4,r1; bl 0xb45d0.
        pc = target.SIMPLE_TARGET + 12
        displacement = 0xb45d0 - (pc + 8)
        bl = (0xeb000000 | ((displacement >> 2) & 0xffffff)).to_bytes(4, "little")
        body = bytes.fromhex("70402de90050a0e10140a0e1") + bl
        # Check actual original ELF gates in the mock and run real Unicorn.
        source = {target.SOURCE: caller, target.SIMPLE_TARGET: body}
        def fetch(binary, addr, size):
            if addr not in source or size != len(source[addr]):
                raise AssertionError("Unexpected original ELF read")
            return source[addr]
        with mock.patch.object(semantic_evidence, "read_function", side_effect=fetch):
            target.prefix_original(None)
            for seed in (0, 0x12345678, 0xffffffff):
                for flags in (0, 0x20000000, 0x40000000, 0x90000000):
                    with self.subTest(seed=seed, flags=flags):
                        target.execute(None, seed, flags)
            source[target.SIMPLE_TARGET] = bytes(len(body))
            with self.assertRaisesRegex(ValueError, "prologue"):
                target.prefix_original(None)

    def test_static_bl_first_target_requires_correct_original_destination(self):
        src = target.SIMPLE_TARGET
        pc = src + 12
        displacement = 0xb45d0 - (pc + 8)
        good_bl = (0xeb000000 | ((displacement >> 2) & 0xffffff)).to_bytes(4, "little")
        body = bytes.fromhex("70402de90050a0e10140a0e1") + good_bl
        # Static scan itself cannot prove the callee. Refuse a changed first BL.
        with mock.patch.object(
                semantic_evidence, "read_function",
                return_value=body + bytes(target.SCAN_BYTES - len(body))):
            row = target.first_call(None, src, 0xb45d0)
            self.assertEqual(row["call"]["target"], "000b45d0")
            self.assertFalse(row["call"]["executed"])
            with self.assertRaisesRegex(ValueError, "target"):
                target.first_call(None, src, 0xb6620)

    def test_snapshot_only_records_a_bounded_prefix(self):
        state = {"callsites": [], "scanned_bytes": 672}
        snap = target.checkpoint(state, [
            {"iteration": 1, "cases": 32, "scope": "stop_before_original_BL"}
        ])
        self.assertEqual(snap["new_certificates"], 0)
        msg = target.report(snap)
        self.assertIn("BEFORE", msg)
        self.assertIn("zero BL targets executed", msg)


if __name__ == "__main__":
    unittest.main()
