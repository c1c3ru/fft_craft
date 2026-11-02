"""T08 (RE_COMPLETUDE_TASKS.md) vertical slice: differential test of the
real DisposeObject(short, _Object*) ARM body (0x22599c, 196 B) against
a compiled, independent C reimplementation
(c-models/t08_disposeobject.c).

Free (0x22541c) and DisposeEffectAnimation (0x217f5c) are stubbed via
callables recording their argument. The per-table-slot array base,
the live-object counter and the free-list head are built as real
memory at the ELF's own GOT-resolved addresses (resolved by hand --
see NOTES sec. 677), same technique as test_t14_boot_framemove.py.

The final "free_list_head becomes obj's own address" write is NOT
compared as a raw number across the real ELF side and the model side
(a real ARM address and a ctypes-allocated host address are not the
same kind of value) -- each side is checked against its OWN obj
address instead. Every other effect is compared by exact bytes.
"""
import ctypes
import subprocess
import tempfile
import unittest
from pathlib import Path

import differential_harness as dh

DIR = Path(__file__).resolve().parent
SO = DIR.parents[1] / "src/lib/armeabi/libgl2jni.so"
START, END = 0x22599c, 0x22599c + 196

FREE_ADDR = 0x22541c
DISPOSE_EFFECT_ANIM_ADDR = 0x217f5c

GOT_PAGE = 0x347000
TABLE_SLOT = 0x3477f8
COUNT_SLOT = 0x34787c
FREE_HEAD_SLOT = 0x347870

TABLE_BASE = 0x660000
OBJ_COUNT_ADDR = 0x670000
FREE_HEAD_ADDR = 0x680000
OBJ_ADDR = 0x600000
NEXT_ADDR = 0x610000
PREV_ADDR = 0x620000

TABLE_ID = 2
STRIDE = 0xf8
OBJ_SIZE = 0x60
NEIGHBOR_SIZE = 0x10


def build_model(output: Path):
    subprocess.run(
        ["cc", "-std=c11", "-O2", "-Wall", "-Wextra", "-Werror", "-pedantic",
         "-shared", "-fPIC", str(DIR / "c-models/t08_disposeobject.c"),
         "-o", str(output)],
        check=True, capture_output=True,
    )
    lib = ctypes.CDLL(str(output))
    fn = lib.DisposeObject_model
    fn.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p,
                   ctypes.POINTER(ctypes.c_int32), ctypes.POINTER(ctypes.c_uint32),
                   ctypes.c_void_p, ctypes.c_void_p]
    fn.restype = None
    return lib


def _pack32(value: int) -> bytes:
    return (value & 0xffffffff).to_bytes(4, "little")


def _pack16(value: int) -> bytes:
    return (value & 0xffff).to_bytes(2, "little")


def _build_obj_bytes(prev, next_, category, payload):
    obj = bytearray(OBJ_SIZE)
    obj[0x00:0x04] = _pack32(prev)
    obj[0x04:0x08] = _pack32(next_)
    obj[0x4c:0x4e] = _pack16(category)
    obj[0x54:0x58] = _pack32(payload)
    return bytes(obj)


