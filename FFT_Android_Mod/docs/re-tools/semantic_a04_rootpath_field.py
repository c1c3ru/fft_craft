#!/usr/bin/env python3
"""Original ARM CAPP_INFO::GetRootPath field contract and constructor links.

Executes ONLY the original eight-byte getter in Unicorn. Constructor and
PLT linkage are static evidence; no unknown import or initializer executes.
"""
import argparse
import hashlib
import json
from pathlib import Path

from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
from capstone.arm import (ARM_INS_ADD, ARM_INS_BX, ARM_INS_LDR,
                          ARM_OP_IMM, ARM_OP_MEM, ARM_OP_REG,
                          ARM_REG_IP, ARM_REG_PC)
from elftools.elf.elffile import ELFFile
from elftools.elf.relocation import RelocationSection
from elftools.elf.sections import SymbolTableSection
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_PROT_ALL, UC_HOOK_CODE, UC_HOOK_MEM_READ, UC_HOOK_MEM_WRITE
from unicorn.arm_const import (UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3,
                               UC_ARM_REG_SP, UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_CPSR)

import semantic_evidence
from semantic_a04_714a0_slot import SHA

GETTER=0x2b04f0
INITIALIZER=0x2b052c
FIELD=0x98
FIELD_SETUP=0x2b05c8
CALL_TO_PROVIDER=0x2b05d8
PROVIDER_VENEER=0x729e4
CALLER=0x20ca0c


def require_original(binary):
    if hashlib.sha256(binary.read_bytes()).hexdigest()!=SHA:
        raise ValueError("Original ARM ELF changed")
    raw=semantic_evidence.read_function(binary,GETTER,8)
    cs=Cs(CS_ARCH_ARM,CS_MODE_ARM)
    cs.detail=True
    ops=list(cs.disasm(raw,GETTER))
    if len(ops)!=2 or [op.id for op in ops] != [ARM_INS_ADD,ARM_INS_BX]:
        raise ValueError("Getter ARM instruction class drift")
    if ops[0].op_str!="r0, r0, #0x98" or ops[1].op_str!="lr":
        raise ValueError("Getter ARM operands drift")
    return raw


def emulate_getter(original):
    count=0
    for obj in (0x400000,0x500000,0x700000,0x7f0000,0x900000):
        for flags in (0,0x20000000,0x40000000,0xf0000000):
            em=Uc(UC_ARCH_ARM,UC_MODE_ARM)
            em.mem_map(GETTER&~0xfff,0x1000,UC_PROT_ALL)
            em.mem_map(0x710000,0x1000,UC_PROT_ALL)
            em.mem_write(GETTER,original)
            em.reg_write(UC_ARM_REG_CPSR,flags|0x10)
            setup=[(UC_ARM_REG_R0,obj),(UC_ARM_REG_R1,0x12345678),
                   (UC_ARM_REG_R2,0x87654321),(UC_ARM_REG_R3,0xdeadbeef),
                   (UC_ARM_REG_SP,0x600ffc),(UC_ARM_REG_LR,0x710000)]
            for reg,val in setup:
                em.reg_write(reg,val)
            pcs,reads,writes=[],[],[]
            def on_code(uc,addr,width,unused):
                pcs.append(addr)
                if addr==0x710000:
                    uc.emu_stop()
                elif addr not in (GETTER,GETTER+4):
                    raise AssertionError(f"Original getter unknown PC {addr:08x}")
            em.hook_add(UC_HOOK_CODE,on_code)
            em.hook_add(UC_HOOK_MEM_READ,lambda uc,k,a,w,v,u:reads.append((a,w)))
            em.hook_add(UC_HOOK_MEM_WRITE,lambda uc,k,a,w,v,u:writes.append((a,w)))
            em.emu_start(GETTER,0x710004,count=5,timeout=1000000)
            if pcs!=[GETTER,GETTER+4,0x710000] or reads or writes:
                raise AssertionError("Original getter instruction trace or memory differs")
            if em.reg_read(UC_ARM_REG_R0)!=obj+FIELD or em.reg_read(UC_ARM_REG_PC)!=0x710000:
                raise AssertionError("Original getter returned wrong field pointer")
            if any(em.reg_read(r)!=v for r,v in setup if r!=UC_ARM_REG_R0):
                raise AssertionError("Getter corrupted non-output register")
            if em.reg_read(UC_ARM_REG_CPSR)&0xf0000000 != flags:
                raise AssertionError("Getter altered NZCV")
            count+=1
    return count


