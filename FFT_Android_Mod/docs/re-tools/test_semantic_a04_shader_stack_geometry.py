"""Bounded, fail-closed numeric bounds for original shader locals."""
import unittest
from semantic_a04_shader_stack_geometry import boundaries

class ShaderStackTests(unittest.TestCase):
    def test_original_frame_partitions_have_metadata_capacity(self):
        b=boundaries()
        self.assertEqual(b["first_max_to_second_local"],0x10c)
        self.assertEqual(b["second_max_to_frame_end"],0x114)
        self.assertEqual(b["required_metadata_end"],0x108)
        self.assertFalse(b["real_length_and_nul_proven"])

    def test_first_partition_too_small_fails(self):
        with self.assertRaises(ValueError):
            boundaries(second=0x11b)

    def test_second_partition_too_small_fails(self):
        with self.assertRaises(ValueError):
            boundaries(frame=0x227)

    def test_invalid_local_ordering_fails(self):
        with self.assertRaises(ValueError):
            boundaries(first=0x120,second=0x14)

if __name__=="__main__":
    unittest.main()
