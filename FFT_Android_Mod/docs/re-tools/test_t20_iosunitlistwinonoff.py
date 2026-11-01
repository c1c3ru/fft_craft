"""T20 (RE_COMPLETUDE_TASKS.md) vertical slice: differential test of the
real iOSUnitListWinOnOff(int) ARM body (0x15ef7c, via the T10 harness)
against a compiled, independent C reimplementation
(c-models/t20_iosunitlistwinonoff.c).

This is the first slice whose non-tail-call path return value is NOT a
constant: r0 is never reassigned after the `bl` to
iOSdisp_personalWinPosGet, so the real return value IS that call's
result, confirmed by execution with three different stub values before
writing the C model -- a model that assumed "returns 0" would have
been wrong and this test would have caught it.

The offFlag!=0 path is a genuine ARM tail call (pop{r4,lr}; b, not bl)
-- reproducing it against the real ELF is what exposed and fixed a
real bug in differential_harness.py itself (NOTES sec. 666,
test_differential_harness_tail_call_stub.py).
"""
import ctypes
import subprocess
import tempfile
import unittest
from pathlib import Path

import differential_harness as dh

DIR = Path(__file__).resolve().parent
SO = DIR.parents[1] / "src/lib/armeabi/libgl2jni.so"
START, END = 0x15ef7c, 0x15ef7c + 88

G1_SLOT, G2_SLOT = 0x3467a0, 0x3467a4  # window_active, window_x_offset GOT pointer slots
FLAG_ADDR, XOFFSET_ADDR = 0x600000, 0x610000
TAIL_CALL_TARGET = 0x15ee2c


def build_model(output: Path):
    subprocess.run(
        ["cc", "-std=c11", "-O2", "-Wall", "-Wextra", "-Werror", "-pedantic",
         "-shared", "-fPIC", str(DIR / "c-models/t20_iosunitlistwinonoff.c"),
         "-o", str(output)],
        check=True, capture_output=True,
    )
    lib = ctypes.CDLL(str(output))
    fn = lib.iOSUnitListWinOnOff_model
    fn.argtypes = [ctypes.c_int32, ctypes.POINTER(ctypes.c_int32),
                   ctypes.POINTER(ctypes.c_int32), ctypes.c_void_p, ctypes.c_void_p]
    fn.restype = ctypes.c_int32
    return lib


def run_model(lib, off_flag, pos_flag_result, tail_stub_value=0):
    active = ctypes.c_int32(0)
    xoffset = ctypes.c_int32(0)
    pos_get = ctypes.CFUNCTYPE(ctypes.c_int32)(lambda: pos_flag_result)
    other_path = ctypes.CFUNCTYPE(ctypes.c_int32)(lambda: tail_stub_value)
    ret = lib.iOSUnitListWinOnOff_model(
        off_flag, ctypes.byref(active), ctypes.byref(xoffset),
        ctypes.cast(pos_get, ctypes.c_void_p), ctypes.cast(other_path, ctypes.c_void_p))
    return ret, active.value, xoffset.value


def _put(buf: bytearray, addr: int, base: int, val: int) -> None:
    off = addr - base
    buf[off:off + 4] = (val & 0xffffffff).to_bytes(4, "little")


def run_original(off_flag, pos_flag_result, tail_stub_value=None):
    globals_page = bytearray(0x1000)
    _put(globals_page, G1_SLOT, 0x346000, FLAG_ADDR)
    _put(globals_page, G2_SLOT, 0x346000, XOFFSET_ADDR)
    stubs = {0x12f228: pos_flag_result}
    if tail_stub_value is not None:
        stubs[TAIL_CALL_TARGET] = tail_stub_value
    return dh.run_original(
        SO, START, END, {"r0": off_flag},
        buffers=[
            dh.MemoryBuffer("globals", 0x346000, bytes(globals_page)),
            dh.MemoryBuffer("flag", FLAG_ADDR, bytes(4)),
            dh.MemoryBuffer("xoffset", XOFFSET_ADDR, bytes(4)),
        ],
        stub_calls=stubs,
    )


class IOSUnitListWinOnOffDifferentialTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        cls.lib = build_model(Path(cls.temp.name) / "model.so")

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def test_main_path_matches_for_several_pos_flag_values(self):
        for pos_flag in (0, 5, -1, 0x7fffffff):
            with self.subTest(pos_flag=pos_flag):
                res = run_original(0, pos_flag)
                self.assertTrue(res.ok, res.error)
                m_ret, m_active, m_xoff = run_model(self.lib, 0, pos_flag)
                self.assertEqual(res.registers["r0"] & 0xffffffff, m_ret & 0xffffffff)
                active = int.from_bytes(res.final_buffers["flag"], "little")
                xoff = int.from_bytes(res.final_buffers["xoffset"], "little", signed=True)
                self.assertEqual(active, m_active)
                self.assertEqual(xoff, m_xoff)

    def test_tail_call_path_return_value_matches(self):
        for tail_value in (0x11, 0x77777777, 0):
            with self.subTest(tail_value=tail_value):
                res = run_original(1, pos_flag_result=0, tail_stub_value=tail_value)
                self.assertTrue(res.ok, res.error)
                m_ret, _, _ = run_model(self.lib, 1, 0, tail_stub_value=tail_value)
                self.assertEqual(res.registers["r0"] & 0xffffffff, m_ret & 0xffffffff)

    def test_fault_injection_assuming_constant_zero_return_is_detected(self):
        # A model that (wrongly) assumes the main path always returns 0
        # instead of pos_flag would disagree with the real ELF whenever
        # pos_flag != 0.
        res = run_original(0, pos_flag_result=5)
        self.assertTrue(res.ok, res.error)
        wrong_constant_guess = 0
        self.assertNotEqual(res.registers["r0"] & 0xffffffff, wrong_constant_guess)


if __name__ == "__main__":
    unittest.main()
