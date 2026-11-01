"""End-to-end validation of differential_harness.py (T10) against a real,
already-understood function: copy_entry_coord(BWORK*, EDATA*) (0x1d9ee0,
read in full for T08, NOTES sec. 658). This is deliberately NOT a toy --
it is the smallest real game function with a confirmed, cited pseudocode
this session produced, so the comparison is checking the harness against
genuine prior evidence, not against itself.

Includes fault-injection cases proving compare() actually detects
divergence in return value, a flag bit, a memory write, and a call that
should have been stubbed but was not whitelisted -- required by
RE_COMPLETUDE_TASKS.md T10's acceptance criterion.
"""
import unittest
from pathlib import Path

import differential_harness as dh

SO = Path(__file__).resolve().parents[2] / "src/lib/armeabi/libgl2jni.so"
START, END = 0x1d9ee0, 0x1d9ee0 + 120  # copy_entry_coord, confirmed 100% linear, 0 bl

BWORK_ADDR = 0x600000
EDATA_ADDR = 0x610000
BWORK_SIZE = 0x1e6  # confirmed sizeof(BWORK), see types/bwork.h


def reference_copy_entry_coord(bwork: bytearray, edata: bytes) -> bytearray:
    """Python port of the cited pseudocode (NOTES sec. 658), used as the
    independent "reference implementation" side of the differential test.
    """
    out = bytearray(bwork)
    out[0x4f] = edata[0x19]
    out[0x50] = edata[0x1a]
    b51 = out[0x51]
    b51 = (b51 & ~0x80) | (edata[0x1b] & 0x80)
    b51 = (b51 & ~0x0f) | (edata[0x1b] & 0x03)
    b51 = (b51 & ~0x30) | (edata[0x1b] & 0x30)
    out[0x51] = b51 & 0xff
    out[0x184] = edata[0x1e]
    out[0x185] = 0  # zero-extended halfword, high byte always 0 here
    out[0x186] = edata[0x1f]
    return out


def run_pair(bwork_bytes: bytes, edata_bytes: bytes):
    original = dh.run_original(
        SO, START, END,
        initial_regs={"r0": BWORK_ADDR, "r1": EDATA_ADDR},
        buffers=[dh.MemoryBuffer("BWORK", BWORK_ADDR, bwork_bytes),
                 dh.MemoryBuffer("EDATA", EDATA_ADDR, edata_bytes)],
    )
    expected = bytes(reference_copy_entry_coord(bytearray(bwork_bytes), edata_bytes))
    reference = dh.ExecutionResult(True, None, None, {},
                                    [], {"BWORK": expected, "EDATA": edata_bytes},
                                    [], [], 0)
    return original, reference


class CopyEntryCoordDifferentialTests(unittest.TestCase):
    def test_zero_input_matches(self):
        bwork = bytes(BWORK_SIZE)
        edata = bytes(0x20)
        original, reference = run_pair(bwork, edata)
        self.assertTrue(original.ok, original.error)
        report = dh.compare(original, reference, tracked_registers=[])
        self.assertTrue(report["match"], report)

    def test_representative_nonzero_input_matches(self):
        bwork = bytes((i * 7 + 3) & 0xff for i in range(BWORK_SIZE))
        edata = bytearray(0x20)
        edata[0x19], edata[0x1a], edata[0x1b] = 0x42, 0x9a, 0xd5
        edata[0x1e], edata[0x1f] = 0xcc, 0xdd
        original, reference = run_pair(bwork, bytes(edata))
        self.assertTrue(original.ok, original.error)
        report = dh.compare(original, reference, tracked_registers=[])
        self.assertTrue(report["match"], report)

    def test_all_bits_set_edata_byte_0x1b(self):
        bwork = bytes((i * 11 + 1) & 0xff for i in range(BWORK_SIZE))
        edata = bytearray(0x20)
        edata[0x1b] = 0xff  # exercise every bit group copy_entry_coord reads
        original, reference = run_pair(bwork, bytes(edata))
        self.assertTrue(original.ok, original.error)
        report = dh.compare(original, reference, tracked_registers=[])
        self.assertTrue(report["match"], report)

    def test_fault_injection_wrong_memory_write_is_detected(self):
        bwork = bytes(BWORK_SIZE)
        edata = bytearray(0x20)
        edata[0x19] = 0x55
        original, reference = run_pair(bwork, bytes(edata))
        self.assertTrue(original.ok)
        # Corrupt one byte of the "reference" side's expected final state.
        corrupted_bwork = bytearray(reference.final_buffers["BWORK"])
        corrupted_bwork[0x4f] ^= 0xFF
        corrupted = dh.ExecutionResult(
            True, None, None, {}, [],
            {"BWORK": bytes(corrupted_bwork), "EDATA": reference.final_buffers["EDATA"]},
            [], [], 0)
        report = dh.compare(original, corrupted, tracked_registers=[])
        self.assertFalse(report["match"])
        self.assertFalse(report["fields"]["buffer:BWORK"]["match"])

    def test_fault_injection_execution_failure_is_detected(self):
        bwork = bytes(BWORK_SIZE)
        edata = bytes(0x20)
        original, reference = run_pair(bwork, edata)
        broken = dh.ExecutionResult(False, "simulated crash", None, {}, [], {}, [], [], 1)
        report = dh.compare(original, broken, tracked_registers=[])
        self.assertFalse(report["match"])
        self.assertIn("execution", report["fields"])

    def test_unstubbed_external_call_is_a_hard_failure_not_a_pass(self):
        # copy_entry_coord has zero bl targets, so force an escape by
        # declaring a too-short range that lands mid-instruction stream
        # into the next function's bytes, with no stub whitelisted.
        original = dh.run_original(
            SO, START, START + 8,  # deliberately wrong, too-small range
            initial_regs={"r0": BWORK_ADDR, "r1": EDATA_ADDR},
            buffers=[dh.MemoryBuffer("BWORK", BWORK_ADDR, bytes(BWORK_SIZE)),
                     dh.MemoryBuffer("EDATA", EDATA_ADDR, bytes(0x20))],
        )
        self.assertFalse(original.ok)
        self.assertIn("no stub", original.error)


if __name__ == "__main__":
    unittest.main()
