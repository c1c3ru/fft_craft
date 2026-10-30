#!/usr/bin/env python3
"""B01: isolate original ELF POP {...,PC} from nine overlapping ARM groups.

The stack bytes and return addresses are synthetic. Correct 1-instruction
return under tested input does NOT prove caller stack-frame layout or whole CFG.
"""
import argparse
import ctypes
import hashlib
import json
import subprocess
import tempfile
from pathlib import Path

from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
from elftools.elf.elffile import ELFFile
from unicorn import (Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_PROT_ALL,
                     UC_HOOK_CODE, UC_HOOK_MEM_WRITE)
from unicorn.arm_const import (
    UC_ARM_REG_CPSR, UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2,
    UC_ARM_REG_R3, UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6,
    UC_ARM_REG_R7, UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10,
    UC_ARM_REG_R11, UC_ARM_REG_R12, UC_ARM_REG_SP, UC_ARM_REG_LR, UC_ARM_REG_PC,
)

import b01_overlap_elf_evidence as original
import b01_recursive_group_paths as cfg

STACK = 0x600000
STORAGE = 0x200
RETURN_PC = 0x730000
SEEDS = (0, 1, 0x7fffffff, 0xffffffff)
FLAGS = (0, 0xf0000000)
REG_IDS = (UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3,
           UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7,
           UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11,
           UC_ARM_REG_R12, UC_ARM_REG_SP, UC_ARM_REG_LR, UC_ARM_REG_PC)
MAX_UNIQUE = 64


def is_safe_pop(raw):
    if len(raw) != 4:
        return False
    word = int.from_bytes(raw,"little")
    return ((word & 0xffff0000) == 0xe8bd0000
            and (word & 0x8000) and not (word & 0x2000))


def c_model(path, dest):
    subprocess.run(["cc","-std=c11","-O2","-Wall","-Wextra","-Werror",
                    "-pedantic","-shared","-fPIC",str(path),"-o",str(dest)],
                   check=True,capture_output=True)
    lib=ctypes.CDLL(str(dest))
    fun=lib.b01_pop_pc_model
    fun.argtypes=[ctypes.c_uint32,ctypes.POINTER(ctypes.c_uint32),
                  ctypes.POINTER(ctypes.c_uint8),ctypes.c_size_t,
                  ctypes.POINTER(ctypes.c_uint32)]
    fun.restype=ctypes.c_int
    return fun


def compare_one(address, raw, fn, seed, flags):
    opcode=int.from_bytes(raw,"little")
    assert is_safe_pop(raw)
    mask=opcode & 0xffff
    initial=[(seed ^ (0x9e3779b9*i)) & 0xffffffff for i in range(16)]
    initial[13]=STACK
    initial[14]=0x740000
    words=mask.bit_count()
    stack=bytearray((seed + n*37) & 0xff for n in range(STORAGE))
    k=0
    for r in range(16):
        if mask & (1<<r):
            val=(RETURN_PC if r==15 else (seed ^ (r * 0x11223345)) & 0xffffffff)
            stack[k:k+4]=val.to_bytes(4,"little")
            k+=4
    before=bytes(stack)
    c_regs=(ctypes.c_uint32*16)(*initial)
    c_stack=(ctypes.c_uint8*STORAGE).from_buffer_copy(before)
    ret=ctypes.c_uint32()
    if fn(opcode,c_regs,c_stack,STORAGE,ctypes.byref(ret))!=0:
        raise AssertionError("C11 refused original POP PC")
    if ret.value!=RETURN_PC:
        raise AssertionError("Independent return model mismatch")
    expected=list(c_regs)
    uc=Uc(UC_ARCH_ARM,UC_MODE_ARM)
    for page in {address & ~0xfff,STACK,RETURN_PC}:
        uc.mem_map(page,0x1000,UC_PROT_ALL)
    uc.mem_write(address,raw)
    uc.mem_write(STACK,before)
    uc.mem_write(RETURN_PC,bytes(4))
    uc.reg_write(UC_ARM_REG_CPSR,0x10 | flags)
    for reg,val in zip(REG_IDS,initial):
        uc.reg_write(reg,val)
    executed, writes=[],[]
    uc.hook_add(UC_HOOK_CODE,lambda emu,pc,size,ctx:executed.append(pc))
    uc.hook_add(UC_HOOK_MEM_WRITE,
                lambda emu,kind,a,size,val,ctx:writes.append((a,size,val)))
    uc.emu_start(address,RETURN_PC,timeout=1_000_000,count=1)
    if executed!=[address] or uc.reg_read(UC_ARM_REG_PC)!=RETURN_PC:
        raise AssertionError("Original return did not branch through stack PC")
    if [uc.reg_read(r) for r in REG_IDS]!=expected:
        raise AssertionError("Original POP registers/SP mismatch vs C11")
    if writes or bytes(uc.mem_read(STACK,STORAGE))!=before:
        raise AssertionError("POP unexpectedly changed stack memory")
    if (uc.reg_read(UC_ARM_REG_CPSR)&0xf000003f)!=(flags|0x10):
        raise AssertionError("POP changed CPSR")
    return True


