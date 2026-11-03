"""T23 (RE_COMPLETUDE_TASKS.md) vertical slice: differential test of the
real Winitsprt(tagSPRT*) ARM body (0xfe96c, 100 B) against a compiled,
independent C reimplementation (c-models/t23_initsprt.c).

Winitsprt is byte-identical to initsprt (test_t23_initsprt.py) except
for ONE difference: it calls SetShadeTex(sprt, 0) instead of
SetShadeTex(sprt, 1) -- confirmed by disassembly diff, not assumed
from the "W" naming convention. SetSprt/SetShadeTex are stubbed via
callables; Winitsprt ends in the same genuine ARM tail call (`b`, not
`bl`) into SetSemiTrans(sprt, 1) as initsprt -- the ninth tail call
confirmed this session.
"""
import ctypes
import subprocess
import tempfile
import unittest
from pathlib import Path

import differential_harness as dh

DIR = Path(__file__).resolve().parent
SO = DIR.parents[1] / "src/lib/armeabi/libgl2jni.so"
START, END = 0xfe96c, 0xfe96c + 100

SET_SPRT_ADDR = 0x2914e4
SET_SHADE_TEX_ADDR = 0x291a84
SET_SEMI_TRANS_ADDR = 0x291a6c

SPRT_ADDR = 0x600000
SPRT_SIZE = 0x20


def build_model(output: Path):
    subprocess.run(
        ["cc", "-std=c11", "-O2", "-Wall", "-Wextra", "-Werror", "-pedantic",
         "-shared", "-fPIC", str(DIR / "c-models/t23_initsprt.c"),
         "-o", str(output)],
        check=True, capture_output=True,
    )
    lib = ctypes.CDLL(str(output))
    fn = lib.Winitsprt_model
    fn.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p]
    fn.restype = None
    return lib


def _sentinel_sprt_bytes():
    return bytes((i + 1) & 0xff or 1 for i in range(SPRT_SIZE))


def run_original(calls):
    def set_sprt_stub(uc):
        calls.append(("SetSprt", None))
        return 0

    def set_shade_tex_stub(uc):
        from unicorn.arm_const import UC_ARM_REG_R1
        calls.append(("SetShadeTex", uc.reg_read(UC_ARM_REG_R1)))
        return 0

    def set_semi_trans_stub(uc):
        from unicorn.arm_const import UC_ARM_REG_R1
        calls.append(("SetSemiTrans", uc.reg_read(UC_ARM_REG_R1)))
        return 0

    sentinel = _sentinel_sprt_bytes()
    res = dh.run_original(
        SO, START, END, {"r0": SPRT_ADDR},
        buffers=[dh.MemoryBuffer("sprt", SPRT_ADDR, sentinel)],
        stub_calls={
            SET_SPRT_ADDR: set_sprt_stub,
            SET_SHADE_TEX_ADDR: set_shade_tex_stub,
            SET_SEMI_TRANS_ADDR: set_semi_trans_stub,
        },
    )
    return res


def run_model(lib, calls):
    sprt_buf = (ctypes.c_uint8 * SPRT_SIZE)(*_sentinel_sprt_bytes())

    set_sprt_cb = ctypes.CFUNCTYPE(None, ctypes.c_void_p)(lambda s: calls.append(("SetSprt", None)))
    set_shade_tex_cb = ctypes.CFUNCTYPE(None, ctypes.c_void_p, ctypes.c_int32)(
        lambda s, flag: calls.append(("SetShadeTex", flag)))
    set_semi_trans_cb = ctypes.CFUNCTYPE(None, ctypes.c_void_p, ctypes.c_int32)(
        lambda s, flag: calls.append(("SetSemiTrans", flag)))

    lib.Winitsprt_model(sprt_buf, set_sprt_cb, set_shade_tex_cb, set_semi_trans_cb)
    return bytes(sprt_buf)


class WinitsprtDifferentialTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        cls.lib = build_model(Path(cls.temp.name) / "model.so")

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def test_fields_written_and_calls_made_in_order_exactly_once(self):
        orig_calls, model_calls = [], []
        res = run_original(orig_calls)
        self.assertTrue(res.ok, res.error)
        model_sprt = run_model(self.lib, model_calls)

        self.assertEqual(orig_calls, [("SetSprt", None), ("SetShadeTex", 0), ("SetSemiTrans", 1)])
        self.assertEqual(model_calls, orig_calls)

        original_sprt = res.final_buffers["sprt"]
        self.assertEqual(original_sprt, model_sprt)

    def test_fault_injection_shade_tex_flag_differs_from_initsprt(self):
        # The one real difference from initsprt: confirm it is
        # exactly 0, not 1 -- a model that copy-pasted initsprt's
        # flag verbatim would diverge here.
        calls = []
        res = run_original(calls)
        self.assertTrue(res.ok, res.error)
        shade_tex_calls = [c for c in calls if c[0] == "SetShadeTex"]
        self.assertEqual(len(shade_tex_calls), 1)
        self.assertEqual(shade_tex_calls[0][1], 0)
        self.assertNotEqual(shade_tex_calls[0][1], 1)


if __name__ == "__main__":
    unittest.main()
