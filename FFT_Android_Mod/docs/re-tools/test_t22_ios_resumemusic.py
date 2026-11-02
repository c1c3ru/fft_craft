"""T22 (RE_COMPLETUDE_TASKS.md) vertical slice: differential test of the
real iOS_ResumeMusic() ARM body (0xcbd90, 100 B) against a compiled,
independent C reimplementation (c-models/t22_ios_resumemusic.c).

CFFT_STATE::GetMusicBuffer (called twice, index 0 and 1) and
iOS_SetLastBGMFromResumeData are stubbed via callables; both are
already independently read_full elsewhere (NOTES sec. 682), not
re-verified here. iOS_ResumeMusic ends in a genuine ARM tail call
(`b`, not `bl`) into an unsymbolized local function -- the eighth
tail call confirmed this session -- also stubbed, recording its
arguments.
"""
import ctypes
import subprocess
import tempfile
import unittest
from pathlib import Path

import differential_harness as dh

DIR = Path(__file__).resolve().parent
SO = DIR.parents[1] / "src/lib/armeabi/libgl2jni.so"
START, END = 0xcbd90, 0xcbd90 + 100

GET_MUSIC_BUFFER_ADDR = 0x28c2f4
SET_LAST_BGM_ADDR = 0x27f654
TAIL_TARGET_ADDR = 0xbebec

GOT_PAGE = 0x346000
CFFT_STATE_VAR_SLOT = 0x34615c   # holds the address of the CFFT_STATE* variable
LASTBGM0_SLOT = 0x3461a8
LASTBGM1_SLOT = 0x3461ac

CFFT_STATE_VAR_ADDR = 0x650000   # this test's own stand-in for that pointer variable
CFFT_STATE_THIS = 0x12340000     # sentinel CFFT_STATE* value, never dereferenced (GetMusicBuffer stubbed)
LASTBGM0_ADDR = 0x660000
LASTBGM1_ADDR = 0x670000


def _pack32(value: int) -> bytes:
    return (value & 0xffffffff).to_bytes(4, "little")


def _pack16(value: int) -> bytes:
    return (value & 0xffff).to_bytes(2, "little")


def build_model(output: Path):
    subprocess.run(
        ["cc", "-std=c11", "-O2", "-Wall", "-Wextra", "-Werror", "-pedantic",
         "-shared", "-fPIC", str(DIR / "c-models/t22_ios_resumemusic.c"),
         "-o", str(output)],
        check=True, capture_output=True,
    )
    lib = ctypes.CDLL(str(output))
    fn = lib.iOS_ResumeMusic_model
    fn.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p,
                   ctypes.POINTER(ctypes.c_uint16), ctypes.POINTER(ctypes.c_uint16), ctypes.c_void_p]
    fn.restype = None
    return lib


def run_original(buf0, buf1, resume0, resume1, reached):
    got_page = bytearray(0x1000)
    got_page[CFFT_STATE_VAR_SLOT - GOT_PAGE:CFFT_STATE_VAR_SLOT - GOT_PAGE + 4] = _pack32(CFFT_STATE_VAR_ADDR)
    got_page[LASTBGM0_SLOT - GOT_PAGE:LASTBGM0_SLOT - GOT_PAGE + 4] = _pack32(LASTBGM0_ADDR)
    got_page[LASTBGM1_SLOT - GOT_PAGE:LASTBGM1_SLOT - GOT_PAGE + 4] = _pack32(LASTBGM1_ADDR)

    def get_music_buffer_stub(uc):
        from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R1
        this_val, index = uc.reg_read(UC_ARM_REG_R0), uc.reg_read(UC_ARM_REG_R1)
        reached.append(("GetMusicBuffer", this_val, index))
        return buf0 if index == 0 else buf1

    def set_last_bgm_stub(uc):
        from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R1
        out0_ptr, out1_ptr = uc.reg_read(UC_ARM_REG_R0), uc.reg_read(UC_ARM_REG_R1)
        reached.append(("SetLastBGMFromResumeData", out0_ptr, out1_ptr))
        uc.mem_write(out0_ptr, _pack16(resume0))
        uc.mem_write(out1_ptr, _pack16(resume1))
        return 0

    def tail_target_stub(uc):
        from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R1
        reached.append(("tail_target", uc.reg_read(UC_ARM_REG_R0) & 0xffff, uc.reg_read(UC_ARM_REG_R1) & 0xffff))
        return 0

    res = dh.run_original(
        SO, START, END, {},
        buffers=[
            dh.MemoryBuffer("got_page", GOT_PAGE, bytes(got_page)),
            dh.MemoryBuffer("cfft_state_var", CFFT_STATE_VAR_ADDR, _pack32(CFFT_STATE_THIS)),
            dh.MemoryBuffer("lastbgm0", LASTBGM0_ADDR, _pack16(0)),
            dh.MemoryBuffer("lastbgm1", LASTBGM1_ADDR, _pack16(0)),
        ],
        stub_calls={
            GET_MUSIC_BUFFER_ADDR: get_music_buffer_stub,
            SET_LAST_BGM_ADDR: set_last_bgm_stub,
            TAIL_TARGET_ADDR: tail_target_stub,
        },
    )
    return res


