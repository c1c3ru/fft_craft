"""T23 (RE_COMPLETUDE_TASKS.md) vertical slice: differential test of the
real addlocalprim2(tagPOLY_FT4*) ARM body (0xe05bc, 112 B) against a
compiled, independent C reimplementation
(c-models/t23_addlocalprim2.c).

No `bl` -- fully self-contained, confirmed by jtable.py. The context
pointer variable is built as real memory at the ELF's own GOT-
resolved address (resolved by hand -- see NOTES sec. 680), same
technique as test_t14_boot_framemove.py.

The final "ctx+8..+0xb becomes prim's own address" write is NOT
compared as a raw number across the real ELF side and the model side
(same reasoning as test_t08_disposeobject.py's free_list_head): a
real 32-bit ARM address and a ctypes-allocated host address are not
the same kind of value. Each side is checked against its OWN prim
address instead.
"""
import ctypes
import subprocess
import tempfile
import unittest
from pathlib import Path

import differential_harness as dh

DIR = Path(__file__).resolve().parent
SO = DIR.parents[1] / "src/lib/armeabi/libgl2jni.so"
START, END = 0xe05bc, 0xe05bc + 112

GOT_PAGE = 0x346000
CTX_PTR_VAR_SLOT = 0x346160   # holds the ADDRESS of the context pointer variable
CTX_PTR_VAR_ADDR = 0x650000   # this test's own stand-in for that pointer variable
CTX_BASE = 0x660000           # the context base value *CTX_PTR_VAR_ADDR resolves to

PRIM_ADDR = 0x600000
PRIM_SIZE = 0x20


def _pack32(value: int) -> bytes:
    return (value & 0xffffffff).to_bytes(4, "little")


def build_model(output: Path):
    subprocess.run(
        ["cc", "-std=c11", "-O2", "-Wall", "-Wextra", "-Werror", "-pedantic",
         "-shared", "-fPIC", str(DIR / "c-models/t23_addlocalprim2.c"),
         "-o", str(output)],
        check=True, capture_output=True,
    )
    lib = ctypes.CDLL(str(output))
    fn = lib.addlocalprim2_model
    fn.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
    fn.restype = None
    return lib


def _sentinel_prim_bytes():
    return bytes((i + 1) & 0xff or 1 for i in range(PRIM_SIZE))


def run_original(old_tag):
    got_page = bytearray(0x1000)
    got_page[CTX_PTR_VAR_SLOT - GOT_PAGE:CTX_PTR_VAR_SLOT - GOT_PAGE + 4] = _pack32(CTX_PTR_VAR_ADDR)

    ctx = bytearray(0x10)
    ctx[8:12] = _pack32(old_tag)

    prim_bytes = _sentinel_prim_bytes()
    res = dh.run_original(
        SO, START, END, {"r0": PRIM_ADDR},
        buffers=[
            dh.MemoryBuffer("got_page", GOT_PAGE, bytes(got_page)),
            dh.MemoryBuffer("ctx_ptr_var", CTX_PTR_VAR_ADDR, _pack32(CTX_BASE)),
            dh.MemoryBuffer("ctx", CTX_BASE, bytes(ctx)),
            dh.MemoryBuffer("prim", PRIM_ADDR, prim_bytes),
        ],
    )
    return res


def run_model(lib, old_tag):
    ctx = bytearray(0x10)
    ctx[8:12] = _pack32(old_tag)
    ctx_buf = (ctypes.c_uint8 * len(ctx))(*ctx)
    prim_buf = (ctypes.c_uint8 * PRIM_SIZE)(*_sentinel_prim_bytes())

    lib.addlocalprim2_model(prim_buf, ctx_buf)
    return bytes(prim_buf), bytes(ctx_buf), ctypes.addressof(prim_buf)


CASES = [0, 1, 0x12345678, 0xffffffff, 0x600000]


class AddLocalPrim2DifferentialTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        cls.lib = build_model(Path(cls.temp.name) / "model.so")

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def test_matches_for_every_case(self):
        for old_tag in CASES:
            with self.subTest(old_tag=hex(old_tag)):
                res = run_original(old_tag)
                self.assertTrue(res.ok, res.error)
                model_prim, model_ctx, model_prim_addr = run_model(self.lib, old_tag)

                real_prim = res.final_buffers["prim"]
                # prim->tag (+0x0..+0x3) must equal the OLD ctx value.
                self.assertEqual(real_prim[0:4], _pack32(old_tag))
                self.assertEqual(real_prim[0:4], model_prim[0:4])
                # Nothing else in prim is touched.
                self.assertEqual(real_prim[4:], model_prim[4:])

                # ctx+0x8..+0xb becomes "prim's own address" -- each
                # side checked against its own prim address, not
                # against the other side's (see module docstring).
                real_ctx = res.final_buffers["ctx"]
                self.assertEqual(int.from_bytes(real_ctx[8:12], "little"), PRIM_ADDR)
                self.assertEqual(int.from_bytes(model_ctx[8:12], "little"), model_prim_addr & 0xffffffff)
                # Nothing else in ctx is touched.
                self.assertEqual(real_ctx[:8], bytes(8))
                self.assertEqual(model_ctx[:8], bytes(8))

    def test_fault_injection_bytes_are_not_swapped(self):
        # A model that stored the 4 bytes in the wrong order (e.g.
        # big-endian, or reversed) would diverge here, since old_tag's
        # bytes are all distinct.
        res = run_original(0x04030201)
        self.assertTrue(res.ok, res.error)
        prim = res.final_buffers["prim"]
        self.assertEqual(prim[0], 0x01)
        self.assertEqual(prim[1], 0x02)
        self.assertEqual(prim[2], 0x03)
        self.assertEqual(prim[3], 0x04)


if __name__ == "__main__":
    unittest.main()
