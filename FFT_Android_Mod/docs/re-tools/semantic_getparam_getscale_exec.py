#!/usr/bin/env python3
"""Execute two original ARM getters and their exact BL callsites in Unicorn.

Modes are standalone (synthetic LR) and linked (original BL + callee + return
to next caller instruction). Never execute the next caller instruction.
All object/table words are controlled synthetic inputs.
"""
import argparse
import hashlib
from pathlib import Path

from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
from unicorn import (Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_PROT_ALL, UC_HOOK_CODE,
                     UC_HOOK_MEM_READ, UC_HOOK_MEM_WRITE)
from unicorn.arm_const import (
    UC_ARM_REG_CPSR, UC_ARM_REG_LR, UC_ARM_REG_PC,
    UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3,
)
import semantic_branch_microexec as branches
import semantic_evidence
import semantic_getparam_getscale as audit

GET_PARAM = 0x28C320
GET_SCALE = 0x0A6F28
PARAM_CALLSITE = 0x2B2B98
SCALE_CALLSITE = 0x2B8938
SYNTH_RETURN = 0x710100
TABLE = 0x620100
SOURCE = 0x620100
OUTPUT = 0x630100
WORD_LEFT = 0xC0DEC0DE
WORD_RIGHT = 0xDEADC0DE
OUTPUT_CANARY = 0xDEAD1234
INITIAL_OUTPUT = 0xAABBCCDD
R2_SEED = 0x22223333
R3_SEED = 0x33334444
INDICES = (0, 1, 0x28, 100)
WORDS = (0, 1, 0x12345678, 0xFFFFFFFF)
MODES = ("standalone", "linked")
PARAM_SIG = (
    ("add", "r1, r1, #0xe"),
    ("ldr", "r0, [r0, r1, lsl #2]"),
    ("bx", "lr"),
)
SCALE_SIG = (
    ("cmp", "r1, #0"),
    ("ldrne", "r3, [r0, #4]"),
    ("strne", "r3, [r1]"),
    ("bx", "lr"),
)
PAGE_SIZE = 0x1000


def exact_opcode(raw, start, signature):
    if len(raw) != len(signature)*4:
        raise ValueError("ARM getter length changed")
    md = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    got = list(md.disasm(raw, start))
    if ([i.address for i in got] != list(range(start,start+len(raw),4))
            or [(i.mnemonic,i.op_str) for i in got] != list(signature)):
        raise ValueError("Original ARM getter opcode signature changed")


def exact_bl(raw, source, target):
    from capstone.arm import ARM_INS_BL, ARM_OP_IMM
    md = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    md.detail = True
    got = list(md.disasm(raw, source))
    if (len(raw)!=4 or len(got)!=1 or got[0].id!=ARM_INS_BL
            or len(got[0].operands)!=1 or got[0].operands[0].type!=ARM_OP_IMM
            or got[0].operands[0].imm!=target):
        raise ValueError(f"Original BL target changed at 0x{source:x}")


def _page(addr):
    return addr & ~(PAGE_SIZE-1)


def _seed(uc, addr, value):
    uc.mem_write(addr, int(value).to_bytes(4,"little"))


def _read(uc, addr):
    return int.from_bytes(uc.mem_read(addr,4),"little")


