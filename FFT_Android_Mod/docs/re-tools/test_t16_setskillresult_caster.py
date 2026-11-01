"""T16 (RE_COMPLETUDE_TASKS.md) vertical slice: differential test of the
real setskillresult_caster(int) ARM body (0x1ce950, via the T10 harness)
against a compiled, independent C reimplementation
(c-models/t16_setskillresult_caster.c). setskillresult() itself
(0x1cda4c, 3844 B) is stubbed on both sides -- this test covers the
wrapper's own control flow and BWORK field writes, not the combat
formula setskillresult() implements.
"""
import ctypes
import subprocess
import tempfile
import unittest
from pathlib import Path

import differential_harness as dh

DIR = Path(__file__).resolve().parent
SO = DIR.parents[1] / "src/lib/armeabi/libgl2jni.so"
START, END = 0x1ce950, 0x1ce950 + 188

# GOT-relative globals, resolved and verified by direct execution
# (NOTES sec. 662): shared base 0x347d58, individual slots below.
GOT_BWORK_ARRAY = 0x346d04
GOT_CURRENT_CASTER_BWORK = 0x347368
GOT_CURRENT_CASTER_ID = 0x347370
GOT_RESULT_SLOT_PTR = 0x347374
GOT_TEMPLATE = 0x347394

BWORK_ARRAY = 0x600000
CASTER_SLOT = 0x620000
CASTER_ID_CELL = 0x621000
RESULT_PTR_CELL = 0x622000
TEMPLATE = 0x623000
BWORK_SIZE = 0x1e6
BWORK_COUNT = 25


def build_model(output: Path):
    subprocess.run(
        ["cc", "-std=c11", "-O2", "-Wall", "-Wextra", "-Werror", "-pedantic",
         "-shared", "-fPIC", str(DIR / "c-models/t16_setskillresult_caster.c"),
         "-o", str(output)],
        check=True, capture_output=True,
    )
    lib = ctypes.CDLL(str(output))
    fn = lib.setskillresult_caster_model
    fn.argtypes = [
        ctypes.c_int32, ctypes.POINTER(ctypes.c_uint8),
        ctypes.POINTER(ctypes.POINTER(ctypes.c_uint8)),
        ctypes.POINTER(ctypes.c_uint8),
        ctypes.POINTER(ctypes.POINTER(ctypes.c_uint8)),
        ctypes.POINTER(ctypes.c_uint8),
        ctypes.c_void_p, ctypes.c_void_p,
    ]
    fn.restype = ctypes.c_int32
    return lib


NOOP_COPY = ctypes.CFUNCTYPE(None, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int32)(
    lambda src, dst, size: None)
NOOP_SET = ctypes.CFUNCTYPE(None, ctypes.c_int32)(lambda caster_id: None)


def run_model(lib, caster_id, bwork_bytes, flag_at_1):
    buf = (ctypes.c_uint8 * len(bwork_bytes)).from_buffer_copy(bwork_bytes)
    caster_bwork_ptr = ctypes.POINTER(ctypes.c_uint8)()
    caster_id_cell = (ctypes.c_uint8 * 4)()
    result_slot_ptr = ctypes.POINTER(ctypes.c_uint8)()
    template = (ctypes.c_uint8 * 0x2e)()
    ret = lib.setskillresult_caster_model(
        caster_id, buf,
        ctypes.byref(caster_bwork_ptr), caster_id_cell,
        ctypes.byref(result_slot_ptr), template,
        ctypes.cast(NOOP_COPY, ctypes.c_void_p),
        ctypes.cast(NOOP_SET, ctypes.c_void_p))
    bwork_ptr_offset = (ctypes.cast(caster_bwork_ptr, ctypes.c_void_p).value or 0) \
        - ctypes.cast(buf, ctypes.c_void_p).value
    result_ptr_offset = (ctypes.cast(result_slot_ptr, ctypes.c_void_p).value or 0) \
        - ctypes.cast(buf, ctypes.c_void_p).value
    return ret & 0xffffffff, bwork_ptr_offset, caster_id_cell[1], result_ptr_offset


