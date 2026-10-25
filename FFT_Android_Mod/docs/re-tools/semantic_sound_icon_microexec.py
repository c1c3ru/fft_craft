#!/usr/bin/env python3
"""Bounded original-ELF Unicorn execution at two previously unknown edges.

1) Execute three validated sound B trampolines plus SysSE_PlayDef's three
   instructions, stop BEFORE the new target 0x2b2b7c.
2) Execute first ten iOS_SetIconPosition instructions, stop BEFORE its first
   indexed global-pointer dereference at 0x2b8928.

Neither exercise runs an unresolved callee, claims audio output, or validates
the complete 5,036-byte icon-positioning function.
"""
import argparse
import hashlib
from pathlib import Path

from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
from unicorn import (Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_PROT_ALL, UC_HOOK_CODE,
                     UC_HOOK_MEM_READ, UC_HOOK_MEM_WRITE)
from unicorn.arm_const import (
    UC_ARM_REG_CPSR, UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_R0,
    UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_R4,
    UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7, UC_ARM_REG_R8,
    UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11, UC_ARM_REG_SP,
)

import semantic_evidence
import semantic_sound_chain as chain
import semantic_branch_microexec as branches

SOUND_ENTRY = 0x2B2CF8
SOUND_STOP = 0x2B2B7C
SOUND_SIGNATURE = (
    ("mov", "r1, r0"),
    ("mov", "r0, #0"),
    ("b", "#0x2b2b7c"),
)
ICON_ENTRY = 0x2B8900
ICON_STOP = 0x2B8928
ICON_SIGNATURE = (
    ("push", "{r4, r5, r6, r7, r8, sb, sl, fp, lr}"),
    ("ldr", "r3, [pc, #0xff8]"),
    ("sub", "sp, sp, #0x24"),
    ("ldr", "sl", "r0"),
)
# Complete exact signature; do not infer it from a symbol name.
ICON_SIGNATURE = (
    ("push", "{r4, r5, r6, r7, r8, sb, sl, fp, lr}"),
    ("ldr", "r3, [pc, #0xff8]"),
    ("sub", "sp, sp, #0x24"),
    ("ldr", "sl, [pc, #0xff4]"),
    ("add", "r3, pc, r3"),
    ("str", "r3, [sp, #0xc]"),
    ("ldr", "r2, [sp, #0xc]"),
    ("ldr", "r3, [pc, #0xfe8]"),
    ("add", "r1, sp, #0x1c"),
    ("ldr", "sb, [pc, #0xfe4]"),
)
LITERAL_ADDRS = (0x2B9904, 0x2B9908, 0x2B990C, 0x2B9910)
STACK_TOP = 0x701000
SAVED_REGS = (UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6,
              UC_ARM_REG_R7, UC_ARM_REG_R8, UC_ARM_REG_R9,
              UC_ARM_REG_R10, UC_ARM_REG_R11, UC_ARM_REG_LR)
SAVED_WORDS = (0x04040404, 0x05050505, 0x06060606, 0x07070707,
               0x08080808, 0x09090909, 0x10101010, 0x11111111,
               0x710100)
ARGUMENTS = (0, 1, 2, 0x34, 0xFFFFFFFF)
CANARY = 0xC0DEC0DE
PAGE = 0x1000


def disasm_exact(data, start, signature):
    if len(data) != 4 * len(signature):
        raise ValueError("Truncated original ARM boundary code")
    md = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    insns = list(md.disasm(data, start))
    if ([x.address for x in insns] !=
            list(range(start, start + len(data), 4))
            or [(x.mnemonic, x.op_str) for x in insns] != list(signature)):
        raise ValueError("Original ARM boundary instruction signature changed")
    return insns


def read_original(binary):
    sound = semantic_evidence.read_function(binary, SOUND_ENTRY, 12)
    icon = semantic_evidence.read_function(binary, ICON_ENTRY, ICON_STOP-ICON_ENTRY)
    literals = tuple(int.from_bytes(
        semantic_evidence.read_function(binary, a, 4), "little")
        for a in LITERAL_ADDRS)
    disasm_exact(sound, SOUND_ENTRY, SOUND_SIGNATURE)
    disasm_exact(icon, ICON_ENTRY, ICON_SIGNATURE)
    visited, boundary, _ = chain.follow(binary)
    if boundary != SOUND_ENTRY or len(visited) != 3:
        raise ValueError("Unexpected sound trampoline chain")
    return visited, sound, icon, literals


