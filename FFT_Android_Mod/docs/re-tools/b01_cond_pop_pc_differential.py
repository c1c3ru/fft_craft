#!/usr/bin/env python3
"""B01: 4 conditional A32 POP PC original ELF instructions vs independent C11.

Test taken AND not-taken NZCV states. The current stack is synthetic, and
the destination PC is never followed. Function-level certificates stay zero.
"""
import argparse
import ctypes
import hashlib
import json
import subprocess
import tempfile
from pathlib import Path

from elftools.elf.elffile import ELFFile
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM,UC_PROT_ALL,UC_HOOK_CODE,UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_ARM_REG_CPSR,UC_ARM_REG_PC

import b01_pop_pc_differential as prev
import b01_overlap_elf_evidence as baseline
import b01_recursive_group_paths as recursive

NZCV_STATES = tuple(n << 28 for n in range(16))
SEEDS = (0, 1, 0x7fffffff, 0xffffffff)


def is_conditional_pop(raw):
    if len(raw)!=4:
        return False
    word=int.from_bytes(raw,"little")
    cond=word>>28
    return (0<=cond<14
            and (word & 0x0fff0000)==0x08bd0000
            and (word & 0x8000)!=0
            and (word & 0x2000)==0)


def model_fn(base,conditional,output):
    subprocess.run(["cc","-std=c11","-O2","-Wall","-Wextra",
                    "-Werror","-pedantic","-shared","-fPIC",
                    str(base),str(conditional),"-o",str(output)],
                   check=True,capture_output=True)
    lib=ctypes.CDLL(str(output))
    fn=lib.b01_cond_pop_pc_model
    fn.argtypes=[ctypes.c_uint32,ctypes.POINTER(ctypes.c_uint32),
                 ctypes.POINTER(ctypes.c_uint8),ctypes.c_size_t,
                 ctypes.c_uint32,ctypes.c_uint32,
                 ctypes.POINTER(ctypes.c_uint32),ctypes.POINTER(ctypes.c_int)]
    fn.restype=ctypes.c_int
    return fn


def test_one(addr,raw,model,seed,flags):
    if not is_conditional_pop(raw):
        raise ValueError("Attempt to execute a non-whitelisted conditional POP PC")
    opcode=int.from_bytes(raw,"little")
    mask=opcode & 0xffff
    vals=[(seed ^ (r * 0x9e3779b9)) & 0xffffffff for r in range(16)]
    vals[13]=prev.STACK
    vals[14]=0x740000
    vals[15]=addr
    data=bytearray((seed + i*37) & 255 for i in range(prev.STORAGE))
    start=0
    for r in range(16):
        if mask & (1 << r):
            v=prev.RETURN_PC if r==15 else ((seed ^ (r*0x11223345)) & 0xffffffff)
            data[start:start+4]=v.to_bytes(4,"little")
            start+=4
    before=bytes(data)
    rbuf=(ctypes.c_uint32*16)(*vals)
    dbuf=(ctypes.c_uint8*prev.STORAGE).from_buffer_copy(before)
    nextpc=ctypes.c_uint32()
    taken=ctypes.c_int()
    rc=model(opcode,rbuf,dbuf,prev.STORAGE,flags|0x10,addr,
             ctypes.byref(nextpc),ctypes.byref(taken))
    if rc!=0:
        raise AssertionError("C11 condition model rejected original opcode")
    expected=list(rbuf)
    uc=Uc(UC_ARCH_ARM,UC_MODE_ARM)
    for page in {addr & ~0xfff,prev.STACK,prev.RETURN_PC}:
        uc.mem_map(page,0x1000,UC_PROT_ALL)
    uc.mem_write(addr,raw)
    uc.mem_write(prev.STACK,before)
    uc.mem_write(prev.RETURN_PC,bytes(4))
    uc.reg_write(UC_ARM_REG_CPSR,flags|0x10)
    for reg,v in zip(prev.REG_IDS,vals):
        uc.reg_write(reg,v)
    code_hits, writes=[],[]
    uc.hook_add(UC_HOOK_CODE,
                lambda u,pc,size,context:code_hits.append(pc))
    uc.hook_add(UC_HOOK_MEM_WRITE,
                lambda u,mode,at,length,v,context:writes.append((at,length)))
    # count=1 means the return destination is never executed.
    uc.emu_start(addr,nextpc.value,timeout=1_000_000,count=1)
    if code_hits != [addr]:
        raise AssertionError("Original conditional POP did not execute exactly one instruction")
    if [uc.reg_read(x) for x in prev.REG_IDS]!=expected:
        raise AssertionError("NZCV-conditioned POP registers/SP/PC diverged")
    if uc.reg_read(UC_ARM_REG_PC)!=nextpc.value:
        raise AssertionError("NZCV-conditioned next PC mismatch")
    if writes or bytes(uc.mem_read(prev.STACK,prev.STORAGE))!=before:
        raise AssertionError("Unexpected stack writes from POP")
    if (uc.reg_read(UC_ARM_REG_CPSR)&0xf000003f)!=(flags|0x10):
        raise AssertionError("CPSR flags/mode mutated")
    if taken.value not in (0,1) or (
            (nextpc.value == prev.RETURN_PC) != bool(taken.value)):
        raise AssertionError("Invalid condition/taken-state classification")
    return bool(taken.value)


