#!/usr/bin/env python3
"""Isolated real ARM V2Icon getter microexecution (no caller emulation).

Executes only the five reachable machine instructions at 0x2b7ccc.
The word at 0x2b7ce0 is a PC-relative literal, NOT a sixth instruction.
All global memory and return addresses are synthetic and controlled.
"""
import argparse
import hashlib
from pathlib import Path

from unicorn import (Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_PROT_ALL,
                     UC_HOOK_CODE, UC_HOOK_MEM_READ, UC_HOOK_MEM_WRITE)
from unicorn.arm_const import (
    UC_ARM_REG_CPSR, UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_R0,
    UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3,
)

import semantic_callee_v2icon as callee
import semantic_evidence
import semantic_branch_microexec as branches

PAGE = 0x1000
RETURN_PC = 0x710100
INDICES = (0, 1, 2, 3, 7, 15, 31, 63, 127, 255, 1024, 65535)
WORDS = (0, 0x40, 0x12345678, 0x80000000, 0xFFFFFFFF)
R1_SEED = 0x71371371
R2_SEED = 0x82482482
R3_SEED = 0x93593593
NEIGHBOR_LEFT = 0xA5A5C3C3
NEIGHBOR_RIGHT = 0xC3C3A5A5


def _page(address):
    return address & ~(PAGE - 1)


def execute(body, literal, index, value, cpsr):
    """Execute exactly five actual ARM instructions, stop at synthetic return."""
    if len(body) != callee.CALLEE_SIZE:
        raise ValueError("V2Icon ELF body must include five opcodes and one literal")
    # Check only the function's five opcodes and literal location.
    from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
    md = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    instructions = list(md.disasm(body[:20], callee.CALLEE))
    if ([(i.mnemonic, i.op_str) for i in instructions] != list(callee.OPCODES)
            or [i.address for i in instructions] !=
            list(range(callee.CALLEE, callee.LITERAL_ADDR, 4))
            or int.from_bytes(body[20:], "little") != literal):
        raise ValueError("V2Icon code or PC literal no longer matches expected input")
    if (index not in INDICES or not 0 <= value <= 0xFFFFFFFF
            or cpsr not in branches.CPSR_STATES):
        raise ValueError("Invalid sampled index, memory value or CPSR")

    slot = callee.indexed_address(literal, index)
    neighbors = (slot - 4, slot + 4)
    # We never map unknown address zero or a test slot within the code/return pages.
    if any(not 4 <= a <= 0xFFFFFFFB for a in (slot, *neighbors)):
        raise ValueError("Calculated slot is outside safe aligned memory range")
    if slot % 4:
        raise ValueError("Global table word is not aligned")
    code_page, return_page = _page(callee.CALLEE), _page(RETURN_PC)
    target_pages = {_page(a) for a in (slot, *neighbors)}
    if target_pages.intersection((code_page, return_page)):
        raise ValueError("ELF-derived table slot overlaps mapped code/return page")

    emu = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    for page in sorted({code_page, return_page, *target_pages}):
        emu.mem_map(page, PAGE, UC_PROT_ALL)
    emu.mem_write(callee.CALLEE, body)
    emu.mem_write(RETURN_PC, bytes.fromhex("0000a0e1"))
    for at, word in ((slot - 4, NEIGHBOR_LEFT),
                     (slot, value), (slot + 4, NEIGHBOR_RIGHT)):
        emu.mem_write(at, word.to_bytes(4, "little"))
    emu.reg_write(UC_ARM_REG_CPSR, cpsr)
    emu.reg_write(UC_ARM_REG_LR, RETURN_PC)
    for register, initial in ((UC_ARM_REG_R0, index),
                              (UC_ARM_REG_R1, R1_SEED),
                              (UC_ARM_REG_R2, R2_SEED),
                              (UC_ARM_REG_R3, R3_SEED)):
        emu.reg_write(register, initial)

    trace, reads, writes = [], [], []

    def code_hook(uc, address, size, unused):
        trace.append(address)
        if address == RETURN_PC:
            uc.emu_stop()

    def read_hook(uc, access, address, size, value, unused):
        reads.append((address, size))

    def write_hook(uc, access, address, size, value, unused):
        writes.append((address, size))

    emu.hook_add(UC_HOOK_CODE, code_hook)
    emu.hook_add(UC_HOOK_MEM_READ, read_hook)
    emu.hook_add(UC_HOOK_MEM_WRITE, write_hook)
    emu.emu_start(callee.CALLEE, RETURN_PC + 4, timeout=1_000_000, count=7)

    if trace != list(range(callee.CALLEE, callee.LITERAL_ADDR, 4)) + [RETURN_PC]:
        raise AssertionError(f"Unexpected V2Icon call trace: {list(map(hex, trace))}")
    if reads != [(callee.LITERAL_ADDR, 4), (slot, 4)]:
        raise AssertionError(f"Unexpected memory reads: {reads}")
    if writes:
        raise AssertionError(f"Callee wrote unexpected memory locations: {writes}")
    if emu.reg_read(UC_ARM_REG_R0) != value:
        raise AssertionError("V2Icon getter did not return the selected table word")
    if emu.reg_read(UC_ARM_REG_PC) != RETURN_PC:
        raise AssertionError("V2Icon getter did not return through LR")
    if emu.reg_read(UC_ARM_REG_R3) != (
            callee.CALLEE + 12 + literal) & 0xFFFFFFFF:
        raise AssertionError("PC-relative table base calculation differs")
    if any(emu.reg_read(reg) != expected for reg, expected in (
            (UC_ARM_REG_R1, R1_SEED), (UC_ARM_REG_R2, R2_SEED),
            (UC_ARM_REG_LR, RETURN_PC))):
        raise AssertionError("Unrelated registers changed")
    for address, expected in ((slot - 4, NEIGHBOR_LEFT),
                              (slot, value), (slot + 4, NEIGHBOR_RIGHT)):
        if int.from_bytes(emu.mem_read(address, 4), "little") != expected:
            raise AssertionError("Adjacent global data mutated")
    return {"slot": slot, "result": value, "trace": trace, "reads": reads}


