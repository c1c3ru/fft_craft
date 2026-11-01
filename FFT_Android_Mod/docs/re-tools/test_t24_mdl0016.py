"""T24 (RE_COMPLETUDE_TASKS.md) vertical slice: differential test of the
real Mdl0016(short, int, int, int) ARM body (0x23c6b0, via the T10
harness) against a compiled, independent C reimplementation
(c-models/t24_mdl0016.c). ASHURA_snowMatrix is stubbed on both sides,
with a callable stub that captures its exact call arguments so the
delta computation (global_field - my_field) is checked, not just the
final return value.
"""
import ctypes
import struct
import subprocess
import tempfile
import unittest
from pathlib import Path

import differential_harness as dh
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R1

DIR = Path(__file__).resolve().parent
SO = DIR.parents[1] / "src/lib/armeabi/libgl2jni.so"
START, END = 0x23c6b0, 0x23c6b0 + 120

ARRAY_BASE_SLOT, GLOBAL_PTR_SLOT = 0x3477f8, 0x3477b4
ARRAY_BASE, G, STRUCT = 0x600000, 0x610000, 0x620000
STRIDE = 0xf8


def build_model(output: Path):
    subprocess.run(
        ["cc", "-std=c11", "-O2", "-Wall", "-Wextra", "-Werror", "-pedantic",
         "-shared", "-fPIC", str(DIR / "c-models/t24_mdl0016.c"),
         "-o", str(output)],
        check=True, capture_output=True,
    )
    lib = ctypes.CDLL(str(output))
    fn = lib.Mdl0016_model
    fn.argtypes = [ctypes.c_int16, ctypes.c_int32, ctypes.c_int32, ctypes.c_int32,
                   ctypes.POINTER(ctypes.c_uint8), ctypes.POINTER(ctypes.c_void_p),
                   ctypes.c_void_p]
    fn.restype = ctypes.c_uint8
    return lib


def _put(buf: bytearray, addr: int, base: int, val: int) -> None:
    off = addr - base
    buf[off:off + 4] = (val & 0xffffffff).to_bytes(4, "little")


def run_model(lib, model_id, p1, state_byte, field_0x28, struct_field_0x2):
    captured = {}
    snow_fn = ctypes.CFUNCTYPE(None, ctypes.c_int32, ctypes.c_int32)(
        lambda r0, r1: captured.update(r0=r0, r1=r1))
    array = (ctypes.c_uint8 * (STRIDE * 4))()
    entry_off = model_id * STRIDE
    struct.pack_into("<h", array, entry_off + 0x28, field_0x28)
    array[entry_off + p1 + 0x20 + 2] = state_byte
    struct_buf = (ctypes.c_uint8 * 4)()
    struct.pack_into("<h", struct_buf, 2, struct_field_0x2)
    g_val = ctypes.cast(struct_buf, ctypes.c_void_p)
    ret = lib.Mdl0016_model(model_id, p1, 0, 0, array, ctypes.byref(g_val),
                             ctypes.cast(snow_fn, ctypes.c_void_p))
    final_state = array[entry_off + p1 + 0x20 + 2]
    return ret & 0xff, final_state, captured


def run_original(model_id, p1, state_byte, field_0x28, struct_field_0x2):
    captured = {}

    def stub_snow(uc):
        captured["r0"] = uc.reg_read(UC_ARM_REG_R0)
        r1 = uc.reg_read(UC_ARM_REG_R1)
        captured["r1"] = r1 if r1 < 0x80000000 else r1 - 0x100000000
        return 0

    got_page = bytearray(0x1000)
    _put(got_page, ARRAY_BASE_SLOT, 0x347000, ARRAY_BASE)
    _put(got_page, GLOBAL_PTR_SLOT, 0x347000, G)
    g_page = bytearray(0x1000)
    _put(g_page, G, G, STRUCT)
    struct_page = bytearray(0x1000)
    struct_page[2:4] = (struct_field_0x2 & 0xffff).to_bytes(2, "little")
    array_page = bytearray(STRIDE * 4)
    entry_off = model_id * STRIDE
    array_page[entry_off + 0x28:entry_off + 0x2a] = (field_0x28 & 0xffff).to_bytes(2, "little")
    array_page[entry_off + p1 + 0x20 + 2] = state_byte

    res = dh.run_original(
        SO, START, END, {"r0": model_id, "r1": p1},
        buffers=[
            dh.MemoryBuffer("got", 0x347000, bytes(got_page)),
            dh.MemoryBuffer("g", G, bytes(g_page)),
            dh.MemoryBuffer("struct", STRUCT, bytes(struct_page)),
            dh.MemoryBuffer("array", ARRAY_BASE, bytes(array_page)),
        ],
        stub_calls={0x16a0ec: stub_snow},
    )
    final_state = res.final_buffers["array"][entry_off + p1 + 0x20 + 2] if res.ok else None
    return res, final_state, captured


