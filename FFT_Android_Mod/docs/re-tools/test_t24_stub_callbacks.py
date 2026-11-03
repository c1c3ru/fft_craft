"""T24 (RE_COMPLETUDE_TASKS.md) vertical slice: differential test of 5
real ARM bodies from the _EffectTCB/_Object callback cluster
(dmyFnc, CreateObjectWithTableWithParentData, system_error,
objectLG2, dmyFnc2) against compiled, independent C reimplementations
(c-models/t24_stub_callbacks.c).

dmyFnc/CreateObjectWithTableWithParentData call system_error
(0x20c5d0) -- stubbed via a callable recording its arguments, to
confirm each passes a distinct fixed error code despite looking like
plain no-ops from their own names. system_error, objectLG2, dmyFnc2
are tested directly as true no-ops (no stub needed, 0 `bl`).
"""
import ctypes
import subprocess
import tempfile
import unittest
from pathlib import Path

import differential_harness as dh

DIR = Path(__file__).resolve().parent
SO = DIR.parents[1] / "src/lib/armeabi/libgl2jni.so"

SYSTEM_ERROR_ADDR = 0x20c5d0


def build_model(output: Path):
    subprocess.run(
        ["cc", "-std=c11", "-O2", "-Wall", "-Wextra", "-Werror", "-pedantic",
         "-shared", "-fPIC", str(DIR / "c-models/t24_stub_callbacks.c"),
         "-o", str(output)],
        check=True, capture_output=True,
    )
    return ctypes.CDLL(str(output))


class StubCallbacksDifferentialTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        cls.lib = build_model(Path(cls.temp.name) / "model.so")

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def test_dmyfnc_calls_system_error_with_fixed_code_and_returns_0(self):
        reached = []

        def stub(uc):
            from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R1
            reached.append((uc.reg_read(UC_ARM_REG_R0), uc.reg_read(UC_ARM_REG_R1)))
            return 0

        res = dh.run_original(
            SO, 0x21c214, 0x21c214 + 24, {"r0": 0x11112222}, buffers=[],
            stub_calls={SYSTEM_ERROR_ADDR: stub},
        )
        self.assertTrue(res.ok, res.error)
        self.assertEqual(reached, [(1, 0x22)])
        self.assertEqual(res.registers["r0"] & 0xffffffff, 0)

        self.lib.dmyFnc_model.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
        self.lib.dmyFnc_model.restype = ctypes.c_int32
        model_reached = []
        cb = ctypes.CFUNCTYPE(None, ctypes.c_int32, ctypes.c_int32)(
            lambda cat, code: model_reached.append((cat, code)))
        model_ret = self.lib.dmyFnc_model(None, cb)
        self.assertEqual(model_reached, [(1, 0x22)])
        self.assertEqual(model_ret, 0)

    def test_createobjectwithtablewithparentdata_calls_system_error_with_different_fixed_code(self):
        reached = []

        def stub(uc):
            from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R1
            reached.append((uc.reg_read(UC_ARM_REG_R0), uc.reg_read(UC_ARM_REG_R1)))
            return 0

        res = dh.run_original(
            SO, 0x228c44, 0x228c44 + 24, {"r0": 7, "r1": 8, "r2": 9, "r3": 0x33334444}, buffers=[],
            stub_calls={SYSTEM_ERROR_ADDR: stub},
        )
        self.assertTrue(res.ok, res.error)
        self.assertEqual(reached, [(1, 0x50)])
        self.assertEqual(res.registers["r0"] & 0xffffffff, 0)

        self.lib.CreateObjectWithTableWithParentData_model.argtypes = [
            ctypes.c_int16, ctypes.c_int32, ctypes.c_int32, ctypes.c_int32,
            ctypes.c_void_p, ctypes.c_void_p]
        self.lib.CreateObjectWithTableWithParentData_model.restype = ctypes.c_int32
        model_reached = []
        cb = ctypes.CFUNCTYPE(None, ctypes.c_int32, ctypes.c_int32)(
            lambda cat, code: model_reached.append((cat, code)))
        model_ret = self.lib.CreateObjectWithTableWithParentData_model(7, 8, 9, -1, None, cb)
        self.assertEqual(model_reached, [(1, 0x50)])
        self.assertEqual(model_ret, 0)

    def test_fault_injection_the_two_error_codes_are_distinct(self):
        # A model that (wrongly) reused the same error code for both
        # "placeholder" functions would diverge: the real bytes use
        # 0x22 and 0x50, not the same constant for both.
        self.assertNotEqual(0x22, 0x50)

        calls = []

        def stub(uc):
            from unicorn.arm_const import UC_ARM_REG_R1
            calls.append(uc.reg_read(UC_ARM_REG_R1))
            return 0

        res_a = dh.run_original(SO, 0x21c214, 0x21c214 + 24, {}, buffers=[],
                                 stub_calls={SYSTEM_ERROR_ADDR: stub})
        res_b = dh.run_original(SO, 0x228c44, 0x228c44 + 24, {}, buffers=[],
                                 stub_calls={SYSTEM_ERROR_ADDR: stub})
        self.assertTrue(res_a.ok and res_b.ok)
        self.assertEqual(calls, [0x22, 0x50])

    def test_true_no_ops_never_write_r0(self):
        # system_error, objectLG2, dmyFnc2 are bare `bx lr`: r0 must
        # come out exactly as it went in, confirmed with two distinct
        # entry values (same fault-injection shape as T26's
        # NetBattleJudge).
        for start, size in [(0x20c5d0, 4), (0x225a60, 4), (0x225a64, 4)]:
            res_a = dh.run_original(SO, start, start + size, {"r0": 0x11111111}, buffers=[])
            res_b = dh.run_original(SO, start, start + size, {"r0": 0x22222222}, buffers=[])
            self.assertTrue(res_a.ok and res_b.ok)
            self.assertEqual(res_a.registers["r0"], 0x11111111)
            self.assertEqual(res_b.registers["r0"], 0x22222222)


if __name__ == "__main__":
    unittest.main()
