#!/usr/bin/env python3
"""Execute the real BL into iOS_getV2Icon and caller's return-value branches.

Starts at houkoku_okng 0x25a298 with r0=0x34, as set by the preceding MOV.
The original 5-instruction V2Icon getter runs and returns; the caller compares
the returned r0 with 1 and 2. Stop BEFORE executing any branch destination.
Global table contents and pre-BL state are synthetic, not live-game evidence.
"""
import argparse
import hashlib
from pathlib import Path

from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
from unicorn import (Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_PROT_ALL,
                     UC_HOOK_CODE, UC_HOOK_MEM_READ, UC_HOOK_MEM_WRITE)
from unicorn.arm_const import (
    UC_ARM_REG_CPSR, UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_R0,
    UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3,
)

import semantic_evidence
import semantic_callee_v2icon as getter
import semantic_branch_microexec as branches

CALLSITE = getter.CALLSITE
CALL_END = 0x25A2AC
CALLER_ARGS = 0x34  # mov r0,#0x34 immediately before BL in the original ELF.
DEST_ONE = 0x25A2C8
DEST_TWO = 0x25A2AC
DEST_OTHER = 0x25A2F8
RETURN_AFTER_BL = 0x25A29C
EXPECTED_CALLER = (
    ("bl", "#0x2b7ccc"),
    ("cmp", "r0, #1"),
    ("beq", "#0x25a2c8"),
    ("cmp", "r0, #2"),
    ("bne", "#0x25a2f8"),
)
RETURN_VALUES = (0, 1, 2, 3, 0x34, 0x40, 0x100, 0x7FFFFFFF,
                 0x80000000, 0xFFFFFFFE, 0xFFFFFFFF, 0x12345678)
NEIGHBOR_SEEDS = ((0xA5B6C7D8, 0xD8C7B6A5),
                  (0xFFFFFFFF, 0))
OTHER_REGS = (0xABCDEF01, 0x12344321, 0xEEEE1234)
PAGE = 0x1000


def _page(address):
    return address & ~(PAGE - 1)


def verify(caller_code, callee_code):
    """Exact five caller instructions, exact getter opcodes, one data literal."""
    if (len(caller_code) != CALL_END - CALLSITE
            or len(callee_code) != getter.CALLEE_SIZE):
        raise ValueError("Original caller/callee code extent changed")
    md = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    first = list(md.disasm(caller_code, CALLSITE))
    second = list(md.disasm(callee_code[:20], getter.CALLEE))
    if ([i.address for i in first] != list(range(CALLSITE, CALL_END, 4))
            or [(i.mnemonic, i.op_str) for i in first] != list(EXPECTED_CALLER)
            or [(i.mnemonic, i.op_str) for i in second] != list(getter.OPCODES)
            or [i.address for i in second] !=
            list(range(getter.CALLEE, getter.LITERAL_ADDR, 4))):
        raise ValueError("Caller return-value branch or callee instruction changed")
    return int.from_bytes(callee_code[20:], "little")


def choose_destination(value):
    if value == 1:
        return DEST_ONE
    if value == 2:
        return DEST_TWO
    return DEST_OTHER


