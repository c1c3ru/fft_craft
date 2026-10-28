"""Synthetic fixtures for the verifier; never claim original ELF was tested here."""
import hashlib
import json
import tempfile
import unittest
from pathlib import Path

import semantic_manifest_audit as module


class ManifestAuditTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.binary = self.root / "synthetic.elf"
        self.binary.write_bytes(b"FAKE ELF - tests only")
        self.digest = hashlib.sha256(self.binary.read_bytes()).hexdigest()
        self.manifests = self.root / "manifests"
        self.outputs = self.root / "outputs"
        self.manifests.mkdir()
        self.outputs.mkdir()
        for worker in range(1, 26):
            tasks = []
            for number in range(10):
                address = f"{0x1000 + ((worker - 1) * 10 + number) * 4:08x}"
                task = {"address": address, "size": 4, "name": "synthetic",
                        "binary_sha256": self.digest}
                tasks.append(task)
                (self.outputs / f"{address}.json").write_text(json.dumps({
                    **task, "semantic_status": "partial", "evidence_class": "static_bounded",
                    "instruction_set": "arm", "decoded_instructions": 1,
                    "unvisited_slots": 0, "resolved_jump_tables": 0,
                    "candidate_literal_addresses": [], "call_sites": [], "store_sites": [],
                    "unresolved_dispatches": [],
                    "unverified": sorted(module.REQUIRED_UNVERIFIED),
                }), encoding="utf-8")
            (self.manifests / f"semantic-worker-{worker:02d}.json").write_text(
                json.dumps({"schema": 1, "worker": worker, "elf_sha256": self.digest,
                            "total_bytes": 40, "tasks": tasks}), encoding="utf-8")

    def verify(self, **kwargs):
        return module.audit(self.binary, self.manifests, self.outputs,
                            expected_sha256=self.digest, **kwargs)

    def test_250_outputs_and_25_manifest_shards(self):
        summary = self.verify(reinspect=True, inspector=lambda task, _b, _d:
                              json.loads((self.outputs / f"{task['address']}.json").read_text()))
        self.assertEqual((summary["workers"], summary["tasks"], summary["outputs"]),
                         (25, 250, 250))
        self.assertEqual(summary["shard_sizes"], [10] * 25)
        self.assertTrue(summary["reinspected"])
        self.assertIn("não** é execução ARM/Unicorn", module.render(summary))

    def test_wrong_original_binary_rejected(self):
        with self.assertRaisesRegex(ValueError, "SHA-256 mismatch"):
            module.audit(self.binary, self.manifests, self.outputs)

    def test_missing_result_rejected(self):
        next(self.outputs.glob("*.json")).unlink()
        with self.assertRaisesRegex(ValueError, "output set mismatch"):
            self.verify()

    def test_misleading_certification_rejected(self):
        path = next(self.outputs.glob("*.json"))
        data = json.loads(path.read_text())
        data["certified"] = True
        path.write_text(json.dumps(data))
        with self.assertRaisesRegex(ValueError, "invalid partial static evidence"):
            self.verify()

    def test_missing_manifest_rejected(self):
        (self.manifests / "semantic-worker-25.json").unlink()
        with self.assertRaisesRegex(ValueError, "expected 25 manifests"):
            self.verify()

    def test_reinspection_detects_fabricated_result(self):
        with self.assertRaisesRegex(ValueError, "reinspection .* differs"):
            self.verify(reinspect=True, inspector=lambda _task, _binary, _digest: {})

    def test_corrupt_decoding_rejected(self):
        path = next(self.outputs.glob("*.json"))
        data = json.loads(path.read_text())
        data["decoded_instructions"] = 0
        path.write_text(json.dumps(data))
        with self.assertRaisesRegex(ValueError, "invalid partial static evidence"):
            self.verify()


if __name__ == "__main__":
    unittest.main()
