"""T39 triage must not transform discovery into certification."""
import unittest

import re_40_task_orchestrator as audit


def plan(done=True, slices=True):
    lines = ["# Plan"]
    for n in range(1, 41):
        lines.append("- [ ] **T%02d — Tarefa %d.** Critério obrigatório." % (n, n))
    lines += ["## 7. Registro de execução por IA executora"]
    if done:
        lines.append("- **T11 — %sdone%s (escopo BX LR restrito).**" %
                     (chr(96), chr(96)))
    if slices:
        lines.append("- **T14 (fatia vertical pequena) — %sready_for_review%s "
                     "(não conclui T14).**" % (chr(96), chr(96)))
    lines += ["## 8. Referências locais principais"]
    return "\n".join(lines)


def gap(address="0x1000", size=64, cls="plausible_function_start"):
    return {"address": address, "size": size, "classification": cls,
            "first_instruction": "push {r4, lr}"}


def gaps(rows=None):
    rows = rows if rows is not None else [gap()]
    return {"elf_sha256": audit.SHA, "gap_interval_count": len(rows),
            "gaps": rows, "text_bytes_uncovered": sum(r["size"] for r in rows),
            "text_section": {"start": "0x1000", "end": "0x2000"},
            "init_array_fini_array_targets_not_in_inventory": ["0x1004"]}


def structural():
    return {"review_count": 1, "core_review": 1,
            "review_rows": [(64, "00001001", "foo", "needs_review", 70, 0, 0)]}


def history():
    return {"total_needs_review": 0, "entries": []}


class OrchestratorTests(unittest.TestCase):
    def test_40_states_never_inferred_from_fatias(self):
        tasks, unchecked = audit.read_plan(plan())
        by_id = {x["id"]: x for x in tasks}
        self.assertEqual(len(tasks), 40)
        self.assertEqual(by_id["T11"]["status"], "done")
        self.assertEqual(by_id["T14"]["status"], "partial_slice")
        self.assertEqual(by_id["T14"]["partial_slices"], 1)
        self.assertEqual(by_id["T32"]["status"], "pending")
        self.assertEqual(unchecked, ["T11"])

    def test_unverified_checkmark_fails_closed(self):
        raw = plan(done=False, slices=False)
        raw = raw.replace("- [ ] **T01", "- [x] **T01")
        with self.assertRaisesRegex(ValueError, "Checkbox"):
            audit.read_plan(raw)

    def test_missing_task_or_duplicate_rejected(self):
        raw = plan()
        with self.assertRaisesRegex(ValueError, "Expected"):
            audit.read_plan(raw.replace("- [ ] **T40", "- [ ] **T39"))

    def test_duplicate_primary_status_rejected(self):
        raw = plan().replace("## 8. Referências",
                             "- **T11 — " + chr(96) + "done" + chr(96) +
                             ".**\n## 8. Referências")
        with self.assertRaisesRegex(ValueError, "Duplicate"):
            audit.read_plan(raw)

    def test_incorrect_gap_sha_rejected(self):
        broken = gaps()
        broken["elf_sha256"] = "f" * 64
        with self.assertRaisesRegex(ValueError, "different ELF"):
            audit.validated_gaps(broken, audit.SHA)

    def test_overlapping_gaps_rejected(self):
        with self.assertRaisesRegex(ValueError, "overlapping"):
            audit.validated_gaps(gaps([gap("0x1000", 64),
                                       gap("0x1030", 64)]), audit.SHA)

    def test_gaps_sorted_without_promoting_candidate(self):
        doc = gaps([gap("0x1080", 64), gap("0x1000", 64)])
        items = audit.gap_queue(doc, audit.validated_gaps(doc, audit.SHA))
        self.assertEqual(items[0]["address"], "0x1000")
        self.assertEqual(items[0]["init_fini_targets"], ["0x1004"])
        self.assertFalse(items[0]["is_confirmed_function"])
        self.assertFalse(items[0]["certified"])

    def test_review_uses_live_data_not_old_baseline(self):
        rows = audit.review_queue(structural(), history(), {"00001001"})
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["historical_category"], "not_in_old_triage")
        self.assertTrue(rows[0]["core"])
        self.assertFalse(rows[0]["certified"])

    def test_no_approvals_or_coverage_forged(self):
        data = audit.assemble(plan(), gaps(), history(), structural(),
                              {"00001001"}, audit.SHA, "123")
        self.assertEqual(data["task_count"], 40)
        self.assertEqual(data["task_states"]["done"], 1)
        self.assertEqual(data["t04"]["certified_functions_added"], 0)
        self.assertEqual(data["t06"]["approved_automatically"], 0)
        self.assertFalse(data["safety"]["issues_semantic_certificate"])
        self.assertIn("T04", audit.markdown(data))

    def test_duplicate_historical_review_fails_closed(self):
        rec = {"address": "00001001", "category": "test"}
        old = {"total_needs_review": 2, "entries": [rec, rec]}
        with self.assertRaisesRegex(ValueError, "Duplicate"):
            audit.review_queue(structural(), old, set())


if __name__ == "__main__":
    unittest.main()
