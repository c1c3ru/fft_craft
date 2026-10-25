#!/usr/bin/env python3
"""Execute the entry setup and two guards of houkoku_okng on original ARM ELF.

Starts at the function entry, tests the real literal-pool pointer arithmetic
and stack prologue, stops BEFORE either early POP or the next block at 0x25a27c.
Synthetic pointers and globals are used; this is NOT whole-function execution.
"""
import argparse
import hashlib
from pathlib import Path

from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE, UC_PROT_ALL
from unicorn.arm_const import (
    UC_ARM_REG_CPSR, UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_R0,
    UC_ARM_REG_R3, UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_SP,
)

import semantic_branch_microexec as branches
import semantic_evidence
import semantic_guarded_block as guarded
import semantic_two_guards as two

START = 0x25A228
END = two.END
EARLY_EXIT = two.EARLY_EXIT
LITERAL_START = 0x25A404
LITERAL_VALUES = (0x000EDB14, 0xFFFFFC58, 0xFFFFFC74)
CODE_BASE = guarded.CODE_BASE
OBJECT_BASE = guarded.OBJECT_BASE
GLOBAL_PAGE = 0x347000
STATUS_BASE = two.STATUS_ADDR
FLAG_BASE = guarded.GLOBAL_FLAG_BASE
STACK_PAGE = 0x700000
INITIAL_SP = STACK_PAGE + 0x1000
REGISTER_SEEDS = (0x33333333, 0x44444444, 0x55555555, 0xEEEEEEEE)
STACK_CANARY = 0xA5B6C7D8
STATUS_VALUES = (0, 0x80, 0x100, 0xFFFFFFFF)
FIELD_VALUES = two.OBJECT_FIELDS
FLAGS = guarded.FLAGS
INDICES = (0, 1, 2, 3)

PREFIX = (
    ("push", "{r3, r4, r5, lr}"),
    ("ldr", "r3, [r0, #4]"),
    ("ldr", "r4, [pc, #0x1cc]"),
    ("ldr", "r2, [pc, #0x1cc]"),
    ("mov", "r1, #0x38"),
    ("add", "r4, pc, r4"),
    ("mul", "r3, r1, r3"),
    ("ldr", "r2, [r4, r2]"),
    ("mov", "r5, r0"),
)
EXPECTED = PREFIX + two.EXPECTED
GLOBAL_ANCHOR = (0x25A23C + 8 + LITERAL_VALUES[0]) & 0xFFFFFFFF
STATUS_SLOT = (GLOBAL_ANCHOR + LITERAL_VALUES[1]) & 0xFFFFFFFF
FLAG_SLOT = (GLOBAL_ANCHOR + LITERAL_VALUES[2]) & 0xFFFFFFFF


def verify(data, literals):
    """Fail closed on changes to original instructions or the three literals."""
    if len(data) != END - START or tuple(literals) != LITERAL_VALUES:
        raise ValueError("Original ARM instructions or PC-relative literal pool changed")
    md = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    decoded = list(md.disasm(data, START))
    if ([ins.address for ins in decoded] != list(range(START, END, 4))
            or [(ins.mnemonic, ins.op_str) for ins in decoded] != list(EXPECTED)):
        raise ValueError("ARM function-entry opcode signature has changed")
    if not (GLOBAL_PAGE <= STATUS_SLOT < GLOBAL_PAGE + 0x1000
            and GLOBAL_PAGE <= FLAG_SLOT < GLOBAL_PAGE + 0x1000
            and STATUS_SLOT != FLAG_SLOT):
        raise ValueError("Unexpected relative global-pointer addresses")
    return decoded


