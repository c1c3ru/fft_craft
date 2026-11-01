"""differential_harness.py: stub_calls now accepts a callable, so a real
address called more than once with different input registers (e.g. a
"get buffer N" getter called for N=0 then N=1) can return a different
value each time -- added while building the T26 pspNetPadRead slice,
which calls the same getter twice with r0=0 then r0=1.
"""
import struct
import tempfile
import unittest
from pathlib import Path

import elf_test_fixture
import differential_harness as dh
from unicorn.arm_const import UC_ARM_REG_R0


def _bl(from_addr: int, to_addr: int) -> bytes:
    offset = (to_addr - (from_addr + 8)) >> 2
    return struct.pack("<I", 0xEB000000 | (offset & 0xFFFFFF))


class StubCallableTests(unittest.TestCase):
    def _write(self, text_bytes: bytes) -> str:
        data = elf_test_fixture.build_elf(text_bytes)
        f = tempfile.NamedTemporaryFile(suffix=".so", delete=False)
        f.write(data)
        f.close()
        self.addCleanup(lambda: Path(f.name).unlink(missing_ok=True))
        return f.name

    def test_fixed_int_stub_still_works(self):
        # A realistic shape: push {lr} to preserve the caller's return
        # address around the bl, pop {pc} to actually return to it --
        # without this, bl's own LR clobber has nothing to restore.
        base = elf_test_fixture.TEXT_VADDR
        target = base + 0x100
        body = b"".join([
            bytes.fromhex("00402de9"),  # push {lr}
            _bl(base + 4, target),       # bl target
            bytes.fromhex("0080bde8"),  # pop {pc}
        ])
        path = self._write(body)
        res = dh.run_original(Path(path), base, base + len(body), {}, [],
                               stub_calls={target: 7})
        self.assertTrue(res.ok, res.error)
        self.assertEqual(res.registers["r0"], 7)

    def test_callable_stub_sees_call_specific_r0(self):
        seen = []

        def getter(uc):
            r0 = uc.reg_read(UC_ARM_REG_R0)
            seen.append(r0)
            return {0: 0x100, 1: 0x200}[r0]

        base = elf_test_fixture.TEXT_VADDR
        target = base + 0x100
        body = b"".join([
            bytes.fromhex("10402de9"),        # push {r4, lr}
            bytes.fromhex("0000a0e3"),        # mov r0, #0
            _bl(base + 8, target),             # bl target
            bytes.fromhex("0040a0e1"),        # mov r4, r0
            bytes.fromhex("0100a0e3"),        # mov r0, #1
            _bl(base + 20, target),            # bl target
            bytes.fromhex("004084e1"),        # orr r4, r4, r0
            bytes.fromhex("0400a0e1"),        # mov r0, r4
            bytes.fromhex("1080bde8"),        # pop {r4, pc}
        ])
        path = self._write(body)
        res = dh.run_original(Path(path), base, base + len(body), {}, [],
                               stub_calls={target: getter})
        self.assertTrue(res.ok, res.error)
        self.assertEqual(seen, [0, 1])
        self.assertEqual(res.registers["r0"], 0x100 | 0x200)


if __name__ == "__main__":
    unittest.main()
