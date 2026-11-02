"""T22 (RE_COMPLETUDE_TASKS.md) vertical slice: differential test of the
real iOS_ResumeGetData(unsigned char**, unsigned int*) ARM body
(0x27f620, 32 B) against a compiled, independent C reimplementation
(c-models/t22_ios_resumegetdata.c).

No `bl`, no branch -- fully self-contained, confirmed by jtable.py.
The real function always writes the exact same fixed address
(0x6b4680, resolved by hand from the real PC-relative literal) and
size (0x84558) regardless of its inputs; this test confirms that
constancy directly, rather than assuming it from the single-path
disassembly.
"""
import ctypes
import subprocess
import tempfile
import unittest
from pathlib import Path

import differential_harness as dh

DIR = Path(__file__).resolve().parent
SO = DIR.parents[1] / "src/lib/armeabi/libgl2jni.so"
START, END = 0x27f620, 0x27f620 + 32

REAL_BUFFER_ADDR = 0x6b4680   # resolved by hand from the real PC-relative literal
REAL_BUFFER_SIZE = 0x84558    # resolved the same way -- new evidence, not previously documented

OUT_BUFFER_PTR_ADDR = 0x600000
OUT_SIZE_PTR_ADDR = 0x610000


def build_model(output: Path):
    subprocess.run(
        ["cc", "-std=c11", "-O2", "-Wall", "-Wextra", "-Werror", "-pedantic",
         "-shared", "-fPIC", str(DIR / "c-models/t22_ios_resumegetdata.c"),
         "-o", str(output)],
        check=True, capture_output=True,
    )
    lib = ctypes.CDLL(str(output))
    fn = lib.iOS_ResumeGetData_model
    fn.argtypes = [ctypes.POINTER(ctypes.c_void_p), ctypes.POINTER(ctypes.c_uint32), ctypes.c_void_p]
    fn.restype = None
    return lib


def run_original():
    res = dh.run_original(
        SO, START, END, {"r0": OUT_BUFFER_PTR_ADDR, "r1": OUT_SIZE_PTR_ADDR},
        buffers=[
            dh.MemoryBuffer("out_buffer_ptr", OUT_BUFFER_PTR_ADDR, bytes(4)),
            dh.MemoryBuffer("out_size_ptr", OUT_SIZE_PTR_ADDR, bytes(4)),
        ],
    )
    return res


def run_model(lib):
    out_buffer = ctypes.c_void_p()
    out_size = ctypes.c_uint32()
    lib.iOS_ResumeGetData_model(ctypes.byref(out_buffer), ctypes.byref(out_size),
                                 ctypes.c_void_p(0x11112222))
    return out_buffer.value, out_size.value


class IOSResumeGetDataDifferentialTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        cls.lib = build_model(Path(cls.temp.name) / "model.so")

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def test_returns_the_exact_fixed_address_and_size(self):
        res = run_original()
        self.assertTrue(res.ok, res.error)
        real_buffer_addr = int.from_bytes(res.final_buffers["out_buffer_ptr"], "little")
        real_size = int.from_bytes(res.final_buffers["out_size_ptr"], "little")

        self.assertEqual(real_buffer_addr, REAL_BUFFER_ADDR)
        self.assertEqual(real_size, REAL_BUFFER_SIZE)

        model_addr, model_size = run_model(self.lib)
        self.assertEqual(model_addr, 0x11112222)
        self.assertEqual(model_size, real_size)

    def test_fault_injection_constants_do_not_depend_on_caller_state(self):
        # Run twice with completely different out-pointer addresses;
        # the written VALUES (not the out-pointers themselves) must
        # be identical both times, confirming the function reads no
        # input to compute them.
        res_a = dh.run_original(
            SO, START, END, {"r0": 0x620000, "r1": 0x630000},
            buffers=[
                dh.MemoryBuffer("out_buffer_ptr", 0x620000, bytes(4)),
                dh.MemoryBuffer("out_size_ptr", 0x630000, bytes(4)),
            ],
        )
        res_b = dh.run_original(
            SO, START, END, {"r0": 0x640000, "r1": 0x645000},
            buffers=[
                dh.MemoryBuffer("out_buffer_ptr", 0x640000, bytes(4)),
                dh.MemoryBuffer("out_size_ptr", 0x645000, bytes(4)),
            ],
        )
        self.assertTrue(res_a.ok and res_b.ok)
        self.assertEqual(res_a.final_buffers["out_buffer_ptr"], res_b.final_buffers["out_buffer_ptr"])
        self.assertEqual(res_a.final_buffers["out_size_ptr"], res_b.final_buffers["out_size_ptr"])


if __name__ == "__main__":
    unittest.main()
