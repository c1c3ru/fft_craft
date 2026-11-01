"""T21 (RE_COMPLETUDE_TASKS.md) vertical slice: differential test of the
real pagenext_cursor(PAGEWININFO*) ARM body (0x270b04, 88 B) against a
compiled, independent C reimplementation (c-models/t21_pagenext_cursor.c).

No `bl` in this function (0 external calls, confirmed by jtable.py) --
the only indirection is a GOT-resolved global array shared by both
branches, confirmed to be the same address on both sides by hand (see
NOTES sec. 669). The array is built as real memory in the ELF's own
GOT page, same technique as test_t14_boot_framemove.py.
"""
import ctypes
import subprocess
import tempfile
import unittest
from pathlib import Path

import differential_harness as dh

DIR = Path(__file__).resolve().parent
SO = DIR.parents[1] / "src/lib/armeabi/libgl2jni.so"
START, END = 0x270b04, 0x270b04 + 88

# Real GOT slot address, resolved by hand from both branches' literal
# pool + pc-relative chain (0x270b20/0x270b24 and 0x270b3c/0x270b40,
# both resolve to the SAME slot) -- see NOTES sec. 669.
GOT_PAGE = 0x347000
ARRAY_SLOT = 0x3479a4

ARRAY_BASE = 0x660000   # this test's own stand-in for the real array
STRIDE = 0x24


def build_model(output: Path):
    subprocess.run(
        ["cc", "-std=c11", "-O2", "-Wall", "-Wextra", "-Werror", "-pedantic",
         "-shared", "-fPIC", str(DIR / "c-models/t21_pagenext_cursor.c"),
         "-o", str(output)],
        check=True, capture_output=True,
    )
    lib = ctypes.CDLL(str(output))
    fn = lib.pagenext_cursor_model
    fn.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
    fn.restype = None
    return lib


def _pack32(value: int) -> bytes:
    return (value & 0xffffffff).to_bytes(4, "little")


def _build_info_bytes(index, max_page, cur_page):
    info = bytearray(0x58)
    info[0x38:0x3c] = _pack32(index)
    info[0x50:0x54] = _pack32(max_page)
    info[0x54:0x58] = _pack32(cur_page)
    return bytes(info)


def run_original(index, max_page, cur_page, initial_flags, num_entries=4):
    got_page = bytearray(0x1000)
    got_page[ARRAY_SLOT - GOT_PAGE:ARRAY_SLOT - GOT_PAGE + 4] = _pack32(ARRAY_BASE)

    array = bytearray(STRIDE * num_entries)
    array[index * STRIDE:index * STRIDE + 4] = _pack32(initial_flags)

    info_bytes = _build_info_bytes(index, max_page, cur_page)
    res = dh.run_original(
        SO, START, END, {"r0": 0x600000},
        buffers=[
            dh.MemoryBuffer("info", 0x600000, info_bytes),
            dh.MemoryBuffer("got_page", GOT_PAGE, bytes(got_page)),
            dh.MemoryBuffer("array", ARRAY_BASE, bytes(array)),
        ],
    )
    return res


def run_model(lib, index, max_page, cur_page, initial_flags, num_entries=4):
    array_buf = (ctypes.c_uint8 * (STRIDE * num_entries))()
    array_buf[index * STRIDE:index * STRIDE + 4] = (ctypes.c_uint8 * 4)(*_pack32(initial_flags))
    info_bytes = _build_info_bytes(index, max_page, cur_page)
    info_buf = (ctypes.c_uint8 * len(info_bytes))(*info_bytes)

    lib.pagenext_cursor_model(info_buf, array_buf)
    return bytes(array_buf)[index * STRIDE:index * STRIDE + 4]


CASES = [
    # (index, max_page, cur_page, initial_flags)
    (0, 3, 0, 0x10),    # not last page, flag already set: must clear
    (0, 2, 2, 0),        # curPage == maxPage: last page, must set
    (1, 2, 5, 0x23),     # curPage > maxPage: last page, other bits preserved
    (2, 1, 0, 0xff),     # not last page, other bits preserved while clearing
]


class PagenextCursorDifferentialTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        cls.lib = build_model(Path(cls.temp.name) / "model.so")

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def test_matches_for_every_case(self):
        for index, max_page, cur_page, initial_flags in CASES:
            with self.subTest(index=index, max_page=max_page, cur_page=cur_page,
                               initial_flags=initial_flags):
                res = run_original(index, max_page, cur_page, initial_flags)
                self.assertTrue(res.ok, res.error)
                model_entry = run_model(self.lib, index, max_page, cur_page, initial_flags)

                original_entry = res.final_buffers["array"][index * STRIDE:index * STRIDE + 4]
                self.assertEqual(original_entry, model_entry)

    def test_fault_injection_other_flag_bits_must_survive(self):
        # A model that simply assigned 0x10/0x00 instead of OR/AND-NOT
        # would wipe out any other bits already set in the entry.
        # Confirm the real ELF preserves them.
        res = run_original(0, 5, 1, 0xff)
        self.assertTrue(res.ok, res.error)
        entry = res.final_buffers["array"][0:4]
        value = int.from_bytes(entry, "little")
        self.assertEqual(value, 0xff & ~0x10)
        self.assertNotEqual(value, 0x00)

    def test_fault_injection_boundary_is_inclusive(self):
        # curPage == maxPage must be treated as "last page" (>=, not
        # >) -- confirm the real ELF sets the bit exactly at equality,
        # not only strictly past it.
        res_equal = run_original(0, 4, 4, 0)
        self.assertTrue(res_equal.ok, res_equal.error)
        self.assertEqual(res_equal.final_buffers["array"][0:4], _pack32(0x10))

        res_below = run_original(0, 4, 3, 0)
        self.assertTrue(res_below.ok, res_below.error)
        self.assertEqual(res_below.final_buffers["array"][0:4], _pack32(0))


if __name__ == "__main__":
    unittest.main()
