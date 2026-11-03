"""T18 (RE_COMPLETUDE_TASKS.md) vertical slice: differential test of the
real wldlop_chk() ARM body (0x25f63c, 88 B) against a compiled,
independent C reimplementation (c-models/t18_wldlop_chk.c).

frmbuf_get (0x25f44c, already read_full) is stubbed via a callable
that can mutate the source flags global, to confirm the real re-load
after the call matters.
"""
import ctypes
import subprocess
import tempfile
import unittest
from pathlib import Path

import differential_harness as dh

DIR = Path(__file__).resolve().parent
SO = DIR.parents[1] / "src/lib/armeabi/libgl2jni.so"
START, END = 0x25f63c, 0x25f63c + 88

FRMBUF_GET_ADDR = 0x25f44c

SRC_SLOT = 0x346754
DST_SLOT = 0x347a6c
SRC_VAR = 0x650000
DST_VAR = 0x660000


def _pack32(value: int) -> bytes:
    return (value & 0xffffffff).to_bytes(4, "little")


def build_model(output: Path):
    subprocess.run(
        ["cc", "-std=c11", "-O2", "-Wall", "-Wextra", "-Werror", "-pedantic",
         "-shared", "-fPIC", str(DIR / "c-models/t18_wldlop_chk.c"),
         "-o", str(output)],
        check=True, capture_output=True,
    )
    lib = ctypes.CDLL(str(output))
    fn = lib.wldlop_chk_model
    fn.argtypes = [ctypes.POINTER(ctypes.c_int32), ctypes.POINTER(ctypes.c_int32), ctypes.c_void_p]
    fn.restype = None
    return lib


def run_original(src_value, dst_value, mutated_src_value, reached):
    page_a_base = SRC_SLOT & ~0xfff
    page_b_base = DST_SLOT & ~0xfff
    page_a = bytearray(0x1000)
    page_a[SRC_SLOT - page_a_base:SRC_SLOT - page_a_base + 4] = _pack32(SRC_VAR)
    page_b = bytearray(0x1000)
    page_b[DST_SLOT - page_b_base:DST_SLOT - page_b_base + 4] = _pack32(DST_VAR)

    def frmbuf_get_stub(uc):
        reached.append(True)
        if mutated_src_value is not None:
            uc.mem_write(SRC_VAR, _pack32(mutated_src_value))
        return 0

    res = dh.run_original(
        SO, START, END, {},
        buffers=[
            dh.MemoryBuffer("page_a", page_a_base, bytes(page_a)),
            dh.MemoryBuffer("page_b", page_b_base, bytes(page_b)),
            dh.MemoryBuffer("src", SRC_VAR, _pack32(src_value)),
            dh.MemoryBuffer("dst", DST_VAR, _pack32(dst_value)),
        ],
        stub_calls={FRMBUF_GET_ADDR: frmbuf_get_stub},
    )
    return res


def run_model(lib, src_value, dst_value, mutated_src_value, reached):
    src = ctypes.c_int32(src_value)
    dst = ctypes.c_int32(dst_value)

    def _frmbuf_get():
        reached.append(True)
        if mutated_src_value is not None:
            src.value = mutated_src_value

    cb = ctypes.CFUNCTYPE(None)(_frmbuf_get)
    lib.wldlop_chk_model(ctypes.byref(src), ctypes.byref(dst), cb)
    return src.value, dst.value


CASES = [
    # (src_value, dst_value, mutated_src_value_or_None)
    (0x2, 0x0, None),      # src has bit set -> plain copy, no call
    (0x0, 0x0, None),      # neither has bit -> plain copy, no call
    (0x0, 0x2, None),      # src lacks bit, dst has it -> calls frmbuf_get, then copies (unmutated)
    (0x0, 0x2, 0x7),       # same, but frmbuf_get mutates src -> copy uses the NEW value
    (0x5, 0x2, None),      # src bit set (other bits too) -> plain copy, no call, other bits preserved
]


class WldlopChkDifferentialTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        cls.lib = build_model(Path(cls.temp.name) / "model.so")

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def test_matches_for_every_case(self):
        for src_value, dst_value, mutated in CASES:
            with self.subTest(src=hex(src_value), dst=hex(dst_value), mutated=mutated):
                orig_reached, model_reached = [], []
                res = run_original(src_value, dst_value, mutated, orig_reached)
                self.assertTrue(res.ok, res.error)
                model_src, model_dst = run_model(self.lib, src_value, dst_value, mutated, model_reached)

                real_dst = int.from_bytes(res.final_buffers["dst"], "little")
                self.assertEqual(real_dst, model_dst & 0xffffffff)
                self.assertEqual(len(orig_reached), len(model_reached))

    def test_fault_injection_mutation_during_frmbuf_get_is_observed(self):
        # A model that reused the PRE-call value of src (instead of
        # re-reading it after frmbuf_get) would diverge here.
        reached = []
        res = run_original(src_value=0x0, dst_value=0x2, mutated_src_value=0x7, reached=reached)
        self.assertTrue(res.ok, res.error)
        self.assertEqual(len(reached), 1)
        self.assertEqual(int.from_bytes(res.final_buffers["dst"], "little"), 0x7)
        self.assertNotEqual(int.from_bytes(res.final_buffers["dst"], "little"), 0x0)


if __name__ == "__main__":
    unittest.main()
