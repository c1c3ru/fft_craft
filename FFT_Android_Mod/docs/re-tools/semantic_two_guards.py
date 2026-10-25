#!/usr/bin/env python3
"""Emulate two consecutive ARM guards and their state writes from real ELF.

Begin mid-function at 0x25a24c; do not execute predecessor setup or callees.
Stop BEFORE any instruction at the two branch exits. The experiments cannot
prove whole-function reachability or semantic equivalence.
"""
import argparse
import hashlib
from pathlib import Path

from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE, UC_PROT_ALL
from unicorn.arm_const import (
    UC_ARM_REG_CPSR, UC_ARM_REG_PC, UC_ARM_REG_R0, UC_ARM_REG_R2,
    UC_ARM_REG_R3, UC_ARM_REG_R4,
)

import semantic_branch_microexec as branches
import semantic_evidence
import semantic_guarded_block as previous

START = 0x25A24C
END = previous.END
EARLY_EXIT = 0x25A2F4
STATUS_ADDR = 0x620000
CODE_BASE = previous.CODE_BASE
OBJECT_BASE = previous.OBJECT_BASE
TABLE_BASE = previous.TABLE_BASE
TABLE_ANCHOR = previous.TABLE_ANCHOR
GLOBAL_FLAG_BASE = previous.GLOBAL_FLAG_BASE
LITERAL_ADDRESS = previous.LITERAL_ADDRESS
LITERAL_WORD = previous.LITERAL_WORD
STATUS_SEEDS = (0, 0x80, 0x100, 0xFFFFFFFF)
OBJECT_FIELDS = (0, 1, 43, 256, 0x7FFFFFFF, 0x80000000,
                 0xFFFFFFFF, 0xFFFFFFFE)
GUARD_SEQUENCE = (
    ("ldr", "r3, [r2, r3]"),
    ("ands", "r3, r3, #0x100"),
    ("bne", "#0x25a2f4"),
    ("ldr", "r2, [r0, #0x14]"),
)
EXPECTED = GUARD_SEQUENCE + previous.EXPECTED


def validate(data, literal):
    """Check all opcode addresses and both branch destinations against ELF."""
    if len(data) != END - START or literal != LITERAL_WORD:
        raise ValueError("Original ARM byte range or literal changed")
    md = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    instructions = list(md.disasm(data, START))
    actual = [(ins.mnemonic, ins.op_str) for ins in instructions]
    if actual != list(EXPECTED) or [ins.address for ins in instructions] != list(range(START, END, 4)):
        raise ValueError(f"Expected 12 consecutive ARM instructions, got {actual}")
    return instructions


def simulate(code, literal, status, control, initial_flags, cpsr):
    """Execute the original 12-instruction slice, stopping at first external exit."""
    validate(code, literal)
    if any(not 0 <= n <= 0xFFFFFFFF for n in (status, control, initial_flags)):
        raise ValueError("Inputs must be unsigned 32-bit words")
    if cpsr not in branches.CPSR_STATES:
        raise ValueError("Unexpected CPSR seed")
    uc = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    for page in (CODE_BASE, OBJECT_BASE, TABLE_BASE, GLOBAL_FLAG_BASE, STATUS_ADDR):
        uc.mem_map(page, 0x1000, UC_PROT_ALL)
    uc.mem_write(START, code)
    uc.mem_write(LITERAL_ADDRESS, literal.to_bytes(4, "little"))
    uc.mem_write(STATUS_ADDR, status.to_bytes(4, "little"))
    uc.mem_write(STATUS_ADDR + 4, previous.NEIGHBOR.to_bytes(4, "little"))
    uc.mem_write(OBJECT_BASE + 0x14, control.to_bytes(4, "little"))
    uc.mem_write(OBJECT_BASE + 0x18, previous.NEIGHBOR.to_bytes(4, "little"))
    uc.mem_write(TABLE_BASE, GLOBAL_FLAG_BASE.to_bytes(4, "little"))
    uc.mem_write(GLOBAL_FLAG_BASE, initial_flags.to_bytes(4, "little"))
    uc.mem_write(GLOBAL_FLAG_BASE + 4, previous.FLAG_NEIGHBOR.to_bytes(4, "little"))
    uc.reg_write(UC_ARM_REG_CPSR, cpsr)
    uc.reg_write(UC_ARM_REG_R0, OBJECT_BASE)
    uc.reg_write(UC_ARM_REG_R2, STATUS_ADDR)
    uc.reg_write(UC_ARM_REG_R3, 0)  # Array index for status lookup.
    uc.reg_write(UC_ARM_REG_R4, TABLE_ANCHOR)
    trace, writes = [], []

    def on_instruction(machine, address, size, unused):
        trace.append(address)
        if address in (END, EARLY_EXIT):
            machine.emu_stop()

    def on_store(machine, access, address, size, value, unused):
        writes.append((address, size, value & ((1 << (8 * size)) - 1)))

    uc.hook_add(UC_HOOK_CODE, on_instruction)
    uc.hook_add(UC_HOOK_MEM_WRITE, on_store)
    uc.emu_start(START, CODE_BASE + 0x1000, timeout=1_000_000, count=16)

    early = bool(status & 0x100)
    active = not early and branches.signed32(control) > 0
    endpoint = EARLY_EXIT if early else END
    expected_trace = (
        [START, START + 4, START + 8, EARLY_EXIT] if early
        else list(range(START, END + 4, 4)) if active
        else list(range(START, 0x25A260 + 4, 4)) + [END]
    )
    if trace != expected_trace or uc.reg_read(UC_ARM_REG_PC) != endpoint:
        raise AssertionError(f"Wrong two-guard ARM control flow: {list(map(hex, trace))}")
    expected_flags = initial_flags | 0x40 if active else initial_flags
    expected_object = 0 if active else control
    expected_writes = ([(OBJECT_BASE + 0x14, 4, 0),
                        (GLOBAL_FLAG_BASE, 4, expected_flags)] if active else [])
    def read32(address):
        return int.from_bytes(uc.mem_read(address, 4), "little")
    for address, expected in (
            (STATUS_ADDR, status),
            (STATUS_ADDR + 4, previous.NEIGHBOR),
            (OBJECT_BASE + 0x14, expected_object),
            (OBJECT_BASE + 0x18, previous.NEIGHBOR),
            (TABLE_BASE, GLOBAL_FLAG_BASE),
            (GLOBAL_FLAG_BASE, expected_flags),
            (GLOBAL_FLAG_BASE + 4, previous.FLAG_NEIGHBOR)):
        if read32(address) != expected:
            raise AssertionError(f"Unexpected memory state at 0x{address:x}")
    if writes != expected_writes:
        raise AssertionError(f"Unexpected writes: {writes}")
    if (uc.reg_read(UC_ARM_REG_R0) != OBJECT_BASE
            or uc.reg_read(UC_ARM_REG_R4) != TABLE_ANCHOR):
        raise AssertionError("Object/table base registers changed")
    return {"path": "early_status" if early else "nonpositive" if not active else "writes",
            "writes": writes, "trace": trace}