def sound_execute(visited, sound, argument, cpsr):
    disasm_exact(sound, SOUND_ENTRY, SOUND_SIGNATURE)
    if argument not in ARGUMENTS or cpsr not in branches.CPSR_STATES:
        raise ValueError("Invalid sound argument or flags")
    if len(visited) != 3 or next(iter(visited)) != chain.ENTRY:
        raise ValueError("Sound chain not verified")
    pc = chain.ENTRY
    for at, (word, target) in visited.items():
        if at != pc:
            raise ValueError("Sound branch chain disconnected")
        _, proven = chain.classify(word, at)
        if proven != target:
            raise ValueError("Changed sound branch target")
        pc = target
    if pc != SOUND_ENTRY:
        raise ValueError("Sound chain no longer reaches dispatcher")
    pages = {a & ~0xfff for a in (*visited, SOUND_ENTRY, SOUND_STOP)}
    uc=Uc(UC_ARCH_ARM, UC_MODE_ARM)
    for page in sorted(pages):
        uc.mem_map(page, PAGE, UC_PROT_ALL)
    for addr, (word, _) in visited.items():
        uc.mem_write(addr, word)
    uc.mem_write(SOUND_ENTRY, sound)
    uc.mem_write(SOUND_STOP, bytes.fromhex("0000a0e1"))
    uc.reg_write(UC_ARM_REG_CPSR,cpsr)
    uc.reg_write(UC_ARM_REG_R0,argument)
    uc.reg_write(UC_ARM_REG_R1,0xABABABAB)
    uc.reg_write(UC_ARM_REG_LR,0x710100)
    trace, reads, writes=[], [], []
    def hook_code(machine, addr, size, unused):
        trace.append(addr)
        if addr == SOUND_STOP:
            machine.emu_stop()
    uc.hook_add(UC_HOOK_CODE, hook_code)
    uc.hook_add(UC_HOOK_MEM_READ,
                lambda _,a,addr,size,v,d: reads.append((addr,size)))
    uc.hook_add(UC_HOOK_MEM_WRITE,
                lambda _,a,addr,size,v,d: writes.append((addr,size)))
    uc.emu_start(chain.ENTRY, 0xffffffff, timeout=1_000_000, count=12)
    expected=list(visited)+[SOUND_ENTRY,SOUND_ENTRY+4,SOUND_ENTRY+8,SOUND_STOP]
    if trace!=expected or uc.reg_read(UC_ARM_REG_PC)!=SOUND_STOP:
        raise AssertionError(f"Wrong real sound dispatcher trace {list(map(hex,trace))}")
    if reads or writes:
        raise AssertionError("Sound forwarding prefix unexpectedly accessed memory")
    if (uc.reg_read(UC_ARM_REG_R0)!=0 or uc.reg_read(UC_ARM_REG_R1)!=argument
            or uc.reg_read(UC_ARM_REG_LR)!=0x710100):
        raise AssertionError("Sound dispatcher r0/r1/LR contract violated")
    if (uc.reg_read(UC_ARM_REG_CPSR)&0xf0000000)!=(cpsr&0xf0000000):
        raise AssertionError("Sound dispatcher unexpectedly changed NZCV flags")
    return {"trace":trace, "end":SOUND_STOP}