class Mdl0016DifferentialTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        cls.lib = build_model(Path(cls.temp.name) / "model.so")

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def test_state_3_resets_to_0(self):
        res, real_state, _ = run_original(1, 0, state_byte=3, field_0x28=0, struct_field_0x2=0)
        self.assertTrue(res.ok, res.error)
        m_ret, m_state, _ = run_model(self.lib, 1, 0, state_byte=3, field_0x28=0, struct_field_0x2=0)
        self.assertEqual(res.registers["r0"] & 0xff, m_ret)
        self.assertEqual(real_state, m_state)

    def test_state_0_passthrough(self):
        res, real_state, _ = run_original(1, 0, state_byte=0, field_0x28=0, struct_field_0x2=0)
        self.assertTrue(res.ok, res.error)
        m_ret, m_state, _ = run_model(self.lib, 1, 0, state_byte=0, field_0x28=0, struct_field_0x2=0)
        self.assertEqual(res.registers["r0"] & 0xff, m_ret)
        self.assertEqual(real_state, m_state)

    def test_state_1_transitions_and_calls_snow_matrix_with_exact_delta(self):
        for my_field, global_field in [(100, 50), (-30, 40), (0, 0)]:
            with self.subTest(my_field=my_field, global_field=global_field):
                res, real_state, real_call = run_original(
                    1, 0, state_byte=1, field_0x28=my_field, struct_field_0x2=global_field)
                self.assertTrue(res.ok, res.error)
                m_ret, m_state, m_call = run_model(
                    self.lib, 1, 0, state_byte=1, field_0x28=my_field, struct_field_0x2=global_field)
                self.assertEqual(res.registers["r0"] & 0xff, m_ret)
                self.assertEqual(real_state, m_state)
                self.assertEqual(real_call["r0"], m_call["r0"])
                self.assertEqual(real_call["r1"], m_call["r1"])
                self.assertEqual(real_call["r0"], 0x96)
                self.assertEqual(real_call["r1"], global_field - my_field)

    def test_fault_injection_wrong_field_base_is_detected(self):
        # A model that reads my_field relative to `sub` (entry+p1+0x20)
        # instead of `entry` -- the mistake pattern already seen in
        # T18/T26 -- would read whatever garbage bytes sit at that
        # shifted address instead of the real field. Plant a DIFFERENT
        # value there than at the real field's address and confirm the
        # real ELF uses the one at `entry+0x28`, not the shifted one.
        model_id, p1 = 1, 8
        entry_off = model_id * STRIDE
        got_page = bytearray(0x1000)
        _put(got_page, ARRAY_BASE_SLOT, 0x347000, ARRAY_BASE)
        _put(got_page, GLOBAL_PTR_SLOT, 0x347000, G)
        g_page = bytearray(0x1000)
        _put(g_page, G, G, STRUCT)
        struct_page = bytearray(0x1000)
        struct_page[2:4] = (50 & 0xffff).to_bytes(2, "little")
        array_page = bytearray(STRIDE * 4)
        array_page[entry_off + 0x28:entry_off + 0x2a] = (100 & 0xffff).to_bytes(2, "little")  # real field
        wrong_addr = entry_off + p1 + 0x20 + 0x28  # the "sub-relative" (wrong) guess
        array_page[wrong_addr:wrong_addr + 2] = (999 & 0xffff).to_bytes(2, "little")
        array_page[entry_off + p1 + 0x20 + 2] = 1  # state byte

        def stub_snow(uc):
            r1 = uc.reg_read(UC_ARM_REG_R1)
            stub_snow.r1 = r1 if r1 < 0x80000000 else r1 - 0x100000000
            return 0

        res = dh.run_original(
            SO, START, END, {"r0": model_id, "r1": p1},
            buffers=[dh.MemoryBuffer("got", 0x347000, bytes(got_page)),
                     dh.MemoryBuffer("g", G, bytes(g_page)),
                     dh.MemoryBuffer("struct", STRUCT, bytes(struct_page)),
                     dh.MemoryBuffer("array", ARRAY_BASE, bytes(array_page))],
            stub_calls={0x16a0ec: stub_snow},
        )
        self.assertTrue(res.ok, res.error)
        real_delta = stub_snow.r1
        wrong_guess_delta = 50 - 999
        self.assertEqual(real_delta, 50 - 100)
        self.assertNotEqual(real_delta, wrong_guess_delta)


if __name__ == "__main__":
    unittest.main()
