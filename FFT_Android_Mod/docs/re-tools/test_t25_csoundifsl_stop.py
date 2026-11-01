"""T25 (RE_COMPLETUDE_TASKS.md) vertical slice: differential test of the
real CSOUND_IF_SL::Stop(int) ARM body (0xbb838, 88 B) against a
compiled, independent C reimplementation (c-models/t25_csoundifsl_stop.c).

The virtual call through the SLPlayItf vtable (SetPlayState) is stubbed
on both sides: on the ELF side via differential_harness.stub_calls
(a callable, since the return value must vary by case, same mechanism
extended for T26), on the model side via a real ctypes callback reached
through a hand-built one-entry vtable.

channel_data/play_itf are passed into the model as direct native
pointers rather than read out of an ARM-width (4-byte) struct field --
see the comment in c-models/t25_csoundifsl_stop.c for why a genuine
64-bit host pointer cannot be round-tripped through a 4-byte slot that
matches the real 32-bit struct. Consequently only the two plain int32
flag fields (+0x48, +0x50) are compared byte-for-byte between the real
ELF side and the model side; everything else is compared by value
(r0), not by raw struct bytes.
"""
import ctypes
import subprocess
import tempfile
import unittest
from pathlib import Path

import differential_harness as dh

DIR = Path(__file__).resolve().parent
SO = DIR.parents[1] / "src/lib/armeabi/libgl2jni.so"
START, END = 0xbb838, 0xbb838 + 88

THIS_ADDR = 0x600000
CHANDATA_ADDR = 0x610000
ITF_ADDR = 0x620000
VTBL_ADDR = 0x630000
STUB_TARGET = 0x640000
STRIDE = 0x88


def build_model(output: Path):
    subprocess.run(
        ["cc", "-std=c11", "-O2", "-Wall", "-Wextra", "-Werror", "-pedantic",
         "-shared", "-fPIC", str(DIR / "c-models/t25_csoundifsl_stop.c"),
         "-o", str(output)],
        check=True, capture_output=True,
    )
    lib = ctypes.CDLL(str(output))
    fn = lib.CSOUND_IF_SL_Stop_model
    fn.argtypes = [ctypes.c_void_p, ctypes.c_int32, ctypes.c_void_p, ctypes.c_uint32]
    fn.restype = ctypes.c_uint32
    return lib


def _pack32(value: int) -> bytes:
    return (value & 0xffffffff).to_bytes(4, "little")


def _build_entry_bytes(field_0x04: int, has_sample_buf: bool, has_play_itf: bool):
    entry = bytearray(STRIDE)
    entry[0x4:0x8] = _pack32(field_0x04)
    entry[0x3c:0x40] = _pack32(0x12345678 if has_sample_buf else 0)
    entry[0x78:0x7c] = _pack32(ITF_ADDR if has_play_itf else 0)
    return bytes(entry)


def run_original(channel, field_0x04, has_sample_buf, has_play_itf, stub_result):
    this_page = bytearray(0x1000)
    this_page[0x10:0x14] = _pack32(CHANDATA_ADDR)

    chandata_page = bytearray(0x1000 * 2)
    entry_bytes = _build_entry_bytes(field_0x04, has_sample_buf, has_play_itf)
    off = channel * STRIDE
    chandata_page[off:off + STRIDE] = entry_bytes

    itf_page = bytearray(0x1000)
    itf_page[0:4] = _pack32(VTBL_ADDR)
    vtbl_page = bytearray(0x1000)
    vtbl_page[0:4] = _pack32(STUB_TARGET)
    # Known Unicorn quirk (see differential_harness.py module docstring):
    # the blx instruction that branches to STUB_TARGET can fault on an
    # entirely unmapped target page even though the harness intercepts
    # the call before any instruction there actually runs. An empty
    # mapping is enough.
    stub_page = bytearray(0x1000)

    def set_play_state_stub(uc):
        del uc
        return stub_result

    res = dh.run_original(
        SO, START, END, {"r0": THIS_ADDR, "r1": channel},
        buffers=[
            dh.MemoryBuffer("this", THIS_ADDR, bytes(this_page)),
            dh.MemoryBuffer("chandata", CHANDATA_ADDR, bytes(chandata_page)),
            dh.MemoryBuffer("itf", ITF_ADDR, bytes(itf_page)),
            dh.MemoryBuffer("vtbl", VTBL_ADDR, bytes(vtbl_page)),
            dh.MemoryBuffer("stub_target", STUB_TARGET, bytes(stub_page)),
        ],
        stub_calls={STUB_TARGET: set_play_state_stub},
    )
    return res, off