def audit(binary,inventory,base_model,condition_model):
    if baseline.sha256(binary)!=baseline.PINNED_ELF_SHA:
        raise ValueError("Pinned original ELF SHA mismatch")
    state=recursive.audit(binary,inventory)
    sites=sorted({int(x["at"],16) for g in state["groups"]
                  for path in g["entry_witnesses"]
                  for x in path["unresolved_boundaries"]
                  if x["reason"]=="return_via_stack_not_modeled"})
    if len(sites)!=14:
        raise ValueError("Expected 14 distinct stack-return source sites")
    selected=[]
    with binary.open("rb") as f:
        elf=ELFFile(f)
        for addr in sites:
            raw,off=baseline.read_executable(elf,f,addr,4)
            if raw is None:
                raise ValueError("POP source not backed by ELF segment")
            if not prev.is_safe_pop(raw):
                if not is_conditional_pop(raw):
                    raise ValueError("Unsupported A32 return encoding must be audited explicitly")
                selected.append((addr,raw,off))
    if len(selected)!=4:
        raise ValueError("Expected four conditional POP PC encodings")
    with tempfile.TemporaryDirectory(prefix="b01-conditional-pop-") as tmp:
        model=model_fn(base_model,condition_model,Path(tmp)/"model.so")
        out=[]
        for addr,raw,off in selected:
            passed,taken,skipped=0,0,0
            for seed in SEEDS:
                for flags in NZCV_STATES:
                    is_taken=test_one(addr,raw,model,seed,flags)
                    taken+=int(is_taken)
                    skipped+=int(not is_taken)
                    passed+=1
            if not taken or not skipped:
                raise AssertionError("Conditional POP requires both NZCV branches")
            out.append({
                "instruction_address":f"{addr:08x}",
                "word_hex":raw.hex(),"file_offset":off,
                "opcode_sha256":hashlib.sha256(raw).hexdigest(),
                "condition_code":int.from_bytes(raw,"little")>>28,
                "scenarios_passed":passed,
                "condition_true_samples":taken,
                "condition_false_samples":skipped,
                "real_caller_stack_verified":False,
                "function_control_flow_proven":False})
    return {"schema":1,"stage":"B01","original_elf_sha256":baseline.PINNED_ELF_SHA,
            "unique_conditionally_returning_instructions":len(out),
            "scenarios_passed":sum(r["scenarios_passed"] for r in out),
            "condition_true_total":sum(r["condition_true_samples"] for r in out),
            "condition_false_total":sum(r["condition_false_samples"] for r in out),
            "evidence":out,"all_callers_verified":False,
            "certificates_issued":0,"B01_done":False}


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--binary",type=Path,required=True)
    p.add_argument("--inventory",type=Path,required=True)
    p.add_argument("--base-model",type=Path,default=Path(__file__).parent/"c-models/b01_pop_pc.c")
    p.add_argument("--conditional-model",type=Path,default=Path(__file__).parent/"c-models/b01_cond_pop_pc.c")
    p.add_argument("--output",type=Path,required=True)
    a=p.parse_args()
    report=audit(a.binary,a.inventory,a.base_model,a.conditional_model)
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(report,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print("B01_CONDITIONAL_POP_ADDRESSES="+str(report["unique_conditionally_returning_instructions"]))
    print("B01_CONDITIONAL_POP_DIFFERENTIALS="+str(report["scenarios_passed"]))
    print("B01_CONDITIONAL_POP_TAKEN="+str(report["condition_true_total"]))
    print("B01_CONDITIONAL_POP_NOT_TAKEN="+str(report["condition_false_total"]))
    print("B01_COMPLETE_CALLER_STACK_CERTIFICATES=0")


if __name__=="__main__":
    main()
