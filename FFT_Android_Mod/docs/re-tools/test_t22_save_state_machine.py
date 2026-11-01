"""T22 (RE_COMPLETUDE_TASKS.md) vertical slice: differential test of the
real pspFftSave/pspFftDelete ARM bodies (via the T10 harness) against a
compiled, independent C reimplementation (c-models/t22_fft_save_state_machine.c).

This is the first genuine "original vs. reimplementation" differential
test in the project for a multi-instruction, multi-state function (T10's
own test only covered a single branch-free leaf copy). Includes fault
injection, required by the project's own harness contract (T10).
"""
import ctypes
import subprocess
import tempfile
import unittest
from pathlib import Path

import differential_harness as dh

DIR = Path(__file__).resolve().parent
SO = DIR.parents[1] / "src/lib/armeabi/libgl2jni.so"

STATE_ADDR = 0xbab940
SAVE_CACHED_ADDR = 0xbd3308
DELETE_CACHED_ADDR = 0xbd5e50
OUT_ADDR = 0x600000

SAVE_RANGE = (0x2899a0, 0x2899a0 + 288)
DELETE_RANGE = (0x289c1c, 0x289c1c + 320)


def build_model(output: Path):
    subprocess.run(
        ["cc", "-std=c11", "-O2", "-Wall", "-Wextra", "-Werror", "-pedantic",
         "-shared", "-fPIC", str(DIR / "c-models/t22_fft_save_state_machine.c"),
         "-o", str(output)],
        check=True, capture_output=True,
    )
    lib = ctypes.CDLL(str(output))
    for name in ("pspFftSave_model", "pspFftDelete_model"):
        fn = getattr(lib, name)
        fn.argtypes = [ctypes.POINTER(ctypes.c_int32)] * 3 + [ctypes.c_void_p] * 3
        fn.restype = ctypes.c_int32
    return lib


NOOP_START = ctypes.CFUNCTYPE(ctypes.c_int32, ctypes.c_int32)(lambda op: 0)
NOOP_END = ctypes.CFUNCTYPE(ctypes.c_int32)(lambda: 0)


def run_model(lib, fn_name, state, cached, start_op_ignored, check_result):
    check_fn = ctypes.CFUNCTYPE(ctypes.c_int32)(lambda: check_result)
    state_c = ctypes.c_int32(state)
    cached_c = ctypes.c_int32(cached)
    out_c = ctypes.c_int32(0)
    ret = getattr(lib, fn_name)(
        ctypes.byref(state_c), ctypes.byref(cached_c), ctypes.byref(out_c),
        ctypes.cast(NOOP_START, ctypes.c_void_p),
        ctypes.cast(check_fn, ctypes.c_void_p),
        ctypes.cast(NOOP_END, ctypes.c_void_p))
    return ret & 0xffffffff, state_c.value, cached_c.value, out_c.value


def run_original(start, end, state, cached_addr, cached, check_result):
    page_base = cached_addr & ~0xfff
    cached_buf = bytearray(4096)
    off = cached_addr - page_base
    cached_buf[off:off + 4] = (cached & 0xffffffff).to_bytes(4, "little")
    state_buf = bytearray(8192)
    soff = STATE_ADDR - 0xbab000
    state_buf[soff:soff + 4] = (state & 0xffffffff).to_bytes(4, "little")
    initial_regs = ({"r0": 1, "r1": 0x610000, "r2": OUT_ADDR} if start == SAVE_RANGE[0]
                     else {"r0": OUT_ADDR})
    res = dh.run_original(
        SO, start, end, initial_regs,
        [dh.MemoryBuffer("state", 0xbab000, bytes(state_buf)),
         dh.MemoryBuffer("cached", page_base, bytes(cached_buf)),
         dh.MemoryBuffer("out", OUT_ADDR, bytes(4)),
         dh.MemoryBuffer("data", 0x610000, bytes(0x20))],
        stub_calls={0x2898e0: 0, 0x28e010: 0, 0x28e0a4: 0, 0x28e0c8: check_result},
    )
    if not res.ok:
        return res, None, None, None
    new_state = int.from_bytes(res.final_buffers["state"][soff:soff + 4], "little", signed=True)
    new_cached = int.from_bytes(res.final_buffers["cached"][off:off + 4], "little", signed=True)
    out_val = int.from_bytes(res.final_buffers["out"], "little", signed=True)
    return res, new_state, new_cached, out_val


CASES = [(-13, 0), (0, 13), (1, 14), (2, 15), (5, 18), (-1, 12)]


class SaveStateMachineDifferentialTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        cls.lib = build_model(Path(cls.temp.name) / "model.so")

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def test_pspFftSave_state0_matches(self):
        res, new_state, new_cached, _ = run_original(*SAVE_RANGE, 0, SAVE_CACHED_ADDR, 0xdead, 0)
        self.assertTrue(res.ok, res.error)
        ret, m_state, m_cached, _ = run_model(self.lib, "pspFftSave_model", 0, 0xdead, 1, 0)
        self.assertEqual((new_state, new_cached), (m_state, m_cached))

    def test_pspFftSave_state1_matches_for_every_result(self):
        for result, idx in CASES:
            with self.subTest(result=result, idx=idx):
                res, new_state, new_cached, _ = run_original(
                    *SAVE_RANGE, 1, SAVE_CACHED_ADDR, 0x1234, result)
                self.assertTrue(res.ok, res.error)
                ret, m_state, m_cached, _ = run_model(
                    self.lib, "pspFftSave_model", 1, 0x1234, 0, result)
                self.assertEqual((new_state, new_cached), (m_state, m_cached),
                                  f"mismatch at result={result}")

    def test_pspFftDelete_state1_matches_for_every_result(self):
        for result, idx in CASES:
            with self.subTest(result=result, idx=idx):
                res, new_state, new_cached, ret_val = run_original(
                    *DELETE_RANGE, 1, DELETE_CACHED_ADDR, 0x1234, result)
                self.assertTrue(res.ok, res.error)
                ret, m_state, m_cached, _ = run_model(
                    self.lib, "pspFftDelete_model", 1, 0x1234, 0, result)
                self.assertEqual((new_state, new_cached), (m_state, m_cached),
                                  f"mismatch at result={result}")

    def test_pspFftDelete_state2_finalize_matches(self):
        for cached in (-99, 0, 42, -1):
            with self.subTest(cached=cached):
                res, new_state, new_cached, out_val = run_original(
                    *DELETE_RANGE, 2, DELETE_CACHED_ADDR, cached, 0)
                self.assertTrue(res.ok, res.error)
                ret, m_state, m_cached, m_out = run_model(
                    self.lib, "pspFftDelete_model", 2, cached, 0, 0)
                self.assertEqual((new_state, out_val), (m_state, m_out))
                self.assertEqual(res.registers["r0"], ret)

    def test_fault_injection_wrong_model_is_detected(self):
        # A model that forgets the sec.661 correction (always resets to
        # 0 instead of 2) must disagree with the real ELF -- proving
        # this test suite would actually catch a regression back to the
        # original (wrong) section 641 description.
        res, real_state, _, _ = run_original(*DELETE_RANGE, 1, DELETE_CACHED_ADDR, 0, 2)
        self.assertTrue(res.ok, res.error)
        wrong_model_state = 0  # the pre-section-661 (incorrect) belief
        self.assertNotEqual(real_state, wrong_model_state,
                             "fault-injection case stopped being a real divergence")


if __name__ == "__main__":
    unittest.main()
