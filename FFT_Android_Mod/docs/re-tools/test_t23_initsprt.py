"""T23 (RE_COMPLETUDE_TASKS.md) vertical slice: differential test of the
real initsprt(tagSPRT*) ARM body (0xd6e48, 100 B) against a compiled,
independent C reimplementation (c-models/t23_initsprt.c).

SetSprt (0x2914e4) and SetShadeTex (0x291a84) are stubbed via
callables (both independently differential-tested in
test_t23_sprt_setters.py). initsprt ends in a genuine ARM tail call
(`b`, not `bl`) into SetSemiTrans(sprt, 1) -- the seventh tail call
confirmed this session -- also stubbed the same way. Real addresses
inside the same .text section already mapped by the harness, so (per
the T14 lesson) no extra empty-page mapping is needed.
"""
import ctypes
import subprocess
import tempfile
import unittest
from pathlib import Path

import differential_harness as dh

DIR = Path(__file__).resolve().parent
SO = DIR.parents[1] / "src/lib/armeabi/libgl2jni.so"
START, END = 0xd6e48, 0xd6e48 + 100

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
    fn = lib.initsprt_model
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

    lib.initsprt_model(sprt_buf, set_sprt_cb, set_shade_tex_cb, set_semi_trans_cb)
    return bytes(sprt_buf)


class InitsprtDifferentialTests(unittest.TestCase):
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

        self.assertEqual(orig_calls, [("SetSprt", None), ("SetShadeTex", 1), ("SetSemiTrans", 1)])
        self.assertEqual(model_calls, orig_calls)

        original_sprt = res.final_buffers["sprt"]
        self.assertEqual(original_sprt, model_sprt)

        expected = bytearray(_sentinel_sprt_bytes())
        expected[0x8] = expected[0x9] = expected[0xa] = 0x80
        expected[0x10] = expected[0x11] = 0
        expected[0xc:0xe] = (0x200).to_bytes(2, "little")
        expected[0x12:0x14] = (0x7c3c).to_bytes(2, "little")
        expected[0x14:0x18] = bytes(4)
        expected[0xe:0x10] = bytes(2)
        self.assertEqual(original_sprt, bytes(expected))

    def test_fault_injection_field_0x4_0x5_0x6_0x7_0xb_are_not_touched_directly(self):
        # Those offsets are only ever touched through the (stubbed)
        # SetSprt/SetShadeTex/SetSemiTrans calls, never directly by
        # initsprt's own straight-line code -- confirm they survive
        # untouched when the stubs themselves don't write anything
        # (as here: the stubs just record the call, they don't write
        # to `sprt` the way the real callees would).
        calls = []
        res = run_original(calls)
        self.assertTrue(res.ok, res.error)
        sprt = res.final_buffers["sprt"]
        sentinel = _sentinel_sprt_bytes()
        for off in (0x4, 0x5, 0x6, 0x7, 0xb):
            self.assertEqual(sprt[off], sentinel[off])


if __name__ == "__main__":
    unittest.main()