def _execute(raw, bl, entry, source, signature, linked, r0, r1,
             setup_words, end_state, expected_reads, expected_writes, cpsr):
    exact_opcode(raw,entry,signature)
    exact_bl(bl,source,entry)
    if cpsr not in branches.CPSR_STATES or linked not in MODES:
        raise ValueError("Unrecognized CPSR seed or invocation mode")
    stop = source+4 if linked == "linked" else SYNTH_RETURN
    protected = {_page(a) for a in (entry,source,stop)}
    data_pages = {_page(a) for a,_ in setup_words}
    if protected & data_pages:
        raise ValueError("Input data aliases executable or return memory")
    uc=Uc(UC_ARCH_ARM,UC_MODE_ARM)
    for page in sorted(protected | data_pages):
        uc.mem_map(page,PAGE_SIZE,UC_PROT_ALL)
    uc.mem_write(entry,raw)
    uc.mem_write(source,bl)
    uc.mem_write(stop,bytes.fromhex("0000a0e1"))
    for addr,value in setup_words:
        _seed(uc,addr,value)
    uc.reg_write(UC_ARM_REG_CPSR,cpsr)
    uc.reg_write(UC_ARM_REG_R0,r0)
    uc.reg_write(UC_ARM_REG_R1,r1)
    uc.reg_write(UC_ARM_REG_R2,R2_SEED)
    uc.reg_write(UC_ARM_REG_R3,R3_SEED)
    uc.reg_write(UC_ARM_REG_LR,SYNTH_RETURN)
    trace,reads,writes=[],[],[]
    def on_code(machine,pc,size,unused):
        trace.append(pc)
        if pc == stop:
            machine.emu_stop()
    uc.hook_add(UC_HOOK_CODE,on_code)
    uc.hook_add(UC_HOOK_MEM_READ,
                lambda _,a,addr,size,v,d: reads.append((addr,size)))
    uc.hook_add(UC_HOOK_MEM_WRITE,
                lambda _,a,addr,size,v,d: writes.append(
                    (addr,size,v & ((1 << (8*size))-1))))
    start = source if linked == "linked" else entry
    uc.emu_start(start,0xFFFFFFFF,timeout=1_000_000,count=8)
    expected_trace = ([source] if linked=="linked" else []) + [
        *range(entry,entry+len(raw),4),stop]
    if trace!=expected_trace or uc.reg_read(UC_ARM_REG_PC)!=stop:
        raise AssertionError(f"Wrong linked ARM path: {list(map(hex,trace))}")
    if reads!=expected_reads or writes!=expected_writes:
        raise AssertionError(f"Memory effects differ: reads={reads}, writes={writes}")
    for addr,w in end_state.items():
        if _read(uc,addr)!=w:
            raise AssertionError(f"Getter modified memory outside contract at 0x{addr:x}")
    expected_lr=(source+4 if linked=="linked" else SYNTH_RETURN)
    if uc.reg_read(UC_ARM_REG_LR)!=expected_lr:
        raise AssertionError("Original BX LR/BL did not preserve expected link")
    if uc.reg_read(UC_ARM_REG_R2)!=R2_SEED:
        raise AssertionError("Unrelated r2 changed")
    return uc


def getparam(raw,bl,index,value,cpsr,linked):
    if index not in INDICES or value not in WORDS:
        raise ValueError("Unmodeled GetParam input")
    slot = TABLE+4*(index+14)
    state={
        TABLE: WORD_LEFT, slot-4: WORD_LEFT,
        slot: value,slot+4:WORD_RIGHT,
    }
    setup=list(state.items())
    uc=_execute(raw,bl,GET_PARAM,PARAM_CALLSITE,PARAM_SIG,
                linked,TABLE,index,setup,state,[(slot,4)],[],cpsr)
    if (uc.reg_read(UC_ARM_REG_R0)!=value
            or uc.reg_read(UC_ARM_REG_R1)!=index+14
            or uc.reg_read(UC_ARM_REG_R3)!=R3_SEED
            or (uc.reg_read(UC_ARM_REG_CPSR)&0xF0000000)
            !=(cpsr&0xF0000000)):
        raise AssertionError("GetParam indexed return/flags contract differs")
    return {"slot":slot, "value":value, "linked":linked}


