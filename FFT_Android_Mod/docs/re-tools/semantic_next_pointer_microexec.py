#!/usr/bin/env python3
"""Test bounded ELF machine effects at sound and icon pointer-dereference edges.

The original ARM opcodes and literal pool are used, with synthetic globals,
registers and stack. Stop BEFORE external BL at each boundary.
"""
import argparse
import hashlib
from pathlib import Path

from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
from unicorn import (Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_PROT_ALL,
                     UC_HOOK_CODE, UC_HOOK_MEM_READ, UC_HOOK_MEM_WRITE)
from unicorn.arm_const import (
    UC_ARM_REG_CPSR, UC_ARM_REG_PC, UC_ARM_REG_R0, UC_ARM_REG_R1,
    UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_R4, UC_ARM_REG_R5,
    UC_ARM_REG_R6, UC_ARM_REG_R7, UC_ARM_REG_R8, UC_ARM_REG_R9,
    UC_ARM_REG_R10, UC_ARM_REG_R11, UC_ARM_REG_LR, UC_ARM_REG_SP,
)

import semantic_evidence
import semantic_sound_icon_microexec as previous
import semantic_branch_microexec as branches

SOUND_START = 0x2B2B7C
SOUND_END = 0x2B2B98
SOUND_LITERAL_ADDR = 0x2B2CE8
SOUND_SIG = (
    ("push", "{r4, r5, r6, r7, r8, sb, sl, lr}"),
    ("ldr", "r3, [pc, #0x160]"),
    ("sub", "sp, sp, #0x20"),
    ("mov", "r6, r0"),
    ("mov", "r5, r1"),
    ("ldr", "r0, [pc, r3]"),
    ("mov", "r1, #0x28"),
)
ICON_START = previous.ICON_ENTRY
ICON_END = 0x2B8938
ICON_SUFFIX = (
    ("ldr", "r5, [r2, r3]"),
    ("add", "sl, pc, sl"),
    ("sub", "sl, sl, #0xe80"),
    ("mov", "r0, r5"),
)
ICON_SIG = previous.ICON_SIGNATURE + ICON_SUFFIX
ICON_LITERAL_ADDRS = previous.LITERAL_ADDRS
ARGS = (0, 1, 2, 0x34, 0xFFFFFFFF)
POINTER_VALUES = (0, 0x620000, 0xFFFFFFFF)
PAGE = 0x1000
STACK_TOP = previous.STACK_TOP
STACK_CANARY = previous.CANARY
WORD_LEFT = 0xABCD1234
WORD_RIGHT = 0xDCBA4321
SOUND_SAVED_REGS = (
    UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6,
    UC_ARM_REG_R7, UC_ARM_REG_R8, UC_ARM_REG_R9,
    UC_ARM_REG_R10, UC_ARM_REG_LR,
)
SOUND_SAVED = tuple(0xAA000000 + k for k in range(8))


def exact(code, start, signature):
    if len(code) != len(signature)*4:
        raise ValueError("Unexpected ARM prefix length")
    instructions = list(Cs(CS_ARCH_ARM, CS_MODE_ARM).disasm(code, start))
    if ([(i.mnemonic, i.op_str) for i in instructions] != list(signature)
            or [i.address for i in instructions] !=
            list(range(start, start + len(code), 4))):
        raise ValueError("Original ARM instruction signature changed")
    return instructions


def sound_word_addr(literal):
    return (0x2B2B90 + 8 + literal) & 0xFFFFFFFF


def icon_word_addr(literals):
    return ((ICON_START + 0x10 + 8 + literals[0]) + literals[2]) & 0xFFFFFFFF


def usable_slot(slot, protected):
    if slot % 4 or not 4 <= slot <= 0xFFFFFFF7:
        raise ValueError(f"Unaligned or out-of-range ELF indexed slot 0x{slot:x}")
    pages = {(addr & ~0xfff) for addr in (slot-4,slot,slot+4)}
    if pages & protected:
        raise ValueError("Derived global slot overlaps executable or stack page")
    return pages


