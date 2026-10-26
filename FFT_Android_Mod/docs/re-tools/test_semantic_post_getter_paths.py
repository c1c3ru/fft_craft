"""Original sound/icon post-getter ARM branch and register contracts."""
import unittest

import semantic_post_getter_paths as paths
import semantic_branch_microexec as branches
from test_semantic_getparam_getscale_exec import PARAM, SCALE

SOUND = bytes.fromhex(
    "e065ffeb 000050e3 0600000a 014055e2 0600003a 153100eb"
)
ICON = bytes.fromhex(
    "7ab9f7eb 18208de2 0500a0e1 14108de2 b9b9f7eb"
)
CODE = {"sound":SOUND, "icon":ICON, "param":PARAM, "scale":SCALE}


class PostGetterTests(unittest.TestCase):
    def test_exact_arm_callers(self):
        self.assertTrue(paths.validate(CODE))
        self.assertEqual(paths.SOUND_SIG[-1],("bl","#0x2bf008"))
        self.assertEqual(paths.ICON_SIG[-1],("bl","#0xa7034"))

    def test_sound_caller_has_all_three_outcomes(self):
        cases=[
            (0,0,paths.SOUND_ZERO),
            (0,1,paths.SOUND_ZERO),
            (1,0,paths.SOUND_BORROW),
            (0xFFFFFFFF,0,paths.SOUND_BORROW),
            (1,1,paths.SOUND_NEXT_BL),
            (0x12345678,43,paths.SOUND_NEXT_BL),
        ]
        for value,selector,want in cases:
            with self.subTest(value=value,selector=selector):
                r=paths.sound(CODE,value,selector,branches.CPSR_STATES[0])
                self.assertEqual(r["dest"],want)

    def test_icon_output_and_next_call_registers(self):
        for value in paths.WORDS:
            for seed in branches.CPSR_STATES:
                result=paths.icon(CODE,value,seed)
                self.assertEqual(result["dest"],paths.ICON_NEXT_BL)
                self.assertEqual(result["writes"],[(paths.STACK+0x1C,4,value)])
                self.assertEqual(result["reads"],[(paths.SOURCE+4,4)])

    def test_preseeded_nzcv_does_not_alter_decisions(self):
        for v in (0,1,0xFFFFFFFF):
            for selector in paths.SOUND_R5:
                a=paths.sound(CODE,v,selector,branches.CPSR_STATES[0])
                b=paths.sound(CODE,v,selector,branches.CPSR_STATES[1])
                self.assertEqual(a["dest"],b["dest"])
                self.assertEqual(a["trace"],b["trace"])

    def test_mutation_or_invalid_inputs_rejected(self):
        bad=dict(CODE)
        buf=bytearray(bad["icon"])
        buf[0]^=1
        bad["icon"]=bytes(buf)
        with self.assertRaisesRegex(ValueError,"opcode signature changed"):
            paths.validate(bad)
        with self.assertRaisesRegex(ValueError,"Unmodeled sound"):
            paths.sound(CODE,1,10,branches.CPSR_STATES[0])
        with self.assertRaisesRegex(ValueError,"Unmodeled icon"):
            paths.icon(CODE,123456,branches.CPSR_STATES[0])

    def test_elf_matches_exact_callers(self):
        binary=paths.semantic_evidence.ROOT/"src/lib/armeabi/libgl2jni.so"
        if not binary.is_file():
            self.skipTest("Original ELF unavailable")
        originals=paths.originals(binary)
        self.assertEqual(originals,CODE)


if __name__=="__main__":
    unittest.main()
