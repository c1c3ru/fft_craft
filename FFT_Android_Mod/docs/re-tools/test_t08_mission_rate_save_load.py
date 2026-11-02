"""T08 (RE_COMPLETUDE_TASKS.md) vertical slice: differential test of the
real pspSaveDataMissionRateSave/Load ARM bodies (0x289ba8/0x289b8c)
against compiled, independent C reimplementations
(c-models/t08_mission_rate_save_load.c).

Both are genuine ARM tail calls (`b`, not `bl`) into the real memcpy
at 0x714b8 (already confirmed elsewhere in the notes, not re-derived
here) -- stubbed via a callable that performs the actual byte copy
inside Unicorn memory, so the test observes the exact same memory
effect a real memcpy would produce without re-executing libc code.
pspNetEntranceDataMissionBufferGet (0x286e14, already read_full) is
stubbed to return a chosen address for this test's own mission-buffer
stand-in.
"""
import ctypes
import subprocess
import tempfile
import unittest
from pathlib import Path

import differential_harness as dh

DIR = Path(__file__).resolve().parent
SO = DIR.parents[1] / "src/lib/armeabi/libgl2jni.so"

SAVE_START, SAVE_END = 0x289ba8, 0x289ba8 + 32
LOAD_START, LOAD_END = 0x289b8c, 0x289b8c + 28

GET_MISSION_BUFFER_ADDR = 0x286e14
MEMCPY_ADDR = 0x714b8

SAVE_ADDR = 0x600000
SAVE_SIZE = 0x80
MISSION_BUFFER_ADDR = 0x610000
FIELD_OFFSET = 0x60
FIELD_SIZE = 0x20


def build_model(output: Path):
    subprocess.run(
        ["cc", "-std=c11", "-O2", "-Wall", "-Wextra", "-Werror", "-pedantic",
         "-shared", "-fPIC", str(DIR / "c-models/t08_mission_rate_save_load.c"),
         "-o", str(output)],
        check=True, capture_output=True,
    )
    lib = ctypes.CDLL(str(output))
    for symbol in ("pspSaveDataMissionRateSave_model", "pspSaveDataMissionRateLoad_model"):
        fn = getattr(lib, symbol)
        fn.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p]
        fn.restype = None
    return lib


def _sentinel(offset_base, size):
    return bytes((i + offset_base + 1) & 0xff or 1 for i in range(size))


def _memcpy_stub(uc):
    from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2
    dest = uc.reg_read(UC_ARM_REG_R0)
    src = uc.reg_read(UC_ARM_REG_R1)
    size = uc.reg_read(UC_ARM_REG_R2)
    uc.mem_write(dest, bytes(uc.mem_read(src, size)))
    return 0


def run_original(start, end, save_bytes, mission_bytes):
    def get_mission_buffer_stub(uc):
        del uc
        return MISSION_BUFFER_ADDR

    res = dh.run_original(
        SO, start, end, {"r0": SAVE_ADDR},
        buffers=[
            dh.MemoryBuffer("save", SAVE_ADDR, save_bytes),
            dh.MemoryBuffer("mission", MISSION_BUFFER_ADDR, mission_bytes),
        ],
        stub_calls={
            GET_MISSION_BUFFER_ADDR: get_mission_buffer_stub,
            MEMCPY_ADDR: _memcpy_stub,
        },
    )
    return res


def run_model(lib, symbol, save_bytes, mission_bytes):
    save_buf = (ctypes.c_uint8 * len(save_bytes))(*save_bytes)
    mission_buf = (ctypes.c_uint8 * len(mission_bytes))(*mission_bytes)

    get_buf_cb = ctypes.CFUNCTYPE(ctypes.c_void_p)(
        lambda: ctypes.cast(mission_buf, ctypes.c_void_p).value)

    def _copy(dest, src, size):
        ctypes.memmove(dest, src, size)

    copy_cb = ctypes.CFUNCTYPE(None, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int32)(_copy)

    getattr(lib, symbol)(save_buf, get_buf_cb, copy_cb)
    return bytes(save_buf), bytes(mission_buf)


class MissionRateSaveLoadDifferentialTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        cls.lib = build_model(Path(cls.temp.name) / "model.so")

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def test_save_copies_mission_buffer_into_save_struct(self):
        save_bytes = _sentinel(0, SAVE_SIZE)
        mission_bytes = _sentinel(0x80, FIELD_SIZE)

        res = run_original(SAVE_START, SAVE_END, save_bytes, mission_bytes)
        self.assertTrue(res.ok, res.error)
        model_save, model_mission = run_model(
            self.lib, "pspSaveDataMissionRateSave_model", save_bytes, mission_bytes)

        real_save = res.final_buffers["save"]
        real_mission = res.final_buffers["mission"]
        self.assertEqual(real_save, model_save)
        self.assertEqual(real_mission, model_mission)

        # The field at +0x60 must now equal the mission buffer's
        # original bytes; everything else in `save` must be untouched.
        self.assertEqual(real_save[FIELD_OFFSET:FIELD_OFFSET + FIELD_SIZE], mission_bytes)
        self.assertEqual(real_save[:FIELD_OFFSET], save_bytes[:FIELD_OFFSET])
        self.assertEqual(real_mission, mission_bytes)  # source side untouched

    def test_load_copies_save_struct_into_mission_buffer(self):
        save_bytes = _sentinel(0, SAVE_SIZE)
        mission_bytes = _sentinel(0x80, FIELD_SIZE)

        res = run_original(LOAD_START, LOAD_END, save_bytes, mission_bytes)
        self.assertTrue(res.ok, res.error)
        model_save, model_mission = run_model(
            self.lib, "pspSaveDataMissionRateLoad_model", save_bytes, mission_bytes)

        real_save = res.final_buffers["save"]
        real_mission = res.final_buffers["mission"]
        self.assertEqual(real_save, model_save)
        self.assertEqual(real_mission, model_mission)

        self.assertEqual(real_mission, save_bytes[FIELD_OFFSET:FIELD_OFFSET + FIELD_SIZE])
        self.assertEqual(real_save, save_bytes)  # source side (save) untouched

    def test_fault_injection_save_and_load_directions_are_not_interchangeable(self):
        # A model that mixed up dest/src between Save and Load would
        # copy data the wrong way. Confirm the two directions produce
        # DIFFERENT observable effects for inputs where the mission
        # buffer and the save field differ.
        save_bytes = _sentinel(0, SAVE_SIZE)
        mission_bytes = bytes((b ^ 0xff) for b in _sentinel(0x80, FIELD_SIZE))

        res_save = run_original(SAVE_START, SAVE_END, save_bytes, mission_bytes)
        res_load = run_original(LOAD_START, LOAD_END, save_bytes, mission_bytes)
        self.assertTrue(res_save.ok and res_load.ok)

        # After Save: save's field becomes the mission buffer's bytes.
        self.assertEqual(
            res_save.final_buffers["save"][FIELD_OFFSET:FIELD_OFFSET + FIELD_SIZE], mission_bytes)
        # After Load: mission buffer becomes save's field bytes --
        # the opposite direction, and (given the inputs differ) a
        # different result than Save's.
        self.assertEqual(res_load.final_buffers["mission"], save_bytes[FIELD_OFFSET:FIELD_OFFSET + FIELD_SIZE])
        self.assertNotEqual(
            res_save.final_buffers["save"][FIELD_OFFSET:FIELD_OFFSET + FIELD_SIZE],
            res_load.final_buffers["mission"])


if __name__ == "__main__":
    unittest.main()
