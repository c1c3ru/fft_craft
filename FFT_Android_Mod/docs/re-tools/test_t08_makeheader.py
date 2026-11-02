"""T08 (RE_COMPLETUDE_TASKS.md) vertical slice: differential test of the
real MakeHeader(int, int, CARD_HEADER*) ARM body (0x187264, 688 B)
against a compiled, independent C reimplementation
(c-models/t08_makeheader.c).

memcpy/memset/__divsi3/__aeabi_idivmod are stubbed via callables that
perform the real operation in Python (not re-derived GCC division
codegen -- the real ELF side still exercises the actual control flow
and byte layout, only the arithmetic primitives are substituted with
their well-known standard semantics). __stack_chk_fail is stubbed to
raise loudly if ever reached (it must not be, on these inputs).
read_eventflag is stubbed via a callable so its return value can vary
by case.

The three confirmed globals (play_time.hours/minutes/seconds, stride
4, contiguous) and the two single-indirection GOT globals
(event_flag_table, g5_block) are built as real memory at their
resolved GOT addresses -- see NOTES sec. 678 for how each was found,
including by direct empirical probing against the real ELF (the dense
GCC divide-by-constant codegen was not hand-decoded).
"""
import ctypes
import subprocess
import tempfile
import unittest
from pathlib import Path

import differential_harness as dh

DIR = Path(__file__).resolve().parent
SO = DIR.parents[1] / "src/lib/armeabi/libgl2jni.so"
START, END = 0x187264, 0x187264 + 688

MEMCPY_ADDR = 0x714b8
MEMSET_ADDR = 0x714c4
STACK_CHK_FAIL_ADDR = 0x715cc
READ_EVENTFLAG_ADDR = 0xdb83c
DIVSI3_ADDR = 0x2ca79c
IDIVMOD_ADDR = 0x2ca878

CANARY_SLOT = 0x345f0c
VALUE2_SLOT = 0x346b00     # hours
LOOPSRC_SLOT = 0x346af8    # minutes
G3RD_SLOT = 0x346afc       # seconds
G4_SLOT = 0x346e30         # event_flag_table (single indirection)
G5_SLOT = 0x346e34         # g5_block (single indirection)

CANARY_VAR = 0x650000
PLAYTIME_BASE = 0x651000   # hours, minutes, seconds as 3 contiguous int32
ARRAY4_ADDR = 0x660000     # event_flag_table stand-in, stride 20
ARRAY5_ADDR = 0x670000     # g5_block stand-in

OUT_ADDR = 0x600000
OUT_SIZE = 0x200
TITLE_ADDR = 0x308064      # real literal address, real bytes read below

TITLE_BYTES = bytes([
    0x82, 0x65, 0x82, 0x65, 0x82, 0x73, 0x81, 0x40, 0x82, 0x65, 0x82, 0x68,
    0x82, 0x6b, 0x82, 0x64, 0x81, 0x40, 0x81, 0x40, 0x81, 0x40,
])


def build_model(output: Path):
    subprocess.run(
        ["cc", "-std=c11", "-O2", "-Wall", "-Wextra", "-Werror", "-pedantic",
         "-shared", "-fPIC", str(DIR / "c-models/t08_makeheader.c"),
         "-o", str(output)],
        check=True, capture_output=True,
    )
    lib = ctypes.CDLL(str(output))
    fn = lib.MakeHeader_model
    fn.argtypes = [ctypes.c_int32, ctypes.c_int32, ctypes.c_void_p,
                   ctypes.POINTER(ctypes.c_int32), ctypes.c_void_p,
                   ctypes.c_void_p, ctypes.c_void_p]
    fn.restype = None
    return lib


def _pack32(value: int) -> bytes:
    return (value & 0xffffffff).to_bytes(4, "little")


def _page(addr: int) -> int:
    return addr & ~0xfff


