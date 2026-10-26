"""Pure ISA oracle regression tests for normal ARM/Thumb BX LR transitions."""
import unittest
import arm_bx_reference as arm


class ArmBXReferenceTests(unittest.TestCase):
    def test_all_nzcv_combinations_and_interworking(self):
        for nzcv in range(16):
            initial = 0x10 | (nzcv << 28)
            target, cpsr = arm.branch_exchange_lr(arm.ENCODING, 0x710100, initial)
            self.assertEqual((target, cpsr), (0x710100, initial))
            target, cpsr = arm.branch_exchange_lr(arm.ENCODING, 0x710101, initial)
            self.assertEqual((target, cpsr), (0x710100, initial | arm.THUMB_BIT))

    def test_invalid_preconditions_rejected(self):
        invalid = (
            (b"\x00\x00\x00\x00", 0x710100, 0x10),
            (arm.ENCODING, 0x710102, 0x10),
            (arm.ENCODING, 0x710100, 0x30),
            (arm.ENCODING, 0x710100, 0x00),
            (arm.ENCODING, -1, 0x10),
            (arm.ENCODING, 0x710100, -1),
        )
        for word, lr, cpsr in invalid:
            with self.subTest(lr=lr, cpsr=cpsr):
                with self.assertRaises(ValueError):
                    arm.branch_exchange_lr(word, lr, cpsr)


if __name__ == "__main__":
    unittest.main()
