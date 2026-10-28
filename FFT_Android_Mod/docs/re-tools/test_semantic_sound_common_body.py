"""Original ARM 0x2b2b7c constrained common-body regression suite."""
import unittest
from unittest.mock import patch

import semantic_evidence
import semantic_sound_common_body as common
import semantic_sound_three_entry_exec as seed


class CommonSoundBodyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.binary = semantic_evidence.ROOT / "src/lib/armeabi/libgl2jni.so"
        cls.code, cls.insns = common.original(cls.binary)

    def test_binary_bound_entry_and_first_hazard(self):
        self.assertEqual(len(self.code), 128)
        self.assertEqual(self.insns[0].address, 0x2B2B7C)
        count, stop, reason = common.boundary(self.insns)
        self.assertGreaterEqual(count, 0)
        self.assertLessEqual(count, 16)
        self.assertEqual(stop, common.ENTRY + 4 * count)
        self.assertTrue(reason)

    def test_all_128_original_prefix_executions_stop_before_hazard(self):
        count, stop, _ = common.boundary(self.insns)
        samples = 0
        for arg in seed.R0_STATES:
            for nzcv in range(16):
                with self.subTest(arg=arg, nzcv=nzcv):
                    result = common.execute(self.code, self.insns, arg, nzcv)
                    self.assertEqual(result["executed_words"], count)
                    self.assertEqual(result["boundary"], stop)
                    self.assertFalse(result["fully_certified"])
                    self.assertEqual(result["trace"][-1], stop)
                    samples += 1
        self.assertEqual(samples, 128)

    def test_unapproved_state_rejected_and_no_full_function_claim(self):
        with self.assertRaisesRegex(ValueError, "Unexpected ARM sample"):
            common.execute(self.code, self.insns, 0xBADC0DE, 0)
        with self.assertRaisesRegex(ValueError, "Unexpected ARM sample"):
            common.execute(self.code, self.insns, 0, 16)
        report = common.render(self.binary)
        self.assertIn("Estados controlados verificados: 128", report)
        self.assertIn("NÃO é executada", report)
        self.assertIn("Novos certificados semânticos nesta etapa: 0", report)
        self.assertIn("0x2b2b7c", report)

    def test_wrong_elf_identity_fails_closed(self):
        with patch.object(common.hashlib, "sha256") as fake:
            fake.return_value.hexdigest.return_value = "0" * 64
            with self.assertRaisesRegex(ValueError, "identity differs"):
                common.original(self.binary)


if __name__ == "__main__":
    unittest.main()
