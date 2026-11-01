"""struct_pass.py must pick Capstone's Thumb mode for odd (interworking)
function addresses, the same gap fixed in jtable.py (see test_jtable.py and
RE_COMPLETUDE_TASKS.md T06/T07).
"""
import io
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

import elf_test_fixture
import struct_pass

THUMB_PUSH_POP = bytes.fromhex("08b5") + bytes.fromhex("08bd")
ARM_MOV_BX = bytes.fromhex("0000a0e3") + bytes.fromhex("1eff2fe1")


def run_struct_pass(elf_path: str, start_hex: str, end_arg: str) -> str:
    buf = io.StringIO()
    old_argv = sys.argv
    sys.argv = ["struct_pass.py", elf_path, start_hex, end_arg]
    try:
        with redirect_stdout(buf):
            struct_pass.main()
    finally:
        sys.argv = old_argv
    return buf.getvalue()


class ThumbModeTests(unittest.TestCase):
    def _write(self, text_bytes: bytes) -> str:
        data = elf_test_fixture.build_elf(text_bytes)
        f = tempfile.NamedTemporaryFile(suffix=".so", delete=False)
        f.write(data)
        f.close()
        self.addCleanup(lambda: Path(f.name).unlink(missing_ok=True))
        return f.name

    def test_odd_address_decodes_as_thumb_with_full_coverage(self):
        path = self._write(THUMB_PUSH_POP)
        odd_start = hex(elf_test_fixture.TEXT_VADDR | 1)[2:]
        out = run_struct_pass(path, odd_start, "+4")
        self.assertIn("Thumb mode", out)
        self.assertIn("reached 2 of ~2 possible instruction slots", out)

    def test_even_address_still_decodes_as_arm_with_full_coverage(self):
        path = self._write(ARM_MOV_BX)
        even_start = hex(elf_test_fixture.TEXT_VADDR)[2:]
        out = run_struct_pass(path, even_start, "+8")
        self.assertIn("ARM mode", out)
        self.assertNotIn("Thumb mode", out)
        self.assertIn("reached 2 of ~2 possible instruction slots", out)


if __name__ == "__main__":
    unittest.main()
