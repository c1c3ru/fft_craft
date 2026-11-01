"""T26 (RE_COMPLETUDE_TASKS.md) vertical slice: differential test of the
real pspNetPadRead() ARM body (0x28e5e0, via the T10 harness, using the
callable-stub extension added for this slice) against a compiled,
independent C reimplementation (c-models/t26_pspnetpadread.c).

xpPadKeyBufGet (0x2a2a4c), iOSTutoCheck (0x26d798), iOS_getTutorialPad
(0x2b7c44) are stubbed on both sides. The first real run against the
ELF, without modeling xpPadKeyBufGet's double indirection, faulted on
an unmapped read -- that failure is what revealed the real signature,
documented in NOTES sec. 663. This test keeps that double indirection
explicit instead of hiding it behind a convenience helper.
"""
import ctypes
import subprocess
import tempfile
import unittest
from pathlib import Path

import differential_harness as dh
from unicorn.arm_const import UC_ARM_REG_R0

DIR = Path(__file__).resolve().parent
SO = DIR.parents[1] / "src/lib/armeabi/libgl2jni.so"
START, END = 0x28e5e0, 0x28e5e0 + 140

PADMASK_ADDR = 0xfd9b08
PTR0, PTR1 = 0x600000, 0x600010
DATA0, DATA1 = 0x610000, 0x620000


def build_model(output: Path):
    subprocess.run(
        ["cc", "-std=c11", "-O2", "-Wall", "-Wextra", "-Werror", "-pedantic",
         "-shared", "-fPIC", str(DIR / "c-models/t26_pspnetpadread.c"),
         "-o", str(output)],
        check=True, capture_output=True,
    )
    lib = ctypes.CDLL(str(output))
    fn = lib.pspNetPadRead_model
    fn.argtypes = [ctypes.POINTER(ctypes.c_uint32)] + [ctypes.c_void_p] * 3
    fn.restype = ctypes.c_uint32
    return lib


def run_model(lib, data0, data1, pad_mask, tuto_active, tuto_pad):
    buf0 = (ctypes.c_uint8 * len(data0)).from_buffer_copy(data0)
    buf1 = (ctypes.c_uint8 * len(data1)).from_buffer_copy(data1)
    ptr0 = ctypes.cast(buf0, ctypes.POINTER(ctypes.c_uint8))
    ptr1 = ctypes.cast(buf1, ctypes.POINTER(ctypes.c_uint8))
    slots = [ptr0, ptr1]

    get_fn = ctypes.CFUNCTYPE(ctypes.c_void_p, ctypes.c_int32)(
        lambda which: ctypes.cast(ctypes.pointer(slots[which]), ctypes.c_void_p).value)
    tuto_check = ctypes.CFUNCTYPE(ctypes.c_int32)(lambda: tuto_active)
    tuto_pad_fn = ctypes.CFUNCTYPE(ctypes.c_int32)(lambda: tuto_pad)

    mask = ctypes.c_uint32(pad_mask)
    ret = lib.pspNetPadRead_model(
        ctypes.byref(mask),
        ctypes.cast(get_fn, ctypes.c_void_p),
        ctypes.cast(tuto_check, ctypes.c_void_p),
        ctypes.cast(tuto_pad_fn, ctypes.c_void_p))
    return ret & 0xffffffff, mask.value


def run_original(data0, data1, pad_mask, tuto_active, tuto_pad):
    def pad_getter(uc):
        return PTR0 if uc.reg_read(UC_ARM_REG_R0) == 0 else PTR1

    off = PADMASK_ADDR - (PADMASK_ADDR & ~0xfff)
    padmask_page = bytearray(0x1000)
    padmask_page[off:off + 4] = (pad_mask & 0xffffffff).to_bytes(4, "little")
    ptr_page = bytearray(0x1000)
    ptr_page[0:4] = DATA0.to_bytes(4, "little")
    ptr_page[0x10:0x14] = DATA1.to_bytes(4, "little")
    return dh.run_original(
        SO, START, END, {},
        buffers=[
            dh.MemoryBuffer("ptrs", 0x600000, bytes(ptr_page)),
            dh.MemoryBuffer("data0", DATA0, data0),
            dh.MemoryBuffer("data1", DATA1, data1),
            dh.MemoryBuffer("padmaskpage", PADMASK_ADDR & ~0xfff, bytes(padmask_page)),
        ],
        stub_calls={0x2a2a4c: pad_getter, 0x26d798: tuto_active, 0x2b7c44: tuto_pad},
    )


