"""Three callee inventory and BL-target failure cases."""
import csv
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import semantic_three_callees_audit as audit


class CalleeAuditTests(unittest.TestCase):
    def test_all_targets_unique_and_arm_aligned(self):
        self.assertEqual(len(audit.TARGETS), 3)
        self.assertEqual(len({v[0] for v in audit.TARGETS}), 3)
        for address, size, _, callsite in audit.TARGETS:
            self.assertEqual(address % 4, 0)
            self.assertEqual(size % 4, 0)
            self.assertEqual(callsite % 4, 0)
            self.assertGreater(size, 0)

    def test_inventory_size_or_symbol_drift_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "inventory.csv"
            def setup(change=None):
                with p.open("w", newline="") as f:
                    w = csv.DictWriter(f, fieldnames=("address", "size", "demangled"))
                    w.writeheader()
                    for a, n, label, _ in audit.TARGETS:
                        if change and a == change[0]:
                            n = change[1]
                        w.writerow({"address": f"{a:08x}", "size": n, "demangled": label})
            setup()
            self.assertTrue(audit.validate_inventory(p))
            setup((audit.TARGETS[0][0], 36))
            with self.assertRaisesRegex(ValueError, "Inventory mismatch"):
                audit.validate_inventory(p)


if __name__ == "__main__":
    unittest.main()
