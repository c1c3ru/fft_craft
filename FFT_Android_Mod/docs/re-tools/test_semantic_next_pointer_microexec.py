"""Original ARM opcodes: memory read contracts before sound/icon external calls."""
import unittest
import semantic_next_pointer_microexec as current
import semantic_sound_icon_microexec as prior
import semantic_branch_microexec as branches
from test_semantic_sound_icon_microexec import ICON as ICON_PREFIX

SOUND_CODE = bytes.fromhex(
    "f0472de9 60319fe5 20d04de2 0060a0e1 0150a0e1 03009fe7 2810a0e3"
)
ICON_CODE = ICON_PREFIX + bytes.fromhex(
    "035092e7 0aa08fe0 3aad4ae2 0500a0e1"
)
SOUND_LITERAL = (0x610100 - (current.SOUND_START + 0x14 + 8)) & 0xffffffff
ICON_LITERALS = (
    (0x620100 - (current.ICON_START + 0x10 + 8)) & 0xffffffff,
    0x1000, 0, 0x2000,
)


class NextPointerTests(unittest.TestCase):
    def test_elf_arm_signatures_are_exact(self):
        self.assertEqual(len(current.exact(
            SOUND_CODE, current.SOUND_START, current.SOUND_SIG)), 7)
        self.assertEqual(len(current.exact(
            ICON_CODE, current.ICON_START, current.ICON_SIG)), 14)

    def test_sound_pointer_and_call_registers(self):
        self.assertEqual(current.sound_word_addr(SOUND_LITERAL), 0x610100)
        for value in current.POINTER_VALUES:
            for arg in current.ARGS:
                result=current.emulate_sound(
                    SOUND_CODE,SOUND_LITERAL,arg,value,branches.CPSR_STATES[0])
                self.assertEqual(result["slot"],0x610100)
                self.assertEqual(result["reads"],[
                    (current.SOUND_LITERAL_ADDR,4),(0x610100,4)])
                self.assertEqual(result["trace"][-1],current.SOUND_END)
                self.assertEqual(len(result["writes"]),8)

    def test_icon_global_read_and_stack_canary(self):
        self.assertEqual(current.icon_word_addr(ICON_LITERALS),0x620100)
        for value in current.POINTER_VALUES:
            for arg in current.ARGS:
                result=current.emulate_icon(
                    ICON_CODE,ICON_LITERALS,arg,value,branches.CPSR_STATES[1])
                self.assertEqual(result["slot"],0x620100)
                self.assertEqual(result["reads"][-1],(0x620100,4))
                self.assertEqual(len(result["writes"]),10)
                self.assertEqual(result["trace"][-1],current.ICON_END)

    def test_bad_code_and_invalid_state_fail_closed(self):
        changed=bytearray(ICON_CODE)
        changed[-1]^=1
        with self.assertRaisesRegex(ValueError, "signature changed"):
            current.emulate_icon(bytes(changed),ICON_LITERALS,1,0,
                                 branches.CPSR_STATES[0])
        with self.assertRaisesRegex(ValueError,"Invalid synthetic"):
            current.emulate_sound(SOUND_CODE,SOUND_LITERAL,3,123,
                                  branches.CPSR_STATES[0])
        with self.assertRaisesRegex(ValueError,"overlaps"):
            current.usable_slot(current.SOUND_START,{current.SOUND_START & ~0xfff})

    def test_original_elf_prefix_still_matches(self):
        elf = current.semantic_evidence.ROOT/"src/lib/armeabi/libgl2jni.so"
        if not elf.exists():
            self.skipTest("Original ELF is not in this checkout")
        sound,lit,icon,literals=current.read_original(elf)
        self.assertEqual(sound,SOUND_CODE)
        self.assertEqual(icon,ICON_CODE)
        self.assertEqual(len(literals),4)


if __name__ == "__main__":
    unittest.main()
