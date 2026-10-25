"""Regression tests for bounded ARM dispatcher and icon stack prologue."""
import unittest
from pathlib import Path
from unittest.mock import patch

import semantic_sound_icon_microexec as measured
import semantic_sound_chain as chain
import semantic_branch_microexec as branches

SOUND = bytes.fromhex("0010a0e1 0000a0e3 9dffffea")
ICON = bytes.fromhex(
    "f04f2de9 f83f9fe5 24d04de2 f4af9fe5 03308fe0 "
    "0c308de5 0c209de5 e83f9fe5 1c108de2 e49f9fe5"
)


def b_word(addr, target):
    offset = target - addr - 8
    return (0xEA000000 | ((offset >> 2) & 0xFFFFFF)).to_bytes(4, "little")


SOUND_CHAIN = {
    chain.ENTRY: (b_word(chain.ENTRY, 0x2168E0), 0x2168E0),
    0x2168E0: (b_word(0x2168E0, 0x271314), 0x271314),
    0x271314: (b_word(0x271314, measured.SOUND_ENTRY), measured.SOUND_ENTRY),
}


class SoundIconBoundaryTests(unittest.TestCase):
    def test_exact_machine_signatures(self):
        self.assertEqual(
            len(measured.disasm_exact(SOUND, measured.SOUND_ENTRY,
                                      measured.SOUND_SIGNATURE)), 3)
        self.assertEqual(
            len(measured.disasm_exact(ICON, measured.ICON_ENTRY,
                                      measured.ICON_SIGNATURE)), 10)

    def test_real_shape_sound_chain_forwards_and_sets_arguments(self):
        for arg in measured.ARGUMENTS:
            with self.subTest(arg=arg):
                r=measured.sound_execute(
                    SOUND_CHAIN, SOUND, arg, branches.CPSR_STATES[0])
                self.assertEqual(r["end"], measured.SOUND_STOP)
                self.assertEqual(len(r["trace"]), 7)

    def test_real_shape_icon_entry_preserves_stack(self):
        for arg in (0, 1, 0x34, 0xFFFFFFFF):
            literals=(0x123400, 0x567800, 0xABCDEF10, 0xDEADBEEF)
            with self.subTest(arg=arg):
                r=measured.icon_execute(
                    ICON,literals,arg,branches.CPSR_STATES[1])
                self.assertEqual(r["trace"][-1],measured.ICON_STOP)
                self.assertEqual(r["stack_bytes"],72)

    def test_cpsr_seed_does_not_change_sound_and_stack_outcomes(self):
        args=(SOUND_CHAIN,SOUND,0x34)
        a=measured.sound_execute(*args,branches.CPSR_STATES[0])
        b=measured.sound_execute(*args,branches.CPSR_STATES[1])
        self.assertEqual(a,b)
        x=measured.icon_execute(ICON,(0,0,0,0),1,
                                branches.CPSR_STATES[0])
        y=measured.icon_execute(ICON,(0,0,0,0),1,
                                branches.CPSR_STATES[1])
        self.assertEqual(x,y)

    def test_modified_opcodes_and_broken_chain_rejected(self):
        corrupted=bytearray(SOUND)
        corrupted[0]^=1
        with self.assertRaisesRegex(ValueError,"signature changed"):
            measured.sound_execute(SOUND_CHAIN,bytes(corrupted),0,
                                   branches.CPSR_STATES[0])
        corrupted=bytearray(ICON)
        corrupted[0]^=1
        with self.assertRaisesRegex(ValueError,"signature changed"):
            measured.icon_execute(bytes(corrupted),(0,0,0,0),0,
                                  branches.CPSR_STATES[0])
        bad=dict(SOUND_CHAIN)
        bad[chain.ENTRY]=(bad[chain.ENTRY][0],0x2168E4)
        with self.assertRaisesRegex(ValueError,"Changed sound"):
            measured.sound_execute(bad,SOUND,0,branches.CPSR_STATES[0])

    def test_original_elf_instructions_are_still_present(self):
        binary = measured.semantic_evidence.ROOT/"src/lib/armeabi/libgl2jni.so"
        if not binary.is_file():
            self.skipTest("Original ELF not available in test checkout")
        verified, sound, icon, literals=measured.read_original(binary)
        self.assertEqual(sound,SOUND)
        self.assertEqual(icon,ICON)
        self.assertEqual(len(verified),3)
        self.assertEqual(len(literals),4)


if __name__=="__main__":
    unittest.main()