def write32(emu, addr, value):
    emu.mem_write(addr, value.to_bytes(4,"little"))


def read32(emu, addr):
    return int.from_bytes(emu.mem_read(addr,4),"little")


def read_original(binary):
    sound = semantic_evidence.read_function(binary, SOUND_START, SOUND_END-SOUND_START)
    icon = semantic_evidence.read_function(binary, ICON_START, ICON_END-ICON_START)
    sound_lit = int.from_bytes(
        semantic_evidence.read_function(binary, SOUND_LITERAL_ADDR, 4),"little")
    icon_lits = tuple(int.from_bytes(
        semantic_evidence.read_function(binary,a,4),"little")
        for a in ICON_LITERAL_ADDRS)
    exact(sound,SOUND_START,SOUND_SIG)
    exact(icon,ICON_START,ICON_SIG)
    return sound, sound_lit, icon, icon_lits


def emulate_sound(code, literal, argument, table_word, cpsr):
    exact(code,SOUND_START,SOUND_SIG)
    if (argument not in ARGS or table_word not in POINTER_VALUES
            or cpsr not in branches.CPSR_STATES
            or not 0 <= literal <= 0xFFFFFFFF):
        raise ValueError("Invalid synthetic sound input")
    slot = sound_word_addr(literal)
    protected = {SOUND_START & ~0xfff, SOUND_LITERAL_ADDR & ~0xfff,
                 (STACK_TOP-64) & ~0xfff}
    slot_pages = usable_slot(slot,protected)
    emu=Uc(UC_ARCH_ARM,UC_MODE_ARM)
    for page in sorted(protected|slot_pages):
        emu.mem_map(page,PAGE,UC_PROT_ALL)
    emu.mem_write(SOUND_START,code)
    emu.mem_write(SOUND_END,bytes.fromhex("0000a0e1"))
    write32(emu,SOUND_LITERAL_ADDR,literal)
    for at,v in ((slot-4,WORD_LEFT),(slot,table_word),(slot+4,WORD_RIGHT)):
        write32(emu,at,v)
    write32(emu,STACK_TOP-0x80,STACK_CANARY)
    emu.reg_write(UC_ARM_REG_CPSR,cpsr)
    emu.reg_write(UC_ARM_REG_R0,0)       # SysSE_PlayDef forwards r0=0
    emu.reg_write(UC_ARM_REG_R1,argument)
    emu.reg_write(UC_ARM_REG_SP,STACK_TOP)
    for reg,val in zip(SOUND_SAVED_REGS,SOUND_SAVED):
        emu.reg_write(reg,val)
    trace,reads,writes=[],[],[]
    def on_code(machine,pc,size,unused):
        trace.append(pc)
        if pc==SOUND_END:machine.emu_stop()
    emu.hook_add(UC_HOOK_CODE,on_code)
    emu.hook_add(UC_HOOK_MEM_READ,
                 lambda _,a,pc,size,v,d: reads.append((pc,size)))
    emu.hook_add(UC_HOOK_MEM_WRITE,
                 lambda _,a,pc,size,v,d: writes.append((pc,size,v&0xFFFFFFFF)))
    emu.emu_start(SOUND_START,SOUND_END+4,timeout=1_000_000,count=10)
    expected_saved=[STACK_TOP-32+4*i for i in range(8)]
    if trace!=list(range(SOUND_START,SOUND_END+4,4)):
        raise AssertionError("Sound prefix PC trace differs")
    if reads!=[(SOUND_LITERAL_ADDR,4),(slot,4)]:
        raise AssertionError(f"Sound prefix memory reads differ: {reads}")
    if writes!=[(addr,4,word) for addr,word in zip(expected_saved,SOUND_SAVED)]:
        raise AssertionError(f"Sound prefix stack writes differ: {writes}")
    for addr,word in zip(expected_saved,SOUND_SAVED):
        if read32(emu,addr)!=word:
            raise AssertionError("ARM sound register save differs")
    for addr,word in ((slot-4,WORD_LEFT),(slot,table_word),(slot+4,WORD_RIGHT),
                      (STACK_TOP-0x80,STACK_CANARY)):
        if read32(emu,addr)!=word:
            raise AssertionError("Sound indexed slot or stack canary changed")
    if (emu.reg_read(UC_ARM_REG_PC)!=SOUND_END
            or emu.reg_read(UC_ARM_REG_SP)!=STACK_TOP-64
            or emu.reg_read(UC_ARM_REG_R0)!=table_word
            or emu.reg_read(UC_ARM_REG_R1)!=0x28
            or emu.reg_read(UC_ARM_REG_R3)!=literal
            or emu.reg_read(UC_ARM_REG_R5)!=argument
            or emu.reg_read(UC_ARM_REG_R6)!=0):
        raise AssertionError("Sound prefix call preparation registers differ")
    return {"slot":slot,"reads":reads,"writes":writes,"trace":trace}


