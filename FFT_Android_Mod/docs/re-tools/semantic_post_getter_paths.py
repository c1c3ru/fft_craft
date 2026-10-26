#!/usr/bin/env python3
"""Continue original sound/icon caller execution after GetParam/GetScale BX LR.

Execute original BL, entire tiny callee, return, then caller branches or
argument preparation. Stop BEFORE unmodeled BL/return blocks. Synthetic
table/object/stack inputs; no whole-function semantic equivalence.
"""
import argparse
import hashlib
from pathlib import Path

from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
from unicorn import (Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_PROT_ALL,
                     UC_HOOK_CODE, UC_HOOK_MEM_READ, UC_HOOK_MEM_WRITE)
from unicorn.arm_const import (
    UC_ARM_REG_CPSR, UC_ARM_REG_LR, UC_ARM_REG_PC,
    UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3,
    UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_SP,
)

import semantic_evidence
import semantic_branch_microexec as branches
import semantic_getparam_getscale_exec as getter

SOUND_CALL=0x2B2B98
SOUND_BOUNDARY=0x2B2BB0
SOUND_ZERO=0x2B2BC0
SOUND_BORROW=0x2B2BC8
SOUND_NEXT_BL=0x2B2BAC
SOUND_SIG=(
    ("bl", "#0x28c320"),
    ("cmp", "r0, #0"),
    ("beq", "#0x2b2bc0"),
    ("subs", "r4, r5, #1"),
    ("blo", "#0x2b2bc8"),
    ("bl", "#0x2bf008"),
)
ICON_CALL=0x2B8938
ICON_NEXT_BL=0x2B8948
ICON_END=0x2B894C
ICON_SIG=(
    ("bl", "#0xa6f28"),
    ("add", "r2, sp, #0x18"),
    ("mov", "r0, r5"),
    ("add", "r1, sp, #0x14"),
    ("bl", "#0xa7034"),
)
TABLE=getter.TABLE
SOURCE=getter.SOURCE
STACK=0x700FB8
LR_SEED=0x710100
OBJECT_SEED=0x44445555
CANARY_LEFT=0xAABB3322
CANARY_RIGHT=0x2233BBAA
OUTPUT_CANARY=0xEEDDCCBB
SOUND_R5=(0,1,43)
WORDS=getter.WORDS
PAGE=0x1000


def exact(code, start, sig):
    if len(code)!=len(sig)*4:
        raise ValueError("Truncated original caller code")
    got=list(Cs(CS_ARCH_ARM,CS_MODE_ARM).disasm(code,start))
    if ([i.address for i in got]!=list(range(start,start+len(code),4))
            or [(i.mnemonic,i.op_str) for i in got]!=list(sig)):
        raise ValueError("Original caller post-getter opcode signature changed")


def originals(binary):
    code={
        "sound":semantic_evidence.read_function(binary,SOUND_CALL,
                                                 SOUND_BOUNDARY-SOUND_CALL),
        "icon":semantic_evidence.read_function(binary,ICON_CALL,
                                                ICON_END-ICON_CALL),
        "param":semantic_evidence.read_function(binary,getter.GET_PARAM,12),
        "scale":semantic_evidence.read_function(binary,getter.GET_SCALE,16),
    }
    validate(code)
    return code


def validate(code):
    if set(code)!={"sound","icon","param","scale"}:
        raise ValueError("Missing or unexpected real ARM segments")
    exact(code["sound"],SOUND_CALL,SOUND_SIG)
    exact(code["icon"],ICON_CALL,ICON_SIG)
    getter.exact_opcode(code["param"],getter.GET_PARAM,getter.PARAM_SIG)
    getter.exact_opcode(code["scale"],getter.GET_SCALE,getter.SCALE_SIG)
    getter.exact_bl(code["sound"][:4],SOUND_CALL,getter.GET_PARAM)
    getter.exact_bl(code["icon"][:4],ICON_CALL,getter.GET_SCALE)
    return True


def page(addr):
    return addr & ~(PAGE-1)


def write(uc,address,value):
    uc.mem_write(address,int(value).to_bytes(4,"little"))


def word(uc,address):
    return int.from_bytes(uc.mem_read(address,4),"little")


def hooked(uc,start,end,stops):
    trace,reads,writes=[],[],[]
    def on_code(machine,address,size,unused):
        trace.append(address)
        if address in stops:
            machine.emu_stop()
    uc.hook_add(UC_HOOK_CODE,on_code)
    uc.hook_add(UC_HOOK_MEM_READ,
                lambda _,a,address,size,v,d: reads.append((address,size)))
    uc.hook_add(UC_HOOK_MEM_WRITE,
                lambda _,a,address,size,value,d: writes.append(
                    (address,size,value & ((1 << (size*8))-1))))
    uc.emu_start(start,end,timeout=1_000_000,count=18)
    return trace,reads,writes


