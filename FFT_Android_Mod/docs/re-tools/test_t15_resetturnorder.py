"""T15 (RE_COMPLETUDE_TASKS.md) vertical slice: differential test of the
real resetTurnOrder() ARM body (0x1fd2ac, 24 B) against a compiled,
independent C reimplementation (c-models/t15_resetturnorder.c).

Shares the exact same GOT slot/global as nextTurnOrder (confirmed by
hand, NOTES sec. 673) -- same GOT_PAGE/TURN_INDEX_SLOT constants as
test_t15_nextturnorder.py.
"""
import ctypes
import subprocess
import tempfile
import unittest
from pathlib import Path

import differential_harness as dh

DIR = Path(__file__).resolve().parent
SO = DIR.parents[1] / "src/lib/armeabi/libgl2jni.so"
START, END = 0x1fd2ac, 0x1fd2ac + 24

GOT_PAGE = 0x347000
TURN_INDEX_SLOT = 0x3475dc
TURN_INDEX_VAR = 0x600000


def build_model(output: Path):
    subprocess.run(
        ["cc", "-std=c11", "-O2", "-Wall", "-Wextra", "-Werror", "-pedantic",
         "-shared", "-fPIC", str(DIR / "c-models/t15_resetturnorder.c"),
         "-o", str(output)],
        check=True, capture_output=True,
    )
    lib = ctypes.CDLL(str(output))
    fn = lib.resetTurnOrder_model
    fn.argtypes = [ctypes.POINTER(ctypes.c_int32)]
    fn.restype = None
    return lib


def _pack32(value: int) -> bytes:
    return (value & 0xffffffff).to_bytes(4, "little")


def run_original(initial_value):
    got_page = bytearray(0x1000)
    got_page[TURN_INDEX_SLOT - GOT_PAGE:TURN_INDEX_SLOT - GOT_PAGE + 4] = _pack32(TURN_INDEX_VAR)

    res = dh.run_original(
        SO, START, END, {},
        buffers=[
            dh.MemoryBuffer("got_page", GOT_PAGE, bytes(got_page)),
            dh.MemoryBuffer("turn_index", TURN_INDEX_VAR, _pack32(initial_value)),
        ],
    )
    return res


def run_model(lib, initial_value):
    turn_index = ctypes.c_int32(initial_value)
    lib.resetTurnOrder_model(ctypes.byref(turn_index))
    return turn_index.value


class ResetTurnOrderDifferentialTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        cls.lib = build_model(Path(cls.temp.name) / "model.so")

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def test_matches_for_every_case(self):
        for initial_value in (0, 1, 39, -1, 0x7fffffff):
            with self.subTest(initial_value=initial_value):
                res = run_original(initial_value)
                self.assertTrue(res.ok, res.error)
                model_value = run_model(self.lib, initial_value)
                self.assertEqual(int.from_bytes(res.final_buffers["turn_index"], "little"), 0)
                self.assertEqual(model_value, 0)


if __name__ == "__main__":
    unittest.main()
