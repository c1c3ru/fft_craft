#!/usr/bin/env python3
"""Emulate one real ARM conditional block through its memory-write boundary.

The slice 0x25a25c..0x25a278 is from houkoku_okng(CTLINFO*). The emulator
starts mid-function, seeds every relevant pointer, and stops before 0x25a27c.
It does NOT verify reachability from the function's entry or callees.
"""
import argparse
import hashlib
from pathlib import Path

from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_PROT_ALL, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import (
    UC_ARM_REG_CPSR, UC_ARM_REG_PC, UC_ARM_REG_R0, UC_ARM_REG_R2,
    UC_ARM_REG_R3, UC_ARM_REG_R4,
)

import semantic_branch_microexec as branches
import semantic_evidence

START = 0x25A25C
END = 0x25A27C
LITERAL_ADDRESS = 0x25A40C
LITERAL_WORD = 0xFFFFFC74
CODE_BASE = 0x25A000
OBJECT_BASE = 0x500000
TABLE_BASE = 0x600000
GLOBAL_FLAG_BASE = 0x610000
TABLE_ANCHOR = TABLE_BASE + 0x38C  # 0x38c + signed(0xfffffc74) == 0.
ENTRY_R3 = 0x00BEEF42
OBJECT_BEFORE = 0xDEADBEEF
NEIGHBOR = 0xA5A55A5A
FLAG_NEIGHBOR = 0x55667788

EXPECTED = (
    ("cmp", "r2, #0"),
    ("ble", "#0x25a27c"),
    ("ldr", "r2, [pc, #0x1a0]"),
    ("str", "r3, [r0, #0x14]"),
    ("ldr", "r3, [r4, r2]"),
    ("ldr", "r2, [r3]"),
    ("orr", "r2, r2, #0x40"),
    ("str", "r2, [r3]"),
)
FLAGS = (0, 0x40, 0x55550000, 0xFFFFFFFF)


def verify_original_code(code, literal):
    """Fail closed on changes to any opcode or its PC-relative literal."""
    if len(code) != END - START or literal != LITERAL_WORD:
        raise ValueError("ARM code size or literal pool differs from known baseline")
    md = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    decoded = list(md.disasm(code, START))
    actual = [(ins.mnemonic, ins.op_str) for ins in decoded]
    if actual != list(EXPECTED) or [ins.address for ins in decoded] != list(range(START, END, 4)):
        raise ValueError(f"Unexpected ARM conditional block: {actual}")
    return decoded


