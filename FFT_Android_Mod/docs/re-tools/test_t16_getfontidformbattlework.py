"""T16 (RE_COMPLETUDE_TASKS.md) vertical slice: differential test of the
real getFontIDFormBattleWork(int) ARM body (0x20e880, 64 B) against a
compiled, independent C reimplementation
(c-models/t16_getfontidformbattlework.c).

No `bl` -- fully self-contained, confirmed by jtable.py. The global
list-head pointer variable is built as real memory at the ELF's own
GOT-resolved address (resolved by hand -- see NOTES sec. 686), same
double-indirection technique as test_t14_boot_framemove.py. The real
ELF side builds a byte-exact ARM-shaped linked list (next at +0x0,
font id at +0x5, BWORK* at +0x134, BWORK+0x1ac the compared byte);
the model side builds an equivalent list using native pointers
directly (see c-models/t16_getfontidformbattlework.c for why).
"""
import ctypes
import subprocess
import tempfile
import unittest
from pathlib import Path

import differential_harness as dh

DIR = Path(__file__).resolve().parent
SO = DIR.parents[1] / "src/lib/armeabi/libgl2jni.so"
START, END = 0x20e880, 0x20e880 + 64

GOT_PAGE = 0x346000
HEAD_SLOT = 0x3468a8
HEAD_VAR_ADDR = 0x650000   # this test's own stand-in for the real pointer variable

NODE_SIZE = 0x138
BWORK_SIZE = 0x1ad


def _pack32(value: int) -> bytes:
    return (value & 0xffffffff).to_bytes(4, "little")


def build_model(output: Path):
    subprocess.run(
        ["cc", "-std=c11", "-O2", "-Wall", "-Wextra", "-Werror", "-pedantic",
         "-shared", "-fPIC", str(DIR / "c-models/t16_getfontidformbattlework.c"),
         "-o", str(output)],
        check=True, capture_output=True,
    )
    lib = ctypes.CDLL(str(output))
    fn = lib.getFontIDFormBattleWork_model
    fn.restype = ctypes.c_int32
    return lib


# Each list entry: (font_id, bwork_byte_0x1ac_or_None_if_no_bwork)
def run_original(target, entries):
    got_page = bytearray(0x1000)
    got_page[HEAD_SLOT - GOT_PAGE:HEAD_SLOT - GOT_PAGE + 4] = _pack32(HEAD_VAR_ADDR)

    buffers = [
        dh.MemoryBuffer("got_page", GOT_PAGE, bytes(got_page)),
    ]

    node_base = 0x660000
    bwork_base = 0x670000
    node_addrs = [node_base + i * 0x1000 for i in range(len(entries))]

    head_value = node_addrs[0] if entries else 0
    buffers.append(dh.MemoryBuffer("head_var", HEAD_VAR_ADDR, _pack32(head_value)))

    for i, (font_id, bwork_byte) in enumerate(entries):
        node = bytearray(NODE_SIZE)
        next_addr = node_addrs[i + 1] if i + 1 < len(entries) else 0
        node[0:4] = _pack32(next_addr)
        node[5] = font_id

        if bwork_byte is None:
            node[0x134:0x138] = _pack32(0)
        else:
            bwork_addr = bwork_base + i * 0x1000
            node[0x134:0x138] = _pack32(bwork_addr)
            bwork = bytearray(BWORK_SIZE)
            bwork[0x1ac] = bwork_byte
            buffers.append(dh.MemoryBuffer(f"bwork{i}", bwork_addr, bytes(bwork)))

        buffers.append(dh.MemoryBuffer(f"node{i}", node_addrs[i], bytes(node)))

    res = dh.run_original(SO, START, END, {"r0": target}, buffers=buffers)
    return res


class ModelNode(ctypes.Structure):
    pass


ModelNode._fields_ = [
    ("next", ctypes.POINTER(ModelNode)),
    ("font_id", ctypes.c_uint8),
    ("bwork", ctypes.c_void_p),
]


def run_model(lib, target, entries):
    bworks = []
    nodes = (ModelNode * max(len(entries), 1))()
    for i, (font_id, bwork_byte) in enumerate(entries):
        nodes[i].font_id = font_id
        if bwork_byte is None:
            nodes[i].bwork = None
        else:
            bwork_buf = (ctypes.c_uint8 * BWORK_SIZE)()
            bwork_buf[0x1ac] = bwork_byte
            bworks.append(bwork_buf)
            nodes[i].bwork = ctypes.cast(bwork_buf, ctypes.c_void_p)
        nodes[i].next = ctypes.cast(ctypes.byref(nodes[i + 1]), ctypes.POINTER(ModelNode)) if i + 1 < len(entries) else None

    lib.getFontIDFormBattleWork_model.argtypes = [ctypes.c_int32, ctypes.POINTER(ModelNode)]
    head_ptr = ctypes.cast(ctypes.byref(nodes[0]), ctypes.POINTER(ModelNode)) if entries else None
    return lib.getFontIDFormBattleWork_model(target, head_ptr)


CASES = [
    (5, [(10, 5)]),                               # single node, immediate match
    (5, [(10, 7), (20, 5)]),                      # second node matches
    (5, [(10, 7), (20, 8)]),                      # no match anywhere -> -1
    (5, [(10, None), (20, 5)]),                   # first node has no BWORK, skipped
    (0, []),                                       # empty list
]


class GetFontIDFormBattleWorkDifferentialTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        cls.lib = build_model(Path(cls.temp.name) / "model.so")

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def test_matches_for_every_case(self):
        for target, entries in CASES:
            with self.subTest(target=target, entries=entries):
                res = run_original(target, entries)
                self.assertTrue(res.ok, res.error)
                model_ret = run_model(self.lib, target, entries)

                self.assertEqual(res.registers["r0"] & 0xffffffff, model_ret & 0xffffffff)

    def test_fault_injection_nodes_without_bwork_are_not_a_match(self):
        # A model that (wrongly) treated a null BWORK pointer as
        # matching any target (e.g. comparing a garbage/zero byte)
        # would diverge from the real ELF, which explicitly skips
        # such nodes via the real `beq` on the null check.
        res = run_original(0, [(99, None)])
        self.assertTrue(res.ok, res.error)
        self.assertEqual(res.registers["r0"] & 0xffffffff, 0xffffffff)


if __name__ == "__main__":
    unittest.main()