CASES = [
    (bytes([0, 0, 0x12, 0x34, 0, 0, 0, 0]), bytes([0, 0, 0x56, 0x78, 0, 0, 0, 0]), 0, 0, 0),
    (bytes([0, 0, 0x12, 0x34, 0, 0, 0, 0]), bytes([0, 0, 0x56, 0x78, 0, 0, 0, 0]), 0, 1, 0),
    (bytes([0, 0, 0x12, 0x34, 0, 0, 0, 0]), bytes([0, 0, 0x56, 0x78, 0, 0, 0, 0]), 0, 1, 0x04000000),
    (bytes([0, 0, 0x12, 0x34, 0, 0, 0, 0]), bytes([0, 0, 0x56, 0x78, 0, 0, 0, 0]), 0xffff, 0, 0),
    (bytes(8), bytes(8), 0, 0, 0),
    (bytes([0, 0, 0xff, 0xff, 0, 0, 0, 0]), bytes([0, 0, 0xff, 0xff, 0, 0, 0, 0]), 0xffffffff, 0, 0),
]


class PspNetPadReadDifferentialTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        cls.lib = build_model(Path(cls.temp.name) / "model.so")

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def test_matches_for_every_case(self):
        for data0, data1, pad_mask, tuto_active, tuto_pad in CASES:
            with self.subTest(pad_mask=pad_mask, tuto_active=tuto_active, tuto_pad=tuto_pad):
                res = run_original(data0, data1, pad_mask, tuto_active, tuto_pad)
                self.assertTrue(res.ok, res.error)
                ret, _ = run_model(self.lib, data0, data1, pad_mask, tuto_active, tuto_pad)
                self.assertEqual(res.registers["r0"] & 0xffffffff, ret)

    def test_fault_injection_missing_double_indirection_is_detected(self):
        # The naive (wrong) reading -- treating xpPadKeyBufGet's return
        # value as the buffer itself, skipping the extra dereference
        # that NOTES sec. 663 found by first getting this wrong -- would
        # read the button bytes from PTR0/PTR1 (which hold a pointer
        # value, 0x00610000 / 0x00620000) instead of from DATA0/DATA1.
        # Confirm that naive interpretation's bytes differ from the real
        # data bytes, so a model built on it would disagree with the ELF.
        data0 = bytes([0, 0, 0x12, 0x34, 0, 0, 0, 0])
        data1 = bytes([0, 0, 0x56, 0x78, 0, 0, 0, 0])
        res = run_original(data0, data1, 0, 0, 0)
        self.assertTrue(res.ok, res.error)
        correct = res.registers["r0"] & 0xffffffff

        ptr_page = bytearray(0x1000)
        ptr_page[0:4] = DATA0.to_bytes(4, "little")
        ptr_page[0x10:4 + 0x10] = DATA1.to_bytes(4, "little")
        naive_v0 = ptr_page[3] | (ptr_page[2] << 8)       # bytes of PTR0 itself, not *PTR0
        naive_v1 = ptr_page[0x13] | (ptr_page[0x12] << 8)  # bytes of PTR1 itself, not *PTR1
        naive_wrong = 0xFFFFFFFF & ~(naive_v0 | (naive_v1 << 16))
        self.assertNotEqual(correct, naive_wrong,
                             "fault-injection case stopped being a real divergence")


if __name__ == "__main__":
    unittest.main()
