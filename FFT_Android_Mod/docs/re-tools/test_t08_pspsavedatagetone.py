"""T08 (RE_COMPLETUDE_TASKS.md) vertical slice: differential test of the
real pspSaveDataGetOne(int, FFT_SAVE_DATA*) ARM body (0x289b64, 20 B)
against a compiled, independent C reimplementation
(c-models/t08_pspsavedatagetone.c).

No prologue, ends in a plain `b` -- the sixth genuine ARM tail call
confirmed this session, into a local, unsymbolized function at
0x2898e0. Real address inside the same .text section already mapped
by the harness, so (per the T14/T23/T17 lesson) it needs no extra
empty-page mapping.
"""
import ctypes
import subprocess
import tempfile
import unittest
from pathlib import Path

import differential_harness as dh

DIR = Path(__file__).resolve().parent
SO = DIR.parents[1] / "src/lib/armeabi/libgl2jni.so"
START, END = 0x289b64, 0x289b64 + 20

TARGET_ADDR = 0x2898e0


def build_model(output: Path):
    subprocess.run(
        ["cc", "-std=c11", "-O2", "-Wall", "-Wextra", "-Werror", "-pedantic",
         "-shared", "-fPIC", str(DIR / "c-models/t08_pspsavedatagetone.c"),
         "-o", str(output)],
        check=True, capture_output=True,
    )
    lib = ctypes.CDLL(str(output))
    fn = lib.pspSaveDataGetOne_model
    fn.argtypes = [ctypes.c_int32, ctypes.c_void_p, ctypes.c_void_p]
    fn.restype = ctypes.c_int32
    return lib


def run_original(slot, save_addr, reached, stub_return):
    def target_stub(uc):
        from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2
        reached.append((uc.reg_read(UC_ARM_REG_R0), uc.reg_read(UC_ARM_REG_R1),
                         uc.reg_read(UC_ARM_REG_R2)))
        return stub_return

    res = dh.run_original(
        SO, START, END, {"r0": slot, "r1": save_addr},
        buffers=[],
        stub_calls={TARGET_ADDR: target_stub},
    )
    return res


def run_model(lib, slot, save_addr, reached, stub_return):
    def _target(save, got_slot, flag):
        reached.append((save, got_slot, flag))
        return stub_return

    cb = ctypes.CFUNCTYPE(ctypes.c_int32, ctypes.c_void_p, ctypes.c_int32, ctypes.c_int32)(_target)
    return lib.pspSaveDataGetOne_model(slot, save_addr, cb)


CASES = [(0, 0x600000, 0), (3, 0x650000, 5), (-1, 0x700000, -7)]


class PspSaveDataGetOneDifferentialTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        cls.lib = build_model(Path(cls.temp.name) / "model.so")

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def test_arguments_reordered_and_return_value_matches(self):
        for slot, save_addr, stub_return in CASES:
            with self.subTest(slot=slot, save_addr=save_addr, stub_return=stub_return):
                orig_reached, model_reached = [], []
                res = run_original(slot, save_addr, orig_reached, stub_return)
                self.assertTrue(res.ok, res.error)
                model_ret = run_model(self.lib, slot, save_addr, model_reached, stub_return)

                self.assertEqual(len(orig_reached), 1)
                self.assertEqual(orig_reached[0], (save_addr & 0xffffffff, slot & 0xffffffff, 1))
                self.assertEqual(len(model_reached), 1)
                self.assertEqual(model_reached[0], (save_addr, slot, 1))

                self.assertEqual(res.registers["r0"] & 0xffffffff, model_ret & 0xffffffff)
                self.assertEqual(res.registers["r0"] & 0xffffffff, stub_return & 0xffffffff)


if __name__ == "__main__":
    unittest.main()
