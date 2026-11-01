"""T19 (RE_COMPLETUDE_TASKS.md) vertical slice: differential test of the
real evt_get_flgdt(int*, int*) ARM body (0x2591d4, 80 B) against a
compiled, independent C reimplementation (c-models/t19_evt_get_flgdt.c).

No `bl` in this function -- fully self-contained, confirmed by
jtable.py. The VM context struct's buf/pos fields (+0x8/+0xc) are
built as real memory at the ELF's own GOT-resolved address (0x67b35c,
resolved by hand -- see NOTES sec. 671), same technique as
test_t14_boot_framemove.py/test_t21_pagenext_cursor.py.
"""
import ctypes
import subprocess
import tempfile
import unittest
from pathlib import Path

import differential_harness as dh

DIR = Path(__file__).resolve().parent
SO = DIR.parents[1] / "src/lib/armeabi/libgl2jni.so"
START, END = 0x2591d4, 0x2591d4 + 80

GOT_PAGE = 0x347000
CTX_SLOT = 0x347a80
CTX_BASE = 0x67b35c   # VM context struct base (resolved by hand)
BUF_ADDR = 0x650000    # this test's own stand-in for the real script buffer


def build_model(output: Path):
    subprocess.run(
        ["cc", "-std=c11", "-O2", "-Wall", "-Wextra", "-Werror", "-pedantic",
         "-shared", "-fPIC", str(DIR / "c-models/t19_evt_get_flgdt.c"),
         "-o", str(output)],
        check=True, capture_output=True,
    )
    lib = ctypes.CDLL(str(output))
    fn = lib.evt_get_flgdt_model
    fn.argtypes = [ctypes.POINTER(ctypes.c_uint16), ctypes.POINTER(ctypes.c_uint16),
                   ctypes.POINTER(ctypes.c_int32), ctypes.POINTER(ctypes.c_int32)]
    fn.restype = None
    return lib


def _pack32(value: int) -> bytes:
    return (value & 0xffffffff).to_bytes(4, "little")


def _pack16(value: int) -> bytes:
    return (value & 0xffff).to_bytes(2, "little")


def run_original(script_values, pos):
    got_page = bytearray(0x1000)
    got_page[CTX_SLOT - GOT_PAGE:CTX_SLOT - GOT_PAGE + 4] = _pack32(CTX_BASE)

    ctx_bytes = bytearray(0x10)
    ctx_bytes[0x8:0xc] = _pack32(BUF_ADDR)
    ctx_bytes[0xc:0xe] = _pack16(pos)

    script_bytes = b"".join(_pack16(v) for v in script_values)

    out1_addr, out2_addr = 0x600000, 0x610000
    res = dh.run_original(
        SO, START, END, {"r0": out1_addr, "r1": out2_addr},
        buffers=[
            dh.MemoryBuffer("got_page", GOT_PAGE, bytes(got_page)),
            dh.MemoryBuffer("ctx", CTX_BASE, bytes(ctx_bytes)),
            dh.MemoryBuffer("script", BUF_ADDR, script_bytes),
            dh.MemoryBuffer("out1", out1_addr, bytes(4)),
            dh.MemoryBuffer("out2", out2_addr, bytes(4)),
        ],
    )
    return res


def run_model(lib, script_values, pos):
    buf = (ctypes.c_uint16 * len(script_values))(*script_values)
    pos_c = ctypes.c_uint16(pos)
    out1, out2 = ctypes.c_int32(), ctypes.c_int32()
    lib.evt_get_flgdt_model(buf, ctypes.byref(pos_c), ctypes.byref(out1), ctypes.byref(out2))
    return out1.value, out2.value, pos_c.value


CASES = [
    ([0x1111, 0x2222, 0x3333, 0x4444, 0x5555], 0),
    ([0x1111, 0x2222, 0x3333, 0x4444, 0x5555], 3),
    ([0xffff, 0x0001] * 4, 2),
]


class EvtGetFlgdtDifferentialTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        cls.lib = build_model(Path(cls.temp.name) / "model.so")

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def test_matches_for_every_case(self):
        for script_values, pos in CASES:
            with self.subTest(pos=pos):
                res = run_original(script_values, pos)
                self.assertTrue(res.ok, res.error)
                m_out1, m_out2, m_pos = run_model(self.lib, script_values, pos)

                self.assertEqual(int.from_bytes(res.final_buffers["out1"], "little"), m_out1)
                self.assertEqual(int.from_bytes(res.final_buffers["out2"], "little"), m_out2)
                final_pos = int.from_bytes(res.final_buffers["ctx"][0xc:0xe], "little")
                self.assertEqual(final_pos, m_pos)
                self.assertEqual(final_pos, (pos + 2) & 0xffff)

    def test_fault_injection_cursor_wraps_at_16_bits(self):
        # The real instructions explicitly truncate pos+1 to 16 bits
        # (lsl #16 / lsr #16) before storing it back -- a model using
        # a wider int for the cursor without matching truncation would
        # diverge here. buf must be large enough to also cover the
        # wrapped index 0.
        script_values = [0x5555] * 0x10000
        script_values[0xffff] = 0xcccc
        script_values[0] = 0xdddd
        res = run_original(script_values, 0xffff)
        self.assertTrue(res.ok, res.error)
        final_pos = int.from_bytes(res.final_buffers["ctx"][0xc:0xe], "little")
        self.assertEqual(final_pos, 1)  # (0xffff + 2) truncated to 16 bits
        out1 = int.from_bytes(res.final_buffers["out1"], "little")
        self.assertEqual(out1, 0xcccc)  # buf[0xffff]
        out2 = int.from_bytes(res.final_buffers["out2"], "little")
        self.assertEqual(out2, 0xdddd)  # buf[0] after wrap

        m_out1, m_out2, m_pos = run_model(self.lib, script_values, 0xffff)
        self.assertEqual((m_out1, m_out2, m_pos), (out1, out2, final_pos))


if __name__ == "__main__":
    unittest.main()
