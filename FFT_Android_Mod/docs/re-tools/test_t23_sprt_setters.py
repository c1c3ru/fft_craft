"""T23 (RE_COMPLETUDE_TASKS.md) vertical slice: differential test of 5
real, tiny tagSPRT setter ARM bodies (SetSprt, SetSprt8, SetSprt16,
SetSemiTrans, SetShadeTex) against compiled, independent C
reimplementations (c-models/t23_sprt_setters.c).

No `bl` in any of the five -- confirmed by jtable.py.
"""
import ctypes
import subprocess
import tempfile
import unittest
from pathlib import Path

import differential_harness as dh

DIR = Path(__file__).resolve().parent
SO = DIR.parents[1] / "src/lib/armeabi/libgl2jni.so"

SPRT_ADDR = 0x600000
SPRT_SIZE = 0x20


def build_model(output: Path):
    subprocess.run(
        ["cc", "-std=c11", "-O2", "-Wall", "-Wextra", "-Werror", "-pedantic",
         "-shared", "-fPIC", str(DIR / "c-models/t23_sprt_setters.c"),
         "-o", str(output)],
        check=True, capture_output=True,
    )
    lib = ctypes.CDLL(str(output))
    for symbol in ("SetSprt_model", "SetSprt16_model", "SetSprt8_model"):
        fn = getattr(lib, symbol)
        fn.argtypes = [ctypes.c_void_p]
        fn.restype = None
    for symbol in ("SetSemiTrans_model", "SetShadeTex_model"):
        fn = getattr(lib, symbol)
        fn.argtypes = [ctypes.c_void_p, ctypes.c_int32]
        fn.restype = None
    return lib


def _sentinel_sprt_bytes():
    return bytes((i + 1) & 0xff or 1 for i in range(SPRT_SIZE))


def run_original(start, size, initial_bytes, extra_regs=None):
    regs = {"r0": SPRT_ADDR}
    if extra_regs:
        regs.update(extra_regs)
    return dh.run_original(
        SO, start, start + size, regs,
        buffers=[dh.MemoryBuffer("sprt", SPRT_ADDR, initial_bytes)],
    )


SETTERS = [
    ("SetSprt", 0x2914e4, 36, "SetSprt_model"),
    ("SetSprt16", 0x291508, 36, "SetSprt16_model"),
    ("SetSprt8", 0x29152c, 36, "SetSprt8_model"),
]

FLAG_SETTERS = [
    ("SetSemiTrans", 0x291a6c, 24, "SetSemiTrans_model", 2),
    ("SetShadeTex", 0x291a84, 24, "SetShadeTex_model", 1),
]


class SprtSettersDifferentialTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        cls.lib = build_model(Path(cls.temp.name) / "model.so")

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def test_sprt_variants_match(self):
        for name, start, size, model_symbol in SETTERS:
            with self.subTest(name=name):
                sentinel = _sentinel_sprt_bytes()
                res = run_original(start, size, sentinel)
                self.assertTrue(res.ok, res.error)

                model_buf = (ctypes.c_uint8 * SPRT_SIZE)(*sentinel)
                getattr(self.lib, model_symbol)(model_buf)

                self.assertEqual(res.final_buffers["sprt"], bytes(model_buf))

    def test_flag_setters_match_set_and_clear(self):
        for name, start, size, model_symbol, bit in FLAG_SETTERS:
            for initial_0xb, flag in [(0x64, 1), (0x64, 0), (0xff, 1), (0xff, 0), (0x00, 1)]:
                with self.subTest(name=name, initial_0xb=hex(initial_0xb), flag=flag):
                    sentinel = bytearray(_sentinel_sprt_bytes())
                    sentinel[0xb] = initial_0xb
                    res = run_original(start, size, bytes(sentinel), {"r1": flag})
                    self.assertTrue(res.ok, res.error)

                    model_buf = (ctypes.c_uint8 * SPRT_SIZE)(*sentinel)
                    getattr(self.lib, model_symbol)(model_buf, flag)

                    self.assertEqual(res.final_buffers["sprt"], bytes(model_buf))

    def test_fault_injection_flag_setters_touch_only_bit_and_offset(self):
        # A model that cleared/set the WHOLE byte (instead of just its
        # own bit) would diverge whenever other bits of +0xb are set,
        # and a model touching any offset other than +0xb would
        # diverge against the sentinel bytes everywhere else.
        for name, start, size, _model_symbol, bit in FLAG_SETTERS:
            sentinel = bytearray(_sentinel_sprt_bytes())
            sentinel[0xb] = 0xff
            res = run_original(start, size, bytes(sentinel), {"r1": 0})
            self.assertTrue(res.ok, res.error)
            final = res.final_buffers["sprt"]
            self.assertEqual(final[0xb], 0xff & ~bit)
            self.assertEqual(final[:0xb], bytes(sentinel[:0xb]))
            self.assertEqual(final[0xc:], bytes(sentinel[0xc:]))


if __name__ == "__main__":
    unittest.main()
