#!/usr/bin/env python3
"""Bounded ARM execution from houkoku_okng entry through return or first call.

Early BNE executes its real POP {r3,r4,r5,pc} and returns to a synthetic
caller address. Other routes execute the next conditional global-slot reset
and STOP BEFORE BL 0x2b7ccc. No function calls are emulated or stubbed.
Original ELF instructions and literal pool words are validated before use.
"""
import argparse
import hashlib
from pathlib import Path

from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
from unicorn import (
    Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE, UC_PROT_ALL,
)
from unicorn.arm_const import (
    UC_ARM_REG_CPSR, UC_ARM_REG_LR, UC_ARM_REG_PC,
    UC_ARM_REG_R0, UC_ARM_REG_R3, UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_SP,
)

import semantic_branch_microexec as branches
import semantic_evidence
import semantic_entry_prefix as prefix
import semantic_guarded_block as guarded

START = prefix.START
FIRST_CALL = 0x25A298
RETURN_INSN = prefix.EARLY_EXIT
RETURN_PC = 0x710100
RETURN_PAGE = 0x710000
CONTINUATION = (
    ("ldr", "r3, [pc, #0x18c]"),
    ("mov", "r0, #0x34"),
    ("add", "r3, pc, r3"),
    ("ldr", "r2, [r3]"),
    ("cmp", "r2, #0"),
    ("movne", "r2, #0"),
    ("strne", "r2, [r3]"),
)
RETURN_OPCODE = ("pop", "{r3, r4, r5, pc}")
NEXT_LITERAL_ADDR = 0x25A410
NEXT_LITERAL = 0x0042106C
NEXT_SLOT = (0x25A284 + 8 + NEXT_LITERAL) & 0xFFFFFFFF
NEXT_PAGE = NEXT_SLOT & ~0xFFF
NEXT_CANARY = 0x5566AA77
INITIAL_SEEDS = (0x12331233, 0x22332233, 0x32333233)
NEXT_VALUES = (0, 0x9ABCDEF0)
INDEX_VALUES = prefix.INDICES
STATUS_VALUES = prefix.STATUS_VALUES
FIELD_VALUES = prefix.FIELD_VALUES
FLAG_VALUES = prefix.FLAGS


def validate(program, pop_code, literals):
    """Verify opcodes at all entry, continuation and return instruction sites."""
    if (len(program) != FIRST_CALL - START or len(pop_code) != 4
            or tuple(literals) != prefix.LITERAL_VALUES + (NEXT_LITERAL,)):
        raise ValueError("ELF program extent, POP bytes or PC-relative literals changed")
    md = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    main = list(md.disasm(program, START))
    ret = list(md.disasm(pop_code, RETURN_INSN))
    expected = prefix.EXPECTED + CONTINUATION
    if ([x.address for x in main] != list(range(START, FIRST_CALL, 4))
            or [(x.mnemonic, x.op_str) for x in main] != list(expected)
            or len(ret) != 1
            or (ret[0].mnemonic, ret[0].op_str) != RETURN_OPCODE):
        raise ValueError("Original ARM entry/continuation/return opcode signature changed")
    if NEXT_PAGE <= NEXT_SLOT < NEXT_PAGE + 0x1000 and NEXT_PAGE not in (
            prefix.GLOBAL_PAGE, prefix.STATUS_BASE, prefix.FLAG_BASE,
            prefix.OBJECT_BASE, prefix.STACK_PAGE, prefix.CODE_BASE):
        return main
    raise ValueError("Continuation pointer slot aliases another synthetic mapping")