def execute(caller_code, callee_code, value, cpsr, neighbors=NEIGHBOR_SEEDS[0]):
    literal = verify(caller_code, callee_code)
    if (value not in RETURN_VALUES or cpsr not in branches.CPSR_STATES
            or neighbors not in NEIGHBOR_SEEDS):
        raise ValueError("Controlled return value, flags or canaries invalid")
    slot = getter.indexed_address(literal, CALLER_ARGS)
    if slot % 4 or not 4 <= slot <= 0xFFFFFFF7:
        raise ValueError("Unsafe ELF-derived indexed data address")
    code_pages = {_page(CALLSITE), _page(getter.CALLEE)}
    data_pages = {_page(slot - 4), _page(slot), _page(slot + 4)}
    if code_pages & data_pages:
        raise ValueError("Global table slot aliases executable mappings")

    emu = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    for page in sorted(code_pages | data_pages):
        emu.mem_map(page, PAGE, UC_PROT_ALL)
    emu.mem_write(CALLSITE, caller_code)
    emu.mem_write(getter.CALLEE, callee_code)
    for address, word in ((slot - 4, neighbors[0]), (slot, value),
                          (slot + 4, neighbors[1])):
        emu.mem_write(address, word.to_bytes(4, "little"))
    emu.reg_write(UC_ARM_REG_CPSR, cpsr)
    emu.reg_write(UC_ARM_REG_R0, CALLER_ARGS)
    for register, initial in zip((UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3),
                                 OTHER_REGS):
        emu.reg_write(register, initial)
    emu.reg_write(UC_ARM_REG_LR, 0x710100)

    trace, reads, writes = [], [], []
    destination = choose_destination(value)
    endpoints = {DEST_ONE, DEST_TWO, DEST_OTHER}

    def on_code(uc, address, size, unused):
        trace.append(address)
        if address in endpoints:
            uc.emu_stop()

    def on_read(uc, access, address, size, word, unused):
        reads.append((address, size))

    def on_write(uc, access, address, size, word, unused):
        writes.append((address, size, word))

    emu.hook_add(UC_HOOK_CODE, on_code)
    emu.hook_add(UC_HOOK_MEM_READ, on_read)
    emu.hook_add(UC_HOOK_MEM_WRITE, on_write)
    emu.emu_start(CALLSITE, 0x25A300, timeout=1_000_000, count=16)

    expected_trace = ([CALLSITE]
                      + list(range(getter.CALLEE, getter.LITERAL_ADDR, 4))
                      + [RETURN_AFTER_BL, 0x25A2A0]
                      + ([] if value == 1 else [0x25A2A4, 0x25A2A8])
                      + [destination])
    if trace != expected_trace or emu.reg_read(UC_ARM_REG_PC) != destination:
        raise AssertionError(f"Wrong callee/return-branch trace: {list(map(hex,trace))}")
    if reads != [(getter.LITERAL_ADDR, 4), (slot, 4)] or writes:
        raise AssertionError(f"Unexpected indexed reads or writes: {reads}, {writes}")
    if emu.reg_read(UC_ARM_REG_R0) != value:
        raise AssertionError("Caller did not receive getter's result in r0")
    if emu.reg_read(UC_ARM_REG_LR) != RETURN_AFTER_BL:
        raise AssertionError("BL did not establish correct ARM link register")
    if tuple(emu.reg_read(r) for r in (UC_ARM_REG_R1, UC_ARM_REG_R2)) != OTHER_REGS[:2]:
        raise AssertionError("Getter modified unrelated registers")
    for address, expected in ((slot-4, neighbors[0]), (slot, value),
                              (slot+4, neighbors[1])):
        if int.from_bytes(emu.mem_read(address, 4), "little") != expected:
            raise AssertionError("Synthetic getter table memory mutated")
    return {"destination": destination, "slot": slot, "trace": trace,
            "reads": reads, "writes": writes}


def run(binary):
    digest = hashlib.sha256(binary.read_bytes()).hexdigest()
    call, instructions, literal = getter.decode(binary)
    caller = semantic_evidence.read_function(binary, CALLSITE, CALL_END - CALLSITE)
    callee = semantic_evidence.read_function(binary, getter.CALLEE, getter.CALLEE_SIZE)
    if verify(caller, callee) != literal:
        raise AssertionError("Inconsistent original ELF V2Icon literal")
    counts = {"one": 0, "two": 0, "other": 0}
    for value in RETURN_VALUES:
        for cpsr in branches.CPSR_STATES:
            for neighbors in NEIGHBOR_SEEDS:
                result = execute(caller, callee, value, cpsr, neighbors)
                kind = ("one" if result["destination"] == DEST_ONE else
                        "two" if result["destination"] == DEST_TWO else "other")
                counts[kind] += 1
    total = sum(counts.values())
    if total != 48 or not all(counts.values()):
        raise AssertionError("Expected all three modeled return-value branches")
    return "\n".join([
        "# ARM V2Icon BL and caller return-value branch microexecution", "",
        f"ELF SHA-256: `{digest}`", "",
        "Starts **mid-function** at `0x25a298`, with `r0 = 0x34` "
        "as set by the immediately preceding ARM MOV. Executes original "
        "`BL 0x2b7ccc`, the five-opcode getter and BX LR return, "
        "then the caller's comparisons. Each destination instruction "
        "is **not executed**.", "",
        f"ELF indexed getter word (for r0=0x34): "
        f"`0x{getter.indexed_address(literal,CALLER_ARGS):x}`.", "",
        "| Getter return r0 | Caller target | Controlled tests |",
        "|---|---|---:|",
        f'| 1 | `0x{DEST_ONE:x}` | {counts["one"]} |',
        f'| 2 | `0x{DEST_TWO:x}` | {counts["two"]} |',
        f'| Other sampled 32-bit words | `0x{DEST_OTHER:x}` | {counts["other"]} |',
        "", f"**Caller-and-callee micro-executions: {total}/{total} PASS.**", "",
        "Verified exact original instruction trace through BL and BX LR, "
        "two getter memory reads, returned r0, untouched table data, "
        "and three post-call branch destinations.", "",
        "## Limits", "",
        "- The V2Icon table contents are **synthetic**, not observed live data.",
        "- The caller's preceding blocks, branch-destination instructions "
        "and later calls are not part of these executions.",
        "- This is bounded machine behavior, NOT complete-function "
        "semantic equivalence.", "",
    ])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--binary", type=Path,
                        default=semantic_evidence.ROOT / "src/lib/armeabi/libgl2jni.so")
    parser.add_argument("--results", type=Path,
                        default=semantic_evidence.ROOT / "docs/re-results")
    args = parser.parse_args()
    report = run(args.binary)
    dest = args.results / "SEMANTIC_V2ICON_CALL_FLOW.md"
    dest.write_text(report, encoding="utf-8")
    print(f"Caller and original V2Icon callee branch test: {dest}")


if __name__ == "__main__":
    main()
