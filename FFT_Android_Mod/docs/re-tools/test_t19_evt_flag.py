"""T19 (RE_COMPLETUDE_TASKS.md) vertical slice: differential test of the
real evt_flag() ARM body (0x259224, 72 B) against a compiled,
independent C reimplementation (c-models/t19_evt_flag.c).

evt_get_flgdt (0x2591d4, itself independently differential-tested in
test_t19_evt_get_flgdt.py) and Wread_eventflag (0x103400, not read in
this slice) are stubbed on both sides via callables.
"""
import ctypes
import subprocess
import tempfile
import unittest
from pathlib import Path

import differential_harness as dh

DIR = Path(__file__).resolve().parent
SO = DIR.parents[1] / "src/lib/armeabi/libgl2jni.so"
START, END = 0x259224, 0x259224 + 72

GOT_PAGE = 0x347000
CTX_SLOT = 0x347a80
CTX_BASE = 0x67b35c   # VM status word lives at CTX_BASE+0x0 -- same global as evt_get_flgdt's buf/pos

EVT_GET_FLGDT_ADDR = 0x2591d4
WREAD_EVENTFLAG_ADDR = 0x103400

FLAG_INDEX = 0x2a
EXPECTED_VALUE = 0x7


def build_model(output: Path):
    subprocess.run(
        ["cc", "-std=c11", "-O2", "-Wall", "-Wextra", "-Werror", "-pedantic",
         "-shared", "-fPIC", str(DIR / "c-models/t19_evt_flag.c"),
         "-o", str(output)],
        check=True, capture_output=True,
    )
    lib = ctypes.CDLL(str(output))
    fn = lib.evt_flag_model
    fn.argtypes = [ctypes.POINTER(ctypes.c_int32), ctypes.c_void_p, ctypes.c_void_p]
    fn.restype = ctypes.c_int32
    return lib


def _pack32(value: int) -> bytes:
    return (value & 0xffffffff).to_bytes(4, "little")


def run_original(actual_value, initial_vm_status=0):
    got_page = bytearray(0x1000)
    got_page[CTX_SLOT - GOT_PAGE:CTX_SLOT - GOT_PAGE + 4] = _pack32(CTX_BASE)

    ctx_bytes = bytearray(4)
    ctx_bytes[0:4] = _pack32(initial_vm_status)

    def evt_get_flgdt_stub(uc):
        from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R1
        out1_ptr = uc.reg_read(UC_ARM_REG_R0)
        out2_ptr = uc.reg_read(UC_ARM_REG_R1)
        uc.mem_write(out1_ptr, _pack32(FLAG_INDEX))
        uc.mem_write(out2_ptr, _pack32(EXPECTED_VALUE))
        return 0

    def wread_eventflag_stub(uc):
        del uc
        return actual_value

    res = dh.run_original(
        SO, START, END, {},
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


def run_model(lib, actual_value, initial_vm_status=0):
    vm_status = ctypes.c_int32(initial_vm_status)

    evt_get_flgdt_cb = ctypes.CFUNCTYPE(
        None, ctypes.POINTER(ctypes.c_int32), ctypes.POINTER(ctypes.c_int32))(
        lambda out1, out2: (out1.__setitem__(0, FLAG_INDEX), out2.__setitem__(0, EXPECTED_VALUE)))
    wread_eventflag_cb = ctypes.CFUNCTYPE(ctypes.c_int32, ctypes.c_int32)(lambda index: actual_value)

    ret = lib.evt_flag_model(ctypes.byref(vm_status), evt_get_flgdt_cb, wread_eventflag_cb)
    return ret, vm_status.value


CASES = [
    (EXPECTED_VALUE, 0),       # match: no status bit set
    (EXPECTED_VALUE + 1, 0),   # mismatch: bit 0x2 set
    (0, 0x5),                  # mismatch, other status bits already set: must be preserved
    (EXPECTED_VALUE, 0x4),     # match, other bits already set: must be preserved untouched
]


class EvtFlagDifferentialTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        cls.lib = build_model(Path(cls.temp.name) / "model.so")

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def test_matches_for_every_case(self):
        for actual_value, initial_vm_status in CASES:
            with self.subTest(actual_value=actual_value, initial_vm_status=initial_vm_status):
                res = run_original(actual_value, initial_vm_status)
                self.assertTrue(res.ok, res.error)
                ret, vm_status = run_model(self.lib, actual_value, initial_vm_status)

                self.assertEqual(res.registers["r0"] & 0xffffffff, ret & 0xffffffff)
                real_status = int.from_bytes(res.final_buffers["ctx"], "little")
                self.assertEqual(real_status, vm_status & 0xffffffff)

    def test_fault_injection_return_value_is_the_real_flag_not_a_boolean(self):
        # A model that (wrongly) treated this as a pure predicate --
        # returning 0/1 for match/mismatch -- would diverge from the
        # real ELF, which returns Wread_eventflag's actual value on
        # BOTH branches (r0 is never reassigned after that call).
        res = run_original(actual_value=0x7777, initial_vm_status=0)
        self.assertTrue(res.ok, res.error)
        real_r0 = res.registers["r0"] & 0xffffffff
        self.assertEqual(real_r0, 0x7777)
        self.assertNotIn(real_r0, (0, 1))

    def test_fault_injection_status_bit_survives_on_match(self):
        # A model that cleared other status bits whenever the values
        # matched (instead of leaving the word fully untouched) would
        # diverge here.
        res = run_original(actual_value=EXPECTED_VALUE, initial_vm_status=0xff)
        self.assertTrue(res.ok, res.error)
        self.assertEqual(int.from_bytes(res.final_buffers["ctx"], "little"), 0xff)


if __name__ == "__main__":
    unittest.main()
