#!/usr/bin/env python3
"""Evidence-only bounded trace of two unusual CEGL2_SHADER::Load callsites.

This static symbol-scoped disassembly cannot prove CFG reachability, exact
stack allocation size, runtime pointer provenance or NUL termination.
"""
import argparse
import hashlib
import json
from pathlib import Path

from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
from capstone.arm import ARM_INS_BL, ARM_OP_IMM
from semantic_a04_b6620_xrefs import scan_original
from semantic_a04_714a0_slot import SHA
import semantic_evidence

SITES = ("000ab6a4","000ab6cc")
TARGET = "000b6620"


def analyze(binary):
    if hashlib.sha256(binary.read_bytes()).hexdigest()!=SHA:
        raise ValueError("Original ARM ELF SHA mismatch")
    references=scan_original(binary)["direct_bl_candidates"]
    output=[]
    for addr in SITES:
        matched=[x for x in references if x["callsite"]==addr
                 and x["target"]==TARGET]
        if len(matched)!=1:
            raise ValueError("Expected exactly one shader A32 BL in original ELF")
        site=matched[0]
        owners=[s for s in site["symbol_owners"] if
                s["name"]=="_ZN12CEGL2_SHADER4LoadEiPKcS1_"]
        if len(owners)!=1:
            raise ValueError("Shader symbols missing in original ELF")
        sym=owners[0]
        begin=int(sym["start"],16)
        pos=int(addr,16)
        if begin>pos or pos-begin>0x1200:
            raise ValueError("Unbounded shader lookback in ELF")
        raw=semantic_evidence.read_function(binary,begin,pos-begin+4)
        md=Cs(CS_ARCH_ARM,CS_MODE_ARM)
        md.detail=True
        ops=list(md.disasm(raw,begin))
        if not ops or ops[-1].address!=pos or ops[-1].id!=ARM_INS_BL or (
                ops[-1].operands[0].type!=ARM_OP_IMM or
                ops[-1].operands[0].imm!=int(TARGET,16)):
            raise ValueError("Shader callsite not proven at original last PC")
        def row(x):
            return {"pc":f"{x.address:08x}","mnemonic":x.mnemonic,
                    "operands":x.op_str,"bytes":x.bytes.hex()}
        # Syntactic candidates: previous writes to R5/R6, changes to SP,
        # producer of R1 and final source of R0. Do not claim reaching defs.
        selected=[]
        for x in ops:
            operands=x.op_str.replace(" ","")
            writing_register=(x.mnemonic.startswith(("mov","ldr","add","sub"))
                              and operands.startswith(("r0,","r1,","r5,","r6,","sp,")))
            if writing_register or (x.mnemonic in ("push","pop","stmdb") and
                                    ("sp" in operands or x.mnemonic=="push")):
                selected.append(row(x))
        entries=[row(x) for x in ops[-18:]]
        before=selected[-45:]
        output.append({"callsite":addr,"owner":sym,"symbol_linear_instructions":len(ops),
                       "source_register_candidates":before,
                       "last_18_original_instructions":entries,
                       "branch_reachability_proven":False,
                       "stack_frame_size_proven":False,
                       "r0_capacity_proven":False,
                       "r1_source_max_length_proven":False})
    return {"schema":1,"elf_sha256":SHA,
            "callsite_count":len(output),"cases":output,
            "runtime_memory_safety_proven":False,"new_certificates":0}


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--binary",required=True,type=Path)
    p.add_argument("--checkpoint",required=True,type=Path)
    a=p.parse_args()
    data=analyze(a.binary)
    payload=json.dumps(data,indent=2,sort_keys=True)+"\n"
    a.checkpoint.parent.mkdir(parents=True,exist_ok=True)
    if a.checkpoint.exists() and a.checkpoint.read_text(encoding="utf-8")!=payload:
        raise ValueError("Original shader static provenance drift")
    a.checkpoint.write_text(payload,encoding="utf-8")
    for item in data["cases"]:
        print("A04_SHADER_SITE="+item["callsite"]+" "+item["owner"]["name"])
        for row in item["source_register_candidates"]:
            print("A04_SHADER_CANDIDATE "+row["pc"]+" "+row["mnemonic"]+" "+row["operands"])
    print("A04_SHADER_REAL_BUFFER_CAPACITY_PROVEN=0")
    print("A04_SHADER_R1_TERMINATION_PROVEN=0")

if __name__=="__main__":
    main()