def emulate(program, pop_code, literals, index, status, field, flags, next_value, cpsr):
    """Execute from true function entry and check all modeled memory writes."""
    validate(program, pop_code, literals)
    if index not in INDEX_VALUES or any(
            not 0 <= value <= 0xFFFFFFFF for value in (
                status, field, flags, next_value)):
        raise ValueError("Controlled inputs must be 32-bit with a supported index")
    if cpsr not in branches.CPSR_STATES:
        raise ValueError("Invalid ARM CPSR seed")

    emulator = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    pages = (prefix.CODE_BASE, prefix.OBJECT_BASE, prefix.GLOBAL_PAGE,
             prefix.STATUS_BASE, prefix.FLAG_BASE, prefix.STACK_PAGE,
             RETURN_PAGE, NEXT_PAGE)
    if len(set(pages)) != len(pages):
        raise ValueError("Synthetic memory mappings overlap")
    for page in pages:
        emulator.mem_map(page, 0x1000, UC_PROT_ALL)
    emulator.mem_write(START, program)
    emulator.mem_write(RETURN_INSN, pop_code)
    emulator.mem_write(RETURN_PC, bytes.fromhex("0000a0e1"))
    for n, literal in enumerate(literals):
        emulator.mem_write(prefix.LITERAL_START + 4 * n, literal.to_bytes(4, "little"))

    def write32(addr, value):
        emulator.mem_write(addr, value.to_bytes(4, "little"))
    def read32(addr):
        return int.from_bytes(emulator.mem_read(addr, 4), "little")

    write32(prefix.OBJECT_BASE + 4, index)
    write32(prefix.OBJECT_BASE + 8, guarded.NEIGHBOR)
    write32(prefix.OBJECT_BASE + 0x14, field)
    write32(prefix.OBJECT_BASE + 0x18, guarded.NEIGHBOR)
    write32(prefix.STATUS_SLOT, prefix.STATUS_BASE)
    write32(prefix.FLAG_SLOT, prefix.FLAG_BASE)
    for k in INDEX_VALUES:
        write32(prefix.STATUS_BASE + k * 0x38,
                status if k == index else 0xABC00000 + k)
    write32(prefix.STATUS_BASE + 0xF0, guarded.NEIGHBOR)
    write32(prefix.FLAG_BASE, flags)
    write32(prefix.FLAG_BASE + 4, guarded.FLAG_NEIGHBOR)
    write32(NEXT_SLOT - 4, NEXT_CANARY)
    write32(NEXT_SLOT, next_value)
    write32(NEXT_SLOT + 4, NEXT_CANARY)
    write32(prefix.INITIAL_SP - 0x20, prefix.STACK_CANARY)

    emulator.reg_write(UC_ARM_REG_CPSR, cpsr)
    emulator.reg_write(UC_ARM_REG_R0, prefix.OBJECT_BASE)
    emulator.reg_write(UC_ARM_REG_SP, prefix.INITIAL_SP)
    for reg, value in zip(
        (UC_ARM_REG_R3, UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_LR),
        INITIAL_SEEDS + (RETURN_PC,),
    ):
        emulator.reg_write(reg, value)

    trace, writes = [], []

    def on_code(uc, address, size, unused):
        trace.append(address)
        if address in (FIRST_CALL, RETURN_PC):
            uc.emu_stop()

    def on_write(uc, access, address, size, value, unused):
        writes.append((address, size, value & ((1 << (8 * size)) - 1)))

    emulator.hook_add(UC_HOOK_CODE, on_code)
    emulator.hook_add(UC_HOOK_MEM_WRITE, on_write)
    emulator.emu_start(START, RETURN_PC + 4, timeout=1_000_000, count=44)

    early = bool(status & 0x100)
    active = not early and branches.signed32(field) > 0
    end = RETURN_PC if early else FIRST_CALL
    if early:
        expected_trace = list(range(START, 0x25A258, 4)) + [
            RETURN_INSN, RETURN_PC]
    else:
        last = 0x25A278 if active else 0x25A260
        expected_trace = (list(range(START, last + 4, 4))
                          + list(range(0x25A27C, FIRST_CALL + 4, 4)))
    if trace != expected_trace or emulator.reg_read(UC_ARM_REG_PC) != end:
        raise AssertionError(f"Unexpected entry-to-return/call instruction trace: {list(map(hex, trace))}")

    expected_flag = flags | 0x40 if active else flags
    expected_next = next_value if early or next_value == 0 else 0
    state_writes = (
        ([(prefix.OBJECT_BASE + 0x14, 4, 0),
          (prefix.FLAG_BASE, 4, expected_flag)] if active else [])
        + ([(NEXT_SLOT, 4, 0)] if not early and next_value else [])
    )
    stack_writes = [(a, s, v) for a, s, v in writes
                    if prefix.INITIAL_SP - 16 <= a < prefix.INITIAL_SP]
    rest = [(a, s, v) for a, s, v in writes
            if not (prefix.INITIAL_SP - 16 <= a < prefix.INITIAL_SP)]
    if (sorted(a for a, _, _ in stack_writes) !=
            [prefix.INITIAL_SP - 16, prefix.INITIAL_SP - 12,
             prefix.INITIAL_SP - 8, prefix.INITIAL_SP - 4]
            or rest != state_writes):
        raise AssertionError(f"Unexpected stack or non-stack writes: {writes}")

    for k, seed in enumerate(INITIAL_SEEDS + (RETURN_PC,)):
        if read32(prefix.INITIAL_SP - 16 + 4 * k) != seed:
            raise AssertionError("Original stack saves do not match initial registers")
    expected_memory = {
        prefix.INITIAL_SP - 0x20: prefix.STACK_CANARY,
        prefix.OBJECT_BASE + 4: index,
        prefix.OBJECT_BASE + 8: guarded.NEIGHBOR,
        prefix.OBJECT_BASE + 0x14: 0 if active else field,
        prefix.OBJECT_BASE + 0x18: guarded.NEIGHBOR,
        prefix.STATUS_SLOT: prefix.STATUS_BASE,
        prefix.FLAG_SLOT: prefix.FLAG_BASE,
        prefix.STATUS_BASE + 0xF0: guarded.NEIGHBOR,
        prefix.FLAG_BASE: expected_flag,
        prefix.FLAG_BASE + 4: guarded.FLAG_NEIGHBOR,
        NEXT_SLOT - 4: NEXT_CANARY,
        NEXT_SLOT: expected_next,
        NEXT_SLOT + 4: NEXT_CANARY,
    }
    for k in INDEX_VALUES:
        expected_memory[prefix.STATUS_BASE + k * 0x38] = (
            status if k == index else 0xABC00000 + k)
    for addr, expected in expected_memory.items():
        if read32(addr) != expected:
            raise AssertionError(f"Incorrect state at 0x{addr:x}")

    if early:
        if (emulator.reg_read(UC_ARM_REG_SP) != prefix.INITIAL_SP
                or tuple(emulator.reg_read(r) for r in (
                    UC_ARM_REG_R3, UC_ARM_REG_R4, UC_ARM_REG_R5)) != INITIAL_SEEDS):
            raise AssertionError("POP failed to restore stack and saved ARM registers")
    else:
        if (emulator.reg_read(UC_ARM_REG_SP) != prefix.INITIAL_SP - 16
                or emulator.reg_read(UC_ARM_REG_R0) != 0x34
                or emulator.reg_read(UC_ARM_REG_R5) != prefix.OBJECT_BASE):
            raise AssertionError("Pre-BL register/stack state unexpected")
    return {
        "path": ("early_return" if early else
                 "writes" if active else "nonpositive"),
        "next_slot_zeroed": (not early and bool(next_value)),
        "trace": trace, "writes": writes, "endpoint": end,
    }


