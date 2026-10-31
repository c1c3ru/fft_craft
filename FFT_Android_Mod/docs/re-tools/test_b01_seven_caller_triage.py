"""B01 seven-method caller triage: linear-sweep data stays non-certified."""
import tempfile
import unittest
from pathlib import Path

import b01_seven_caller_triage as triage
import b01_seven_cpp_contracts as methods
import b01_overlap_elf_evidence as original


def incoming():
    return {target: {"total": 0, "witnesses": []} for target in methods.SEVEN}


def witness(source_addr, target, mnemonic="bl", raw="000000eb"):
    return {"source": f"{source_addr:08x}",
            "target": f"{target:08x}",
            "instruction_hex": raw, "mnemonic": mnemonic}


class CallerTriageTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.path = Path(tmp.name)
        self.target = methods.SEVEN[0]
        self.entries = [{"start": 0x1000, "end": 0x1100, "size": 0x100},
                        {"start": 0x2000, "end": 0x2100, "size": 0x100}]

    def classify(self, incoming_data, entries=None):
        return triage.classify(
            incoming_data, self.entries if entries is None else entries,
            self.path, original.PINNED_ELF_SHA, "f" * 64, 4096)

    def test_zero_candidates_is_not_zero_possible_runtime_callers(self):
        output = self.classify(incoming())
        self.assertEqual(output["linear_sweep_candidate_callsites"], 0)
        self.assertEqual(output["verified_original_callers"], 0)
        self.assertFalse(output["B01_done"])
        self.assertEqual(len(output["by_target"]), 7)

    def test_owner_and_gap_are_unverified(self):
        rows = incoming()
        rows[self.target] = {"total": 2, "witnesses": [
            witness(0x1004, self.target),
            witness(0x3004, self.target, mnemonic="b", raw="000000ea")]}
        output = self.classify(rows)
        self.assertEqual(output["linear_sweep_candidate_callsites"], 2)
        self.assertEqual(output["tiers"]["unresolved_source"], 1)
        self.assertEqual(output["tiers"]["no_inventory_owner"], 1)
        self.assertEqual(output["verified_object_layouts"], 0)
        self.assertEqual(output["semantic_certificates_added"], 0)
        self.assertEqual(output["candidate_callsites"][0]["candidate_kind"],
                         "candidate_direct_call")
        self.assertFalse(output["candidate_callsites"][0]["caller_reachable"])

    def test_duplicate_candidate_refused(self):
        rows = incoming()
        x = witness(0x1004, self.target)
        rows[self.target] = {"total": 2, "witnesses": [x, x]}
        with self.assertRaisesRegex(ValueError, "Duplicate"):
            self.classify(rows)

    def test_truncated_candidates_refused(self):
        rows = incoming()
        rows[self.target] = {"total": 2, "witnesses": [witness(0x1004, self.target)]}
        with self.assertRaisesRegex(ValueError, "Truncated"):
            self.classify(rows)

    def test_wrong_target_refused(self):
        rows = incoming()
        rows[self.target] = {"total": 1, "witnesses": [
            witness(0x1004, methods.SEVEN[1])]}
        with self.assertRaisesRegex(ValueError, "mismatch"):
            self.classify(rows)

    def test_nonmatching_binary_is_refused(self):
        with self.assertRaisesRegex(ValueError, "pinned"):
            triage.classify(incoming(), self.entries, self.path,
                            "0" * 64, "f" * 64, 4096)

    def test_missing_method_target_refused(self):
        rows = incoming()
        rows.pop(self.target)
        with self.assertRaisesRegex(ValueError, "Incomplete"):
            self.classify(rows)

    def test_unsorted_inventory_refused(self):
        with self.assertRaisesRegex(ValueError, "not sorted"):
            self.classify(incoming(), list(reversed(self.entries)))


if __name__ == "__main__":
    unittest.main()