def imported_symbol(binary):
    raw=semantic_evidence.read_function(binary,PROVIDER_VENEER,12)
    dis=Cs(CS_ARCH_ARM,CS_MODE_ARM)
    dis.detail=True
    ins=list(dis.disasm(raw,PROVIDER_VENEER))
    if len(ins)!=3 or [x.id for x in ins]!=[ARM_INS_ADD,ARM_INS_ADD,ARM_INS_LDR]:
        return {"address":f"{PROVIDER_VENEER:08x}",
                "veneer_contract":"not_standard_ADD_ADD_LDR",
                "disassembly":[f"{x.mnemonic} {x.op_str}" for x in ins],
                "relocation_identified":False}
    for row,src in ((ins[0],ARM_REG_PC),(ins[1],ARM_REG_IP)):
        ops=row.operands
        if (len(ops)!=3 or ops[0].type!=ARM_OP_REG or ops[0].reg!=ARM_REG_IP
                or ops[1].type!=ARM_OP_REG or ops[1].reg!=src
                or ops[2].type!=ARM_OP_IMM):
            raise ValueError("Original provider veneer ADD operands changed")
    op=ins[2].operands
    if (len(op)!=2 or op[0].type!=ARM_OP_REG or op[0].reg!=ARM_REG_PC
            or op[1].type!=ARM_OP_MEM or op[1].mem.base!=ARM_REG_IP
            or not ins[2].writeback):
        raise ValueError("Original provider veneer LDR changed")
    slot=(PROVIDER_VENEER+8 + int(ins[0].operands[2].imm)
          +int(ins[1].operands[2].imm)+int(op[1].mem.disp)) & 0xffffffff
    found=[]
    with binary.open("rb") as stream:
        elf=ELFFile(stream)
        for sec in elf.iter_sections():
            if not isinstance(sec,RelocationSection):
                continue
            syms=elf.get_section(int(sec["sh_link"]))
            for r in sec.iter_relocations():
                if int(r["r_offset"])!=slot:
                    continue
                sym=syms.get_symbol(int(r["r_info_sym"]))
                found.append({"section":sec.name,"type_id":int(r["r_info_type"]),
                              "symbol":sym.name,"defined":str(sym["st_shndx"])})
    if len(found)!=1:
        raise ValueError("Original provider veneer lacks one exact relocation")
    return {"veneer":f"{PROVIDER_VENEER:08x}","slot":f"{slot:08x}",
            "relocation":found[0],"import_executed":False}


def initializer_context(binary):
    size=0x1e0
    data=semantic_evidence.read_function(binary,INITIALIZER,size)
    md=Cs(CS_ARCH_ARM,CS_MODE_ARM)
    md.detail=True
    ins=list(md.disasm(data,INITIALIZER))
    by={x.address:x for x in ins}
    must={FIELD_SETUP:("add","r5, r4, #0x98"),
          0x2b05d0:("mov","r1, r5"),
          0x2b05d4:("mov","r0, r6"),
          CALL_TO_PROVIDER:("bl","#0x729e4")}
    for pc,(mn,ops) in must.items():
        inst=by.get(pc)
        if not inst or inst.mnemonic!=mn or inst.op_str!=ops:
            raise ValueError(f"Original initializer field setup differs at {pc:08x}")
    functions=[]
    with binary.open("rb") as stream:
        elf=ELFFile(stream)
        for sec in elf.iter_sections():
            if not isinstance(sec,SymbolTableSection):
                continue
            for s in sec.iter_symbols():
                if s["st_info"]["type"]!="STT_FUNC":
                    continue
                v=int(s["st_value"])&~1
                sz=int(s["st_size"])
                if v==INITIALIZER or (sz and v<=INITIALIZER<v+sz):
                    functions.append({"name":s.name,"start":f"{v:08x}",
                                      "size":sz})
    # Include all relevant branch paths and operations around the field,
    # with explicit no-CFG status: contextual disassembly, not a proof.
    window=[{"pc":f"{i.address:08x}","mnemonic":i.mnemonic,
             "operands":i.op_str,"hex":i.bytes.hex()}
            for i in ins if 0x2b05b4<=i.address<=0x2b06ec]
    return {"address":f"{INITIALIZER:08x}",
            "owners":functions,"field_setup":f"{FIELD_SETUP:08x}",
            "calls_field_provider_at":f"{CALL_TO_PROVIDER:08x}",
            "original_window_linear_not_cfg":window,
            "provider_return_semantics_not_executed":True,
            "branch_paths_not_proven":True}


def audit(binary):
    getter=require_original(binary)
    return {"schema":1,"elf_sha256":SHA,
            "getter":f"{GETTER:08x}","field_offset":FIELD,
            "original_getter_executions":emulate_getter(getter),
            "initializer":initializer_context(binary),
            "field_provider_import":imported_symbol(binary),
            "field_data_length_bound_proven":False,
            "field_is_nul_terminated_proven":False,
            "actual_android_initializer_executed":False,
            "new_certificates":0}


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--binary",required=True,type=Path)
    p.add_argument("--checkpoint",required=True,type=Path)
    a=p.parse_args()
    record=audit(a.binary)
    out=json.dumps(record,sort_keys=True,indent=2)+"\n"
    a.checkpoint.parent.mkdir(parents=True,exist_ok=True)
    if a.checkpoint.exists() and a.checkpoint.read_text(encoding="utf-8")!=out:
        raise ValueError("Original CAPP_INFO field checkpoint drift")
    a.checkpoint.write_text(out,encoding="utf-8")
    print("A04_ROOTPATH_GETTER_CASES="+str(record["original_getter_executions"]))
    print("A04_ROOTPATH_INITIALIZER="+json.dumps(record["initializer"]["owners"]))
    print("A04_ROOTPATH_FIELD_IMPORT="+json.dumps(record["field_provider_import"]))
    for ins in record["initializer"]["original_window_linear_not_cfg"]:
        print("A04_ROOTPATH_INIT_DISASM "+ins["pc"]+" "+ins["mnemonic"]+" "+ins["operands"])
    print("A04_ROOTPATH_NUL_BOUND_PROVEN=0")


if __name__=="__main__":
    main()
