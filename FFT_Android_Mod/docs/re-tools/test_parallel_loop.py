"""Regression tests for the parallel FFT reverse-engineering coordinator."""
import importlib.util
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

PATH = Path(__file__).with_name("parallel_loop.py")
SPEC = importlib.util.spec_from_file_location("parallel_loop", PATH)
loop = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(loop)


class PipelineTests(unittest.TestCase):
    def test_family_detection(self):
        self.assertEqual(loop.family("Mdl0024(short, int)"), "Mdl")
        self.assertEqual(loop.family("Wdisp_personalwindow()"), "personalwindow")
        self.assertIsNone(loop.family("battle()"))

    def test_inventory_bytes_descending(self):
        with tempfile.TemporaryDirectory() as d:
            file = Path(d) / "inventory.csv"
            file.write_text("address,size,mangled,demangled,status,section_ref\n"
                            "00000010,12,a,small(),pending,x\n"
                            "00000020,100,b,big(),pending,x\n")
            self.assertEqual([r["size"] for r in loop.load_inventory(file)], [100, 12])


    def test_core_priority_precedes_larger_general_function(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "core.csv"
            path.write_text("address,size,mangled,demangled,status,section_ref\n"
                            "00000010,12,a,core(),unread,\n")
            rows = [
                {"address": "00000020", "size": 100, "status": "unread"},
                {"address": "00000010", "size": 12, "status": "unread"},
                {"address": "00000030", "size": 50, "status": "unread"},
            ]
            ranked = loop.prioritize(rows, path)
            self.assertEqual([x["address"] for x in ranked],
                             ["00000010", "00000020", "00000030"])
            self.assertEqual(rows[1]["status"], "unread")

    def test_priority_disable_keeps_inventory_order(self):
        rows = [{"address": "00000020"}, {"address": "00000010"}]
        self.assertEqual(loop.prioritize(rows, None), rows)

    def test_duplicate_priority_addresses_do_not_duplicate_work(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "core.csv"
            path.write_text("address\n00000010\n00000010\n000000ff\n")
            rows = [{"address": "00000020"}, {"address": "00000010"}]
            self.assertEqual([x["address"] for x in loop.prioritize(rows, path)],
                             ["00000010", "00000020"])

    def test_automatic_no_jump_table(self):
        output = ("=== jtable.py: 0x10..0x74 (100 bytes) ===\n"
                  "coverage: 25 of ~25 instruction slots (100%)\n"
                  "-- jump tables resolved: 0 --\n"
                  "-- bl targets: 1 distinct --\n"
                  "  0x40 x1 func\n-- branches: 0 total")
        row = {"address": "00000010", "size": 100,
               "demangled": "battle()", "status": "pending"}
        with patch.object(loop, "run_script", return_value=output):
            result = loop.analyze_one(row, Path("/unused"), 10, {}, 5, 0.9)
        self.assertEqual(result["status"], "auto_structural")
        self.assertEqual(result["distinct_bl"], 1)

    def test_table_requires_review(self):
        output = ("coverage: 25 of ~25 instruction slots (100%)\n"
                  "-- jump tables resolved: 1 --\n"
                  "  guard cmp @0x10, dispatch @0x20: 2 cases, 2 distinct handlers\n"
                  "-- bl targets: 0 distinct --\n-- branches: 0 total")
        row = {"address": "00000010", "size": 100,
               "demangled": "battle()", "status": "pending"}
        with patch.object(loop, "run_script", return_value=output):
            result = loop.analyze_one(row, Path("/unused"), 10, {}, 5, 0.9)
        self.assertEqual(result["status"], "needs_review")

    def test_unresolved_jump_table_requires_review(self):
        output = ("[WARN] jump table at 0x20 could not be safely resolved\\n"
                  "coverage: 25 of ~25 instruction slots (100%)\\n"
                  "-- jump tables resolved: 0 --\\n"
                  "-- bl targets: 0 distinct --\\n-- branches: 0 total")
        row = {"address": "00000010", "size": 100,
               "demangled": "battle()", "status": "pending"}
        with patch.object(loop, "run_script", return_value=output):
            result = loop.analyze_one(row, Path("/unused"), 10, {}, 5, 0.9)
        self.assertEqual(result["status"], "needs_review")
        self.assertEqual(result["tables_unresolved"], 1)

    def test_similarity_with_insufficient_calls_falls_back(self):
        import subprocess
        sim = ("=== reference 0x10..0x74: 25/25 insns (100%), "
               "2 distinct bl targets, 0 unresolved jump-table dispatch(es) ===\\n"
               "-- candidate 0x80..0xe4 (100 B): 25/25 insns "
               "(100%), 2 bl targets, jaccard=1.00, "
               "jt_unresolved=0 -> CONFIRMED-BY-SIMILARITY")
        output = ("coverage: 25 of ~25 instruction slots (100%)\\n"
                  "-- jump tables resolved: 0 --\\n"
                  "-- bl targets: 0 distinct --\\n-- branches: 0 total")
        row = {"address": "00000080", "size": 100,
               "demangled": "Mdl0025()", "status": "pending"}
        ref = {"address": "00000010", "size": 100}
        with patch.object(loop.subprocess, "run",
                          return_value=subprocess.CompletedProcess([], 0, sim, "")):
            with patch.object(loop, "run_script", return_value=output):
                result = loop.analyze_one(
                    row, Path("/unused"), 10, {"Mdl": ref}, 5, 0.9)
        self.assertEqual(result["status"], "auto_structural")
        self.assertEqual(result["reference_address"], ref["address"])

    def test_unparsed_output_fails_closed(self):
        row = {"address": "00000010", "size": 100,
               "demangled": "battle()", "status": "pending"}
        with patch.object(loop, "run_script", return_value="garbled"):
            with self.assertRaises(ValueError):
                loop.analyze_one(row, Path("/unused"), 10, {}, 5, 0.9)


if __name__ == "__main__":
    unittest.main()
