"""Safety regressions for the original ELF A02 11-entry ARM branch boundary."""
import unittest
from unittest import mock

import semantic_a02_branch_11 as a02
import semantic_evidence


class A02Tests(unittest.TestCase):
    def test_original_elf_byte_allowlist_and_destinations(self):
        destinations = {
            "00072910": 0x2b1bb0, "00082404": 0x714e8,
            "0008240c": 0x714dc, "000a94bc": 0xab674,
            "000b4700": 0xb461c, "000b6c68": 0xb6c58,
            "000b6cd0": 0xb6c58, "000b6ee0": 0xb6c58,
            "000b6ee8": 0xb6c58, "000b6f80": 0xb8a18,
            "002a1268": 0x2a1268,
        }
        self.assertEqual(set(destinations), set(a02.EXPECTED))
        for key, target in destinations.items():
            with self.subTest(key=key):
                hexbytes, op = a02.EXPECTED[key]
                spec = a02.decode(bytes.fromhex(hexbytes), int(key, 16))
                self.assertIsNotNone(spec)
                self.assertEqual(spec["target"], target)
                self.assertEqual(spec["op"], op)

    def test_unknown_or_modified_opcode_is_never_run(self):
        self.assertIsNone(a02.decode(bytes.fromhex("00000000"), 0x00072910))
        self.assertIsNone(a02.decode(bytes.fromhex("0200a0e1a5fc08eb"), 0x00072910))
        self.assertIsNone(a02.decode(bytes.fromhex("feffffea"), 0x00072914))
        self.assertIsNone(a02.decode(bytes.fromhex("feffffea"), 0x002a126a))
        with self.assertRaisesRegex(ValueError, "unconditional"):
            a02.branch_target(0xeb000000, 0x1000)

    def test_references_are_independent_and_no_unmodeled_writes(self):
        for key in a02.EXPECTED:
            with self.subTest(key=key):
                original = bytes.fromhex(a02.EXPECTED[key][0])
                spec = a02.decode(original, int(key, 16))
                for seed in (0, 1, 0xffffffff):
                    regs, memory, reads = a02.reference(spec, seed)
                    self.assertEqual(len(regs), 13)
                    self.assertEqual(memory[0x300:0x308], a02.CANARY)
                    self.assertEqual(reads, [(a02.BASE, 4)] if spec["op"] == "ldr_r0_ptr" else [])
                    if spec["op"] == "mul_r0_r2_r1":
                        self.assertEqual(regs[0], (regs[1] * regs[2]) & a02.MASK)
                    if spec["op"] == "self_branch":
                        self.assertEqual(regs[0], seed)

    def test_real_unicorn_executes_prefix_but_not_destination(self):
        for key in a02.EXPECTED:
            address = int(key, 16)
            raw = bytes.fromhex(a02.EXPECTED[key][0])
            row = {"address": key, "size": len(raw), "raw_hex": raw.hex(),
                   "contract": a02.decode(raw, address)}
            def mocked_elf(binary, loc, size):
                if (loc, size) != (address, len(raw)):
                    raise AssertionError("unexpected original ELF range")
                return raw
            with self.subTest(key=key):
                with mock.patch.object(semantic_evidence, "read_function", side_effect=mocked_elf):
                    for seed in (0, 0x12345678, 0xffffffff):
                        for flags in (0, 0x40000000, 0x90000000):
                            a02.execute(None, row, seed, flags)

    def test_static_catalog_refuses_missing_elf_or_duplicate(self):
        rows = []
        for key, (hexbytes, op) in a02.EXPECTED.items():
            rows.append({"address": key, "size": len(bytes.fromhex(hexbytes)),
                         "raw_hex": hexbytes, "assembly": [], "contract": None})
        def read(binary, loc, size):
            return bytes.fromhex(a02.EXPECTED[f"{loc:08x}"][0])
        with mock.patch.object(semantic_evidence, "read_function", side_effect=read):
            classified = a02.classify(None, rows)
            self.assertEqual(len(classified), 11)
            self.assertEqual(sum(x["contract"]["op"] == "self_branch" for x in classified), 1)
            with self.assertRaisesRegex(ValueError, "incomplete or duplicated"):
                a02.classify(None, rows + rows[:1])

    def test_state_never_claims_full_function_or_formal_certificate(self):
        item = {"address": "002a1268", "raw_hex": "feffffea",
                "assembly": ["b #0x2a1268"],
                "contract": a02.decode(bytes.fromhex("feffffea"), 0x2a1268)}
        state = a02.snapshot("a"*64, "b"*64, "c"*64, [item], [])
        self.assertEqual(state["new_certificates"], 0)
        rendered = a02.render(state)
        self.assertIn("NOT", rendered)
        self.assertIn("not proven", rendered)


if __name__ == "__main__":
    unittest.main()
