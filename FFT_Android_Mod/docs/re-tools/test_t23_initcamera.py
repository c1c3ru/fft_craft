"""T23 (RE_COMPLETUDE_TASKS.md) vertical slice: differential test of the
real InitCamera() ARM body (0x218dcc, 40 B) against a compiled,
independent C reimplementation (c-models/t23_initcamera.c).

InitCamera has no prologue and ends in a plain `b` to 0x218cf4 -- a
genuine ARM tail call into SetDefaultCamera(), the same tail-call-as-
stub treatment already exercised (and, in that case, needed to fix a
real harness bug) for T20's iOSUnitListWinOnOff. Here the tail-call
target address is a real address inside the same .text section the
harness already maps in full, so (unlike a synthetic ELF) it needs no
extra empty-page mapping -- same lesson as T14's Boot_FrameMove.
"""
import ctypes
import subprocess
import tempfile
import unittest
from pathlib import Path

import differential_harness as dh

DIR = Path(__file__).resolve().parent
SO = DIR.parents[1] / "src/lib/armeabi/libgl2jni.so"
START, END = 0x218dcc, 0x218dcc + 40

# Real global camera struct base address, resolved by hand from the
# PC-relative literal at 0x218dcc (no GOT indirection -- a local/static
# data symbol). The real function hardcodes this address; it is not
# passed in through any register, so the test buffer must sit exactly
# here, not at an arbitrary chosen address.
CAMERA_ADDR = 0x60593c
SET_DEFAULT_CAMERA_ADDR = 0x218cf4  # confirmed: SetDefaultCamera's real entry (= InitCamera's own start - 216 B)

FIELD_OFFSETS = (0xa0, 0xa4, 0xa8, 0xac, 0xb0)
CAMERA_SIZE = 0xc0


def build_model(output: Path):
    subprocess.run(
        ["cc", "-std=c11", "-O2", "-Wall", "-Wextra", "-Werror", "-pedantic",
         "-shared", "-fPIC", str(DIR / "c-models/t23_initcamera.c"),
         "-o", str(output)],
        check=True, capture_output=True,
    )
    lib = ctypes.CDLL(str(output))
    fn = lib.InitCamera_model
    fn.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
    fn.restype = None
    return lib


def _sentinel_camera_bytes():
    # Every byte distinct and nonzero, so an accidental off-by-field
    # write (e.g. zeroing +0xa4 instead of +0xa0) is visible, not
    # masked by coincidentally-equal sentinel values.
    return bytes((i + 1) & 0xff or 1 for i in range(CAMERA_SIZE))


def run_original(reached_tail_call):
    camera_bytes = bytearray(_sentinel_camera_bytes())

    def tail_call_stub(uc):
        reached_tail_call.append(True)
        return 0

    res = dh.run_original(
        SO, START, END, {},
        buffers=[dh.MemoryBuffer("camera", CAMERA_ADDR, bytes(camera_bytes))],
        stub_calls={SET_DEFAULT_CAMERA_ADDR: tail_call_stub},
    )
    return res


def run_model(lib, reached_tail_call):
    camera_buf = (ctypes.c_uint8 * CAMERA_SIZE)(*_sentinel_camera_bytes())

    def _set_default_camera():
        reached_tail_call.append(True)

    cb = ctypes.CFUNCTYPE(None)(_set_default_camera)
    lib.InitCamera_model(camera_buf, cb)
    return bytes(camera_buf)


class InitCameraDifferentialTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        cls.lib = build_model(Path(cls.temp.name) / "model.so")

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def test_fields_zeroed_and_tail_call_reached_exactly_once(self):
        orig_reached, model_reached = [], []
        res = run_original(orig_reached)
        self.assertTrue(res.ok, res.error)
        final_camera = run_model(self.lib, model_reached)

        self.assertEqual(len(orig_reached), 1)
        self.assertEqual(len(model_reached), 1)

        original_camera = res.final_buffers["camera"]
        self.assertEqual(original_camera, final_camera)

        expected = bytearray(_sentinel_camera_bytes())
        for field_off in FIELD_OFFSETS:
            expected[field_off:field_off + 4] = bytes(4)
        self.assertEqual(original_camera, bytes(expected))

    def test_fault_injection_only_the_five_fields_are_touched(self):
        # A model that zeroed a wider range (e.g. the whole struct, or
        # an off-by-one field window) would diverge from the real ELF,
        # which leaves every other byte at its original sentinel
        # value. Confirm a byte just before the first field and one
        # just after the last field survive untouched.
        res = run_original([])
        self.assertTrue(res.ok, res.error)
        camera = res.final_buffers["camera"]
        sentinel = _sentinel_camera_bytes()
        self.assertEqual(camera[0xa0 - 1], sentinel[0xa0 - 1])
        self.assertEqual(camera[0xb0 + 4], sentinel[0xb0 + 4])
        self.assertNotEqual(camera[0xa0 - 1], 0)
        self.assertNotEqual(camera[0xb0 + 4], 0)


if __name__ == "__main__":
    unittest.main()