def getscale(raw,bl,value,output_nonnull,cpsr,linked):
    if value not in WORDS or type(output_nonnull) is not bool:
        raise ValueError("Unmodeled GetScale input")
    out = OUTPUT if output_nonnull else 0
    state={
        SOURCE: WORD_LEFT,
        SOURCE+4: value,
        SOURCE+8: WORD_RIGHT,
        OUTPUT-4: OUTPUT_CANARY,
        OUTPUT: value if output_nonnull else INITIAL_OUTPUT,
        OUTPUT+4: OUTPUT_CANARY,
    }
    setup=list(state.items())
    setup[-2]=(OUTPUT,INITIAL_OUTPUT)
    uc=_execute(raw,bl,GET_SCALE,SCALE_CALLSITE,SCALE_SIG,
                linked,SOURCE,out,setup,state,
                [(SOURCE+4,4)] if output_nonnull else [],
                [(OUTPUT,4,value)] if output_nonnull else [],cpsr)
    expected_nzcv=0x20000000 if output_nonnull else 0x60000000
    if (uc.reg_read(UC_ARM_REG_R0)!=SOURCE
            or uc.reg_read(UC_ARM_REG_R1)!=out
            or uc.reg_read(UC_ARM_REG_R3)!=
            (value if output_nonnull else R3_SEED)
            or uc.reg_read(UC_ARM_REG_CPSR)&0xF0000000!=expected_nzcv):
        raise AssertionError("GetScale conditional copy/flags contract differs")
    return {"value":value,"written":output_nonnull,"linked":linked}


def run(binary):
    digest=hashlib.sha256(binary.read_bytes()).hexdigest()
    data={}
    for address,length,_,site in audit.TARGETS:
        name = "param" if address == GET_PARAM else "scale"
        data[name]=(
            semantic_evidence.read_function(binary,address,length),
            semantic_evidence.read_function(binary,site,4),
        )
    counts={"param":0,"scale":0}
    for mode in MODES:
        for idx in INDICES:
            for word in WORDS:
                for cpsr in branches.CPSR_STATES:
                    getparam(*data["param"],idx,word,cpsr,mode)
                    counts["param"]+=1
        for word in WORDS:
            for present in (False,True):
                for cpsr in branches.CPSR_STATES:
                    getscale(*data["scale"],word,present,cpsr,mode)
                    counts["scale"]+=1
    assert counts=={"param":64,"scale":32}
    return "\n".join([
        "# Original ARM GetParam / GetScale — microexecuted contracts","",
        f"ELF SHA-256: `{digest}`","",
        "Two invocation modes are tested: from each callee entry with a "
        "synthetic LR, or through the actual original caller **BL**. "
        "The experiment stops on return before the next caller instruction.","",
        "## CFFT_STATE::GetParam(int)","",
        "Three original ARM opcodes: add 14 to r1, load indexed word "
        "from the r0 base table with a four-byte stride, return via BX LR. "
        "Verified exact data read, r0 return, r1 change, other register/flag "
        "preservation and neighboring canaries.",
        f"**GetParam microexecutions: {counts['param']}/{counts['param']} PASS.**","",
        "## CGX_SCREEN_CORRECT::GetScale(float*)","",
        "Four original ARM opcodes: CMP output pointer with zero; "
        "only if non-null, load a word at r0+4 and store to [r1], "
        "then return via BX LR. Null output performs no data reads/stores. "
        "Verified destination, conditional state, NZCV flags and canaries.",
        f"**GetScale microexecutions: {counts['scale']}/{counts['scale']} PASS.**","",
        f"**Combined GetParam/GetScale microexecutions: {sum(counts.values())}/"
        f"{sum(counts.values())} PASS.**","",
        "## Unverified","",
        "- Table contents and object/float destination are synthetic inputs.",
        "- No caller code after the returning BL was executed.",
        "- Sound playback and UI effects after these getters remain unknown.",
        "- Tested local effects are NOT a complete semantic-equivalence proof.",
        "",
    ])


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--binary",type=Path,
                   default=semantic_evidence.ROOT/"src/lib/armeabi/libgl2jni.so")
    p.add_argument("--results",type=Path,
                   default=semantic_evidence.ROOT/"docs/re-results")
    args=p.parse_args()
    path=args.results/"SEMANTIC_GETPARAM_GETSCALE_MICROEXEC.md"
    path.write_text(run(args.binary),encoding="utf-8")
    print(f"Published {path}")


if __name__=="__main__":
    main()
