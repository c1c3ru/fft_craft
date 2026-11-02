"""T15 (RE_COMPLETUDE_TASKS.md) vertical slice: differential test of the
real nextTurnOrder() ARM body (0x1fd1dc, 36 B) against a compiled,
independent C reimplementation (c-models/t15_nextturnorder.c).

No `bl` in this function -- fully self-contained, confirmed by
jtable.py. The turn-index global is built as real memory in the ELF's
own GOT-resolved address, same technique as
test_t21_pagenext_cursor.py/test_t19_evt_get_flgdt.py.
"""
import ctypes
import subprocess
import tempfile
import unittest
from pathlib import Path

import differential_harness as dh

DIR = Path(__file__).resolve().parent
SO = DIR.parents[1] / "src/lib/armeabi/libgl2jni.so"
START, END = 0x1fd1dc, 0x1fd1dc + 36

# Real GOT slot address, resolved by hand from the literal pool +
# pc-relative chain (also shared with resetTurnOrder -- see NOTES
# sec. 673).
GOT_PAGE = 0x347000
TURN_INDEX_SLOT = 0x3475dc
TURN_INDEX_VAR = 0x600000   # this test's own stand-in for the real global


def build_model(output: Path):
    subprocess.run(
        ["cc", "-std=c11", "-O2", "-Wall", "-Wextra", "-Werror", "-pedantic",
         "-shared", "-fPIC", str(DIR / "c-models/t15_nextturnorder.c"),
         "-o", str(output)],
        check=True, capture_output=True,
    )
    lib = ctypes.CDLL(str(output))
    fn = lib.nextTurnOrder_model
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
    lib.nextTurnOrder_model(ctypes.byref(turn_index))
    return turn_index.value


CASES = [0, 1, 20, 38, 39, 40, 0x7fffffff]


class NextTurnOrderDifferentialTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        cls.lib = build_model(Path(cls.temp.name) / "model.so")

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def test_matches_for_every_case(self):
        for initial_value in CASES:
            with self.subTest(initial_value=initial_value):
                res = run_original(initial_value)
                self.assertTrue(res.ok, res.error)
                model_value = run_model(self.lib, initial_value)

                real_value = int.from_bytes(res.final_buffers["turn_index"], "little", signed=True)
                self.assertEqual(real_value, model_value)

    def test_fault_injection_boundary_is_strictly_greater_than(self):
        # The real instructions compute new = old+1 THEN compare new
        # (not old) against 39 with `movgt` (strictly greater than).
        # So old=38 -> new=39, 39>39 is false -> stays 39 (no wrap
        # yet); old=39 -> new=40, 40>39 is true -> wraps to 0. A model
        # that wrapped one step early (e.g. comparing old, or using
        # >=39 on new) would diverge exactly at old=38.
        res_38 = run_original(38)
        self.assertTrue(res_38.ok, res_38.error)
        self.assertEqual(int.from_bytes(res_38.final_buffers["turn_index"], "little"), 39)

        res_39 = run_original(39)
        self.assertTrue(res_39.ok, res_39.error)
        self.assertEqual(int.from_bytes(res_39.final_buffers["turn_index"], "little"), 0)


if __name__ == "__main__":
    unittest.main()
