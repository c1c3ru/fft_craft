"""A04 safety and repeatability tests; no code/data or equivalence claims."""
import hashlib
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import semantic_a02_branch_11 as a02
import semantic_a04_destinations as a04
import semantic_evidence


class A04Tests(unittest.TestCase):
    def test_seven_destinations_and_four_shared_dispatcher_inputs(self):
        mapping = a04.mapped_sources()
        self.assertEqual(len(mapping), 7)
        self.assertEqual(sum(len(x) for x in mapping.values()), 10)
        self.assertEqual(
            {x["entry"] for x in mapping["000b6c58"]},
            {"000b6c68", "000b6cd0", "000b6ee0", "000b6ee8"})
        self.assertNotIn("002a1268", mapping)

    def test_bytes_belong_to_original_sources_before_destination_inspection(self):
        source = {int(key, 16): bytes.fromhex(words)
                  for key, (words, _) in a02.EXPECTED.items()}
        def fetch(binary, address, size):
            if address not in source:
                raise ValueError("Unexpected address")
            self.assertEqual(size, len(source[address]))
            return source[address]
        with mock.patch.object(semantic_evidence, "read_function", side_effect=fetch):
            a04.verify_sources(None)
        def altered(binary, address, size):
            if address == 0x00072910:
                return bytes(size)
            return fetch(binary, address, size)
        with mock.patch.object(semantic_evidence, "read_function", side_effect=altered):
            with self.assertRaisesRegex(ValueError, "source mismatch"):
                a04.verify_sources(None)

    def test_first_transfer_is_candidate_only_and_not_executed(self):
        data = bytes.fromhex("1eff2fe1") + bytes(92)  # BX LR then data
        with mock.patch.object(semantic_evidence, "read_function", return_value=data):
            entry = a04.inspect(None, 0x000b6c58, [{"entry": "000b6cd0", "op": "mov_r2_one"}])
        self.assertEqual(len(entry["candidate_insns"]), 1)
        self.assertEqual(entry["first_transfer"]["op"], "bx")
        self.assertIsNone(entry["first_transfer"]["immediate_destination"])
        self.assertIs(entry["first_transfer"]["executed"], False)
        self.assertEqual(entry["code_vs_data"], "unproven")
        self.assertEqual(entry["whole_function"], "unknown")

    def test_hash_mismatch_never_inspects_elf(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "binary"
            path.write_bytes(bytes(123))
            with self.assertRaisesRegex(ValueError, "hash mismatch"):
                a04.build(path)

    def test_report_and_checkpoint_never_promote_certificates(self):
        sample = {
            "schema": 1, "elf_sha256": a04.ELF_DIGEST,
            "unique_external_targets": 7, "original_file_bytes": 672,
            "destinations_executed": 0, "new_certificates": 0,
            "targets": [{"address": "000b6c58", "from": [{"entry": "000b6cd0", "op": "mov_r2_one"}],
                         "candidate_insns": [], "first_transfer": None}],
        }
        report = a04.report(sample)
        self.assertIn("unverified", report)
        self.assertIn("provenance", report)
        self.assertEqual(sample["new_certificates"], 0)
        self.assertEqual(sample["destinations_executed"], 0)


if __name__ == "__main__":
    unittest.main()
