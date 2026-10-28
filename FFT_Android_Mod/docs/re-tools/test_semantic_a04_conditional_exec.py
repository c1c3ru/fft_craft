"""A04 original ELF conditional BXNE boundary, not full function."""
import unittest
from unittest import mock

import semantic_a04_conditional_exec as cond
import semantic_a02_branch_11 as a02
import semantic_evidence


class ConditionalA04Tests(unittest.TestCase):
    def test_conditional_provenance_matches_exact_a02_source(self):
        src = a02.decode(bytes.fromhex(a02.EXPECTED[f"{cond.SOURCE:08x}"][0]), cond.SOURCE)
        self.assertEqual(src["target"], cond.TARGET)
        self.assertEqual(cond.PREFIX_HEX, "002050e21eff2f11")

    def test_subs_nzcv_independent_reference_and_branch_decision(self):
        cases = {
            0: (cond.FALLTHROUGH, 0x60000010),
            1: (cond.RETURN, 0x20000010),
            0x80000000: (cond.RETURN, 0xa0000010),
            0xffffffff: (cond.RETURN, 0xa0000010),
        }
        for val, (destination, cpsr) in cases.items():
            for seed in (0, 0xa5a5a5a5, 0xffffffff):
                regs, observed_flags, target = cond.model(seed, val)
                self.assertEqual(target, destination)
                self.assertEqual(observed_flags, cpsr)
                self.assertEqual(regs[0], val)
                self.assertEqual(regs[2], val)

    def test_actual_unicorn_for_return_and_fallthrough_boundary(self):
        original = {
            cond.SOURCE: bytes.fromhex(a02.EXPECTED[f"{cond.SOURCE:08x}"][0]),
            cond.TARGET: bytes.fromhex(cond.PREFIX_HEX),
        }
        def fetch(binary, address, length):
            if address not in original or length != len(original[address]):
                raise AssertionError("Unlisted original ARM opcode")
            return original[address]
        with mock.patch.object(semantic_evidence, "read_function", side_effect=fetch):
            cond.exact_original(None)
            for value in cond.VALUES:
                for seed in (0, 0x12345678, 0xffffffff):
                    for flags in (0, 0x40000000, 0x90000000):
                        with self.subTest(value=value, seed=seed, flags=flags):
                            cond.execute(None, seed, value, flags)
            original[cond.TARGET] = bytes(8)
            with self.assertRaisesRegex(ValueError, "bytes have changed"):
                cond.exact_original(None)

    def test_checkpoint_cannot_create_certification(self):
        state = cond.snapshot("a"*64, "b"*64, [
            {"iteration": 1, "r2_input": 0, "cases": 32,
             "branch": "fallthrough_stopped", "status": "bounded_pass"}])
        self.assertEqual(state["new_certificates"], 0)
        self.assertIn("UNKNOWN", cond.report(state).upper())
        self.assertNotEqual(cond.RETURN, cond.FALLTHROUGH)


if __name__ == "__main__":
    unittest.main()
