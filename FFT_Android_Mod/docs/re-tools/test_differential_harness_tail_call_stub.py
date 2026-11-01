"""differential_harness.py: a stub whose return (via LR) lands exactly
on RETURN_SENTINEL -- i.e. the stubbed call is itself a tail call, the
last thing the function does before returning to ITS OWN caller -- must
be caught immediately, not after one more (garbage) instruction
executes at the sentinel page.

Found while building the T20 iOSUnitListWinOnOff slice: that function
does `pop {r4, lr}; b other_function` on one path -- a real ARM tail
call, not a bl. Before this fix, the harness's sentinel check only ran
right after emu_start, but the stub path writes PC directly outside of
emu_start, so the next loop iteration executed one instruction at the
zeroed sentinel page (decodes as `andeq r0, r0, r0`, a 4-byte no-op)
before the top-of-loop check ever saw the sentinel -- landing on
RETURN_SENTINEL+4 and reporting "no stub" for THAT address instead.
"""
import unittest
from pathlib import Path

import elf_test_fixture
import differential_harness as dh

# push {r4, lr}; b external_target  (ARM tail call: no bl, pop then plain branch)
# external_target is placed far outside this tiny function's own range,
# the same situation as the real binary.
PUSH_R4_LR = bytes.fromhex("10402de9")  # push {r4, lr}
POP_R4_LR = bytes.fromhex("1040bde8")   # pop {r4, lr}


def _b(from_addr: int, to_addr: int) -> bytes:
    import struct
    offset = (to_addr - (from_addr + 8)) >> 2
    return struct.pack("<I", 0xEA000000 | (offset & 0xFFFFFF))


class TailCallStubTests(unittest.TestCase):
    def test_tail_call_whose_lr_is_the_sentinel_is_caught_immediately(self):
        base = elf_test_fixture.TEXT_VADDR
        target = base + 0x1000  # a real address far from [base, base+len(body))
        body = PUSH_R4_LR + POP_R4_LR + _b(base + 8, target)
        data = elf_test_fixture.build_elf(body)
        import tempfile
        f = tempfile.NamedTemporaryFile(suffix=".so", delete=False)
        f.write(data)
        f.close()
        self.addCleanup(lambda: Path(f.name).unlink(missing_ok=True))

        # The target's own page must be mapped (as it would be in a real
        # binary, where "external" functions still live in mapped
        # memory) -- Unicorn's branch handling touches the destination
        # page even for a single-stepped `count=1` call, independent of
        # the bug this test targets.
        res = dh.run_original(Path(f.name), base, base + len(body),
                               {}, [dh.MemoryBuffer("target_page", target & ~0xfff, bytes(0x1000))],
                               stub_calls={target: 0x77777777})
        self.assertTrue(res.ok, res.error)
        self.assertEqual(res.registers["r0"], 0x77777777)


if __name__ == "__main__":
    unittest.main()