def emulate_icon(code, literals, argument, table_word, cpsr):
    exact(code,ICON_START,ICON_SIG)
    if (argument not in ARGS or table_word not in POINTER_VALUES
            or cpsr not in branches.CPSR_STATES
            or len(literals)!=4 or any(not 0<=x<=0xFFFFFFFF for x in literals)):
        raise ValueError("Invalid synthetic icon input")
    slot=icon_word_addr(literals)
    code_page=ICON_START&~0xfff
    lit_page=ICON_LITERAL_ADDRS[0]&~0xfff
    stack_page=(STACK_TOP-72)&~0xfff
    slot_pages=usable_slot(slot,{code_page,lit_page,stack_page})
    emu=Uc(UC_ARCH_ARM,UC_MODE_ARM)
    for page in sorted({code_page,lit_page,stack_page}|slot_pages):
        emu.mem_map(page,PAGE,UC_PROT_ALL)
    emu.mem_write(ICON_START,code)
    emu.mem_write(ICON_END,bytes.fromhex("0000a0e1"))
    for at,val in zip(ICON_LITERAL_ADDRS,literals):
        write32(emu,at,val)
    for at,val in ((slot-4,WORD_LEFT),(slot,table_word),(slot+4,WORD_RIGHT)):
        write32(emu,at,val)
    write32(emu,STACK_TOP-0x80,STACK_CANARY)
    emu.reg_write(UC_ARM_REG_CPSR,cpsr)
    emu.reg_write(UC_ARM_REG_SP,STACK_TOP)
    emu.reg_write(UC_ARM_REG_R0,argument)
    for reg,val in zip(previous.SAVED_REGS,previous.SAVED_WORDS):
        emu.reg_write(reg,val)
    trace,reads,writes=[],[],[]
    def on_code(machine,pc,size,unused):
        trace.append(pc)
        if pc==ICON_END:machine.emu_stop()
    emu.hook_add(UC_HOOK_CODE,on_code)
    emu.hook_add(UC_HOOK_MEM_READ,
                 lambda _,a,pc,size,v,d: reads.append((pc,size)))
    emu.hook_add(UC_HOOK_MEM_WRITE,
                 lambda _,a,pc,size,v,d: writes.append((pc,size,v&0xFFFFFFFF)))
    emu.emu_start(ICON_START,ICON_END+4,timeout=1_000_000,count=16)
    saved=[STACK_TOP-36+4*i for i in range(9)]
    after_sp=STACK_TOP-72
    local=after_sp+0xC
    derived=(ICON_START+0x10+8+literals[0])&0xFFFFFFFF
    expected_reads=[(ICON_LITERAL_ADDRS[0],4),(ICON_LITERAL_ADDRS[1],4),
                    (local,4),(ICON_LITERAL_ADDRS[2],4),
                    (ICON_LITERAL_ADDRS[3],4),(slot,4)]
    if trace!=list(range(ICON_START,ICON_END+4,4)):
        raise AssertionError("Icon prefix PC trace differs")
    if reads!=expected_reads:
        raise AssertionError(f"Icon prefix memory reads differ: {reads}")
    if (len(writes)!=10 or sorted(a for a,_,_ in writes)!=sorted(saved+[local])
            or (local,4,derived) not in writes):
        raise AssertionError("Icon prefix stack writes differ")
    for addr,word in zip(saved,previous.SAVED_WORDS):
        if read32(emu,addr)!=word:
            raise AssertionError("Icon saved register changed")
    for addr,word in ((slot-4,WORD_LEFT),(slot,table_word),(slot+4,WORD_RIGHT),
                      (STACK_TOP-0x80,STACK_CANARY)):
        if read32(emu,addr)!=word:
            raise AssertionError("Icon global pointer slot/canary changed")
    expected_sl=((ICON_START+0x2c+8+literals[1])-0xe80)&0xFFFFFFFF
    if (emu.reg_read(UC_ARM_REG_PC)!=ICON_END
            or emu.reg_read(UC_ARM_REG_SP)!=after_sp
            or emu.reg_read(UC_ARM_REG_R0)!=table_word
            or emu.reg_read(UC_ARM_REG_R5)!=table_word
            or emu.reg_read(UC_ARM_REG_R2)!=derived
            or emu.reg_read(UC_ARM_REG_R10)!=expected_sl):
        raise AssertionError("Icon first-global-LDR or first-call argument differs")
    return {"slot":slot,"reads":reads,"writes":writes,"trace":trace}


