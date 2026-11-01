"""T14 (RE_COMPLETUDE_TASKS.md) vertical slice: differential test of the
real Boot_FrameMove() ARM body (0x2b3590, 128 B) against a compiled,
independent C reimplementation (c-models/t14_boot_framemove.c).

CTHREAD::Sync (0xb9f44), CEGL2_IF::ClearBackdrop (0xa7e7c) and
onGotoNextMode (0x2b20f4) are stubbed on both sides via callables, so
the stubs can both vary their return value per case and record the
arguments they were called with -- used here to confirm ClearBackdrop
is called with (gl_this, 0.0f, 0.0f, 0.0f) and onGotoNextMode with (3),
exactly as read off the real bytes.

The three GOT-indirected globals (flag_a, thread_this, gl_this) are
built as real memory in the ELF's own GOT page (0x347000, holding the
three real GOT-slot addresses resolved by hand -- see NOTES sec. 668)
pointing at this test's own small globals, instead of being passed to
the real ELF side as plain arguments (the real function reads them
from memory, not from registers, so the differential test must put
real bytes where the real code looks for them).
"""
import ctypes
import subprocess
import tempfile
import unittest
from pathlib import Path

import differential_harness as dh

DIR = Path(__file__).resolve().parent
SO = DIR.parents[1] / "src/lib/armeabi/libgl2jni.so"
START, END = 0x2b3590, 0x2b3590 + 128

# Real GOT slot addresses, resolved by hand from the literal pool +
# pc-relative chain in the real instructions at 0x2b3594/0x2b35b0/0x2b35d8
# (see NOTES sec. 668) -- NOT invented addresses.
GOT_PAGE = 0x347000
FLAG_A_SLOT = 0x347cb4
THREAD_SLOT = 0x347c7c
GL_SLOT = 0x347c48

FLAG_A_VAR = 0x650000      # this test's own stand-in for the real .bss var
THREAD_VAR = 0x651000
GL_VAR = 0x652000

SYNC_ADDR = 0xb9f44
CLEAR_BACKDROP_ADDR = 0xa7e7c
GOTO_NEXT_MODE_ADDR = 0x2b20f4

THREAD_THIS = 0x11110000   # sentinel "this" pointer values -- never
GL_THIS = 0x22220000        # dereferenced by the stubs, only compared


def build_model(output: Path):
    subprocess.run(
        ["cc", "-std=c11", "-O2", "-Wall", "-Wextra", "-Werror", "-pedantic",
         "-shared", "-fPIC", str(DIR / "c-models/t14_boot_framemove.c"),
         "-o", str(output)],
        check=True, capture_output=True,
    )
    lib = ctypes.CDLL(str(output))
    fn = lib.Boot_FrameMove_model
    fn.argtypes = [ctypes.c_int32, ctypes.c_void_p, ctypes.c_void_p,
                   ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p]
    fn.restype = ctypes.c_int32
    return lib


def _pack32(value: int) -> bytes:
    return (value & 0xffffffff).to_bytes(4, "little")


def run_original(flag_a, sync_result):
    got_page = bytearray(0x1000)
    got_page[FLAG_A_SLOT - GOT_PAGE:FLAG_A_SLOT - GOT_PAGE + 4] = _pack32(FLAG_A_VAR)
    got_page[THREAD_SLOT - GOT_PAGE:THREAD_SLOT - GOT_PAGE + 4] = _pack32(THREAD_VAR)
    got_page[GL_SLOT - GOT_PAGE:GL_SLOT - GOT_PAGE + 4] = _pack32(GL_VAR)

    calls = {"clear_backdrop": None, "goto_next_mode": None}

    def sync_stub(uc):
        del uc
        return sync_result

    def clear_backdrop_stub(uc):
        from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3
        calls["clear_backdrop"] = tuple(
            uc.reg_read(r) for r in (UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3))
        return 0

    def goto_next_mode_stub(uc):
        from unicorn.arm_const import UC_ARM_REG_R0
        calls["goto_next_mode"] = uc.reg_read(UC_ARM_REG_R0)
        return 0

    res = dh.run_original(
        SO, START, END, {},
        buffers=[
            dh.MemoryBuffer("got_page", GOT_PAGE, bytes(got_page)),
            dh.MemoryBuffer("flag_a_var", FLAG_A_VAR, _pack32(flag_a)),
            dh.MemoryBuffer("thread_var", THREAD_VAR, _pack32(THREAD_THIS)),
            dh.MemoryBuffer("gl_var", GL_VAR, _pack32(GL_THIS)),
            # SYNC_ADDR/CLEAR_BACKDROP_ADDR/GOTO_NEXT_MODE_ADDR need no
            # explicit empty-page mapping (contrast T14/T25's own
            # synthetic STUB_TARGET pages): they are real addresses
            # inside the same huge .text section Boot_FrameMove itself
            # lives in, which the harness already maps whole because
            # that section overlaps [START, END) -- mapping them again
            # here would collide with that existing mapping.
        ],
        stub_calls={
            SYNC_ADDR: sync_stub,
            CLEAR_BACKDROP_ADDR: clear_backdrop_stub,
            GOTO_NEXT_MODE_ADDR: goto_next_mode_stub,
        },
    )
    return res, calls