def run(binary):
    digest = hashlib.sha256(binary.read_bytes()).hexdigest()
    data = semantic_evidence.read_function(binary, START, END - START)
    literal = int.from_bytes(
        semantic_evidence.read_function(binary, LITERAL_ADDRESS, 4), "little")
    validate(data, literal)
    outcomes = {"early_status": 0, "nonpositive": 0, "writes": 0}
    for status in STATUS_SEEDS:
        for control in OBJECT_FIELDS:
            for initial in previous.FLAGS:
                for cpsr in branches.CPSR_STATES:
                    path = simulate(data, literal, status, control, initial, cpsr)["path"]
                    outcomes[path] += 1
    total = sum(outcomes.values())
    if not all(outcomes.values()):
        raise AssertionError("Every guarded path needs at least one test")
    return "\n".join([
        "# Two consecutive ARM guards — bounded machine execution", "",
        f"ELF SHA-256: `{digest}`", "",
        "Uses actual ARM instructions and a PC-relative literal from "
        "`houkoku_okng(CTLINFO*)`, beginning **mid-function** at "
        "`0x25a24c`. Only this bounded slice is executed, with synthetic "
        "registers, pointers, status and memory.", "",
        "| Guarded path | Preconditions | Memory writes | Test cases |",
        "|---|---|---|---:|",
        f'| Early BNE to `0x25a2f4` | status & 0x100 != 0 | None | {outcomes["early_status"]} |',
        f'| BLE to `0x25a27c` | status & 0x100 == 0 and signed control <= 0 | None | {outcomes["nonpositive"]} |',
        f'| Fallthrough | status & 0x100 == 0 and signed control > 0 | '
        f'Object field := 0; global flag |= 0x40 | {outcomes["writes"]} |',
        "", f"**Two-guard machine executions: {total}/{total} PASS.**", "",
        "Checks every instruction address on the bounded path, exact writes, "
        "status-slot immutability, adjacent memory canaries and object/table pointers.", "",
        "## Limitations", "",
        "- The statuses, field values and pointers were synthesized for testing.",
        "- No predecessor path, live caller or subsequent exit instruction was executed.",
        "- The early branch target and normal continuation are not executed.",
        "- This does not prove whole-function reachability, behavior of callees "
        "or semantic equivalence. Structural status is independent of "
        "semantic approval.", "",
    ])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--binary", type=Path,
                        default=semantic_evidence.ROOT / "src/lib/armeabi/libgl2jni.so")
    parser.add_argument("--results", type=Path,
                        default=semantic_evidence.ROOT / "docs/re-results")
    args = parser.parse_args()
    dest = args.results / "SEMANTIC_TWO_GUARDS.md"
    dest.write_text(run(args.binary), encoding="utf-8")
    print(f"Wrote bounded two-guard ARM machine report: {dest}")


if __name__ == "__main__":
    main()