def run(binary):
    digest=hashlib.sha256(binary.read_bytes()).hexdigest()
    sound,sound_lit,icon,icon_lits=read_original(binary)
    scores={"sound":0,"icon":0}
    for arg in ARGS:
        for word in POINTER_VALUES:
            for cpsr in branches.CPSR_STATES:
                emulate_sound(sound,sound_lit,arg,word,cpsr)
                emulate_icon(icon,icon_lits,arg,word,cpsr)
                scores["sound"]+=1
                scores["icon"]+=1
    return "\n".join([
        "# ARM sound and icon — bounded pointer dereference microexecution","",
        f"ELF SHA-256: `{digest}`","",
        "## SysSE_Play(int,int) prologue to first BL","",
        "Executes 7 original ARM instructions at `0x2b2b7c..0x2b2b94`. "
        "Saves 8 registers (32 bytes), reserves 32 more stack bytes, "
        "reads one PC-relative literal and one derived pointer. "
        "Pre-call `r0` equals synthetic indexed pointer word and `r1=0x28`.",
        f"Sound next-boundary microexecutions: **{scores['sound']}/{scores['sound']} PASS**.",
        "Stops **before** `BL 0x28c320` at `0x2b2b98`. "
        "No heap allocator, audio backend or sound playback was executed.", "",
        "## iOS_SetIconPosition() first global-pointer read","",
        "Executes 14 original ARM instructions from `0x2b8900` "
        "through `0x2b8934`, including `LDR r5, [r2,r3]` "
        "at `0x2b8928`. The indexed address comes from two original "
        "ELF literal words; adjacent canaries and 72-byte stack frame "
        "are verified. `r0` before call equals the controlled memory word.",
        f"Icon first-global-read microexecutions: **{scores['icon']}/{scores['icon']} PASS**.",
        "Stops **before** `BL 0xa6f28` at `0x2b8938`.", "",
        "## Limitations","",
        "Global words, stack and arguments are synthetic. "
        "The two external calls are **not executed**; the post-call "
        "effects and full function semantics remain unverified. "
        "These microexecutions do not establish equivalence.", "",
    ])


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--binary",type=Path,
                   default=semantic_evidence.ROOT/"src/lib/armeabi/libgl2jni.so")
    p.add_argument("--results",type=Path,
                   default=semantic_evidence.ROOT/"docs/re-results")
    a=p.parse_args()
    dest=a.results/"SEMANTIC_NEXT_POINTER_MICROEXEC.md"
    dest.write_text(run(a.binary),encoding="utf-8")
    print(f"Published {dest}")


if __name__=="__main__":
    main()
