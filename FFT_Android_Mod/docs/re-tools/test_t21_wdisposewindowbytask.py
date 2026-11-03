"""T21 (RE_COMPLETUDE_TASKS.md) vertical slice: differential test of the
real Wdisposewindowbytask(int) ARM body (0xfeeb4, 112 B) against a
compiled, independent C reimplementation
(c-models/t21_wdisposewindowbytask.c).

No `bl` -- fully self-contained, confirmed by jtable.py. The global
struct/array is built as real memory at the ELF's own PC-relative
resolved address (resolved by hand -- see NOTES sec. 685), same
technique as test_t23_addlocalprim2.c but without any GOT
indirection (a direct literal, confirmed to resolve to the same base
for both the tracker fields and the slot array).
"""
import ctypes
import subprocess
import tempfile
import unittest
from pathlib import Path

import differential_harness as dh

DIR = Path(__file__).resolve().parent
SO = DIR.parents[1] / "src/lib/armeabi/libgl2jni.so"
START, END = 0xfeeb4, 0xfeeb4 + 112

# Real global struct/array base, resolved by hand from the direct
# PC-relative literal at 0xfeeb4 (no GOT indirection -- a local/
# static data symbol, confirmed to resolve to the same address for
# both the tracker fields and the slot array). The real function
# hardcodes this address; it is not passed in through any register,
# so the test buffer must sit exactly here, not at an arbitrary
# chosen address (same lesson as test_t23_addlocalprim2.py's InitCamera).
BASE_ADDR = 0x4711fc
BASE_SIZE = 0x1000
STRIDE = 0x1c0

TRACKER_OFFSETS = {0: 0x5e8, 2: 0x968, 4: 0xce8}


def build_model(output: Path):
    subprocess.run(
        ["cc", "-std=c11", "-O2", "-Wall", "-Wextra", "-Werror", "-pedantic",
         "-shared", "-fPIC", str(DIR / "c-models/t21_wdisposewindowbytask.c"),
         "-o", str(output)],
        check=True, capture_output=True,
    )
    lib = ctypes.CDLL(str(output))
    fn = lib.Wdisposewindowbytask_model
    fn.argtypes = [ctypes.c_int32, ctypes.c_void_p]
    fn.restype = None
    return lib


def _pack32(value: int) -> bytes:
    return (value & 0xffffffff).to_bytes(4, "little")


def _sentinel_base():
    return bytes((i + 1) & 0xff or 1 for i in range(BASE_SIZE))


def _build_base(task_id, owners, field_values):
    base = bytearray(_sentinel_base())
    for slot_pair, owner in owners.items():
        base[TRACKER_OFFSETS[slot_pair]:TRACKER_OFFSETS[slot_pair] + 4] = _pack32(owner)
    for slot, value in field_values.items():
        off = slot * STRIDE + 0x5e4
        base[off:off + 4] = _pack32(value)
    return bytes(base)


def run_original(task_id, owners, field_values):
    base = _build_base(task_id, owners, field_values)
    res = dh.run_original(
        SO, START, END, {"r0": task_id},
        buffers=[dh.MemoryBuffer("base", BASE_ADDR, base)],
    )
    return res


def run_model(lib, task_id, owners, field_values):
    base = bytearray(_build_base(task_id, owners, field_values))
    base_buf = (ctypes.c_uint8 * BASE_SIZE)(*base)
    lib.Wdisposewindowbytask_model(task_id, base_buf)
    return bytes(base_buf)


CASES = [
    # (task_id, owners={slot_pair: owner_task_id}, field_values={slot: nonzero sentinel})
    (42, {0: 42, 2: 99, 4: 77}, {0: 0x11111111, 1: 0x22222222, 2: 0x33333333, 3: 0x44444444}),
    (99, {0: 42, 2: 99, 4: 77}, {0: 0x11111111, 1: 0x22222222, 2: 0x33333333, 3: 0x44444444}),
    (77, {0: 42, 2: 99, 4: 77}, {4: 0x55555555, 5: 0x66666666}),
    (1234, {0: 42, 2: 99, 4: 77}, {}),  # matches none -> no-op
]


class WdisposewindowbytaskDifferentialTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        cls.lib = build_model(Path(cls.temp.name) / "model.so")

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def test_matches_for_every_case(self):
        for task_id, owners, field_values in CASES:
            with self.subTest(task_id=task_id):
                res = run_original(task_id, owners, field_values)
                self.assertTrue(res.ok, res.error)
                model_base = run_model(self.lib, task_id, owners, field_values)

                self.assertEqual(res.final_buffers["base"], model_base)

    def test_fault_injection_no_match_is_a_true_no_op(self):
        # A model that defaulted to clearing slot pair 0 when no
        # tracker matched (instead of returning immediately) would
        # diverge from the real ELF, which leaves everything
        # untouched -- confirmed via the real `bxne lr`.
        task_id = 555
        owners = {0: 1, 2: 2, 4: 3}
        field_values = {0: 0xaaaaaaaa, 1: 0xbbbbbbbb}
        res = run_original(task_id, owners, field_values)
        self.assertTrue(res.ok, res.error)
        expected = _build_base(task_id, owners, field_values)
        self.assertEqual(res.final_buffers["base"], expected)

    def test_fault_injection_both_slots_of_the_pair_are_cleared(self):
        # A model that only cleared ONE of the two paired slots would
        # diverge: both slot_pair and slot_pair+1 must be zeroed.
        task_id = 42
        owners = {0: 42, 2: 99, 4: 77}
        field_values = {0: 0x11111111, 1: 0x22222222}
        res = run_original(task_id, owners, field_values)
        self.assertTrue(res.ok, res.error)
        base = res.final_buffers["base"]
        self.assertEqual(base[0x5e4:0x5e8], bytes(4))
        self.assertEqual(base[0x5e4 + STRIDE:0x5e8 + STRIDE], bytes(4))


if __name__ == "__main__":
    unittest.main()