def audit(binary, inventory, model_path):
    if original.sha256(binary)!=original.PINNED_ELF_SHA:
        raise ValueError("Original ARM ELF SHA drift")
    state=cfg.audit(binary,inventory)
    occurrence=[]
    for group in state["groups"]:
        for witness in group["entry_witnesses"]:
            for unresolved in witness["unresolved_boundaries"]:
                if unresolved["reason"]=="return_via_stack_not_modeled":
                    occurrence.append((int(unresolved["at"],16),witness["entry"]))
    unique=sorted({addr for addr,_ in occurrence})
    if len(unique)>MAX_UNIQUE:
        raise ValueError("Stack return candidate budget exhausted")
    md=Cs(CS_ARCH_ARM,CS_MODE_ARM)
    md.detail=True
    with binary.open("rb") as file:
        elf=ELFFile(file)
        cases=[]
        for addr in unique:
            raw,offset=original.read_executable(elf,file,addr,4)
            if raw is None:
                raise ValueError("POP candidate bytes are missing")
            inst=list(md.disasm(raw,addr))
            enc_valid=bool(is_safe_pop(raw) and len(inst)==1
                           and inst[0].mnemonic=="pop"
                           and "pc" in inst[0].op_str)
            cases.append({"addr":addr,"raw":raw,"file_offset":offset,
                          "eligible":enc_valid})
    with tempfile.TemporaryDirectory(prefix="b01-pop-pc-") as tmp:
        fn=c_model(model_path,Path(tmp)/"pop.so")
        rows=[]
        for case in cases:
            n=0
            if case["eligible"]:
                for seed in SEEDS:
                    for flags in FLAGS:
                        compare_one(case["addr"],case["raw"],fn,seed,flags)
                        n+=1
            rows.append({
                "return_instruction_address":f"{case['addr']:08x}",
                "opcode_hex":case["raw"].hex(),
                "file_offset":case["file_offset"],
                "opcode_sha256":hashlib.sha256(case["raw"]).hexdigest(),
                "eligible_a32_pop_pc":case["eligible"],
                "register_mask":f"{int.from_bytes(case['raw'],'little')&0xffff:04x}",
                "original_vs_c11_samples_passed":n,
                "caller_stack_frame_proven":False,
                "function_semantics_certified":False})
    return {"schema":1,"stage":"B01","original_elf_sha256":original.PINNED_ELF_SHA,
            "stack_return_occurrences_in_recursive_paths":len(occurrence),
            "unique_pop_pc_addresses":len(rows),
            "eligible_stack_return_addresses":sum(r["eligible_a32_pop_pc"] for r in rows),
            "bounded_differentials_passed":sum(r["original_vs_c11_samples_passed"] for r in rows),
            "rows":rows,"stack_frame_layout_verified":False,
            "new_semantic_certificates":0,"B01_done":False}


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--binary",type=Path,required=True)
    p.add_argument("--inventory",type=Path,required=True)
    p.add_argument("--model",type=Path,default=Path(__file__).parent/"c-models/b01_pop_pc.c")
    p.add_argument("--output",type=Path,required=True)
    args=p.parse_args()
    x=audit(args.binary,args.inventory,args.model)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(x,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    for k in ("stack_return_occurrences_in_recursive_paths","unique_pop_pc_addresses",
              "eligible_stack_return_addresses","bounded_differentials_passed"):
        print("B01_POP_PC_"+k.upper()+"="+str(x[k]))
    print("B01_POP_PC_CALLER_STACK_PROVEN=0")


if __name__=="__main__":
    main()
