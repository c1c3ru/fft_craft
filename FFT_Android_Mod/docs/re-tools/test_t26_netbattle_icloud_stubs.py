"""T26 (RE_COMPLETUDE_TASKS.md) vertical slice: differential test of 5
real, trivial leaf-stub ARM bodies (NetBattleJudge, getNetBattleJudge,
iCloud_Send, iCloud_Receive, iCloud_GetSlotCount) against a compiled,
independent C reimplementation
(c-models/t26_netbattle_icloud_stubs.c).

No `bl`, no branch, no memory access in any of the five -- confirmed
by jtable.py and by direct disassembly. This is the direct, byte-level
confirmation of T26's own acceptance criterion: an isolated network/
iCloud symbol must not be read as evidence of active functionality.
Each is tested with several distinct register inputs to confirm the
constant return does not depend on arguments, since none of these
functions even read r0-r3.
"""
import ctypes
import subprocess
import tempfile
import unittest
from pathlib import Path

import differential_harness as dh

DIR = Path(__file__).resolve().parent
SO = DIR.parents[1] / "src/lib/armeabi/libgl2jni.so"

FUNCTIONS = [
    # (name, start, size, model_symbol, expected_r0_or_None_for_void)
    ("NetBattleJudge", 0x2884c8, 4, "NetBattleJudge_model", None),
    ("getNetBattleJudge", 0x2884cc, 8, "getNetBattleJudge_model", 3),
    ("iCloud_Send", 0x2b3444, 8, "iCloud_Send_model", 1),
    ("iCloud_Receive", 0x2b344c, 8, "iCloud_Receive_model", 1),
    ("iCloud_GetSlotCount", 0x2b3454, 8, "iCloud_GetSlotCount_model", 0),
]


def build_model(output: Path):
    subprocess.run(
        ["cc", "-std=c11", "-O2", "-Wall", "-Wextra", "-Werror", "-pedantic",
         "-shared", "-fPIC", str(DIR / "c-models/t26_netbattle_icloud_stubs.c"),
         "-o", str(output)],
        check=True, capture_output=True,
    )
    return ctypes.CDLL(str(output))


def run_original(start, size, initial_r0):
    return dh.run_original(SO, start, start + size, {"r0": initial_r0}, buffers=[])


class NetBattleICloudStubsDifferentialTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        cls.lib = build_model(Path(cls.temp.name) / "model.so")

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def test_matches_for_every_function_and_input(self):
        for name, start, size, model_symbol, expected in FUNCTIONS:
            fn = getattr(self.lib, model_symbol)
            fn.argtypes = []
            fn.restype = ctypes.c_int32
            for initial_r0 in (0, 1, -1, 0x7fffffff, 0x12345678):
                with self.subTest(name=name, initial_r0=initial_r0):
                    res = run_original(start, size, initial_r0)
                    self.assertTrue(res.ok, res.error)
                    model_ret = fn() & 0xffffffff

                    if expected is None:
                        # NetBattleJudge is `bx lr` alone: r0 is never
                        # written, so the real return value is
                        # whatever r0 already held on entry.
                        self.assertEqual(res.registers["r0"] & 0xffffffff, initial_r0 & 0xffffffff)
                    else:
                        self.assertEqual(res.registers["r0"] & 0xffffffff, expected & 0xffffffff)
                    # The model always returns its fixed constant
                    # regardless of what the ARM side's r0 happened to
                    # be (NetBattleJudge's model is void/no-op, so
                    # model_ret is not compared for it).
                    if expected is not None:
                        self.assertEqual(model_ret, expected & 0xffffffff)

    def test_fault_injection_netbattlejudge_is_not_a_constant_returner(self):
        # A model that (wrongly) assumed every function in this
        # cluster returns a fixed constant -- including NetBattleJudge
        # itself -- would diverge: its real body never writes r0 at
        # all, so its "return value" is whatever the caller's r0
        # already was, not a fixed number.
        res_a = run_original(0x2884c8, 4, initial_r0=0x11111111)
        res_b = run_original(0x2884c8, 4, initial_r0=0x22222222)
        self.assertTrue(res_a.ok and res_b.ok)
        self.assertEqual(res_a.registers["r0"], 0x11111111)
        self.assertEqual(res_b.registers["r0"], 0x22222222)
        self.assertNotEqual(res_a.registers["r0"], res_b.registers["r0"])


if __name__ == "__main__":
    unittest.main()
