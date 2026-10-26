"""Snapshots must preserve verified same-ELF results, never invent certification."""
import json
import tempfile
import unittest
from pathlib import Path

import central_semantic_summary as central
import semantic_run_snapshot as snapshot


class SnapshotTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.dir = Path(self.temp.name)
        self.elf = "a" * 64
        self.inventory = self.dir / "inventory.csv"
        self.inventory.write_text(
            "address,size,demangled\n"
            "00000010,4,return_leaf\n00000020,64,unknown\n",
            encoding="utf-8")
        for name in ("pilot", "dynamic", "contracts"):
            (self.dir / name).mkdir()
        self.pilot = self.dir / "pilot"
        self.dynamic = self.dir / "dynamic"
        self.contracts = self.dir / "contracts"
        self.certfile = self.dir / "missing.json"

    def save(self, folder, address, record):
        (folder / (address + ".json")).write_text(json.dumps(record))

    def build(self):
        self.save(self.pilot, "00000010", {
            "address": "00000010", "binary_sha256": self.elf,
            "semantic_status": "partial"})
        self.save(self.dynamic, "00000010", {
            "address": "00000010", "binary_sha256": self.elf,
            "semantic_status": "partial", "certified": False,
            "instruction_encoding": "1eff2fe1",
            "contract_candidate": "ARM BX LR", "size": 4,
            "machine_samples_passed": 4})
        self.save(self.contracts, "00000010", {
            "address": "00000010", "binary_sha256": self.elf,
            "instruction_word": "1eff2fe1",
            "contract_stage": "local_isa_contract_checked_review_pending",
            "semantic_status": "partial", "certified": False, "size": 4,
            "machine_samples_passed": 32, "machine_samples_failed": 0,
            "reviewer": None})
        src = central.summarize(self.inventory, self.elf, self.certfile,
                                self.pilot, self.dynamic,
                                contracts_dir=self.contracts)
        return snapshot.make_snapshot(src, self.elf, {}, "789",
                                      {"static": self.pilot,
                                       "unicorn": self.dynamic,
                                       "contracts": self.contracts})

    def test_snapshot_restores_results_when_directories_not_passed(self):
        state = self.build()
        path = self.dir / "SEMANTIC_RUN_SNAPSHOT.json"
        path.write_text(json.dumps(state))
        after = central.summarize(self.inventory, self.elf, self.certfile,
                                  snapshot_path=path)
        self.assertEqual(after["partial_evidence_unique"], 1)
        self.assertEqual(after["checked_local_contracts"], 1)
        self.assertEqual(after["contract_samples"], 32)
        self.assertEqual(after["certified"], 0)
        self.assertEqual(after["evidence_run_id"], "789")
        self.assertIn("último CI verificado", central.render(after))
        self.assertIn("/actions/runs/789", central.render(after))

    def test_reject_elf_and_certificate_ledger_changes(self):
        state = self.build()
        path = self.dir / "snapshot.json"
        path.write_text(json.dumps(state))
        with self.assertRaisesRegex(ValueError, "snapshot stale"):
            snapshot.load(path, "b" * 64, {}, 2)
        with self.assertRaisesRegex(ValueError, "snapshot stale"):
            snapshot.load(path, self.elf,
                          {"00000010": {"status": "partial"}}, 2)

    def test_reject_tampered_counts_and_forged_certificate(self):
        state = self.build()
        state["metrics"]["checked_local_contracts"] = 9
        with self.assertRaisesRegex(ValueError, "contradictory"):
            snapshot.validate(state, self.elf, {}, 2)
        state = self.build()
        state["metrics"]["certified"] = 303
        with self.assertRaisesRegex(ValueError, "invalid snapshot metrics"):
            snapshot.validate(state, self.elf, {}, 2)

    def test_no_snapshot_is_explicit_not_zero_proof(self):
        summary = central.summarize(
            self.inventory, self.elf, self.certfile,
            snapshot_path=self.dir / "nonexistent.json")
        self.assertEqual(summary["partial_evidence_unique"], 0)
        self.assertIn("Nenhum lote dinâmico carregado", central.render(summary))


if __name__ == "__main__":
    unittest.main()