def run_original(a0, a1, hours, minutes, seconds, eventflag_ret, array4_entry, array5_block):
    canary_page_base = _page(CANARY_SLOT)
    canary_page = bytearray(0x1000)
    canary_page[CANARY_SLOT - canary_page_base:CANARY_SLOT - canary_page_base + 4] = _pack32(CANARY_VAR)

    main_page_base = _page(VALUE2_SLOT)
    main_page = bytearray(0x1000)
    main_page[VALUE2_SLOT - main_page_base:VALUE2_SLOT - main_page_base + 4] = _pack32(PLAYTIME_BASE)
    main_page[LOOPSRC_SLOT - main_page_base:LOOPSRC_SLOT - main_page_base + 4] = _pack32(PLAYTIME_BASE + 4)
    main_page[G3RD_SLOT - main_page_base:G3RD_SLOT - main_page_base + 4] = _pack32(PLAYTIME_BASE + 8)
    main_page[G4_SLOT - main_page_base:G4_SLOT - main_page_base + 4] = _pack32(ARRAY4_ADDR)
    main_page[G5_SLOT - main_page_base:G5_SLOT - main_page_base + 4] = _pack32(ARRAY5_ADDR)

    title_page_base = _page(TITLE_ADDR)
    title_page = bytearray(0x1000)
    off_in_page = TITLE_ADDR - title_page_base
    title_page[off_in_page:off_in_page + len(TITLE_BYTES)] = TITLE_BYTES

    array4 = bytearray(20 * 128)
    idx, data20 = array4_entry
    array4[idx * 20:idx * 20 + 20] = data20
    array5 = bytearray(0x100)
    array5[0x20:0x20 + len(array5_block)] = array5_block

    def memcpy_stub(uc):
        from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2
        dest, src, size = (uc.reg_read(r) for r in (UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2))
        uc.mem_write(dest, bytes(uc.mem_read(src, size)))
        return dest

    def memset_stub(uc):
        from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2
        dest, val, size = (uc.reg_read(r) for r in (UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2))
        uc.mem_write(dest, bytes([val & 0xff]) * size)
        return dest

    def _signed(v):
        return v - (1 << 32) if v & 0x80000000 else v

    def divsi3_stub(uc):
        from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R1
        a, b = _signed(uc.reg_read(UC_ARM_REG_R0)), _signed(uc.reg_read(UC_ARM_REG_R1))
        return (a // b if (a < 0) == (b < 0) else -(-a // b)) & 0xffffffff

    def idivmod_stub(uc):
        from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R1
        a, b = _signed(uc.reg_read(UC_ARM_REG_R0)), _signed(uc.reg_read(UC_ARM_REG_R1))
        q = a // b if (a < 0) == (b < 0) else -(-a // b)
        r = a - q * b
        uc.reg_write(UC_ARM_REG_R1, r & 0xffffffff)
        return q & 0xffffffff

    def eventflag_stub(uc):
        del uc
        return eventflag_ret

    def stackchk_stub(uc):
        del uc
        raise AssertionError("__stack_chk_fail reached -- test input corrupted the canary")

    res = dh.run_original(
        SO, START, END, {"r0": a0, "r1": a1, "r2": OUT_ADDR},
        buffers=[
            dh.MemoryBuffer("canary_page", canary_page_base, bytes(canary_page)),
            dh.MemoryBuffer("main_page", main_page_base, bytes(main_page)),
            dh.MemoryBuffer("canary_var", CANARY_VAR, _pack32(0x12345678)),
            dh.MemoryBuffer("playtime", PLAYTIME_BASE, _pack32(hours) + _pack32(minutes) + _pack32(seconds)),
            dh.MemoryBuffer("array4", ARRAY4_ADDR, bytes(array4)),
            dh.MemoryBuffer("array5", ARRAY5_ADDR, bytes(array5)),
            dh.MemoryBuffer("out", OUT_ADDR, bytes(OUT_SIZE)),
            dh.MemoryBuffer("title_page", title_page_base, bytes(title_page)),
        ],
        stub_calls={
            MEMCPY_ADDR: memcpy_stub,
            MEMSET_ADDR: memset_stub,
            STACK_CHK_FAIL_ADDR: stackchk_stub,
            READ_EVENTFLAG_ADDR: eventflag_stub,
            DIVSI3_ADDR: divsi3_stub,
            IDIVMOD_ADDR: idivmod_stub,
        },
        max_instructions=200000,
    )
    return res


def run_model(lib, a0, a1, hours, minutes, seconds, eventflag_ret, array4_entry, array5_block):
    out_buf = (ctypes.c_uint8 * OUT_SIZE)()
    play_time = (ctypes.c_int32 * 3)(hours, minutes, seconds)

    idx, data20 = array4_entry
    array4 = bytearray(20 * 128)
    array4[idx * 20:idx * 20 + 20] = data20
    array4_buf = (ctypes.c_uint8 * len(array4))(*array4)

    array5 = bytearray(0x100)
    array5[0x20:0x20 + len(array5_block)] = array5_block
    array5_buf = (ctypes.c_uint8 * len(array5))(*array5)

    eventflag_cb = ctypes.CFUNCTYPE(ctypes.c_int32, ctypes.c_int32)(lambda idx_: eventflag_ret)

    lib.MakeHeader_model(a0, a1, out_buf, play_time, eventflag_cb, array4_buf, array5_buf)
    return bytes(out_buf)


CASES = [
    # (a0, a1, hours, minutes, seconds, eventflag_ret)
    (0, 0, 0, 0, 0, 0),
    (12, 34, 56, 43, 29, 3),
    (98, -1, 99, 59, 59, 0),      # exactly at every clamp boundary
    (0, 0, 150, 200, 200, 5),     # all three well past their clamps
]


class MakeHeaderDifferentialTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        cls.lib = build_model(Path(cls.temp.name) / "model.so")

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def test_matches_for_every_case(self):
        array4_entry = (3, bytes(range(1, 21)))
        array5_block = bytes(range(100, 228))
        for a0, a1, hours, minutes, seconds, eventflag_ret in CASES:
            with self.subTest(a0=a0, a1=a1, hours=hours, minutes=minutes, seconds=seconds):
                res = run_original(a0, a1, hours, minutes, seconds, eventflag_ret, array4_entry, array5_block)
                self.assertTrue(res.ok, res.error)
                model_out = run_model(self.lib, a0, a1, hours, minutes, seconds, eventflag_ret,
                                       array4_entry, array5_block)
                real_out = res.final_buffers["out"]
                self.assertEqual(real_out[:0xa0], model_out[:0xa0])
                self.assertEqual(real_out[0x80:0x100], model_out[0x80:0x100])

    def test_fault_injection_clamp_boundary_is_inclusive(self):
        # movge (>=), not movgt (>): confirm 99/59 themselves are
        # already clamped, not just values strictly above them. A
        # model using a plain `> 99`/`> 59` comparison would diverge
        # exactly at these boundary values.
        array4_entry = (0, bytes(20))
        array5_block = bytes(0x80)
        res = run_original(0, 0, hours=99, minutes=59, seconds=59,
                            eventflag_ret=0, array4_entry=array4_entry, array5_block=array5_block)
        self.assertTrue(res.ok, res.error)
        out = res.final_buffers["out"]
        # "99" and "59" and "59" -- clamped value equals the boundary itself.
        self.assertEqual(out[0x1a:0x1e], bytes([0x82, 0x58, 0x82, 0x58]))  # '9','9'
        self.assertEqual(out[0x20:0x24], bytes([0x82, 0x54, 0x82, 0x58]))  # '5','9'
        self.assertEqual(out[0x26:0x2a], bytes([0x82, 0x54, 0x82, 0x58]))  # '5','9'

    def test_fault_injection_a1_is_unused(self):
        # A model that (wrongly) assumed a1 affects the output would
        # diverge here: two runs differing only in a1 must produce
        # byte-identical headers.
        array4_entry = (0, bytes(20))
        array5_block = bytes(0x80)
        res_a = run_original(5, 111, 1, 1, 1, 0, array4_entry, array5_block)
        res_b = run_original(5, 222, 1, 1, 1, 0, array4_entry, array5_block)
        self.assertTrue(res_a.ok and res_b.ok)
        self.assertEqual(res_a.final_buffers["out"], res_b.final_buffers["out"])


if __name__ == "__main__":
    unittest.main()
