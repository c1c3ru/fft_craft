#!/usr/bin/env python3
"""Original ARM function 0x729e4 invoked to fill CAPP_INFO rootpath.

Static bounded disassembly and original ELF symbol provenance. Does not
execute the helper or infer successful NUL termination/capacity from an enum.
"""
import argparse
import hashlib
import json
from pathlib import Path
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
from capstone.arm import ARM_INS_BL,ARM_INS_BLX,ARM_INS_B,ARM_INS_BX,ARM_OP_IMM,ARM_OP_MEM,ARM_REG_PC
from elftools.elf.elffile import ELFFile
from elftools.elf.sections import SymbolTableSection
import semantic_evidence
from semantic_a04_714a0_slot import SHA

ENTRY=0x729e4
CALLERS=(0x2b05d8,0x2b0610,0x2b063c,0x2b0674)
WINDOW=0x380


def inspect(binary):
    if hashlib.sha256(binary.read_bytes()).hexdigest()!=SHA:
        raise ValueError("Original helper ELF digest drift")
    original_symbols=[]
    with binary.open("rb") as fh:
        elf=ELFFile(fh)
        for section in elf.iter_sections():
            if not isinstance(section,SymbolTableSection):
                continue
            for symbol in section.iter_symbols():
                if symbol["st_info"]["type"]!="STT_FUNC":
                    continue
                addr=int(symbol["st_value"])&~1
                size=int(symbol["st_size"])
                if addr==ENTRY or (size and addr<=ENTRY<addr+size):
                    original_symbols.append({
                        "name":symbol.name,"start":f"{addr:08x}",
                        "size":size,"raw_value":f"{int(symbol['st_value']):08x}",
                        "thumb":bool(int(symbol["st_value"])&1),
                        "section":section.name})
    if any(s["thumb"] for s in original_symbols):
        raise ValueError("Helper may be Thumb, cannot safely A32-decode")
    md=Cs(CS_ARCH_ARM,CS_MODE_ARM)
    md.detail=True
    for callsite in CALLERS:
        raw=semantic_evidence.read_function(binary,callsite,4)
        op=list(md.disasm(raw,callsite))
        if (len(op)!=1 or op[0].id!=ARM_INS_BL or
             not op[0].operands or op[0].operands[0].type!=ARM_OP_IMM or
             op[0].operands[0].imm!=ENTRY):
            raise ValueError(f"Original initializer BL to helper drift at {callsite:x}")
    size=WINDOW
    matching=[s for s in original_symbols if int(s["start"],16)==ENTRY and s["size"]]
    if matching:
        size=min(WINDOW,max(s["size"] for s in matching))
        size=(size+3)&~3
    code=semantic_evidence.read_function(binary,ENTRY,size)
    ins=list(md.disasm(code,ENTRY))
    if not ins or ins[0].address!=ENTRY:
        raise ValueError("Invalid original ARM helper disassembly")
    calls,branches,mem,pc_literals=[],[],[],[]
    records=[]
    for i in ins:
        row={"pc":f"{i.address:08x}","hex":i.bytes.hex(),
             "mnemonic":i.mnemonic,"operands":i.op_str}
        records.append(row)
        if i.id in (ARM_INS_BL,ARM_INS_BLX):
            to=int(i.operands[0].imm)&0xffffffff if i.operands and i.operands[0].type==ARM_OP_IMM else None
            calls.append({"pc":row["pc"],"target":f"{to:08x}" if to is not None else None,
                          "type":i.mnemonic,"external_effects_unknown":True})
        elif i.id in (ARM_INS_B,ARM_INS_BX):
            to=int(i.operands[0].imm)&0xffffffff if i.operands and i.operands[0].type==ARM_OP_IMM else None
            branches.append({"pc":row["pc"],"target":f"{to:08x}" if to is not None else None,"type":i.mnemonic})
        for a in i.operands:
            if a.type!=ARM_OP_MEM:
                continue
            mem.append({"pc":row["pc"],"base":i.reg_name(a.mem.base),
                        "disp":int(a.mem.disp),"instruction":i.mnemonic})
            if a.mem.base==ARM_REG_PC and a.mem.index==0:
                literal=(i.address+8+int(a.mem.disp))&0xfffffffc
                try:
                    word=semantic_evidence.read_function(binary,literal,4)
                    pc_literals.append({"pc":row["pc"],"literal":f"{literal:08x}",
                                        "word":word.hex()})
                except ValueError:
                    pc_literals.append({"pc":row["pc"],"literal":f"{literal:08x}",
                                        "word":None})
    return {"schema":1,"elf_sha256":SHA,"entry":f"{ENTRY:08x}",
            "callers":[f"{x:08x}" for x in CALLERS],
            "symbols":original_symbols,"window_bytes":size,
            "linear_not_cfg":records,"calls":calls,"branches":branches,
            "memory_candidates":mem,"pc_literals":pc_literals,
            "r1_write_capacity_proven":False,
            "r1_nul_termination_proven":False,
            "helper_executed":False,"new_certificates":0}


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--binary",required=True,type=Path)
    p.add_argument("--checkpoint",required=True,type=Path)
    a=p.parse_args()
    record=inspect(a.binary)
    content=json.dumps(record,sort_keys=True,indent=2)+"\n"
    a.checkpoint.parent.mkdir(parents=True,exist_ok=True)
    if a.checkpoint.exists() and a.checkpoint.read_text(encoding="utf-8")!=content:
        raise ValueError("Original 0x729e4 helper evidence drift")
    a.checkpoint.write_text(content,encoding="utf-8")
    print("A04_PREFIX_HELPER_SYMBOLS="+json.dumps(record["symbols"]))
    print("A04_PREFIX_HELPER_CALLS="+json.dumps(record["calls"]))
    print("A04_PREFIX_HELPER_BRANCHES="+json.dumps(record["branches"]))
    print("A04_PREFIX_HELPER_LITERALS="+json.dumps(record["pc_literals"]))
    for row in record["linear_not_cfg"][:128]:
        print("A04_PREFIX_HELPER_DISASM "+row["pc"]+" "+row["mnemonic"]+" "+row["operands"])
    print("A04_PREFIX_HELPER_NUL_BOUND_PROVEN=0")


if __name__=="__main__":
    main()
