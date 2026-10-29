"""Reject incorrect ARM GetRootPath field offsets, instructions and returns."""
import unittest
from pathlib import Path
from unittest.mock import patch

import semantic_evidence
import semantic_a04_rootpath_field as p


class GetterTests(unittest.TestCase):
    def check_original(self, raw):
        # Fixture bytes never replace the real binary in production's CI.
        with patch.object(Path, "read_bytes", return_value=b"synthetic"), \
             patch.object(p.hashlib, "sha256") as digest, \
             patch.object(semantic_evidence, "read_function", return_value=raw):
            digest.return_value.hexdigest.return_value=p.SHA
            return p.require_original(Path("synthetic"))

    def test_exact_a32_accessor(self):
        raw=(0xe2800098).to_bytes(4,"little")+(0xe12fff1e).to_bytes(4,"little")
        self.assertEqual(self.check_original(raw),raw)

    def test_wrong_offset_rejected(self):
        bad=(0xe2800094).to_bytes(4,"little")+(0xe12fff1e).to_bytes(4,"little")
        with self.assertRaises(ValueError):
            self.check_original(bad)

    def test_wrong_return_instruction_rejected(self):
        bad=(0xe2800098).to_bytes(4,"little")+(0xe1a00000).to_bytes(4,"little")
        with self.assertRaises(ValueError):
            self.check_original(bad)


if __name__=="__main__":
    unittest.main()