def simulate(data, literals, index, status, field, flags, cpsr):
    """Validate modeled memory/stack effects from function entry to first exit."""
    verify(data, literals)
    if index not in INDICES or any(not 0 <= x <= 0xFFFFFFFF
                                   for x in (status, field, flags)):
        raise ValueError("Invalid controlled 32-bit state or array index")
    if cpsr not in branches.CPSR_STATES:
        raise ValueError("Unrecognized initial CPSR")

    uc = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    for page in (CODE_BASE, OBJECT_BASE, GLOBAL_PAGE, STATUS_BASE, FLAG_BASE, STACK_PAGE):
        uc.mem_map(page, 0x1000, UC_PROT_ALL)
    uc.mem_write(START, data)
    for n, literal in enumerate(literals):
        uc.mem_write(LITERAL_START + n * 4, literal.to_bytes(4, "little"))
    def write32(address, value):
        uc.mem_write(address, value.to_bytes(4, "little"))
    def read32(address):
        return int.from_bytes(uc.mem_read(address, 4), "little")

    write32(OBJECT_BASE + 4, index)
    write32(OBJECT_BASE + 8, guarded.NEIGHBOR)
    write32(OBJECT_BASE + 0x14, field)
    write32(OBJECT_BASE + 0x18, guarded.NEIGHBOR)
    write32(STATUS_SLOT, STATUS_BASE)
    write32(FLAG_SLOT, FLAG_BASE)
    for idx in INDICES:
        write32(STATUS_BASE + idx * 0x38, status if idx == index else 0xABC00000 + idx)
    write32(STATUS_BASE + 0xF0, guarded.NEIGHBOR)
    write32(FLAG_BASE, flags)
    write32(FLAG_BASE + 4, guarded.FLAG_NEIGHBOR)
    write32(INITIAL_SP - 0x20, STACK_CANARY)
    uc.reg_write(UC_ARM_REG_CPSR, cpsr)
    uc.reg_write(UC_ARM_REG_R0, OBJECT_BASE)
    uc.reg_write(UC_ARM_REG_SP, INITIAL_SP)
    for register, value in zip((UC_ARM_REG_R3, UC_ARM_REG_R4, UC_ARM_REG_R5,
                                UC_ARM_REG_LR), REGISTER_SEEDS):
        uc.reg_write(register, value)

    trace, writes = [], []
    def code_hook(machine, address, size, unused):
        trace.append(address)
        if address in (EARLY_EXIT, END):
            machine.emu_stop()

    def write_hook(machine, access, address, size, value, unused):
        writes.append((address, size, value & ((1 << (size * 8)) - 1)))

    uc.hook_add(UC_HOOK_CODE, code_hook)
    uc.hook_add(UC_HOOK_MEM_WRITE, write_hook)
    uc.emu_start(START, CODE_BASE + 0x1000, timeout=1000000, count=28)

    early = bool(status & 0x100)
    active = not early and branches.signed32(field) > 0
    destination = EARLY_EXIT if early else END
    trace_end = 0x25A254 if early else 0x25A260 if not active else 0x25A278
    expected_trace = list(range(START, trace_end + 4, 4)) + [destination]
    if trace != expected_trace or uc.reg_read(UC_ARM_REG_PC) != destination:
        raise AssertionError(f"Bad ARM entry-to-guard trace: {list(map(hex, trace))}")
    expected_flags = flags | 0x40 if active else flags
    expected_writes = ([(OBJECT_BASE + 0x14, 4, 0),
                        (FLAG_BASE, 4, expected_flags)] if active else [])
    stack_writes = [(address, size, value) for address, size, value in writes
                    if INITIAL_SP - 16 <= address < INITIAL_SP]
    non_stack_writes = [(address, size, value) for address, size, value in writes
                        if not (INITIAL_SP - 16 <= address < INITIAL_SP)]
    if len(stack_writes) != 4 or sorted(a for a, _, _ in stack_writes) != [
            INITIAL_SP - 16, INITIAL_SP - 12, INITIAL_SP - 8, INITIAL_SP - 4]:
        raise AssertionError(f"Unexpected stack-prologue writes: {stack_writes}")
    if non_stack_writes != expected_writes:
        raise AssertionError(f"Unexpected state writes: {non_stack_writes}")

    for i, value in enumerate(REGISTER_SEEDS):
        if read32(INITIAL_SP - 16 + 4 * i) != value:
            raise AssertionError("Callee-saved register push did not match")
    checks = {
        INITIAL_SP - 0x20: STACK_CANARY,
        OBJECT_BASE + 4: index,
        OBJECT_BASE + 8: guarded.NEIGHBOR,
        OBJECT_BASE + 0x14: 0 if active else field,
        OBJECT_BASE + 0x18: guarded.NEIGHBOR,
        STATUS_SLOT: STATUS_BASE,
        FLAG_SLOT: FLAG_BASE,
        STATUS_BASE + 0xF0: guarded.NEIGHBOR,
        FLAG_BASE: expected_flags,
        FLAG_BASE + 4: guarded.FLAG_NEIGHBOR,
    }
    checks.update({STATUS_BASE + i * 0x38:
                   status if i == index else 0xABC00000 + i for i in INDICES})
    for address, expected in checks.items():
        if read32(address) != expected:
            raise AssertionError(f"Canary or derived state differs at 0x{address:x}")
    if (uc.reg_read(UC_ARM_REG_SP) != INITIAL_SP - 16
            or uc.reg_read(UC_ARM_REG_R4) != GLOBAL_ANCHOR
            or uc.reg_read(UC_ARM_REG_R5) != OBJECT_BASE
            or uc.reg_read(UC_ARM_REG_R0) != OBJECT_BASE):
        raise AssertionError("Wrong prologue or relative global-pointer setup")
    return {"path": "early_status" if early else "writes" if active else "nonpositive",
            "trace": trace, "writes": writes, "derived_anchor": GLOBAL_ANCHOR}