def icon_execute(icon, literals, r0, cpsr):
    disasm_exact(icon, ICON_ENTRY, ICON_SIGNATURE)
    if r0 not in ARGUMENTS or cpsr not in branches.CPSR_STATES or (
            len(literals)!=4 or any(not 0 <= x <= 0xffffffff for x in literals)):
        raise ValueError("Invalid ARM icon input or PC literal")
    uc=Uc(UC_ARCH_ARM,UC_MODE_ARM)
    # Separate code, PC literals and stack pages; the first global LDR is
    # deliberately not executed or mapped.
    for page in (0x2B8000,0x2B9000,0x700000):
        uc.mem_map(page,PAGE,UC_PROT_ALL)
    uc.mem_write(ICON_ENTRY,icon)
    uc.mem_write(ICON_STOP,bytes.fromhex("0000a0e1"))
    for at,v in zip(LITERAL_ADDRS,literals):
        uc.mem_write(at,v.to_bytes(4,"little"))
    uc.mem_write(STACK_TOP-0x80,CANARY.to_bytes(4,"little"))
    uc.reg_write(UC_ARM_REG_CPSR,cpsr)
    uc.reg_write(UC_ARM_REG_SP,STACK_TOP)
    uc.reg_write(UC_ARM_REG_R0,r0)
    for reg,v in zip(SAVED_REGS,SAVED_WORDS):
        uc.reg_write(reg,v)
    trace,reads,writes=[],[],[]
    def code_hook(machine, addr,size,unused):
        trace.append(addr)
        if addr==ICON_STOP:
            machine.emu_stop()
    uc.hook_add(UC_HOOK_CODE,code_hook)
    uc.hook_add(UC_HOOK_MEM_READ,
                lambda _,a,addr,size,v,d: reads.append((addr,size)))
    uc.hook_add(UC_HOOK_MEM_WRITE,
                lambda _,a,addr,size,v,d: writes.append((addr,size,v&0xffffffff)))
    uc.emu_start(ICON_ENTRY, ICON_STOP+4, timeout=1_000_000, count=12)
    after_sp=STACK_TOP-9*4-0x24
    local_address=after_sp+0xc
    derived=(ICON_ENTRY+0x10+8+literals[0])&0xffffffff
    expected_reads=[(LITERAL_ADDRS[0],4),(LITERAL_ADDRS[1],4),
                    (local_address,4),(LITERAL_ADDRS[2],4),
                    (LITERAL_ADDRS[3],4)]
    saved_addresses=[STACK_TOP-9*4+4*j for j in range(9)]
    if trace!=list(range(ICON_ENTRY,ICON_STOP+4,4)) or (
            uc.reg_read(UC_ARM_REG_PC)!=ICON_STOP):
        raise AssertionError("Unexpected icon positioning entry PC trace")
    if reads!=expected_reads:
        raise AssertionError(f"Unexpected icon prologue reads {reads}")
    if (len(writes)!=10 or
            sorted(addr for addr,_,_ in writes)!=sorted(saved_addresses+[local_address])
            or (local_address,4,derived) not in writes):
        raise AssertionError(f"Unexpected icon prologue stores {writes}")
    for addr,value in zip(saved_addresses,SAVED_WORDS):
        if int.from_bytes(uc.mem_read(addr,4),"little")!=value:
            raise AssertionError("Saved ARM register word changed")
    if int.from_bytes(uc.mem_read(STACK_TOP-0x80,4),"little")!=CANARY:
        raise AssertionError("Stack canary was overwritten")
    if (uc.reg_read(UC_ARM_REG_SP)!=after_sp
            or uc.reg_read(UC_ARM_REG_R0)!=r0
            or uc.reg_read(UC_ARM_REG_R1)!=after_sp+0x1c
            or uc.reg_read(UC_ARM_REG_R2)!=derived
            or uc.reg_read(UC_ARM_REG_R3)!=literals[2]
            or uc.reg_read(UC_ARM_REG_R9)!=literals[3]
            or uc.reg_read(UC_ARM_REG_R10)!=literals[1]):
        raise AssertionError("Incorrect ARM PC-relative literal/stack setup")
    if (uc.reg_read(UC_ARM_REG_CPSR)&0xf0000000)!=(cpsr&0xf0000000):
        raise AssertionError("ARM prologue unexpectedly changed NZCV")
    return {"trace":trace,"stack_bytes":72,"derived":derived}


def run(binary):
    digest=hashlib.sha256(binary.read_bytes()).hexdigest()
    chain_code, sound, icon, literals=read_original(binary)
    sound_count=icon_count=0
    for argument in ARGUMENTS:
        for cpsr in branches.CPSR_STATES:
            sound_execute(chain_code,sound,argument,cpsr)
            icon_execute(icon,literals,argument,cpsr)
            sound_count+=1
            icon_count+=1
    return "\n".join([
        "# Bounded ARM sound dispatcher and icon-position prologue execution", "",
        f"ELF SHA-256: `{digest}`", "",
        "## SysSE_PlayDef(int) and preceding tail calls", "",
        "Three original unconditional ARM B trampolines followed by three "
        "SysSE_PlayDef instructions are executed. `r1 = input`, "
        "`r0 = 0`; `LR` and NZCV preserved and no data memory read/written.",
        f"**Sound dispatcher microexecutions: {sound_count}/{sound_count} PASS.**",
        "Stops **before** `0x2b2b7c`; no audio API effect established.", "",
        "## iOS_SetIconPosition() entry", "",
        "Ten original ARM instructions executed from `0x2b8900`; "
        "nine register saves (36 bytes), 36-byte local stack allocation, "
        "one verified local store/read, four PC-relative literal reads.",
        "Total stack-frame depth observed: 72 bytes.",
        f"**Icon prologue microexecutions: {icon_count}/{icon_count} PASS.**",
        "Stops **before** `0x2b8928`, its first indexed global-pointer "
        "dereference. Does not execute any deeper icon algorithm or BL.", "",
        "## Unknowns", "",
        "Original ARM code/literals are used; stack and register inputs "
        "are synthetic. Actual sound effects, global pointer contents, "
        "large-function control flow, runtime aliases and full-function "
        "semantic equivalence have **not** been established.", "",
    ])


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--binary",type=Path,
                   default=semantic_evidence.ROOT/"src/lib/armeabi/libgl2jni.so")
    p.add_argument("--results",type=Path,
                   default=semantic_evidence.ROOT/"docs/re-results")
    args=p.parse_args()
    report=args.results/"SEMANTIC_SOUND_ICON_MICROEXEC.md"
    report.write_text(run(args.binary),encoding="utf-8")
    print(f"Published original ARM sound/icon machine report: {report}")


if __name__=="__main__":
    main()
