"""T17 (RE_COMPLETUDE_TASKS.md) vertical slice: differential test of the
real ClearMove(MOVE*) ARM body (0x27383c, 40 B) against a compiled,
independent C reimplementation (c-models/t17_clearmove.c).

No `bl` in this function -- fully self-contained, confirmed by
jtable.py. The MOVE pointer is passed in r0 directly, no global
indirection involved.
"""
import ctypes
import subprocess
import tempfile
import unittest
from pathlib import Path

import differential_harness as dh

DIR = Path(__file__).resolve().parent
SO = DIR.parents[1] / "src/lib/armeabi/libgl2jni.so"
START, END = 0x27383c, 0x27383c + 40

MOVE_ADDR = 0x600000
MOVE_SIZE = 0x20


def build_model(output: Path):
    subprocess.run(
        ["cc", "-std=c11", "-O2", "-Wall", "-Wextra", "-Werror", "-pedantic",
         "-shared", "-fPIC", str(DIR / "c-models/t17_clearmove.c"),
         "-o", str(output)],
        check=True, capture_output=True,
    )
    lib = ctypes.CDLL(str(output))
    fn = lib.ClearMove_model
    fn.argtypes = [ctypes.c_void_p]
    fn.restype = None
    return lib


def _sentinel_move_bytes():
    return bytes((i + 1) & 0xff or 1 for i in range(MOVE_SIZE))


def run_original():
    move_bytes = _sentinel_move_bytes()
    res = dh.run_original(
        SO, START, END, {"r0": MOVE_ADDR},
        buffers=[dh.MemoryBuffer("move", MOVE_ADDR, move_bytes)],
    )
    return res


def run_model(lib):
    move_buf = (ctypes.c_uint8 * MOVE_SIZE)(*_sentinel_move_bytes())
    lib.ClearMove_model(move_buf)
    return bytes(move_buf)


class ClearMoveDifferentialTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        cls.lib = build_model(Path(cls.temp.name) / "model.so")

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def test_fields_cleared_rest_untouched(self):
        res = run_original()
        self.assertTrue(res.ok, res.error)
        model_bytes = run_model(self.lib)

        original = res.final_buffers["move"]
        self.assertEqual(original, model_bytes)

        expected = bytearray(_sentinel_move_bytes())
        expected[0x1] = 0
        expected[0x3] = 5
        expected[0x1c] = 0
        expected[0x1d] = 0
        expected[0x1e:0x20] = (0x8001).to_bytes(2, "little")
        self.assertEqual(original, bytes(expected))

    def test_fault_injection_field_0x0_and_0x2_survive(self):
        # A model that (wrongly) cleared the whole struct, or zeroed a
        # wider prefix, would diverge from the real ELF, which leaves
        # +0x0 and +0x2 at their original sentinel values.
        res = run_original()
        self.assertTrue(res.ok, res.error)
        move = res.final_buffers["move"]
        sentinel = _sentinel_move_bytes()
        self.assertEqual(move[0x0], sentinel[0x0])
        self.assertEqual(move[0x2], sentinel[0x2])
        self.assertNotEqual(move[0x0], 0)
        self.assertNotEqual(move[0x2], 0)


if __name__ == "__main__":
    unittest.main()
