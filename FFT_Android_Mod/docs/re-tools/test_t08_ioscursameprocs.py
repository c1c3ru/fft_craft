"""T08 (RE_COMPLETUDE_TASKS.md) vertical slice: differential test of the
real iOSCurSameProcs(ActionRequest*) ARM body (0x15da34, 44 B)
against a compiled, independent C reimplementation
(c-models/t08_ioscursameprocs.c).

iOSCurSameOK (0x15d748) is stubbed via a callable, since its return
value must vary by case.
"""
import ctypes
import subprocess
import tempfile
import unittest
from pathlib import Path

import differential_harness as dh

DIR = Path(__file__).resolve().parent
SO = DIR.parents[1] / "src/lib/armeabi/libgl2jni.so"
START, END = 0x15da34, 0x15da34 + 44

IOS_CUR_SAME_OK_ADDR = 0x15d748
ACTION_REQUEST_ADDR = 0x600000


def build_model(output: Path):
    subprocess.run(
        ["cc", "-std=c11", "-O2", "-Wall", "-Wextra", "-Werror", "-pedantic",
         "-shared", "-fPIC", str(DIR / "c-models/t08_ioscursameprocs.c"),
         "-o", str(output)],
        check=True, capture_output=True,
    )
    lib = ctypes.CDLL(str(output))
    fn = lib.iOSCurSameProcs_model
    fn.argtypes = [ctypes.POINTER(ctypes.c_int32), ctypes.c_void_p]
    fn.restype = None
    return lib


def _pack32(value: int) -> bytes:
    return (value & 0xffffffff).to_bytes(4, "little")


def run_original(initial_value, ok_result):
    def ok_stub(uc):
        del uc
        return ok_result

    res = dh.run_original(
        SO, START, END, {"r0": ACTION_REQUEST_ADDR},
        buffers=[dh.MemoryBuffer("action_request", ACTION_REQUEST_ADDR, _pack32(initial_value))],
        stub_calls={IOS_CUR_SAME_OK_ADDR: ok_stub},
    )
    return res


def run_model(lib, initial_value, ok_result):
    action_request = ctypes.c_int32(initial_value)
    ok_cb = ctypes.CFUNCTYPE(ctypes.c_int32)(lambda: ok_result)
    lib.iOSCurSameProcs_model(ctypes.byref(action_request), ok_cb)
    return action_request.value


CASES = [
    (0xfe, 1),   # pending + confirmed same -> transitions to 7
    (0xfe, 0),   # pending + not confirmed -> stays 0xfe
    (0, 1),      # not pending (BattleRoutine's "0" code, AI sec. 14.4): no-op regardless of ok
    (2, 1),      # not pending (BattleRoutine's "2" code, AI sec. 14.4): no-op regardless of ok
    (7, 1),      # already transitioned: no-op (not re-triggered)
]


class IOSCurSameProcsDifferentialTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        cls.lib = build_model(Path(cls.temp.name) / "model.so")

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def test_matches_for_every_case(self):
        for initial_value, ok_result in CASES:
            with self.subTest(initial_value=initial_value, ok_result=ok_result):
                res = run_original(initial_value, ok_result)
                self.assertTrue(res.ok, res.error)
                model_value = run_model(self.lib, initial_value, ok_result)

                real_value = int.from_bytes(res.final_buffers["action_request"], "little")
                self.assertEqual(real_value, model_value)

    def test_fault_injection_other_codes_are_never_touched(self):
        # A model that (wrongly) treated ANY nonzero/mismatched code
        # as eligible for the OK-check (instead of gating strictly on
        # 0xfe) would call iOSCurSameOK and potentially rewrite codes
        # that BattleRoutine itself writes (0, 2 -- AI sec. 14.4).
        # Confirm the real ELF leaves them completely untouched, with
        # iOSCurSameOK never even reached.
        for code in (0, 2, 7, -1):
            reached = []

            def ok_stub(uc, reached=reached):
                del uc
                reached.append(True)
                return 1

            res = dh.run_original(
                SO, START, END, {"r0": ACTION_REQUEST_ADDR},
                buffers=[dh.MemoryBuffer("action_request", ACTION_REQUEST_ADDR, _pack32(code))],
                stub_calls={IOS_CUR_SAME_OK_ADDR: ok_stub},
            )
            self.assertTrue(res.ok, res.error)
            self.assertEqual(int.from_bytes(res.final_buffers["action_request"], "little"), code & 0xffffffff)
            self.assertEqual(len(reached), 0)


if __name__ == "__main__":
    unittest.main()