def sound(code,value,sound_id,cpsr):
    validate(code)
    if value not in WORDS or sound_id not in SOUND_R5 or cpsr not in branches.CPSR_STATES:
        raise ValueError("Unmodeled sound state")
    slot=TABLE+(0x28+14)*4
    uc=Uc(UC_ARCH_ARM,UC_MODE_ARM)
    for base in (page(SOUND_CALL),page(getter.GET_PARAM),page(TABLE)):
        uc.mem_map(base,PAGE,UC_PROT_ALL)
    uc.mem_write(SOUND_CALL,code["sound"])
    uc.mem_write(getter.GET_PARAM,code["param"])
    for point in (SOUND_ZERO,SOUND_BORROW):
        uc.mem_write(point,bytes.fromhex("0000a0e1"))
    for address,val in (
        (TABLE,CANARY_LEFT),(slot-4,CANARY_LEFT),
        (slot,value),(slot+4,CANARY_RIGHT)):
        write(uc,address,val)
    uc.reg_write(UC_ARM_REG_CPSR,cpsr)
    uc.reg_write(UC_ARM_REG_R0,TABLE)
    uc.reg_write(UC_ARM_REG_R1,0x28)
    uc.reg_write(UC_ARM_REG_R2,getter.R2_SEED)
    uc.reg_write(UC_ARM_REG_R3,getter.R3_SEED)
    uc.reg_write(UC_ARM_REG_R4,OBJECT_SEED)
    uc.reg_write(UC_ARM_REG_R5,sound_id)
    uc.reg_write(UC_ARM_REG_LR,LR_SEED)

    dest = SOUND_ZERO if value==0 else SOUND_BORROW if sound_id==0 else SOUND_NEXT_BL
    trace,reads,writes=hooked(uc,SOUND_CALL,0xFFFFFFFF,
                              {SOUND_ZERO,SOUND_BORROW,SOUND_NEXT_BL})
    expected=([SOUND_CALL]+list(range(getter.GET_PARAM,getter.GET_PARAM+12,4))
              +[0x2B2B9C,0x2B2BA0]
              +([] if value==0 else [0x2B2BA4,0x2B2BA8])
              +[dest])
    if trace!=expected or uc.reg_read(UC_ARM_REG_PC)!=dest:
        raise AssertionError(f"Incorrect GetParam/caller branch path {list(map(hex,trace))}")
    if reads!=[(slot,4)] or writes:
        raise AssertionError(f"Unexpected GetParam caller memory access {reads}/{writes}")
    for address,want in ((TABLE,CANARY_LEFT),(slot-4,CANARY_LEFT),
                         (slot,value),(slot+4,CANARY_RIGHT)):
        if word(uc,address)!=want:
            raise AssertionError("GetParam caller changed table or neighbor")
    if (uc.reg_read(UC_ARM_REG_R0)!=value
            or uc.reg_read(UC_ARM_REG_R1)!=0x36
            or uc.reg_read(UC_ARM_REG_R5)!=sound_id
            or uc.reg_read(UC_ARM_REG_LR)!=0x2B2B9C
            or uc.reg_read(UC_ARM_REG_R4)!=(
                OBJECT_SEED if value==0 else (sound_id-1)&0xFFFFFFFF)):
        raise AssertionError("GetParam caller decision registers differ")
    return {"dest":dest,"trace":trace,"reads":reads}