def run(binary, inventory):
    digest = hashlib.sha256(binary.read_bytes()).hexdigest()
    call, instructions, literal = callee.decode(binary)
    callee.inventory_match(inventory)
    body = semantic_evidence.read_function(binary, callee.CALLEE, callee.CALLEE_SIZE)
    total = 0
    for index in INDICES:
        for value in WORDS:
            for cpsr in branches.CPSR_STATES:
                execute(body, literal, index, value, cpsr)
                total += 1
    expected = len(INDICES) * len(WORDS) * len(branches.CPSR_STATES)
    if total != expected:
        raise AssertionError("Unexpected number of V2Icon machine tests")
    return "\n".join([
        "# Isolated ARM V2Icon getter — machine-executed contract", "",
        f"ELF SHA-256: `{digest}`", "",
        f"Callsite: `0x{callee.CALLSITE:x}` BL "
        f"`0x{callee.CALLEE:x}` — "
        "`iOS_getV2Icon(V2ICON_DATA)`.", "",
        f"Original ELF literal at `0x{callee.LITERAL_ADDR:x}`: "
        f"`0x{literal:08x}`.", "",
        "Under controlled aligned memory, five original ARM instructions "
        "read the literal, compute a word-table address indexed by r0, "
        "load r0 and return via BX LR.", "",
        "| Checked contract | Result |", "|---|---|",
        "| Five executable instructions, sixth word treated as literal | PASS |",
        "| Exact code trace, LR return and address selection | PASS |",
        "| Exactly two 32-bit reads: literal and indexed table word | PASS |",
        "| No memory writes, preserved adjacent table words | PASS |",
        "| Return r0 equals initialized selected word | PASS |",
        "", f"**V2Icon isolated micro-executions: {total}/{total} PASS.**", "",
        "## Boundaries of this evidence", "",
        "- Original callee code and ELF literal are executed, but the "
        "table data and return PC are **synthetic**.",
        "- A valid-index range or actual game-state table contents "
        "has not been established.",
        "- The caller before/after BL, later branches, real runtime "
        "pointers and complete-function equivalence are not demonstrated.", "",
    ])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--binary", type=Path,
                        default=semantic_evidence.ROOT / "src/lib/armeabi/libgl2jni.so")
    parser.add_argument("--inventory", type=Path,
                        default=semantic_evidence.ROOT / "docs/RE_FUNCTION_INVENTORY.csv")
    parser.add_argument("--results", type=Path,
                        default=semantic_evidence.ROOT / "docs/re-results")
    args = parser.parse_args()
    report = run(args.binary, args.inventory)
    dest = args.results / "SEMANTIC_V2ICON_EXECUTION.md"
    dest.write_text(report, encoding="utf-8")
    print(f"ARM V2Icon machine execution: {dest}")


if __name__ == "__main__":
    main()