def run(binary):
    digest = hashlib.sha256(binary.read_bytes()).hexdigest()
    data = semantic_evidence.read_function(binary, START, END - START)
    literals = tuple(int.from_bytes(
        semantic_evidence.read_function(binary, LITERAL_START + 4 * i, 4),
        "little") for i in range(3))
    verify(data, literals)
    counts = {"early_status": 0, "nonpositive": 0, "writes": 0}
    for index in INDICES:
        for status in STATUS_VALUES:
            for field in FIELD_VALUES:
                for flag in FLAGS:
                    for seed in branches.CPSR_STATES:
                        result = simulate(data, literals, index, status, field, flag, seed)
                        counts[result["path"]] += 1
    total = sum(counts.values())
    assert all(counts.values()) and total == 1024
    return "\n".join([
        "# ARM function entry and state-transition microexecution", "",
        f"ELF SHA-256: `{digest}`", "",
        "Execution starts at the **original function entry** `0x25a228` "
        "and stops before the first unresolved return `0x25a2f4` "
        "or continuation `0x25a27c`. Original PC-relative literal words "
        "and instructions are checked before emulation.", "",
        f"- Computed PC-relative global anchor: `0x{GLOBAL_ANCHOR:x}`.",
        f"- Indexed status pointer slot: `0x{STATUS_SLOT:x}`.",
        f"- Global bitmask pointer slot: `0x{FLAG_SLOT:x}`.", "",
        "| Path | Condition | Cases | State writes (excluding ARM stack prologue) |",
        "|---|---|---:|---|",
        f'| Early BNE | status & 0x100 != 0 | {counts["early_status"]} | None |',
        f'| BLE exit | bit clear, signed field <= 0 | {counts["nonpositive"]} | None |',
        f'| State transition | bit clear, signed field > 0 | {counts["writes"]} | '
        "object field := 0; global flag |= 0x40 |",
        "", f"**Function-entry bounded micro-executions: {total}/{total} PASS.**", "",
        "Verified status index multiplied by 0x38, PC-relative pointer "
        "derivations, all instruction addresses, register-save stack writes, "
        "object/global transitions and adjacent-memory canaries.", "",
        "## Evidence boundaries", "",
        "- This is **not a whole-function test**: both exit instructions "
        "and all later branches, calls and returns remain unexecuted.",
        "- Registers, object state and global pointer slots are synthetic "
        "test inputs; no actual caller or real process state was modeled.",
        "- Other array indices and pointer aliases may have different effects.",
        "- No semantic equivalence of the complete function is asserted.", "",
    ])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--binary", type=Path,
                        default=semantic_evidence.ROOT / "src/lib/armeabi/libgl2jni.so")
    parser.add_argument("--results", type=Path,
                        default=semantic_evidence.ROOT / "docs/re-results")
    args = parser.parse_args()
    target = args.results / "SEMANTIC_ENTRY_PREFIX.md"
    target.write_text(run(args.binary), encoding="utf-8")
    print(f"Function-entry ARM prologue and state test: {target}")


if __name__ == "__main__":
    main()
