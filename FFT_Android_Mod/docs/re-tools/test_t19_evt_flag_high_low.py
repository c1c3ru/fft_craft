"""T19 (RE_COMPLETUDE_TASKS.md) vertical slice: differential test of the
real evt_flag_high()/evt_flag_low() ARM bodies (0x25926c/0x2592b4,
72 B each) against compiled, independent C reimplementations
(c-models/t19_evt_flag_high_low.c).

evt_get_flgdt (0x2591d4) and Wread_eventflag (0x103400) are stubbed
via callables, same technique as test_t19_evt_flag.py. Shares the
same VM status global (0x67b35c) as evt_flag/evt_get_flgdt
(NOTES sec. 671/684).
"""
import ctypes
import subprocess
import tempfile
import unittest
from pathlib import Path

import differential_harness as dh

DIR = Path(__file__).resolve().parent
SO = DIR.parents[1] / "src/lib/armeabi/libgl2jni.so"

GOT_PAGE = 0x347000
CTX_SLOT = 0x347a80
CTX_BASE = 0x67b35c

EVT_GET_FLGDT_ADDR = 0x2591d4
WREAD_EVENTFLAG_ADDR = 0x103400

FLAG_INDEX = 0x2a


def _pack32(value: int) -> bytes:
    return (value & 0xffffffff).to_bytes(4, "little")


def build_model(output: Path):
    subprocess.run(
        ["cc", "-std=c11", "-O2", "-Wall", "-Wextra", "-Werror", "-pedantic",
         "-shared", "-fPIC", str(DIR / "c-models/t19_evt_flag_high_low.c"),
         "-o", str(output)],
        check=True, capture_output=True,
    )
    lib = ctypes.CDLL(str(output))
    for symbol in ("evt_flag_high_model", "evt_flag_low_model"):
        fn = getattr(lib, symbol)
        fn.argtypes = [ctypes.POINTER(ctypes.c_int32), ctypes.c_void_p, ctypes.c_void_p]
        fn.restype = ctypes.c_int32
    return lib


def run_original(start, size, expected_value, actual_value, initial_vm_status=0):
    got_page = bytearray(0x1000)
    got_page[CTX_SLOT - GOT_PAGE:CTX_SLOT - GOT_PAGE + 4] = _pack32(CTX_BASE)
    ctx_bytes = bytearray(4)
    ctx_bytes[0:4] = _pack32(initial_vm_status)

    def evt_get_flgdt_stub(uc):
        from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R1
        out1_ptr, out2_ptr = uc.reg_read(UC_ARM_REG_R0), uc.reg_read(UC_ARM_REG_R1)
        uc.mem_write(out1_ptr, _pack32(FLAG_INDEX))
        uc.mem_write(out2_ptr, _pack32(expected_value))
        return 0

    def wread_eventflag_stub(uc):
        del uc
        return actual_value

    res = dh.run_original(
        SO, start, start + size, {},
        buffers=[
            dh.MemoryBuffer("got_page", GOT_PAGE, bytes(got_page)),
            dh.MemoryBuffer("ctx", CTX_BASE, bytes(ctx_bytes)),
        ],
        stub_calls={
            EVT_GET_FLGDT_ADDR: evt_get_flgdt_stub,
            WREAD_EVENTFLAG_ADDR: wread_eventflag_stub,
        },
    )
    return res


def run_model(lib, symbol, expected_value, actual_value, initial_vm_status=0):
    vm_status = ctypes.c_int32(initial_vm_status)
    evt_get_flgdt_cb = ctypes.CFUNCTYPE(
        None, ctypes.POINTER(ctypes.c_int32), ctypes.POINTER(ctypes.c_int32))(
        lambda out1, out2: (out1.__setitem__(0, FLAG_INDEX), out2.__setitem__(0, expected_value)))
    wread_eventflag_cb = ctypes.CFUNCTYPE(ctypes.c_int32, ctypes.c_int32)(lambda index: actual_value)

    ret = getattr(lib, symbol)(ctypes.byref(vm_status), evt_get_flgdt_cb, wread_eventflag_cb)
    return ret, vm_status.value


FUNCTIONS = [
    ("evt_flag_high", 0x25926c, 72, "evt_flag_high_model"),
    ("evt_flag_low", 0x2592b4, 72, "evt_flag_low_model"),
]

CASES = [
    (10, 10),   # actual == expected
    (10, 9),    # actual < expected
    (10, 11),   # actual > expected
]


class EvtFlagHighLowDifferentialTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        cls.lib = build_model(Path(cls.temp.name) / "model.so")

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def test_matches_for_every_function_and_case(self):
        for name, start, size, model_symbol in FUNCTIONS:
            for expected_value, actual_value in CASES:
                with self.subTest(name=name, expected_value=expected_value, actual_value=actual_value):
                    res = run_original(start, size, expected_value, actual_value)
                    self.assertTrue(res.ok, res.error)
                    ret, vm_status = run_model(self.lib, model_symbol, expected_value, actual_value)

                    self.assertEqual(res.registers["r0"] & 0xffffffff, ret & 0xffffffff)
                    real_status = int.from_bytes(res.final_buffers["ctx"], "little")
                    self.assertEqual(real_status, vm_status & 0xffffffff)

    def test_fault_injection_high_and_low_trigger_on_opposite_sides(self):
        # high sets the bit when actual < expected; low sets it when
        # actual > expected. At equality, NEITHER sets it (>=/<= both
        # satisfied). A model that swapped the two comparisons would
        # diverge on at least one of these three cases.
        res_high_below = run_original(0x25926c, 72, expected_value=10, actual_value=5)
        res_low_below = run_original(0x2592b4, 72, expected_value=10, actual_value=5)
        self.assertTrue(res_high_below.ok and res_low_below.ok)
        self.assertEqual(int.from_bytes(res_high_below.final_buffers["ctx"], "little"), 0x2)
        self.assertEqual(int.from_bytes(res_low_below.final_buffers["ctx"], "little"), 0x0)

        res_high_above = run_original(0x25926c, 72, expected_value=10, actual_value=15)
        res_low_above = run_original(0x2592b4, 72, expected_value=10, actual_value=15)
        self.assertTrue(res_high_above.ok and res_low_above.ok)
        self.assertEqual(int.from_bytes(res_high_above.final_buffers["ctx"], "little"), 0x0)
        self.assertEqual(int.from_bytes(res_low_above.final_buffers["ctx"], "little"), 0x2)

        res_high_eq = run_original(0x25926c, 72, expected_value=10, actual_value=10)
        res_low_eq = run_original(0x2592b4, 72, expected_value=10, actual_value=10)
        self.assertTrue(res_high_eq.ok and res_low_eq.ok)
        self.assertEqual(int.from_bytes(res_high_eq.final_buffers["ctx"], "little"), 0x0)
        self.assertEqual(int.from_bytes(res_low_eq.final_buffers["ctx"], "little"), 0x0)


if __name__ == "__main__":
    unittest.main()