def run_model(lib, buf0, buf1, resume0, resume1, reached):
    def _get_music_buffer(this_val, index):
        reached.append(("GetMusicBuffer", this_val, index))
        return buf0 if index == 0 else buf1

    def _set_last_bgm(out0, out1):
        reached.append(("SetLastBGMFromResumeData", None, None))
        out0[0] = resume0
        out1[0] = resume1

    def _tail_target(bgm0, bgm1):
        reached.append(("tail_target", bgm0, bgm1))

    get_cb = ctypes.CFUNCTYPE(ctypes.c_int32, ctypes.c_void_p, ctypes.c_int32)(_get_music_buffer)
    set_cb = ctypes.CFUNCTYPE(None, ctypes.POINTER(ctypes.c_uint16), ctypes.POINTER(ctypes.c_uint16))(_set_last_bgm)
    tail_cb = ctypes.CFUNCTYPE(None, ctypes.c_uint16, ctypes.c_uint16)(_tail_target)

    lastbgm0 = ctypes.c_uint16(0)
    lastbgm1 = ctypes.c_uint16(0)
    lib.iOS_ResumeMusic_model(
        ctypes.c_void_p(CFFT_STATE_THIS), get_cb, set_cb,
        ctypes.byref(lastbgm0), ctypes.byref(lastbgm1), tail_cb)
    return lastbgm0.value, lastbgm1.value


CASES = [
    (5, 7, 100, 200),
    (0xffff, 0, 1, 2),
    (0x1234, 0x5678, 0x9abc, 0xdef0),
]


class IOSResumeMusicDifferentialTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        cls.lib = build_model(Path(cls.temp.name) / "model.so")

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def test_matches_for_every_case(self):
        for buf0, buf1, resume0, resume1 in CASES:
            with self.subTest(buf0=buf0, buf1=buf1, resume0=resume0, resume1=resume1):
                orig_reached, model_reached = [], []
                res = run_original(buf0, buf1, resume0, resume1, orig_reached)
                self.assertTrue(res.ok, res.error)
                model_lastbgm = run_model(self.lib, buf0, buf1, resume0, resume1, model_reached)

                self.assertEqual(
                    [c[0] for c in orig_reached],
                    ["GetMusicBuffer", "GetMusicBuffer", "SetLastBGMFromResumeData", "tail_target"])
                self.assertEqual([c[0] for c in model_reached], [c[0] for c in orig_reached])

                self.assertEqual(orig_reached[0][2], 0)
                self.assertEqual(orig_reached[1][2], 1)

                tail_args_real = orig_reached[-1][1:]
                tail_args_model = model_reached[-1][1:]
                self.assertEqual(tail_args_real, (resume0 & 0xffff, resume1 & 0xffff))
                self.assertEqual(tail_args_model, tail_args_real)
                self.assertEqual(model_lastbgm, (resume0 & 0xffff, resume1 & 0xffff))

    def test_fault_injection_getmusicbuffer_results_are_discarded(self):
        # A model that (wrongly) assumed the tail call uses
        # GetMusicBuffer's results (not SetLastBGMFromResumeData's
        # overwrite) would diverge whenever the two differ.
        reached = []
        res = run_original(buf0=111, buf1=222, resume0=333, resume1=444, reached=reached)
        self.assertTrue(res.ok, res.error)
        tail_args = reached[-1][1:]
        self.assertEqual(tail_args, (333, 444))
        self.assertNotEqual(tail_args, (111, 222))


if __name__ == "__main__":
    unittest.main()