def run_model(lib, channel, field_0x04, has_sample_buf, has_play_itf, stub_result):
    entry_bytes = _build_entry_bytes(field_0x04, has_sample_buf, has_play_itf)
    off = channel * STRIDE
    chandata_buf = (ctypes.c_uint8 * (STRIDE * (channel + 1)))()
    for i, b in enumerate(entry_bytes):
        chandata_buf[off + i] = b
    chandata_ptr = ctypes.cast(chandata_buf, ctypes.c_void_p)

    play_itf_ptr = ctypes.c_void_p(None)
    # Kept alive for the duration of the call: the vtable slot and the
    # callback trampoline it points to.
    keepalive = []
    if has_play_itf:
        set_play_state_cb = ctypes.CFUNCTYPE(ctypes.c_int32, ctypes.c_void_p, ctypes.c_int32)(
            lambda itf, state: stub_result)
        vtbl = (ctypes.c_void_p * 1)(ctypes.cast(set_play_state_cb, ctypes.c_void_p))
        itf_obj = (ctypes.c_void_p * 1)(ctypes.cast(vtbl, ctypes.c_void_p))
        keepalive.extend([set_play_state_cb, vtbl, itf_obj])
        play_itf_ptr = ctypes.cast(itf_obj, ctypes.c_void_p)

    this_value = ctypes.c_uint32(THIS_ADDR)
    ret = lib.CSOUND_IF_SL_Stop_model(chandata_ptr, channel, play_itf_ptr, this_value)
    final_entry = bytes(chandata_buf)[off:off + STRIDE]
    return ret & 0xffffffff, final_entry, keepalive


CASES = [
    # (channel, field_0x04, has_sample_buf, has_play_itf, stub_result)
    (0, 0, False, False, 0),       # nothing active/loaded: early exit, return == this
    (0, 1, False, False, 0),       # "active" flag set, but no playItf cached yet: return 0
    (0, 0, True, True, 0),         # loaded (not "active"), has playItf: SetPlayState succeeds
    (0, 1, False, True, 0),        # active, has playItf: SetPlayState succeeds
    (0, 1, False, True, 5),        # active, has playItf: SetPlayState fails (nonzero)
    (1, 1, False, True, 0),        # non-zero channel index exercises the MLA stride math
    (2, 0, True, True, -1),        # third channel slot, failure code -1
]


class CsoundIfSlStopDifferentialTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        cls.lib = build_model(Path(cls.temp.name) / "model.so")

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def test_matches_for_every_case(self):
        for channel, field_0x04, has_sample_buf, has_play_itf, stub_result in CASES:
            with self.subTest(channel=channel, field_0x04=field_0x04,
                               has_sample_buf=has_sample_buf, has_play_itf=has_play_itf,
                               stub_result=stub_result):
                res, off = run_original(channel, field_0x04, has_sample_buf, has_play_itf, stub_result)
                self.assertTrue(res.ok, res.error)

                ret, final_entry, _keepalive = run_model(
                    self.lib, channel, field_0x04, has_sample_buf, has_play_itf, stub_result)

                expected_r0 = res.registers["r0"] & 0xffffffff
                if field_0x04 == 0 and not has_sample_buf:
                    # Early-exit path returns the caller's own `this`
                    # pointer on both sides; both sides were given the
                    # same THIS_ADDR value for this comparison to hold.
                    self.assertEqual(expected_r0, THIS_ADDR)
                    self.assertEqual(ret, THIS_ADDR)
                else:
                    self.assertEqual(expected_r0, ret)

                original_entry = res.final_buffers["chandata"][off:off + STRIDE]
                # Only the two plain-int flag fields are comparable
                # byte-for-byte across sides (see module docstring).
                self.assertEqual(original_entry[0x48:0x4c], final_entry[0x48:0x4c])
                self.assertEqual(original_entry[0x50:0x54], final_entry[0x50:0x54])

    def test_fault_injection_assuming_zero_on_early_exit_is_detected(self):
        # A model that assumed the early-exit path returns 0 (the
        # "sensible"-looking guess for an unused/no-op Stop call) would
        # diverge from the real ELF, which returns the untouched `this`
        # pointer instead. Confirm the real value is not 0, so that
        # wrong assumption is a genuine, catchable divergence.
        res, _off = run_original(0, 0, False, False, 0)
        self.assertTrue(res.ok, res.error)
        real_r0 = res.registers["r0"] & 0xffffffff
        self.assertNotEqual(real_r0, 0)
        self.assertEqual(real_r0, THIS_ADDR)

    def test_fault_injection_stop_pending_flag_always_set_on_active_path(self):
        # A model that forgot the unconditional entry[0x48]=1 write
        # (setting it only on success, mirroring entry[0x50]) would
        # still pass the r0-only checks for the failing case but
        # diverge on this specific byte. Confirm the real ELF sets it
        # even when SetPlayState reports failure.
        res, off = run_original(0, 1, False, True, 5)
        self.assertTrue(res.ok, res.error)
        entry = res.final_buffers["chandata"][off:off + STRIDE]
        self.assertEqual(entry[0x48:0x4c], _pack32(1))
        self.assertEqual(entry[0x50:0x54], _pack32(0))


if __name__ == "__main__":
    unittest.main()
