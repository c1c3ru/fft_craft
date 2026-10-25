#!/usr/bin/env python3
"""Original ARM BL/getter plus three caller destinations up to call/return edges.

Uses the ELF code and PC-relative literals, but synthetic table contents,
global pointers, caller-saved registers and stack. Stops BEFORE an unknown
BL target executes, or after a real POP returns to a synthetic caller.
Neither a function-wide trace nor an equivalence proof.
"""
import argparse
import hashlib
from pathlib import Path

from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
from unicorn import (Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_PROT_ALL,
                     UC_HOOK_CODE, UC_HOOK_MEM_READ, UC_HOOK_MEM_WRITE)
from unicorn.arm_const import (UC_ARM_REG_CPSR, UC_ARM_REG_LR, UC_ARM_REG_PC,
                               UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2,
                               UC_ARM_REG_R3, UC_ARM_REG_R4, UC_ARM_REG_R5,
                               UC_ARM_REG_SP)

import semantic_evidence
import semantic_callee_v2icon as getter
import semantic_v2icon_call_flow as flow
import semantic_entry_prefix as entry
import semantic_branch_microexec as branches

START = flow.CALLSITE
MAIN_END = 0x25A314
EXTRA_CALL = 0x25A328
CALL_SETTER = 0x25A2BC
CALL_STATUS = 0x25A310
CALL_FOLLOWUP = EXTRA_CALL
RETURN_INSN = 0x25A2F4
RETURN_PC = 0x710100
CALLER_LITERAL_ADDR = 0x25A40C
CALLER_LITERAL = 0xFFFFFC74
OBJECT = entry.OBJECT_BASE
FLAG_PTR_SLOT = entry.FLAG_SLOT
FLAG_WORD = entry.FLAG_BASE
STACK_TOP = entry.INITIAL_SP
PAGE_SIZE = 0x1000
STACK_SAVED = (0x77881122, 0xAABBCCDD, 0x99887766, RETURN_PC)
NEIGHBOR = 0xDDBBAA55
FLAGS = (0, 0x20, 0x40, 0x60, 0xFFFFFFFF, 0x80000000)
EXPECTED_TAIL = (
    ("mov", "r4, #1"),
    ("str", "r4, [r5, #8]"),
    ("mov", "r0, #0x34"),
    ("mov", "r1, #0"),
    ("bl", "#0x2b9cac"),
    ("str", "r4, [r5, #0x14]"),
    ("pop", "{r3, r4, r5, pc}"),
    ("ldr", "r2, [pc, #0x13c]"),
    ("mov", "r3, #0"),
    ("ldr", "r2, [r4, r2]"),
    ("str", "r3, [r5, #8]"),
    ("ldr", "r3, [r2]"),
    ("orr", "r3, r3, #0x20"),
    ("tst", "r3, #0x40"),
    ("str", "r3, [r2]"),
    ("bne", "#0x25a30c"),
    ("tst", "r3, #0x20"),
    ("bne", "#0x25a328"),
    ("pop", "{r3, r4, r5, pc}"),
    ("ldr", "r3, [pc, #0x10c]"),
    ("ldr", "r3, [r4, r3]"),
    ("ldr", "r3, [r3]"),
    ("tst", "r3, #0x40"),
    ("beq", "#0x25a2ec"),
    ("mov", "r0, #2"),
    ("bl", "#0x26b374"),
)
EXPECTED_FOLLOWUP = ("bl", "#0x282268")


def _page(addr):
    return addr & ~(PAGE_SIZE - 1)


def validate(caller_code, getter_code, followup, caller_literal):
    """Reject changes to original opcodes/targets before making behavioral claims."""
    if (len(caller_code) != MAIN_END - START or len(getter_code) != getter.CALLEE_SIZE
            or len(followup) != 4 or caller_literal != CALLER_LITERAL):
        raise ValueError("ARM code boundary or caller literal changed")
    getter_literal = flow.verify(caller_code[:flow.CALL_END - START], getter_code)
    md = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    md.detail = True
    tail = list(md.disasm(caller_code[flow.CALL_END - START:], flow.CALL_END))
    next_insns = list(md.disasm(followup, EXTRA_CALL))
    if ([(i.mnemonic, i.op_str) for i in tail] != list(EXPECTED_TAIL)
            or [i.address for i in tail] != list(range(flow.CALL_END, MAIN_END, 4))
            or len(next_insns) != 1
            or (next_insns[0].mnemonic, next_insns[0].op_str) != EXPECTED_FOLLOWUP):
        raise ValueError("Caller destination instructions or boundary BL changed")
    return getter_literal


