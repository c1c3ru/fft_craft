"""T17 (RE_COMPLETUDE_TASKS.md) vertical slice: differential test of the
real ClearForBattleRoutine() ARM body (0x279ed4, 24 B) against a
compiled, independent C reimplementation
(c-models/t17_clearforbattleroutine.c).

No prologue, ends in a plain `b` -- the third genuine ARM tail call
confirmed this session (after T20's iOSUnitListWinOnOff and T23's
InitCamera), into ClearMove(MOVE*) (0x27383c, independently
differential-tested in test_t17_clearmove.py). The tail-call target
is a real address inside the same .text section already mapped by the
harness, so (per the T14/T23 lesson) it needs no extra empty-page
mapping.
"""
import ctypes
import subprocess
import tempfile
import unittest
from pathlib import Path

import differential_harness as dh

DIR = Path(__file__).resolve().parent
SO = DIR.parents[1] / "src/lib/armeabi/libgl2jni.so"
START, END = 0x279ed4, 0x279ed4 + 24

GOT_PAGE = 0x347000
BASE_SLOT = 0x347bb8
GLOBAL_BASE = 0x650000   # this test's own stand-in for the real global base
CLEAR_MOVE_ADDR = 0x27383c
MOVE_OFFSET = 0x17c0 + 0x3c
MOVE_SIZE = 0x20


def build_model(output: Path):
    subprocess.run(
        ["cc", "-std=c11", "-O2", "-Wall", "-Wextra", "-Werror", "-pedantic",
         "-shared", "-fPIC", str(DIR / "c-models/t17_clearforbattleroutine.c"),
         "-o", str(output)],
        check=True, capture_output=True,
    )
    lib = ctypes.CDLL(str(output))
    fn = lib.ClearForBattleRoutine_model
    fn.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
    fn.restype = None
    return lib


def _pack32(value: int) -> bytes:
    return (value & 0xffffffff).to_bytes(4, "little")


def run_original(reached):
    got_page = bytearray(0x1000)
    got_page[BASE_SLOT - GOT_PAGE:BASE_SLOT - GOT_PAGE + 4] = _pack32(GLOBAL_BASE)

    # The global region only needs to be big enough to be addressable
    # up to +0x17fc; its content is irrelevant since ClearMove is
    # stubbed, not really executed.
    global_region = bytearray(MOVE_OFFSET + MOVE_SIZE)

    def clear_move_stub(uc):
        from unicorn.arm_const import UC_ARM_REG_R0
        reached.append(uc.reg_read(UC_ARM_REG_R0))
        return 0

    res = dh.run_original(
        SO, START, END, {},
        buffers=[
            dh.MemoryBuffer("got_page", GOT_PAGE, bytes(got_page)),
            dh.MemoryBuffer("global_region", GLOBAL_BASE, bytes(global_region)),
        ],
        stub_calls={CLEAR_MOVE_ADDR: clear_move_stub},
    )
    return res


def run_model(lib, reached):
    def _clear_move(move_ptr):
        reached.append(ctypes.cast(move_ptr, ctypes.c_void_p).value)

    cb = ctypes.CFUNCTYPE(None, ctypes.c_void_p)(_clear_move)
    sentinel_ptr = ctypes.c_void_p(0x12345678)
    lib.ClearForBattleRoutine_model(sentinel_ptr, cb)


class ClearForBattleRoutineDifferentialTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        cls.lib = build_model(Path(cls.temp.name) / "model.so")

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def test_tail_calls_clear_move_with_the_right_address_exactly_once(self):
        orig_reached, model_reached = [], []
        res = run_original(orig_reached)
        self.assertTrue(res.ok, res.error)
        run_model(self.lib, model_reached)

        self.assertEqual(len(orig_reached), 1)
        self.assertEqual(orig_reached[0], GLOBAL_BASE + MOVE_OFFSET)
        self.assertEqual(len(model_reached), 1)
        self.assertEqual(model_reached[0], 0x12345678)


if __name__ == "__main__":
    unittest.main()