def run(binary):
    digest = hashlib.sha256(binary.read_bytes()).hexdigest()
    program = semantic_evidence.read_function(binary, START, FIRST_CALL - START)
    pop_code = semantic_evidence.read_function(binary, RETURN_INSN, 4)
    literals = tuple(int.from_bytes(
        semantic_evidence.read_function(
            binary, prefix.LITERAL_START + 4 * k, 4), "little")
        for k in range(4))
    validate(program, pop_code, literals)
    counts = {"early_return": 0, "nonpositive": 0, "writes": 0}
    slot_zeros = 0
    for index in INDEX_VALUES:
        for status in STATUS_VALUES:
            for field in FIELD_VALUES:
                for flags in FLAG_VALUES:
                    for next_value in NEXT_VALUES:
                        for cpsr in branches.CPSR_STATES:
                            result = emulate(program, pop_code, literals,
                                             index, status, field, flags,
                                             next_value, cpsr)
                            counts[result["path"]] += 1
                            slot_zeros += result["next_slot_zeroed"]
    total = sum(counts.values())
    if total != 2048 or not all(counts.values()):
        raise AssertionError("Bounded return/call experiment has unexpected coverage")
    return "\n".join([
        "# ARM entry-to-return / first-call boundary evidence", "",
        f"ELF SHA-256: `{digest}`", "",
        "Original ELF instructions and four PC-relative literals from "
        "`houkoku_okng(CTLINFO*)` are executed or verified. "
        "The early branch executes the actual POP return; other paths "
        "stop **before the first external BL**, at `0x25a298`.", "",
        f"- Conditional next global slot: `0x{NEXT_SLOT:x}`.", "",
        "| Path | Test cases | Observed bounded behavior |",
        "|---|---:|---|",
        f'| Early return | {counts["early_return"]} | '
        "Actual POP restores r3/r4/r5 and stack pointer, returns to synthetic caller |",
        f'| Field <= 0 | {counts["nonpositive"]} | '
        "No object/flag write; continuation may zero a separate nonzero global slot |",
        f'| Field > 0 | {counts["writes"]} | '
        "Object field := 0, global flag |= 0x40; continuation may zero that slot |",
        "", f"**Verified entry-to-boundary microexecutions: {total}/{total} PASS.**",
        f"**Conditional continuation slot clears:** {slot_zeros}.", "",
        "The emulator checks every executed opcode, exact state writes, "
        "saved/restored ARM registers, return address, conditional STRNE and "
        "neighboring memory canaries.", "",
        "## Deliberate uncertainty", "",
        "- The first BL is **not executed or stubbed**. Its inputs, return "
        "value and side effects remain unknown.",
        "- State addresses and caller return address are controlled synthetic data; "
        "no actual application process was executed.",
        "- No subsequent function-wide branches, later calls or error paths "
        "have been proven equivalent.", "",
    ])


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--binary", type=Path,
                   default=semantic_evidence.ROOT / "src/lib/armeabi/libgl2jni.so")
    p.add_argument("--results", type=Path,
                   default=semantic_evidence.ROOT / "docs/re-results")
    args = p.parse_args()
    out = args.results / "SEMANTIC_RETURN_CALL_BOUNDARY.md"
    out.write_text(run(args.binary), encoding="utf-8")
    print(f"Verified ARM entry-to-return/call boundary: {out}")


if __name__ == "__main__":
    main()
