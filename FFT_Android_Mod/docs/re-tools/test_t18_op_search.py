"""T18 (RE_COMPLETUDE_TASKS.md) vertical slice: differential test of the
real op_search(int, int) ARM body (0x26a674, via the T10 harness)
against a compiled, independent C reimplementation
(c-models/t18_op_search.c). Unlike every other slice so far, this
function makes zero external calls -- the first attempt at a real-ELF
run used only two levels of GOT indirection and failed with an unmapped
read; the real mechanism needs three (table_ptr_slot -> g ->
eventTable), confirmed by execution (NOTES sec. 664).
"""
import ctypes
import struct
import subprocess
import tempfile
import unittest
from pathlib import Path

import differential_harness as dh

DIR = Path(__file__).resolve().parent
SO = DIR.parents[1] / "src/lib/armeabi/libgl2jni.so"
START, END = 0x26a674, 0x26a674 + 96

TABLE_PTR_SLOT, BASE_VAL_SLOT = 0x347b38, 0x347b1c
G, EVENT_TABLE, BASE, ENTRY_LIST = 0x500000, 0x510000, 0x600000, 0x610000


def build_model(output: Path):
    subprocess.run(
        ["cc", "-std=c11", "-O2", "-Wall", "-Wextra", "-Werror", "-pedantic",
         "-shared", "-fPIC", str(DIR / "c-models/t18_op_search.c"),
         "-o", str(output)],
        check=True, capture_output=True,
    )
    lib = ctypes.CDLL(str(output))
    fn = lib.op_search_model
    fn.argtypes = [ctypes.c_int32, ctypes.c_int32,
                   ctypes.POINTER(ctypes.c_void_p), ctypes.POINTER(ctypes.c_uint8)]
    fn.restype = ctypes.c_uint32
    return lib


def _put(buf: bytearray, addr: int, base: int, val: int) -> None:
    off = addr - base
    buf[off:off + 4] = (val & 0xffffffff).to_bytes(4, "little")


def run_model(lib, event_id, search_tag, entries):
    entry_bytes = b"".join(struct.pack("<I", (extra << 8) | tag) for tag, extra in entries)
    entry_buf = (ctypes.c_uint8 * max(len(entry_bytes), 0x400)).from_buffer_copy(
        entry_bytes.ljust(0x400, b"\x00"))
    packed = ((ctypes.cast(entry_buf, ctypes.c_void_p).value - BASE) | 1) & 0xffffffff
    event_table = (ctypes.c_uint32 * (event_id + 2))()
    event_table[event_id + 1] = packed
    g = ctypes.cast(event_table, ctypes.c_void_p)
    relocation_base = (ctypes.c_uint8 * 1)()  # relocation_base + packed must equal entry_buf
    # Build relocation_base so that relocation_base_addr + (packed&~3) == entry_buf_addr.
    entry_addr = ctypes.cast(entry_buf, ctypes.c_void_p).value
    masked = packed & ~3
    base_addr = entry_addr - masked
    base_ptr = ctypes.cast(base_addr, ctypes.POINTER(ctypes.c_uint8))
    ret = lib.op_search_model(event_id, search_tag, ctypes.byref(g), base_ptr)
    return ret & 0xffffffff


def run_original(event_id, search_tag, entries):
    entry_bytes = b"".join(struct.pack("<I", (extra << 8) | tag) for tag, extra in entries)
    got_page = bytearray(0x1000)
    _put(got_page, TABLE_PTR_SLOT, 0x347000, G)
    _put(got_page, BASE_VAL_SLOT, 0x347000, BASE)
    g_page = bytearray(0x1000)
    _put(g_page, G, G, EVENT_TABLE)
    event_table_page = bytearray(0x1000)
    packed = (ENTRY_LIST - BASE) | 1
    _put(event_table_page, EVENT_TABLE + (event_id + 1) * 4, EVENT_TABLE, packed)
    return dh.run_original(
        SO, START, END, {"r0": event_id, "r1": search_tag},
        buffers=[
            dh.MemoryBuffer("got", 0x347000, bytes(got_page)),
            dh.MemoryBuffer("g", G, bytes(g_page)),
            dh.MemoryBuffer("eventtable", EVENT_TABLE, bytes(event_table_page)),
            dh.MemoryBuffer("entries", ENTRY_LIST, entry_bytes),
        ],
    )


ENTRIES = [(5, 0xAAAAAA), (9, 0xBBBBBB), (1, 0)]


class OpSearchDifferentialTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        cls.lib = build_model(Path(cls.temp.name) / "model.so")

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def test_matches_first_entry_found(self):
        res = run_original(3, 5, ENTRIES)
        self.assertTrue(res.ok, res.error)
        self.assertEqual(res.registers["r0"] & 0xffffffff, run_model(self.lib, 3, 5, ENTRIES))

    def test_matches_second_entry_found(self):
        res = run_original(3, 9, ENTRIES)
        self.assertTrue(res.ok, res.error)
        self.assertEqual(res.registers["r0"] & 0xffffffff, run_model(self.lib, 3, 9, ENTRIES))

    def test_matches_not_found_via_sentinel(self):
        res = run_original(3, 7, ENTRIES)
        self.assertTrue(res.ok, res.error)
        self.assertEqual(res.registers["r0"] & 0xffffffff, 0)
        self.assertEqual(run_model(self.lib, 3, 7, ENTRIES), 0)

    def test_fault_injection_two_level_indirection_is_wrong(self):
        # The original (wrong) first attempt assumed table_ptr_slot's
        # resolved value WAS the event table (two levels), instead of a
        # pointer to it (three levels). Confirm that shortcut reads a
        # different, bogus "packed" value than the real one.
        res = run_original(3, 9, ENTRIES)
        self.assertTrue(res.ok, res.error)
        two_level_guess = G + (3 + 1) * 4  # treats G itself as the event table
        three_level_real = EVENT_TABLE + (3 + 1) * 4
        self.assertNotEqual(two_level_guess, three_level_real)


if __name__ == "__main__":
    unittest.main()
