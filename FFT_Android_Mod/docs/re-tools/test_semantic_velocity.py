"""REA throughput tests: count unique certified addresses, never synthetic PASSes."""
import datetime as dt
import unittest

import semantic_velocity as v

ELF = "a" * 64
TASKS = [
    {"id": "B01", "status": "in_progress", "depends_on": []},
    {"id": "A04", "status": "in_progress", "depends_on": []},
    {"id": "A03", "status": "planned", "depends_on": ["B01"]},
    {"id": "R01", "status": "planned", "depends_on": ["B01"]},
    {"id": "C01", "status": "planned", "depends_on": ["R01"]},
]


def rows(certified=()):
    return [
        {"address": "00000010", "size": 4,
         "semantic_status": "certified" if "00000010" in certified else "unknown"},
        {"address": "00000020", "size": 128,
         "semantic_status": "certified" if "00000020" in certified else "unknown"},
    ]


def structural():
    return {"digest": ELF, "checkpoints": 2,
            "accepted_count": 1, "review_count": 1}


def sample(certified=(), run_id="1", when="2026-10-01T00:00:00Z"):
    return v.current_snapshot(rows(certified), structural(), TASKS, ELF, run_id, when)


class VelocityTests(unittest.TestCase):
    def test_first_run_baseline_no_fabricated_gain(self):
        h = v.update_history(None, sample(("00000010",)))
        s = v.summarize(h, TASKS)
        self.assertEqual(s["certified"], 1)
        self.assertEqual(s["certified_bytes"], 4)
        self.assertIsNone(s["previous_run_delta"])
        self.assertIsNone(s["rolling_7d"])
        self.assertIn("linha de base", v.render(s))

    def test_repeated_run_does_not_double_count(self):
        first = sample(("00000010",))
        h = v.update_history(None, first)
        again = v.update_history(h, first)
        self.assertEqual(len(again["runs"]), 1)
        with self.assertRaisesRegex(ValueError, "same run ID"):
            v.update_history(h, sample(("00000020",)))

    def test_swapped_certificates_detected_even_if_count_unchanged(self):
        h = v.update_history(None, sample(("00000010",)))
        h = v.update_history(h, sample(("00000020",), "2", "2026-10-02T00:00:00Z"))
        delta = v.summarize(h, TASKS)["previous_run_delta"]
        self.assertEqual(delta["new_certified_addresses"], 1)
        self.assertEqual(delta["removed_certified_addresses"], 1)
        self.assertEqual(delta["certified_bytes_delta"], 124)

    def test_no_auto_promotion_from_microexecution(self):
        h = v.update_history(None, sample())
        h = v.update_history(h, sample((), "2", "2026-10-02T00:00:00Z"))
        s = v.summarize(h, TASKS)
        self.assertEqual(s["certified"], 0)
        self.assertEqual(s["previous_run_delta"]["new_certified_addresses"], 0)

    def test_seven_day_window_with_real_baseline(self):
        h = v.update_history(None, sample((), "1", "2026-10-01T00:00:00Z"))
        h = v.update_history(h, sample(("00000010",), "2", "2026-10-09T00:00:00Z"))
        s = v.summarize(h, TASKS)
        self.assertEqual(s["rolling_7d"]["net_growth"], 1)
        self.assertEqual(s["rolling_7d"]["net_per_day"], .125)

    def test_insufficient_history_has_no_eta(self):
        h = v.update_history(None, sample((), "1", "2026-10-01T00:00:00Z"))
        h = v.update_history(h, sample(("00000010",), "2", "2026-10-02T00:00:00Z"))
        self.assertIsNone(v.summarize(h, TASKS)["rolling_7d"])
        self.assertIn("sem ETA", v.render(v.summarize(h, TASKS)))

    def test_critical_dependency_impact(self):
        impact = v.dependency_impact(TASKS)
        self.assertEqual(impact[0]["task"], "B01")
        self.assertEqual(impact[0]["downstream_not_done"], 3)
        self.assertEqual(impact[1]["task"], "A04")
        self.assertEqual(impact[1]["downstream_not_done"], 0)

    def test_rejects_cycle(self):
        tasks = [{"id": "A", "status": "in_progress", "depends_on": ["B"]},
                 {"id": "B", "status": "planned", "depends_on": ["A"]}]
        with self.assertRaisesRegex(ValueError, "cyclic"):
            v.dependency_impact(tasks)

    def test_rejects_stale_elf_and_inventory(self):
        h = v.update_history(None, sample())
        stale = sample((), "2", "2026-10-02T00:00:00Z")
        stale["elf_sha256"] = "b" * 64
        with self.assertRaisesRegex(ValueError, "incompatible"):
            v.update_history(h, stale)
        wrong = sample((), "2", "2026-10-02T00:00:00Z")
        wrong["inventory_bytes"] = 1
        with self.assertRaisesRegex(ValueError, "inconsistent historical"):
            v.update_history(h, wrong)

    def test_rejects_duplicate_entries_and_broken_dependencies(self):
        with self.assertRaisesRegex(ValueError, "duplicate inventory"):
            v.current_snapshot(rows() + [rows()[0]], structural(), TASKS,
                               ELF, "1", "2026-10-01T00:00:00Z")
        bad = TASKS + [{"id": "Q", "status": "planned", "depends_on": ["missing"]}]
        with self.assertRaisesRegex(ValueError, "unknown"):
            v.current_snapshot(rows(), structural(), bad, ELF, "1",
                               "2026-10-01T00:00:00Z")


if __name__ == "__main__":
    unittest.main()
