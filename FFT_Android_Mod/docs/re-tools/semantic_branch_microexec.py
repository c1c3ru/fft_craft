#!/usr/bin/env python3
"""Microexecute real CMP/conditional-B ARM pairs with controlled NZCV.

Only two original ELF instructions are executed in Unicorn per case. The
selected destination is trapped BEFORE any destination instruction runs.
No surrounding function, calls, or global state transitions are validated.
"""
import argparse
import hashlib
import random
from pathlib import Path

from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
from capstone.arm import (ARM_INS_CMP, ARM_INS_B, ARM_OP_REG, ARM_OP_IMM,
                          ARM_CC_GT, ARM_CC_EQ, ARM_CC_NE, ARM_REG_R2, ARM_REG_R3)
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_PROT_ALL, UC_HOOK_CODE
from unicorn.arm_const import (UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_CPSR,
                               UC_ARM_REG_PC)

import semantic_evidence

CODE_PAGE = 0x244000
PAGE_SIZE = 0x1000
CPSR_STATES = (0x10, 0xF0000010)  # Same mode, opposite seeded NZCV flags.
BRANCHES = (
    {
        "name": "signed_gt_43",
        "start": 0x2442C8, "register": UC_ARM_REG_R2,
        "capstone_register": ARM_REG_R2, "immediate": 43,
        "cc": ARM_CC_GT, "taken": 0x2443C8, "fallthrough": 0x2442D0,
    },
    {
        "name": "equal_256",
        "start": 0x24430C, "register": UC_ARM_REG_R3,
        "capstone_register": ARM_REG_R3, "immediate": 256,
        "cc": ARM_CC_EQ, "taken": 0x24438C, "fallthrough": 0x244314,
    },
    {
        "name": "not_equal_256",
        "start": 0x244380, "register": UC_ARM_REG_R3,
        "capstone_register": ARM_REG_R3, "immediate": 256,
        "cc": ARM_CC_NE, "taken": 0x2442E0, "fallthrough": 0x244388,
    },
)


def vectors():
    """Signed boundaries, conditions and deterministic pseudo-random samples."""
    boundary = [0, 1, 42, 43, 44, 255, 256, 257,
                0x7FFFFFFF, 0x80000000, 0xFFFFFFFF, 0xFFFFFFD5, 0xFFFFFFD4]
    rng = random.Random(0x244310)
    return boundary + [rng.getrandbits(32) for _ in range(19)]


def signed32(value):
    return value if value < 0x80000000 else value - 0x100000000


def expected_taken(case, value):
    if case["name"] == "signed_gt_43":
        return signed32(value) > 43
    if case["name"] == "equal_256":
        return value == 256
    if case["name"] == "not_equal_256":
        return value != 256
    raise ValueError("Unknown branch contract")


def verify_pair(code, case):
    """Reject any ELF bytes that no longer match the asserted two-opcode pair."""
    start = case["start"]
    decoded = list(Cs(CS_ARCH_ARM, CS_MODE_ARM).disasm(code, start))
    if len(code) != 8 or len(decoded) != 2 or [i.address for i in decoded] != [start, start + 4]:
        raise ValueError(f"Bad ARM pair layout at 0x{start:x}")
    md = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    md.detail = True
    first, branch = list(md.disasm(code, start))
    if not (first.id == ARM_INS_CMP and len(first.operands) == 2
            and first.operands[0].type == ARM_OP_REG
            and first.operands[0].reg == case["capstone_register"]
            and first.operands[1].type == ARM_OP_IMM
            and first.operands[1].imm == case["immediate"]
            and branch.id == ARM_INS_B and branch.cc == case["cc"]
            and len(branch.operands) == 1
            and branch.operands[0].type == ARM_OP_IMM
            and branch.operands[0].imm == case["taken"]):
        raise ValueError(f"ELF no longer matches expected CMP/B at 0x{start:x}")
    if case["fallthrough"] != start + 8:
        raise ValueError("Invalid expected fallthrough")
    return first, branch


def execute_pair(code, case, initial, cpsr):
    """Execute two opcodes, stop at the third instruction BEFORE executing it."""
    verify_pair(code, case)
    if not 0 <= initial <= 0xFFFFFFFF or cpsr not in CPSR_STATES:
        raise ValueError("Invalid test state")
    start = case["start"]
    emulator = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    emulator.mem_map(CODE_PAGE, PAGE_SIZE, UC_PROT_ALL)
    emulator.mem_write(start, code)
    emulator.reg_write(UC_ARM_REG_CPSR, cpsr)
    emulator.reg_write(case["register"], initial)
    trace = []
    expected = case["taken"] if expected_taken(case, initial) else case["fallthrough"]
    endpoints = {case["taken"], case["fallthrough"]}

    def observe(uc, address, size, unused):
        trace.append(address)
        if address in endpoints:
            uc.emu_stop()

    emulator.hook_add(UC_HOOK_CODE, observe)
    emulator.emu_start(start, CODE_PAGE + PAGE_SIZE, timeout=1_000_000, count=3)
    if trace != [start, start + 4, expected]:
        raise AssertionError(
            f'{case["name"]}: input={initial:#x} cpsr={cpsr:#x} '
            f'trace={list(map(hex, trace))} expected={expected:#x}')
    if emulator.reg_read(case["register"]) != initial:
        raise AssertionError("Comparison unexpectedly modified the tested operand")
    if emulator.reg_read(UC_ARM_REG_PC) != expected:
        raise AssertionError("PC does not point at the expected successor")
    return expected


def run(binary):
    checksum = hashlib.sha256(binary.read_bytes()).hexdigest()
    lines = [
        "# Isolated ARM conditional branch microexecution", "",
        f"ELF SHA-256: `{checksum}`", "",
        "Only each original two-instruction CMP/B pair executes in Unicorn. "
        "The emulator stops before any destination instruction runs. "
        "This is not a full function trace, reachability proof, "
        "callee verification or proof of semantic equivalence.", "",
        "| Branch address | Contract | Inputs × seed flags | Result |",
        "|---|---|---:|---|",
    ]
    total = 0
    samples = vectors()
    for case in BRANCHES:
        start = case["start"]
        code = semantic_evidence.read_function(binary, start, 8)
        verify_pair(code, case)
        for value in samples:
            for flags in CPSR_STATES:
                execute_pair(code, case, value, flags)
                total += 1
        lines.append(
            f'| `0x{start+4:x}` | `{case["name"]}`: taken `0x{case["taken"]:x}`, '
            f'else `0x{case["fallthrough"]:x}` | {len(samples)} × {len(CPSR_STATES)} '
            "| PASS |")
    lines += [
        "", f"**Total verified isolated branch executions:** {total}.", "",
        "## Limitations", "",
        "- Signed versus unsigned interpretations are checked against the actual "
        "machine flags set by CMP in the two-instruction snippet.",
        "- Two opposite initial NZCV patterns help detect reliance on stale flags.",
        "- Values are sampled, not exhaustively enumerated.",
        "- No surrounding predecessor instructions, globals, calls, exceptions "
        "or destination instructions are executed.",
        "- The entire function remains `needs_review`.", "",
    ]
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--binary", type=Path,
                        default=semantic_evidence.ROOT / "src/lib/armeabi/libgl2jni.so")
    parser.add_argument("--results", type=Path,
                        default=semantic_evidence.ROOT / "docs/re-results")
    args = parser.parse_args()
    dest = args.results / "SEMANTIC_BRANCH_MICROEXEC.md"
    dest.write_text(run(args.binary), encoding="utf-8")
    print(f"Isolated ARM branches validated: {dest}")


if __name__ == "__main__":
    main()