def execute(code, literal, control, initial_flags, initial_cpsr):
    """Run CMP/BLE and up to six following original opcodes with isolated memory."""
    verify_original_code(code, literal)
    if not 0 <= control <= 0xFFFFFFFF or not 0 <= initial_flags <= 0xFFFFFFFF:
        raise ValueError("A 32-bit input is outside its allowed range")
    if initial_cpsr not in branches.CPSR_STATES:
        raise ValueError("Invalid initial CPSR")

    uc = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    for addr in (CODE_BASE, OBJECT_BASE, TABLE_BASE, GLOBAL_FLAG_BASE):
        uc.mem_map(addr, 0x1000, UC_PROT_ALL)
    uc.mem_write(START, code)
    uc.mem_write(LITERAL_ADDRESS, literal.to_bytes(4, "little"))
    uc.mem_write(OBJECT_BASE + 0x14, OBJECT_BEFORE.to_bytes(4, "little"))
    uc.mem_write(OBJECT_BASE + 0x18, NEIGHBOR.to_bytes(4, "little"))
    uc.mem_write(TABLE_BASE, GLOBAL_FLAG_BASE.to_bytes(4, "little"))
    uc.mem_write(GLOBAL_FLAG_BASE, initial_flags.to_bytes(4, "little"))
    uc.mem_write(GLOBAL_FLAG_BASE + 4, FLAG_NEIGHBOR.to_bytes(4, "little"))
    uc.reg_write(UC_ARM_REG_CPSR, initial_cpsr)
    uc.reg_write(UC_ARM_REG_R0, OBJECT_BASE)
    uc.reg_write(UC_ARM_REG_R2, control)
    uc.reg_write(UC_ARM_REG_R3, ENTRY_R3)
    uc.reg_write(UC_ARM_REG_R4, TABLE_ANCHOR)

    trace, writes = [], []

    def on_code(machine, addr, size, ignored):
        trace.append(addr)
        if addr == END:
            machine.emu_stop()

    def on_write(machine, access, addr, size, value, ignored):
        writes.append((addr, size, value & ((1 << (8 * size)) - 1)))

    uc.hook_add(UC_HOOK_CODE, on_code)
    uc.hook_add(UC_HOOK_MEM_WRITE, on_write)
    uc.emu_start(START, CODE_BASE + 0x1000, timeout=1_000_000, count=10)

    active = branches.signed32(control) > 0
    expected_trace = list(range(START, END + 4, 4)) if active else [START, START + 4, END]
    if trace != expected_trace or uc.reg_read(UC_ARM_REG_PC) != END:
        raise AssertionError(f"Unexpected trace for control={control:#x}: {trace}")
    expected_flag = initial_flags | 0x40 if active else initial_flags
    read32 = lambda addr: int.from_bytes(uc.mem_read(addr, 4), "little")
    if read32(GLOBAL_FLAG_BASE) != expected_flag:
        raise AssertionError("Bit 0x40 behavior differs from contract")
    if read32(OBJECT_BASE + 0x14) != (ENTRY_R3 if active else OBJECT_BEFORE):
        raise AssertionError("Object field update disagrees with guarded path")
    if read32(OBJECT_BASE + 0x18) != NEIGHBOR:
        raise AssertionError("Adjacent object field changed")
    if read32(GLOBAL_FLAG_BASE + 4) != FLAG_NEIGHBOR:
        raise AssertionError("Adjacent global flag field changed")
    if read32(TABLE_BASE) != GLOBAL_FLAG_BASE:
        raise AssertionError("Global pointer slot changed")
    if uc.reg_read(UC_ARM_REG_R0) != OBJECT_BASE or uc.reg_read(UC_ARM_REG_R4) != TABLE_ANCHOR:
        raise AssertionError("Object or table base register changed")
    expected_writes = ([(OBJECT_BASE + 0x14, 4, ENTRY_R3),
                        (GLOBAL_FLAG_BASE, 4, expected_flag)] if active else [])
    if writes != expected_writes:
        raise AssertionError(f"Unexpected memory-write trace: {writes}")
    return {"taken": not active, "flag": expected_flag, "trace": trace, "writes": writes}


def run(binary):
    checksum = hashlib.sha256(binary.read_bytes()).hexdigest()
    code = semantic_evidence.read_function(binary, START, END - START)
    literal = int.from_bytes(semantic_evidence.read_function(binary, LITERAL_ADDRESS, 4), "little")
    verify_original_code(code, literal)
    tests = 0
    active = 0
    for control in branches.vectors():
        for cpsr in branches.CPSR_STATES:
            for flags in FLAGS:
                result = execute(code, literal, control, flags, cpsr)
                tests += 1
                active += bool(result["writes"])
    return "\n".join([
        "# Guarded ARM state-write microexecution", "",
        f"ELF SHA-256: `{checksum}`", "",
        "Original ARM code and its PC-relative literal are verified before execution. "
        "The emulator begins **mid-function** at `0x25a25c` and stops "
        "**before** `0x25a27c`; no surrounding calls or whole-function "
        "effects are modeled.", "",
        "| Path | Condition (signed r2) | State update |",
        "|---|---|---|",
        "| BLE taken | r2 <= 0 | no writes to either controlled field |",
        "| BLE not taken | r2 > 0 | object field := entry r3; global flag |= 0x40 |",
        "", f"**Guarded block micro-executions:** {tests}/{tests} PASS.",
        f"**Write-active executions:** {active}; **no-write executions:** {tests-active}.",
        "", "## Boundaries", "",
        "- Pointer slots, memory and registers are artificial controlled inputs.",
        "- Executed exactly the original 8 ARM opcodes on the fallthrough path "
        "or CMP/BLE on the taken path, with two initial NZCV seeds.",
        "- Both adjacent memory words were checked for unexpected modifications.",
        "- The preceding path that initializes these registers was not executed.",
        "- No guarantee that a live call reaches either path, no callee effects, "
        "and no functional equivalence established. Status remains `needs_review`.", "",
    ])


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--binary", type=Path,
                   default=semantic_evidence.ROOT / "src/lib/armeabi/libgl2jni.so")
    p.add_argument("--results", type=Path,
                   default=semantic_evidence.ROOT / "docs/re-results")
    args = p.parse_args()
    out = args.results / "SEMANTIC_GUARDED_BLOCK.md"
    out.write_text(run(args.binary), encoding="utf-8")
    print(f"Guarded ARM block machine validation: {out}")


if __name__ == "__main__":
    main()