def route(value, flag):
    """Expected destination from observed CMP, TST, ORR and conditional branches."""
    if value == 2:
        return "setter_call", CALL_SETTER
    if value == 1:
        return ("status_call", CALL_STATUS) if flag & 0x40 else (
            "followup_call", CALL_FOLLOWUP)
    if flag & 0x40:
        return "status_call", CALL_STATUS
    if flag & 0x20:
        return "followup_call", CALL_FOLLOWUP
    return "pop_return", RETURN_PC


def expected_trace(value, flag):
    """Independent expected ARM PC sequence including the original getter."""
    prefix = ([START] + list(range(getter.CALLEE, getter.LITERAL_ADDR, 4))
              + [0x25A29C, 0x25A2A0])
    if value == 2:
        return prefix + list(range(0x25A2A4, 0x25A2BC + 4, 4))
    if value == 1:
        prefix += list(range(0x25A2C8, 0x25A2E8 + 4, 4))
        if flag & 0x40:
            return prefix + [0x25A30C, CALL_STATUS]
        return prefix + [0x25A2EC, 0x25A2F0, CALL_FOLLOWUP]
    prefix += [0x25A2A4, 0x25A2A8] + list(range(0x25A2F8, 0x25A308 + 4, 4))
    if flag & 0x40:
        return prefix + [0x25A30C, CALL_STATUS]
    prefix += [0x25A2EC, 0x25A2F0]
    if flag & 0x20:
        return prefix + [CALL_FOLLOWUP]
    return prefix + [RETURN_INSN, RETURN_PC]


