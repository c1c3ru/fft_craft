#!/usr/bin/env python3
"""Follow only direct unconditional ARM B trampolines from sound_request.

Never execute the first non-B instruction or unknown target. These machine
tests establish no audio playback, external side effect, ABI or equivalence.
"""
import argparse
import hashlib
from pathlib import Path

from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
from capstone.arm import ARM_CC_AL, ARM_INS_B, ARM_OP_IMM
from unicorn import (Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_PROT_ALL, UC_HOOK_CODE,
                     UC_HOOK_MEM_READ, UC_HOOK_MEM_WRITE)
from unicorn.arm_const import UC_ARM_REG_CPSR, UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_R0

import semantic_evidence
import semantic_branch_microexec as branches

ENTRY = 0x26B374
FIRST_TARGET = 0x2168E0
MAX_HOPS = 12
ARGUMENTS = (0, 1, 2, 0x34, 0xFFFFFFFF)
LR_SEED = 0x710100


def classify(word, address):
    md=Cs(CS_ARCH_ARM,CS_MODE_ARM)
    md.detail=True
    decoded=list(md.disasm(word,address))
    if len(word)!=4 or len(decoded)!=1 or decoded[0].size!=4:
        raise ValueError(f"ARM trampoline word undecodable at 0x{address:x}")
    ins=decoded[0]
    destination=(ins.operands[0].imm if ins.id==ARM_INS_B
                 and ins.cc==ARM_CC_AL
                 and len(ins.operands)==1
                 and ins.operands[0].type==ARM_OP_IMM else None)
    return ins, destination


def follow(binary):
    """Return exact B code and the first boundary that is not a known direct B."""
    pc=ENTRY
    traversed={}
    for depth in range(MAX_HOPS):
        if pc in traversed:
            raise ValueError(f"Cyclic unconditional ARM branch at 0x{pc:x}")
        if pc%4:
            raise ValueError("Unaligned direct branch target; Thumb not modeled")
        try:
            word=semantic_evidence.read_function(binary,pc,4)
        except ValueError:
            if not traversed:
                raise
            return traversed,pc,"target not covered by file-backed executable ELF"
        ins,dest=classify(word,pc)
        if dest is None:
            if not traversed:
                raise ValueError("Expected sound_request to be an unconditional ARM B")
            return traversed,pc,f"first non-B opcode: {ins.mnemonic} {ins.op_str}"
        if depth==0 and dest!=FIRST_TARGET:
            raise ValueError("sound_request no longer jumps to callSystemSound")
        traversed[pc]=(word,dest)
        pc=dest
    raise ValueError("Sound trampoline chain exceeds conservative hop bound")


def emulate(chain, boundary, argument, cpsr):
    if argument not in ARGUMENTS or cpsr not in branches.CPSR_STATES:
        raise ValueError("Unexpected synthetic argument or NZCV")
    if boundary in chain:
        raise ValueError("Boundary must not be executed as a B")
    if not chain or next(iter(chain))!=ENTRY:
        raise ValueError("The original sound_request jump is missing")
    for address,(word,target) in chain.items():
        _,observed=classify(word,address)
        if observed!=target:
            raise ValueError("ARM trampoline opcode/target mismatch")
    pages={address & ~0xfff for address in (*chain,boundary)}
    if len(pages)>MAX_HOPS+1:
        raise ValueError("Too many code mappings")
    uc=Uc(UC_ARCH_ARM,UC_MODE_ARM)
    for page in sorted(pages):
        uc.mem_map(page,0x1000,UC_PROT_ALL)
    for address,(word,_) in chain.items():
        uc.mem_write(address,word)
    uc.mem_write(boundary,bytes.fromhex("0000a0e1"))
    uc.reg_write(UC_ARM_REG_R0,argument)
    uc.reg_write(UC_ARM_REG_LR,LR_SEED)
    uc.reg_write(UC_ARM_REG_CPSR,cpsr)
    trace=[]
    reads=[]
    writes=[]
    def on_code(machine,address,size,unused):
        trace.append(address)
        if address==boundary:
            machine.emu_stop()
    def on_read(machine,access,address,size,value,unused):
        reads.append((address,size))
    def on_write(machine,access,address,size,value,unused):
        writes.append((address,size))
    uc.hook_add(UC_HOOK_CODE,on_code)
    uc.hook_add(UC_HOOK_MEM_READ,on_read)
    uc.hook_add(UC_HOOK_MEM_WRITE,on_write)
    uc.emu_start(ENTRY,0xffffffff,timeout=1_000_000,count=MAX_HOPS+2)
    expected=list(chain)+[boundary]
    if trace!=expected or uc.reg_read(UC_ARM_REG_PC)!=boundary:
        raise AssertionError(f"Unexpected sound branch chain: {list(map(hex,trace))}")
    if reads or writes:
        raise AssertionError("Direct B trampoline unexpectedly accessed data memory")
    if uc.reg_read(UC_ARM_REG_R0)!=argument or uc.reg_read(UC_ARM_REG_LR)!=LR_SEED:
        raise AssertionError("Unconditional tail branch unexpectedly altered arguments")
    if (uc.reg_read(UC_ARM_REG_CPSR) & 0xF0000000)!=(cpsr & 0xF0000000):
        raise AssertionError("Unconditional tail branch unexpectedly altered flags")
    return trace


def run(binary):
    digest=hashlib.sha256(binary.read_bytes()).hexdigest()
    chain,boundary,reason=follow(binary)
    cases=0
    for arg in ARGUMENTS:
        for cpsr in branches.CPSR_STATES:
            emulate(chain,boundary,arg,cpsr)
            cases+=1
    lines=["# sound_request — conservative ARM tail-branch chain", "",
           f"ELF SHA-256: \`{digest}\`", "",
           "Original executable ELF opcodes are followed only while each "
           "instruction is an unconditional ARM B with a direct target.", "",
           "| PC | Opcode word | Direct destination |",
           "|---|---|---|"]
    for pc,(word,target) in chain.items():
        lines.append(f"| \`0x{pc:x}\` | \`0x{int.from_bytes(word,'little'):08x}\` | "
                     f"\`0x{target:x}\` |")
    lines.extend(["",f"Stop **before** \`0x{boundary:x}\`: {reason}.", "",
                  f"**Sound tail-branch microexecutions: {cases}/{cases} PASS.**", "",
                  "## Verified scope and unknowns", "",
                  "- Only the direct-B trampoline opcodes are machine-executed; "
                  "the boundary instruction is not run.",
                  "- Register r0, LR and initial NZCV, plus the absence of "
                  "data reads and writes inside the trampoline, are tested.",
                  "- Actual sound playback, native APIs, system effects and "
                  "the code past the boundary are **not proven**.",
                  "- Inputs and the return address are synthetic. No "
                  "whole-function semantic equivalence is asserted.", ""])
    return "\n".join(lines)


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--binary",type=Path,
                   default=semantic_evidence.ROOT/"src/lib/armeabi/libgl2jni.so")
    p.add_argument("--results",type=Path,
                   default=semantic_evidence.ROOT/"docs/re-results")
    args=p.parse_args()
    dest=args.results/"SEMANTIC_SOUND_CHAIN.md"
    report=run(args.binary)
    dest.write_text(report,encoding="utf-8")
    print(report)
    print(f"Published {dest}")


if __name__=="__main__":
    main()
