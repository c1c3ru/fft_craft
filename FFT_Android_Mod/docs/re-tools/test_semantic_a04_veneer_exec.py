"""Original ARM A04 indirect veneer safety, addressing and GOT effects."""
import unittest
from unittest import mock

import semantic_a02_branch_11 as a02
import semantic_a04_veneer_exec as veneer
import semantic_evidence


class VeneerTests(unittest.TestCase):
    def test_original_two_veneer_offsets_and_source_branches(self):
        self.assertEqual(len(veneer.VENEERS), 2)
        self.assertEqual(veneer.VENEERS[0x714dc]["slot"], 0x347d84)
        self.assertEqual(veneer.VENEERS[0x714e8]["slot"], 0x347d88)
        for target, cfg in veneer.VENEERS.items():
            src = cfg["source"]
            self.assertEqual(
                a02.decode(bytes.fromhex(a02.EXPECTED[f"{src:08x}"][0]), src)["target"],
                target)

    def test_independent_reference_changes_only_r0_and_ip(self):
        for target, cfg in veneer.VENEERS.items():
            for seed in (0, 0xdeadbeef, 0xffffffff):
                initial, result, got = veneer.expected(seed, cfg["kind"], cfg["slot"])
                self.assertEqual(len(got), 256)
                self.assertEqual(result[12], cfg["slot"])
                self.assertEqual(initial[1:12], result[1:12])
                val = int.from_bytes(got[(cfg["slot"]&255):(cfg["slot"]&255)+4], "little")
                self.assertEqual(val, veneer.TRAP)
                if cfg["kind"] == "mul":
                    self.assertEqual(result[0], (initial[2]*initial[1]) & veneer.MASK)
                else:
                    self.assertEqual(result[0], initial[1])

    def test_real_unicorn_executes_sources_and_original_veneer_not_target(self):
        snippets = {a: bytes.fromhex(c["opcode"]) for a, c in veneer.VENEERS.items()}
        for cfg in veneer.VENEERS.values():
            addr = cfg["source"]
            snippets[addr] = bytes.fromhex(a02.EXPECTED[f"{addr:08x}"][0])

        def read(binary, address, size):
            if address not in snippets or len(snippets[address]) != size:
                raise AssertionError("Unknown original ELF address")
            return snippets[address]

        with mock.patch.object(semantic_evidence, "read_function", side_effect=read):
            veneer.validate_sources(None)
            for target in veneer.VENEERS:
                for seed in (0, 0x12345678, 0xffffffff):
                    for flags in (0, 0x20000000, 0xa0000000):
                        with self.subTest(target=hex(target), seed=seed, flags=flags):
                            veneer.execute(None, target, seed, flags)
            with self.assertRaisesRegex(ValueError, "Unlisted"):
                veneer.execute(None, 0, 0, 0)

    def test_modified_veneer_word_is_not_accepted(self):
        snippets = {a: bytes.fromhex(c["opcode"]) for a, c in veneer.VENEERS.items()}
        for cfg in veneer.VENEERS.values():
            s = cfg["source"]
            snippets[s] = bytes.fromhex(a02.EXPECTED[f"{s:08x}"][0])
        snippets[0x714dc] = bytes(12)
        with mock.patch.object(
            semantic_evidence, "read_function",
            side_effect=lambda b, a, s: snippets[a]):
            with self.assertRaisesRegex(ValueError, "Original ELF byte mismatch"):
                veneer.validate_sources(None)

    def test_no_semantic_certificate_promoted(self):
        result = veneer.snapshot("a"*64, "b"*64, [])
        self.assertEqual(result["new_certificates"], 0)
        self.assertIn("unknown", veneer.render(result).lower())


if __name__ == "__main__":
    unittest.main()