def execute(caller_code, getter_code, followup, caller_literal,
            value, flag, cpsr, neighbors=flow.NEIGHBOR_SEEDS[0]):
    getter_literal = validate(caller_code, getter_code, followup, caller_literal)
    if (value not in flow.RETURN_VALUES or flag not in FLAGS
            or cpsr not in branches.CPSR_STATES
            or neighbors not in flow.NEIGHBOR_SEEDS):
        raise ValueError("Unexpected sampled getter state, flag, CPSR or neighbors")
    table = getter.indexed_address(getter_literal, flow.CALLER_ARGS)
    pages = {_page(a) for a in (START, getter.CALLEE, table-4, table,
                               table+4, FLAG_PTR_SLOT, FLAG_WORD-4, FLAG_WORD,
                               FLAG_WORD+4, OBJECT, STACK_TOP-20,
                               STACK_TOP-16, RETURN_PC)}
    # The left canary of an aligned flag at a page boundary requires
    # a separate 0x60f000 mapping; all the other sites are disjoint.
    if len(pages) != 9:
        raise ValueError("Unexpected overlapping synthetic memory mappings")
    emu = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    for page in sorted(pages):
        emu.mem_map(page, PAGE_SIZE, UC_PROT_ALL)
    emu.mem_write(START, caller_code)
    emu.mem_write(EXTRA_CALL, followup)
    emu.mem_write(getter.CALLEE, getter_code)
    emu.mem_write(CALLER_LITERAL_ADDR, caller_literal.to_bytes(4, "little"))
    emu.mem_write(RETURN_PC, bytes.fromhex("0000a0e1"))

    def seed_word(address, word):
        emu.mem_write(address, word.to_bytes(4, "little"))

    for address, word in ((table-4, neighbors[0]), (table, value),
                          (table+4, neighbors[1]),
                          (FLAG_PTR_SLOT, FLAG_WORD),
                          (FLAG_WORD-4, NEIGHBOR), (FLAG_WORD, flag),
                          (FLAG_WORD+4, NEIGHBOR),
                          (OBJECT+4, 0xA1B2C3D4), (OBJECT+8, 0xFEEDBEEF),
                          (OBJECT+12, NEIGHBOR),
                          (OBJECT+0x14, 0xA5A55A5A),
                          (OBJECT+0x18, NEIGHBOR)):
        seed_word(address, word)
    for i, word in enumerate(STACK_SAVED):
        seed_word(STACK_TOP-16+i*4, word)
    seed_word(STACK_TOP-20, NEIGHBOR)
    emu.reg_write(UC_ARM_REG_CPSR, cpsr)
    emu.reg_write(UC_ARM_REG_R0, flow.CALLER_ARGS)
    emu.reg_write(UC_ARM_REG_R1, 0xAAAABBBB)
    emu.reg_write(UC_ARM_REG_R2, 0xCCCCDDDD)
    emu.reg_write(UC_ARM_REG_R3, 0x12345678)
    emu.reg_write(UC_ARM_REG_R4, entry.GLOBAL_ANCHOR)
    emu.reg_write(UC_ARM_REG_R5, OBJECT)
    emu.reg_write(UC_ARM_REG_SP, STACK_TOP-16)
    emu.reg_write(UC_ARM_REG_LR, RETURN_PC)
    trace, reads, writes = [], [], []
    purpose, endpoint = route(value, flag)
    endpoints = {CALL_SETTER, CALL_STATUS, CALL_FOLLOWUP, RETURN_PC}

    def code_hook(uc, address, size, unused):
        trace.append(address)
        if address in endpoints:
            uc.emu_stop()

    def read_hook(uc, access, address, size, word, unused):
        reads.append((address, size))

    def write_hook(uc, access, address, size, word, unused):
        writes.append((address, size, word & ((1 << (8*size))-1)))

    emu.hook_add(UC_HOOK_CODE, code_hook)
    emu.hook_add(UC_HOOK_MEM_READ, read_hook)
    emu.hook_add(UC_HOOK_MEM_WRITE, write_hook)
    emu.emu_start(START, RETURN_PC+4, timeout=1_000_000, count=48)
    if trace != expected_trace(value, flag) or emu.reg_read(UC_ARM_REG_PC) != endpoint:
        raise AssertionError(f"Wrong ARM three-way execution trace: {list(map(hex,trace))}")

    getter_reads = [(getter.LITERAL_ADDR,4), (table,4)]
    flag_reads = ([(CALLER_LITERAL_ADDR,4), (FLAG_PTR_SLOT,4), (FLAG_WORD,4)]
                  if value != 2 else [])
    stack_reads = ([(STACK_TOP-16+i*4,4) for i in range(4)]
                   if purpose == "pop_return" else [])
    if reads != getter_reads + flag_reads + stack_reads:
        raise AssertionError(f"Unexpected memory reads: {reads}")
    expected_writes = (
        [(OBJECT+8,4,1)] if value == 2 else
        [(OBJECT+8,4,0), (FLAG_WORD,4,flag|0x20)] if value == 1 else [])
    if writes != expected_writes:
        raise AssertionError(f"Unexpected memory writes: {writes}")

    def read_word(address):
        return int.from_bytes(emu.mem_read(address,4),"little")
    check = {
        table-4: neighbors[0], table: value, table+4: neighbors[1],
        FLAG_PTR_SLOT: FLAG_WORD, FLAG_WORD-4: NEIGHBOR,
        FLAG_WORD: flag|0x20 if value==1 else flag,
        FLAG_WORD+4: NEIGHBOR,
        OBJECT+4: 0xA1B2C3D4,
        OBJECT+8: 1 if value==2 else 0 if value==1 else 0xFEEDBEEF,
        OBJECT+12: NEIGHBOR,
        OBJECT+0x14: 0xA5A55A5A,
        OBJECT+0x18: NEIGHBOR, STACK_TOP-20: NEIGHBOR,
    }
    for k, word in enumerate(STACK_SAVED):
        check[STACK_TOP-16+k*4] = word
    for address, expected in check.items():
        if read_word(address)!=expected:
            raise AssertionError(f"Canary or state changed unexpectedly: 0x{address:x}")
    if purpose == "pop_return":
        if (emu.reg_read(UC_ARM_REG_SP)!=STACK_TOP
                or (emu.reg_read(UC_ARM_REG_R3),emu.reg_read(UC_ARM_REG_R4),
                    emu.reg_read(UC_ARM_REG_R5))!=STACK_SAVED[:3]):
            raise AssertionError("Real ARM POP did not restore saved register state")
    elif emu.reg_read(UC_ARM_REG_SP)!=STACK_TOP-16:
        raise AssertionError("Unexpected stack change before unresolved call")
    if value==2 and (emu.reg_read(UC_ARM_REG_R0)!=flow.CALLER_ARGS or
                      emu.reg_read(UC_ARM_REG_R1)!=0 or emu.reg_read(UC_ARM_REG_R4)!=1):
        raise AssertionError("Setter call input arguments not established")
    if purpose=="status_call" and emu.reg_read(UC_ARM_REG_R0)!=2:
        raise AssertionError("Status call did not receive r0=2")
    return {"kind":purpose,"endpoint":endpoint,"reads":reads,"writes":writes,"trace":trace}


