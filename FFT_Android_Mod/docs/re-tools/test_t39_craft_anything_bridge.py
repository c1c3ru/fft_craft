"""Craft Anything bridge is provenance-only, and rejects unsafe imports."""
import copy
import unittest

import t39_craft_anything_bridge as bridge

SHA = "a" * 64
EID = "ev_" + "1" * 64


def queue():
    return {
        "schema": 1, "task_count": 40, "elf_sha256": SHA,
        "t04": {"interval_count": 2, "candidates": [
            {"address": "0x1000", "size": 64},
            {"address": "0x2000", "size": 16},
        ]},
        "t06": {"current_review_count": 2, "candidates": [
            {"address": "00003001"},
            {"address": "00004000"},
        ]},
    }


def evidence(address="0x1004", *, ident=EID, sha=SHA,
             operation="native_function_show", locations=None):
    if locations is None:
        locations = [{"kind": "address", "value": address}]
    return {"id": ident, "subject": {"kind": "native", "sha256": sha},
            "operation": operation, "locations": locations,
            "result": {"content": "UNTRUSTED TARGET BYTES DO NOT COPY"},
            "summary": "Untrusted third-party statement",
            "confidence": "Observed"}


def bundle(*items):
    return {"format": "craft-anything-evidence-bundle",
            "version": 1, "records": list(items), "unknowns": []}


class ExternalEvidenceTests(unittest.TestCase):
    def test_t04_match_keeps_only_metadata(self):
        result = bridge.reconcile(queue(), bundle(evidence()))
        self.assertEqual(result["queue_matches"], 1)
        self.assertEqual(result["matched"][0]["task"], "T04")
        self.assertEqual(result["matched"][0]["queue_address"], "0x1000")
        self.assertFalse(result["source_id_cryptographic_verification_performed"])
        self.assertEqual(result["new_semantic_certificates"], 0)
        self.assertFalse(result["task_status_changed"])
        self.assertNotIn("UNTRUSTED", str(result))

    def test_t06_entry_odd_thumb_address(self):
        result = bridge.reconcile(queue(), bundle(evidence("0x3001")))
        self.assertEqual(result["matched"][0]["task"], "T06")
        self.assertEqual(result["matched"][0]["queue_address"], "00003001")

    def test_outside_queue_not_promoted(self):
        result = bridge.reconcile(queue(), bundle(evidence("0x5000")))
        self.assertEqual(result["queue_matches"], 0)
        self.assertEqual(result["new_structural_approvals"], 0)

    def test_foreign_elf_fails_even_if_address_matches(self):
        with self.assertRaisesRegex(ValueError, "Foreign"):
            bridge.reconcile(queue(), bundle(evidence(sha="b" * 64)))

    def test_invalid_schema_fails(self):
        with self.assertRaisesRegex(ValueError, "export bundle"):
            bridge.reconcile(queue(), {"records": [evidence()]})

    def test_duplicate_ids_fails(self):
        with self.assertRaisesRegex(ValueError, "Duplicate"):
            bridge.reconcile(queue(), bundle(evidence(), evidence("0x3001")))

    def test_missing_or_invalid_address_never_matched(self):
        result = bridge.reconcile(queue(), bundle(evidence(locations=[])))
        self.assertEqual(result["relevant_records_without_locations"], 1)
        self.assertEqual(result["queue_matches"], 0)
        with self.assertRaisesRegex(ValueError, "Non-hex"):
            bridge.reconcile(queue(), bundle(evidence("../../../etc/passwd")))

    def test_unknown_operation_does_not_trigger_claim(self):
        result = bridge.reconcile(queue(), bundle(evidence(
            operation="core_action_approve")))
        self.assertEqual(result["ignored_operations"], 1)
        self.assertEqual(result["queue_matches"], 0)

    def test_truncated_queue_fails_closed(self):
        q = queue()
        q["t06"]["current_review_count"] = 3
        with self.assertRaisesRegex(ValueError, "Truncated"):
            bridge.reconcile(q, bundle())

    def test_malformed_evidence_and_id_fail(self):
        with self.assertRaisesRegex(ValueError, "Invalid external evidence"):
            bridge.reconcile(queue(), bundle(evidence(ident="fake")))
        bad = evidence()
        bad["locations"] = "0x1000"
        with self.assertRaisesRegex(ValueError, "location set"):
            bridge.reconcile(queue(), bundle(bad))

    def test_foreign_kind_refused(self):
        bad = evidence()
        bad["subject"]["kind"] = "apk"
        with self.assertRaisesRegex(ValueError, "native"):
            bridge.reconcile(queue(), bundle(bad))

    def test_non_certification_and_no_untrusted_result_leak(self):
        base = queue()
        old = copy.deepcopy(base)
        output = bridge.reconcile(base, bundle(
            evidence("0x1001"),
            evidence("0x2000", ident="ev_" + "2" * 64)
        ))
        self.assertEqual(base, old)
        self.assertEqual(output["queue_matches"], 2)
        self.assertEqual(output["new_semantic_certificates"], 0)
        self.assertFalse(output["integrated_third_party_code"])


if __name__ == "__main__":
    unittest.main()
