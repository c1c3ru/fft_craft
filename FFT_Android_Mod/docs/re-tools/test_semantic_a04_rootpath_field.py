"""Fail closed on mutated ARM CAPP_INFO::GetRootPath accessor."""
import unittest
from pathlib import Path
from unittest.mock import patch
import semantic_evidence
import semantic_a04_rootpath_field as p


class GetterTests(unittest.TestCase):
    def test_exact_a32_accessor(self):
        raw=(0xe2800098).to_bytes(4,"little")+(0xe12fff1e).to_bytes(4,"little")
        with patch.object(p.hashlib,"sha256") as digest, patch.object(
                semantic_evidence,"read_function",return_value=raw):
            digest.return_value.hexdigest.return_value=p.SHA
            self.assertEqual(p.require_original(Path("synthetic")),raw)

    def test_wrong_offset_rejected(self):
        bad=(0xe2800094).to_bytes(4,"little")+(0xe12fff1e).to_bytes(4,"little")
        with patch.object(p.hashlib,"sha256") as digest, patch.object(
                semantic_evidence,"read_function",return_value=bad):
            digest.return_value.hexdigest.return_value=p.SHA
            with self.assertRaises(ValueError):
                p.require_original(Path("synthetic"))

    def test_wrong_return_instruction_rejected(self):
        bad=(0xe2800098).to_bytes(4,"little")+(0xe1a00000).to_bytes(4,"little")
        with patch.object(p.hashlib,"sha256") as digest, patch.object(
                semantic_evidence,"read_function",return_value=bad):
            digest.return_value.hexdigest.return_value=p.SHA
            with self.assertRaises(ValueError):
                p.require_original(Path("synthetic"))


if __name__=="__main__":
    unittest.main()
