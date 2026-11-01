"""jtable.py must pick Capstone's Thumb mode for odd (interworking) function
addresses, instead of the ARM32-only mode it used before. Without this,
Thumb bytes decode as either nothing or nonsense ARM32, and jtable.py was
observed reporting that as "100% coverage, 0 bl targets" for functions it
never actually analyzed (see RE_COMPLETUDE_TASKS.md T06/T07).
"""
import io
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

import elf_test_fixture
import jtable

DIR = Path(__file__).resolve().parent

# push {r3, lr} ; pop {r3, pc}  -- a minimal, real, two-instruction Thumb body
THUMB_PUSH_POP = bytes.fromhex("08b5") + bytes.fromhex("08bd")
# mov r0, #0 ; bx lr  -- a minimal, real, two-instruction A32 body
ARM_MOV_BX = bytes.fromhex("0000a0e3") + bytes.fromhex("1eff2fe1")


def run_jtable(elf_path: str, start_hex: str, end_arg: str) -> str:
    buf = io.StringIO()
    old_argv = sys.argv
    sys.argv = ["jtable.py", elf_path, start_hex, end_arg]
    try:
        with redirect_stdout(buf):
            jtable.main()
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
        out = run_jtable(path, odd_start, "+4")
        self.assertIn("Thumb mode", out)
        self.assertIn("coverage: 2 of ~2 instruction slots (100%)", out)
        self.assertIn("jump tables resolved: 0", out)

    def test_even_address_still_decodes_as_arm_with_full_coverage(self):
        path = self._write(ARM_MOV_BX)
        even_start = hex(elf_test_fixture.TEXT_VADDR)[2:]
        out = run_jtable(path, even_start, "+8")
        self.assertIn("ARM mode", out)
        self.assertNotIn("Thumb mode", out)
        self.assertIn("coverage: 2 of ~2 instruction slots (100%)", out)

    def test_thumb_bytes_misread_as_arm_is_the_bug_being_fixed(self):
        # Documents *why* the mode matters: the same bytes this test proves
        # decode cleanly in Thumb mode either fail to decode at all, or
        # decode into nonsense, when forced through ARM32 -- which is
        # exactly what jtable.py did before this fix for every odd-address
        # function (confirmed against the real binary in T06/T07).
        from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
        md = Cs(CS_ARCH_ARM, CS_MODE_ARM)
        decoded = list(md.disasm(THUMB_PUSH_POP, elf_test_fixture.TEXT_VADDR))
        self.assertNotEqual(
            [(i.mnemonic, i.op_str) for i in decoded],
            [("push", "{r3, lr}"), ("pop", "{r3, pc}")],
        )

    def test_cli_subprocess_still_works_end_to_end(self):
        # The real caller (parallel_loop.py) invokes this as a subprocess,
        # not by importing main() -- make sure that path is intact too.
        path = self._write(THUMB_PUSH_POP)
        odd_start = hex(elf_test_fixture.TEXT_VADDR | 1)[2:]
        proc = subprocess.run(
            [sys.executable, str(DIR / "jtable.py"), path, odd_start, "+4"],
            capture_output=True, text=True, check=True,
        )
        self.assertIn("Thumb mode", proc.stdout)


if __name__ == "__main__":
    unittest.main()