def run(binary):
    digest=hashlib.sha256(binary.read_bytes()).hexdigest()
    caller=semantic_evidence.read_function(binary,START,MAIN_END-START)
    body=semantic_evidence.read_function(binary,getter.CALLEE,getter.CALLEE_SIZE)
    additional=semantic_evidence.read_function(binary,EXTRA_CALL,4)
    literal=int.from_bytes(
        semantic_evidence.read_function(binary,CALLER_LITERAL_ADDR,4),"little")
    validate(caller,body,additional,literal)
    results={"setter_call":0,"status_call":0,"followup_call":0,"pop_return":0}
    for value in flow.RETURN_VALUES:
        for flag in FLAGS:
            for cpsr in branches.CPSR_STATES:
                for neighbors in flow.NEIGHBOR_SEEDS:
                    verdict=execute(caller,body,additional,literal,value,flag,cpsr,neighbors)
                    results[verdict["kind"]]+=1
    total=sum(results.values())
    if total!=288 or not all(results.values()):
        raise AssertionError("Incomplete ARM branch-destination test matrix")
    return "\n".join([
        "# V2Icon caller — three post-return destinations and state effects","",
        f"ELF SHA-256: \x60{digest}\x60","",
        "Execution starts **mid-function** at \x600x25a298\x60, "
        "runs the actual BL/getter/BX LR, then follows one of three "
        "caller branches through its original instructions. Each unknown "
        "BL is a **stop boundary**, not a stub; a return path executes "
        "the original POP and stops at a synthetic caller address.","",
        "| Verified stop boundary | Number of controlled cases | Observed state |",
        "|---|---:|---|",
        f'| setter BL \x600x{CALL_SETTER:x}\x60 | {results["setter_call"]} | '
        "r0=0x34, r1=0, object[8]=1; callee NOT executed |",
        f'| status BL \x600x{CALL_STATUS:x}\x60 | {results["status_call"]} | '
        "r0=2; for getter=1, object[8]=0 and global bit 0x20 set |",
        f'| followup BL \x600x{CALL_FOLLOWUP:x}\x60 | {results["followup_call"]} | '
        "for getter=1, object[8]=0 and global bit 0x20 set |",
        f'| real POP → synthetic return \x600x{RETURN_PC:x}\x60 | '
        f'{results["pop_return"]} | registers and stack restored |',
        "",f"**Post-getter branch micro-executions: {total}/{total} PASS.**","",
        "The trace and read/write hooks check the exact call/return and branch "
        "path, PC-relative literal, global pointer, conditional state stores, "
        "stack restoration and adjacent-memory canaries.","",
        "## Limitations","",
        "- The getter's table contents, object, globals, and caller stack "
        "are synthetic controlled memory.",
        "- The earlier function entry and all three external callees are "
        "outside this bounded experiment.",
        "- A path stopped before BL demonstrates its pre-call state, "
        "not the effect of that call or whole-function equivalence.","",
    ])


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--binary",type=Path,
                   default=semantic_evidence.ROOT/"src/lib/armeabi/libgl2jni.so")
    p.add_argument("--results",type=Path,
                   default=semantic_evidence.ROOT/"docs/re-results")
    args=p.parse_args()
    dest=args.results/"SEMANTIC_V2ICON_DESTINATIONS.md"
    dest.write_text(run(args.binary),encoding="utf-8")
    print(f"Validated post-getter destinations: {dest}")


if __name__=="__main__":
    main()