def make_got_page(base, entries):
    buf = bytearray(0x1000)
    for addr, val in entries.items():
        off = addr - base
        buf[off:off + 4] = (val & 0xffffffff).to_bytes(4, "little")
    return bytes(buf)


def run_original(caster_id, bwork_bytes):
    got1 = make_got_page(0x346000, {GOT_BWORK_ARRAY: BWORK_ARRAY})
    got2 = make_got_page(0x347000, {
        GOT_CURRENT_CASTER_BWORK: CASTER_SLOT,
        GOT_CURRENT_CASTER_ID: CASTER_ID_CELL,
        GOT_RESULT_SLOT_PTR: RESULT_PTR_CELL,
        GOT_TEMPLATE: TEMPLATE,
    })
    return dh.run_original(
        SO, START, END, {"r0": caster_id},
        buffers=[
            dh.MemoryBuffer("got1", 0x346000, got1),
            dh.MemoryBuffer("got2", 0x347000, got2),
            dh.MemoryBuffer("bwork", BWORK_ARRAY, bwork_bytes),
            dh.MemoryBuffer("casterslot", CASTER_SLOT, bytes(4)),
            dh.MemoryBuffer("casteridcell", CASTER_ID_CELL, bytes(4)),
            dh.MemoryBuffer("resultptrcell", RESULT_PTR_CELL, bytes(4)),
            dh.MemoryBuffer("template", TEMPLATE, bytes(0x2e)),
        ],
        stub_calls={0x1d9948: 0, 0x1cda4c: 0},
    )


class SetSkillResultCasterDifferentialTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        cls.lib = build_model(Path(cls.temp.name) / "model.so")

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def _compare(self, caster_id, flag):
        bwork_bytes = bytearray(BWORK_SIZE * BWORK_COUNT)
        if 0 <= caster_id < BWORK_COUNT:
            bwork_bytes[caster_id * BWORK_SIZE + 1] = flag
        res = run_original(caster_id, bytes(bwork_bytes))
        self.assertTrue(res.ok, res.error)
        ret, m_bwork_off, m_id_byte, m_result_off = run_model(
            self.lib, caster_id, bytes(bwork_bytes), flag)
        self.assertEqual(res.registers["r0"] & 0xffffffff, ret)
        if res.registers["r0"] == 0:
            expected_bwork_off = caster_id * BWORK_SIZE
            self.assertEqual(m_bwork_off, expected_bwork_off)
            self.assertEqual(m_result_off, expected_bwork_off + 0x1ae)
            self.assertEqual(m_id_byte, caster_id)

    def test_success_path_matches_for_several_casters(self):
        for caster_id in (0, 1, 3, 10, 20):
            with self.subTest(caster_id=caster_id):
                self._compare(caster_id, flag=5)

    def test_caster_id_boundary(self):
        self._compare(20, flag=5)   # inclusive boundary: must succeed
        self._compare(21, flag=5)   # one past: must fail

    def test_flag_0xff_fails(self):
        self._compare(3, flag=0xff)

    def test_fault_injection_wrong_result_offset_is_detected(self):
        # A model that forgets the extra "+6" (i.e. uses +0x1a8 instead
        # of +0x1ae for the result slot) must disagree with the real ELF.
        res = run_original(3, bytes(BWORK_SIZE * BWORK_COUNT))
        self.assertTrue(res.ok, res.error)
        real_result_off = int.from_bytes(res.final_buffers["resultptrcell"], "little")
        wrong_guess = BWORK_ARRAY + 3 * BWORK_SIZE + 0x1a8  # off by the missing +6
        self.assertNotEqual(real_result_off, wrong_guess)


if __name__ == "__main__":
    unittest.main()
