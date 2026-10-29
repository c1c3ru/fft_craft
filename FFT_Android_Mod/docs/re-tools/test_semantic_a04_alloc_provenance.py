"""Strictly structural tests for caller-side 0x10c A04 pattern."""
import unittest
from semantic_a04_alloc_provenance import classify_candidate


def row(opcode="bl", source="r1, r7", size="r0, #0x10c"):
    return {"callsite": "000a2ecc", "context_linear_not_cfg": [
        {"pc":"000a2ebc","mnemonic":"mov","operands":size},
        {"pc":"000a2ec0","mnemonic":opcode,"operands":"#0x2cdf6c"},
        {"pc":"000a2ec4","mnemonic":"mov","operands":source},
        {"pc":"000a2ec8","mnemonic":"mov","operands":"r5, r0"},
        {"pc":"000a2ecc","mnemonic":"bl","operands":"#0xb6620"}]}


class AllocPatternTests(unittest.TestCase):
    def test_original_shape_is_only_candidate_not_proof(self):
        result=classify_candidate(row())
        self.assertTrue(result["matches_size_and_call"])
        self.assertFalse(result["proven_allocation"])
        self.assertFalse(result["proven_source_length"])
        self.assertEqual(result["size"],0x10c)

    def test_wrong_size_fails(self):
        self.assertFalse(classify_candidate(row(size="r0, #0x100"))["matches_size_and_call"])

    def test_unrelated_allocator_opcode_fails(self):
        self.assertFalse(classify_candidate(row(opcode="b"))["matches_size_and_call"])

    def test_without_source_passing_fails(self):
        self.assertFalse(classify_candidate(row(source="r2, r7"))["matches_size_and_call"])

    def test_modified_destination_register_fails(self):
        a=row()
        a["context_linear_not_cfg"][3]["operands"]="r0, r5"
        self.assertFalse(classify_candidate(a)["matches_size_and_call"])


if __name__=="__main__":
    unittest.main()