def run_original(prev, next_, category, payload, count, old_head, callee_expected):
    got_page = bytearray(0x1000)
    got_page[TABLE_SLOT - GOT_PAGE:TABLE_SLOT - GOT_PAGE + 4] = _pack32(TABLE_BASE)
    got_page[COUNT_SLOT - GOT_PAGE:COUNT_SLOT - GOT_PAGE + 4] = _pack32(OBJ_COUNT_ADDR)
    got_page[FREE_HEAD_SLOT - GOT_PAGE:FREE_HEAD_SLOT - GOT_PAGE + 4] = _pack32(FREE_HEAD_ADDR)

    table = bytearray(STRIDE * (TABLE_ID + 1))
    off = TABLE_ID * STRIDE
    table[off + 0x1c:off + 0x1e] = _pack16(count)

    obj_bytes = _build_obj_bytes(prev, next_, category, payload)
    next_bytes = bytes(NEIGHBOR_SIZE)
    prev_bytes = bytes(NEIGHBOR_SIZE)

    calls = {"free": None, "dispose": None}

    def free_stub(uc):
        from unicorn.arm_const import UC_ARM_REG_R0
        calls["free"] = uc.reg_read(UC_ARM_REG_R0)
        return 0

    def dispose_stub(uc):
        from unicorn.arm_const import UC_ARM_REG_R0
        calls["dispose"] = uc.reg_read(UC_ARM_REG_R0)
        return 0

    res = dh.run_original(
        SO, START, END, {"r0": TABLE_ID, "r1": OBJ_ADDR},
        buffers=[
            dh.MemoryBuffer("got_page", GOT_PAGE, bytes(got_page)),
            dh.MemoryBuffer("table", TABLE_BASE, bytes(table)),
            dh.MemoryBuffer("obj", OBJ_ADDR, obj_bytes),
            dh.MemoryBuffer("next", NEXT_ADDR, next_bytes),
            dh.MemoryBuffer("prev", PREV_ADDR, prev_bytes),
            dh.MemoryBuffer("obj_count", OBJ_COUNT_ADDR, _pack32(count + 100)),
            dh.MemoryBuffer("free_head", FREE_HEAD_ADDR, _pack32(old_head)),
        ],
        stub_calls={FREE_ADDR: free_stub, DISPOSE_EFFECT_ANIM_ADDR: dispose_stub},
    )
    return res, off, calls


def run_model(lib, prev, next_, category, payload, count, old_head):
    obj_buf = (ctypes.c_uint8 * OBJ_SIZE)(*_build_obj_bytes(prev, next_, category, payload))
    next_buf = (ctypes.c_uint8 * NEIGHBOR_SIZE)()
    prev_buf = (ctypes.c_uint8 * NEIGHBOR_SIZE)()
    table_buf = (ctypes.c_uint8 * STRIDE)()
    table_buf[0x1c:0x1e] = (ctypes.c_uint8 * 2)(*_pack16(count))

    obj_count = ctypes.c_int32(count + 100)
    free_head = ctypes.c_uint32(old_head)

    calls = {"free": None, "dispose": None}
    free_cb = ctypes.CFUNCTYPE(None, ctypes.c_void_p)(
        lambda ptr: calls.__setitem__("free", ctypes.cast(ptr, ctypes.c_void_p).value or 0))
    dispose_cb = ctypes.CFUNCTYPE(None, ctypes.c_void_p)(
        lambda ptr: calls.__setitem__("dispose", ctypes.cast(ptr, ctypes.c_void_p).value or 0))

    next_ptr = ctypes.cast(next_buf, ctypes.c_void_p) if next_ else None
    prev_ptr = ctypes.cast(prev_buf, ctypes.c_void_p) if prev else None

    lib.DisposeObject_model(
        obj_buf, next_ptr, prev_ptr, table_buf,
        ctypes.byref(obj_count), ctypes.byref(free_head), free_cb, dispose_cb)

    return {
        "obj": bytes(obj_buf), "next": bytes(next_buf), "prev": bytes(prev_buf),
        "table": bytes(table_buf), "obj_count": obj_count.value, "free_head": free_head.value,
        "calls": calls, "obj_addr": ctypes.addressof(obj_buf),
    }


CASES = [
    # (prev, next, category, payload, count, old_head, expects)
    (0, 0, 0x0000, 0xAAAA0001, 5, 0x11111111, "dispose"),
    (0, NEXT_ADDR, 0x1000, 0xAAAA0002, 3, 0x22222222, "dispose"),
    (PREV_ADDR, 0, 0x2000, 0xAAAA0003, 1, 0x33333333, "dispose"),
    (0, 0, 0x3000, 0xAAAA0004, 9, 0x44444444, "dispose"),
    (0, 0, 0x4000, 0xAAAA0005, 2, 0x55555555, "free"),
    (0, 0, 0x5000, 0xAAAA0006, 4, 0x66666666, None),
]


class DisposeObjectDifferentialTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        cls.lib = build_model(Path(cls.temp.name) / "model.so")

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def test_matches_for_every_case(self):
        for prev, next_, category, payload, count, old_head, expects in CASES:
            with self.subTest(prev=prev, next=next_, category=hex(category)):
                res, off, orig_calls = run_original(prev, next_, category, payload, count, old_head, expects)
                self.assertTrue(res.ok, res.error)
                model = run_model(self.lib, prev, next_, category, payload, count, old_head)

                self.assertEqual(res.final_buffers["next"], model["next"])
                self.assertEqual(res.final_buffers["prev"], model["prev"])
                table_slice_real = res.final_buffers["table"][off:off + STRIDE]
                self.assertEqual(table_slice_real, model["table"])
                self.assertEqual(res.final_buffers["obj_count"], _pack32(model["obj_count"]))

                real_obj = res.final_buffers["obj"]
                self.assertEqual(real_obj[0x04:0x08], model["obj"][0x04:0x08])

                if expects == "free":
                    self.assertEqual(orig_calls["free"] & 0xffffffff, payload & 0xffffffff)
                    self.assertEqual(model["calls"]["free"] & 0xffffffff, payload & 0xffffffff)
                    self.assertIsNone(orig_calls["dispose"])
                    self.assertIsNone(model["calls"]["dispose"])
                elif expects == "dispose":
                    self.assertEqual(orig_calls["dispose"] & 0xffffffff, payload & 0xffffffff)
                    self.assertEqual(model["calls"]["dispose"] & 0xffffffff, payload & 0xffffffff)
                    self.assertIsNone(orig_calls["free"])
                    self.assertIsNone(model["calls"]["free"])
                else:
                    self.assertIsNone(orig_calls["free"])
                    self.assertIsNone(orig_calls["dispose"])
                    self.assertIsNone(model["calls"]["free"])
                    self.assertIsNone(model["calls"]["dispose"])

                # free_list_head: each side becomes ITS OWN obj address,
                # not a cross-side-comparable number (see module docstring).
                self.assertEqual(int.from_bytes(res.final_buffers["free_head"], "little"), OBJ_ADDR)
                self.assertEqual(model["free_head"] & 0xffffffff, model["obj_addr"] & 0xffffffff)

    def test_fault_injection_table_head_write_depends_on_prev_not_next(self):
        # A model that (wrongly) wrote the table head whenever `next`
        # was absent (instead of when `prev` is absent) would diverge
        # on this case: next=0 (no next object) but prev IS present,
        # so the table head (+0xd0) must stay untouched (zero) and
        # prev->next (+0x4) must receive obj->next's actual value (0
        # here, which is still a real, deliberate write, not a sign
        # that nothing happened).
        res, off, _calls = run_original(PREV_ADDR, 0, 0x5000, 0, 1, 0, None)
        self.assertTrue(res.ok, res.error)
        table_entry = res.final_buffers["table"][off:off + STRIDE]
        self.assertEqual(table_entry[0xd0:0xd4], bytes(4))
        self.assertEqual(res.final_buffers["prev"][0x4:0x8], bytes(4))

        # Contrast: same case but obj->next is a nonzero (mapped)
        # value -- it must propagate into prev->next, not get lost or
        # replaced by the table-head-write path.
        res2, _off2, _calls2 = run_original(PREV_ADDR, NEXT_ADDR, 0x5000, 0, 1, 0, None)
        self.assertTrue(res2.ok, res2.error)
        self.assertEqual(res2.final_buffers["prev"][0x4:0x8], _pack32(NEXT_ADDR))


if __name__ == "__main__":
    unittest.main()