def run_model(lib, flag_a, sync_result):
    calls = {"clear_backdrop": None, "goto_next_mode": None}

    sync_cb = ctypes.CFUNCTYPE(ctypes.c_int32, ctypes.c_void_p)(lambda this: sync_result)

    def _clear_backdrop(this, r, g, b):
        calls["clear_backdrop"] = (this, r, g, b)

    def _goto_next_mode(mode):
        calls["goto_next_mode"] = mode

    clear_cb = ctypes.CFUNCTYPE(None, ctypes.c_void_p, ctypes.c_float, ctypes.c_float, ctypes.c_float)(
        _clear_backdrop)
    goto_cb = ctypes.CFUNCTYPE(None, ctypes.c_int32)(_goto_next_mode)

    ret = lib.Boot_FrameMove_model(
        flag_a, ctypes.c_void_p(THREAD_THIS), sync_cb,
        ctypes.c_void_p(GL_THIS), clear_cb, goto_cb)
    return ret, calls


CASES = [
    (1, 0),    # flag_a set: early exit, never reaches Sync at all
    (0, 2),    # flag_a clear, sync "still running" (neither 0 nor 1): return 0
    (0, 1),    # flag_a clear, sync reports error: return -1
    (0, 0),    # flag_a clear, sync succeeded: ClearBackdrop + onGotoNextMode(3), return 1
]


class BootFrameMoveDifferentialTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        cls.lib = build_model(Path(cls.temp.name) / "model.so")

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def test_matches_for_every_case(self):
        for flag_a, sync_result in CASES:
            with self.subTest(flag_a=flag_a, sync_result=sync_result):
                res, orig_calls = run_original(flag_a, sync_result)
                self.assertTrue(res.ok, res.error)
                ret, model_calls = run_model(self.lib, flag_a, sync_result)

                expected_r0 = res.registers["r0"] & 0xffffffff
                self.assertEqual(expected_r0, ret & 0xffffffff)

                if flag_a == 0 and sync_result == 0:
                    self.assertEqual(orig_calls["clear_backdrop"], (GL_THIS, 0, 0, 0))
                    self.assertEqual(model_calls["clear_backdrop"], (GL_THIS, 0.0, 0.0, 0.0))
                    self.assertEqual(orig_calls["goto_next_mode"], 3)
                    self.assertEqual(model_calls["goto_next_mode"], 3)
                else:
                    self.assertIsNone(orig_calls["clear_backdrop"])
                    self.assertIsNone(model_calls["clear_backdrop"])
                    self.assertIsNone(orig_calls["goto_next_mode"])
                    self.assertIsNone(model_calls["goto_next_mode"])

    def test_fault_injection_sync_still_running_is_not_an_error_return(self):
        # A model that treated "any nonzero Sync() result" as the
        # error path (returning -1 unconditionally) would diverge from
        # the real ELF for sync results other than 0 or 1 -- confirm
        # the real ELF actually returns 0 (not -1) for one such value,
        # so that wrong simplification is a genuine divergence.
        res, _calls = run_original(0, 2)
        self.assertTrue(res.ok, res.error)
        self.assertEqual(res.registers["r0"] & 0xffffffff, 0)
        self.assertNotEqual(res.registers["r0"] & 0xffffffff, 0xffffffff)


if __name__ == "__main__":
    unittest.main()