def icon(code,value,cpsr):
    validate(code)
    if value not in WORDS or cpsr not in branches.CPSR_STATES:
        raise ValueError("Unmodeled icon state")
    input_pointer=SOURCE
    output=STACK+0x1C
    uc=Uc(UC_ARCH_ARM,UC_MODE_ARM)
    for base in (page(ICON_CALL),page(getter.GET_SCALE),page(SOURCE),page(STACK)):
        uc.mem_map(base,PAGE,UC_PROT_ALL)
    uc.mem_write(ICON_CALL,code["icon"])
    uc.mem_write(getter.GET_SCALE,code["scale"])
    for at,v in (
        (SOURCE,CANARY_LEFT),(SOURCE+4,value),(SOURCE+8,CANARY_RIGHT),
        (STACK+0x10,OUTPUT_CANARY),(STACK+0x14,OUTPUT_CANARY),
        (STACK+0x18,OUTPUT_CANARY),(STACK+0x1C,0x55AA55AA),
        (STACK+0x20,OUTPUT_CANARY)):
        write(uc,at,v)
    uc.reg_write(UC_ARM_REG_CPSR,cpsr)
    uc.reg_write(UC_ARM_REG_R0,SOURCE)
    uc.reg_write(UC_ARM_REG_R1,output)
    uc.reg_write(UC_ARM_REG_R2,getter.R2_SEED)
    uc.reg_write(UC_ARM_REG_R3,getter.R3_SEED)
    uc.reg_write(UC_ARM_REG_R5,input_pointer)
    uc.reg_write(UC_ARM_REG_SP,STACK)
    uc.reg_write(UC_ARM_REG_LR,LR_SEED)

    trace,reads,writes=hooked(uc,ICON_CALL,0xFFFFFFFF,{ICON_NEXT_BL})
    expected=([ICON_CALL]+list(range(getter.GET_SCALE,getter.GET_SCALE+16,4))
              +[0x2B893C,0x2B8940,0x2B8944,ICON_NEXT_BL])
    if trace!=expected or uc.reg_read(UC_ARM_REG_PC)!=ICON_NEXT_BL:
        raise AssertionError(f"Wrong GetScale/caller path: {list(map(hex,trace))}")
    if reads!=[(SOURCE+4,4)] or writes!=[(output,4,value)]:
        raise AssertionError(f"Wrong GetScale linked memory: {reads}/{writes}")
    for at,want in (
        (SOURCE,CANARY_LEFT),(SOURCE+4,value),(SOURCE+8,CANARY_RIGHT),
        (STACK+0x10,OUTPUT_CANARY),(STACK+0x14,OUTPUT_CANARY),
        (STACK+0x18,OUTPUT_CANARY),(output,value),(STACK+0x20,OUTPUT_CANARY)):
        if word(uc,at)!=want:
            raise AssertionError("GetScale caller affected unrelated state")
    if (uc.reg_read(UC_ARM_REG_R0)!=SOURCE
            or uc.reg_read(UC_ARM_REG_R1)!=STACK+0x14
            or uc.reg_read(UC_ARM_REG_R2)!=STACK+0x18
            or uc.reg_read(UC_ARM_REG_R3)!=value
            or uc.reg_read(UC_ARM_REG_SP)!=STACK
            or uc.reg_read(UC_ARM_REG_LR)!=0x2B893C):
        raise AssertionError("Incorrect GetScale next-call arguments")
    return {"dest":ICON_NEXT_BL,"trace":trace,"reads":reads,"writes":writes}


def run(binary):
    digest=hashlib.sha256(binary.read_bytes()).hexdigest()
    code=originals(binary)
    counts={"sound_zero":0,"sound_borrow":0,"sound_next":0,"icon":0}
    for value in WORDS:
        for sound_id in SOUND_R5:
            for cpsr in branches.CPSR_STATES:
                result=sound(code,value,sound_id,cpsr)
                key=("sound_zero" if result["dest"]==SOUND_ZERO else
                     "sound_borrow" if result["dest"]==SOUND_BORROW else "sound_next")
                counts[key]+=1
    for value in WORDS:
        for cpsr in branches.CPSR_STATES:
            icon(code,value,cpsr)
            counts["icon"]+=1
    assert counts=={"sound_zero":6,"sound_borrow":6,"sound_next":12,"icon":8}
    total=sum(counts.values())
    return "\n".join([
        "# GetParam/GetScale — next caller branches and arguments","",
        f"ELF SHA-256: `{digest}`","",
        "Original ARM BL/callee/BX LR and following caller instructions "
        "are microexecuted with synthetic table, object and stack state. "
        "The next unresolved calls or return blocks are **not executed**.","",
        "| Boundary reached | Sampled paths | Contract before boundary |",
        "|---|---:|---|",
        f'| sound: `0x{SOUND_ZERO:x}` | {counts["sound_zero"]} | '
        "GetParam returns zero; BEQ selects early exit block |",
        f'| sound: `0x{SOUND_BORROW:x}` | {counts["sound_borrow"]} | '
        "Nonzero parameter with r5=0; SUBS/BLO selects the alternate branch |",
        f'| sound: `0x{SOUND_NEXT_BL:x}` | {counts["sound_next"]} | '
        "Nonzero parameter and r5>=1; next BL 0x2bf008 not executed |",
        f'| icon: `0x{ICON_NEXT_BL:x}` | {counts["icon"]} | '
        "GetScale copied synthetic 32-bit word to SP+0x1c; next call "
        "r0=source, r1=SP+0x14, r2=SP+0x18 |",
        "", f"**Post-getter ARM microexecutions: {total}/{total} PASS.**","",
        "Every sample checks the actual instruction PC path, return address, "
        "memory reads/writes and neighboring word canaries.","",
        "## Limitations","",
        "- The table, pointed-to object and stack are controlled synthetic inputs.",
        "- `SysSE_Play` exit blocks and its next BL are not executed.",
        "- The next `iOS_SetIconPosition` BL at `0x2b8948` is not executed.",
        "- No sound output, UI placement or whole-function equivalence is proven.","",
    ])


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--binary",type=Path,
                   default=semantic_evidence.ROOT/"src/lib/armeabi/libgl2jni.so")
    p.add_argument("--results",type=Path,
                   default=semantic_evidence.ROOT/"docs/re-results")
    a=p.parse_args()
    dest=a.results/"SEMANTIC_POST_GETTER_PATHS.md"
    dest.write_text(run(a.binary),encoding="utf-8")
    print(f"Generated {dest}")


if __name__=="__main__":
    main()
