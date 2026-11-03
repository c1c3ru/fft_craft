"""T19 (RE_COMPLETUDE_TASKS.md) vertical slice: differential test of the
real evt_flagset() ARM body (0x2592fc, 40 B) against a compiled,
independent C reimplementation (c-models/t19_evt_flagset.c).

evt_get_flgdt (0x2591d4) and Wwrite_eventflag (0x103340) are stubbed
via callables.
"""
import ctypes
import subprocess
import tempfile
import unittest
from pathlib import Path

import differential_harness as dh

DIR = Path(__file__).resolve().parent
SO = DIR.parents[1] / "src/lib/armeabi/libgl2jni.so"
START, END = 0x2592fc, 0x2592fc + 40

EVT_GET_FLGDT_ADDR = 0x2591d4
WWRITE_EVENTFLAG_ADDR = 0x103340

FLAG_INDEX = 0x17


def build_model(output: Path):
    subprocess.run(
        ["cc", "-std=c11", "-O2", "-Wall", "-Wextra", "-Werror", "-pedantic",
         "-shared", "-fPIC", str(DIR / "c-models/t19_evt_flagset.c"),
         "-o", str(output)],
        check=True, capture_output=True,
    )
    lib = ctypes.CDLL(str(output))
    fn = lib.evt_flagset_model
    fn.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
    fn.restype = None
    return lib


def run_original(value, reached):
    def evt_get_flgdt_stub(uc):
        from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R1
        out1_ptr, out2_ptr = uc.reg_read(UC_ARM_REG_R0), uc.reg_read(UC_ARM_REG_R1)
        uc.mem_write(out1_ptr, (FLAG_INDEX & 0xffffffff).to_bytes(4, "little"))
        uc.mem_write(out2_ptr, (value & 0xffffffff).to_bytes(4, "little"))
        return 0

    def wwrite_eventflag_stub(uc):
        from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R1
        reached.append((uc.reg_read(UC_ARM_REG_R0), uc.reg_read(UC_ARM_REG_R1)))
        return 0

    res = dh.run_original(
        SO, START, END, {},
        buffers=[],
        stub_calls={
            EVT_GET_FLGDT_ADDR: evt_get_flgdt_stub,
            WWRITE_EVENTFLAG_ADDR: wwrite_eventflag_stub,
        },
    )
    return res


def run_model(lib, value, reached):
    evt_get_flgdt_cb = ctypes.CFUNCTYPE(
        None, ctypes.POINTER(ctypes.c_int32), ctypes.POINTER(ctypes.c_int32))(
        lambda out1, out2: (out1.__setitem__(0, FLAG_INDEX), out2.__setitem__(0, value)))
    wwrite_eventflag_cb = ctypes.CFUNCTYPE(None, ctypes.c_int32, ctypes.c_int32)(
        lambda index, val: reached.append((index, val)))

    lib.evt_flagset_model(evt_get_flgdt_cb, wwrite_eventflag_cb)


class EvtFlagsetDifferentialTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        cls.lib = build_model(Path(cls.temp.name) / "model.so")

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def test_matches_for_every_value(self):
        for value in (0, 1, -1, 0x7fffffff):
            with self.subTest(value=value):
                orig_reached, model_reached = [], []
                res = run_original(value, orig_reached)
                self.assertTrue(res.ok, res.error)
                run_model(self.lib, value, model_reached)

                self.assertEqual(len(orig_reached), 1)
                self.assertEqual(orig_reached[0], (FLAG_INDEX, value & 0xffffffff))
                self.assertEqual(len(model_reached), 1)
                self.assertEqual(model_reached[0], (FLAG_INDEX, value))


if __name__ == "__main__":
    unittest.main()
