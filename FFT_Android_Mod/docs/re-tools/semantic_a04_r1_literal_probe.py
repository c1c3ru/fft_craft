#!/usr/bin/env python3
"""Original A04 0x20ca48 R1 producer: 12-byte copy and import provenance.

This is a static probe only. It does not assume source NUL, source bounds,
ABI success, literal address, or linear control flow until explicitly proven.
"""
import argparse
import hashlib
import json
from pathlib import Path

from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
from capstone.arm import (ARM_INS_ADD, ARM_INS_LDR, ARM_OP_REG, ARM_OP_IMM,
                          ARM_OP_MEM, ARM_REG_PC, ARM_REG_IP)
from elftools.elf.elffile import ELFFile
from elftools.elf.relocation import RelocationSection
from semantic_a04_714a0_slot import SHA
from semantic_a04_b6620_xrefs import scan_original
import semantic_evidence

CALLSITE=0x20ca48
COPY_CALL=0x20ca34
VENEER=0x714b8


def import_identity(binary):
    raw=semantic_evidence.read_function(binary,VENEER,12)
    cs=Cs(CS_ARCH_ARM,CS_MODE_ARM)
    cs.detail=True
    rows=list(cs.disasm(raw,VENEER))
    if len(rows)!=3 or [r.id for r in rows]!=[ARM_INS_ADD,ARM_INS_ADD,ARM_INS_LDR]:
        raise ValueError("Original 0x714b8 veneer does not match A32 ADD/ADD/LDR")
    a,b,c=rows
    def immediate(ins,source):
        ops=ins.operands
        if (len(ops)!=3 or ops[0].type!=ARM_OP_REG or ops[0].reg!=ARM_REG_IP
                or ops[1].type!=ARM_OP_REG or ops[1].reg!=source
                or ops[2].type!=ARM_OP_IMM):
            raise ValueError("Original veneer ADD changed")
        return int(ops[2].imm)
    d1=immediate(a,ARM_REG_PC)
    d2=immediate(b,ARM_REG_IP)
    ops=c.operands
    if (len(ops)!=2 or ops[0].type!=ARM_OP_REG or ops[0].reg!=ARM_REG_PC
            or ops[1].type!=ARM_OP_MEM or ops[1].mem.base!=ARM_REG_IP
            or not c.writeback):
        raise ValueError("Original veneer LDR PC changed")
    slot=(VENEER+8+d1+d2+int(ops[1].mem.disp))&0xffffffff
    matches=[]
    with binary.open("rb") as fh:
        elf=ELFFile(fh)
        for sec in elf.iter_sections():
            if not isinstance(sec,RelocationSection):
                continue
            syms=elf.get_section(int(sec["sh_link"]))
            for rel in sec.iter_relocations():
                if int(rel["r_offset"])!=slot:
                    continue
                sym=syms.get_symbol(int(rel["r_info_sym"]))
                matches.append({"slot":f"{slot:08x}","section":sec.name,
                                "type_id":int(rel["r_info_type"]),
                                "symbol":sym.name,
                                "symbol_type":str(sym["st_info"]["type"]),
                                "symbol_def":str(sym["st_shndx"])})
    if len(matches)!=1:
        raise ValueError(f"Expected exactly one original veneer relocation, got {len(matches)}")
    return matches[0]


def surrounding(binary):
    refs=scan_original(binary)["direct_bl_candidates"]
    matches=[r for r in refs if r["target"]=="000b6620"
             and int(r["callsite"],16)==CALLSITE]
    if len(matches)!=1:
        raise ValueError("A04 0x20ca48 direct BL not found")
    symbols=matches[0]["symbol_owners"]
    if not symbols:
        raise ValueError("Cannot establish original containing function")
    first=max(int(s["start"],16) for s in symbols)
    if CALLSITE-first > 0x1600:
        raise ValueError("Unbounded lookback")
    data=semantic_evidence.read_function(binary,first,CALLSITE-first+4)
    md=Cs(CS_ARCH_ARM,CS_MODE_ARM)
    md.detail=True
    ops=list(md.disasm(data,first))
    if not ops or ops[-1].address!=CALLSITE:
        raise ValueError("A32 symbol disassembly did not reach targeted BL")
    by={x.address:x for x in ops}
    expected={0x20c9e4:("sub","sp, sp, #0x11c"),
              0x20c9f8:("str","r0, [sp, #0x114]"),
              0x20ca04:("add","fp, sp, #0x10"),
              0x20ca18:("bl","#0x714a0"),
              0x20ca20:("bl","#0x71494"),
              0x20ca24:("ldr","r1, [pc, #0x17c]"),
              0x20ca28:("mov","r2, #0xc"),
              COPY_CALL:("bl","#0x714b8"),
              0x20ca38:("mov","r0, #0x10c"),
              0x20ca3c:("bl","#0x2cdf6c"),
              0x20ca40:("mov","r1, fp"),
              CALLSITE:("bl","#0xb6620")}
    for pc,(mn,operands) in expected.items():
        i=by.get(pc)
        if i is None or i.mnemonic!=mn or i.op_str!=operands:
            raise ValueError(f"Original copy/create/caller chain mutated at {pc:08x}")
    preceding=[x for x in ops if x.address<COPY_CALL]
    preceding=preceding[-36:]
    # LDR R1,[PC,#0x17c] at 0x20ca24 reads a little-endian
    # PC-relative displacement used by ADD R1,PC,R1 at 0x20ca30.
    literal_word_at = 0x20ca24 + 8 + 0x17c
    relative = int.from_bytes(semantic_evidence.read_function(binary,literal_word_at,4), "little")
    source_addr = (0x20ca30 + 8 + relative) & 0xffffffff
    source = semantic_evidence.read_function(binary,source_addr,12)
    nul = source.find(b"\\x00")
    # FP=SP+0x10; saved guard at SP+0x114. The address interval is
    # 0x104 (260) bytes, but does not by itself prove writable capacity.
    geometric_space = 0x114 - 0x10
    max_length_before_copy = geometric_space - 12
    return {"source_literal": {"ldr_literal_address":f"{literal_word_at:08x}",
                                "relative_u32":f"{relative:08x}",
                                "source_address":f"{source_addr:08x}",
                                "source_12_bytes_hex":source.hex(),
                                "first_nul_offset":nul if nul>=0 else None,
                                "nul_within_12_bytes":nul>=0},
            "preexisting_upstream_calls": {"strcpy_pltsite":"0020ca18",
                                           "strlen_pltsite":"0020ca20",
                                           "memcpy_pltsite":"0020ca34"},
            "stack_geometry": {"local_sp_offset":0x10,
                               "guard_sp_offset":0x114,
                               "bytes_until_guard":geometric_space,
                               "memcpy_bytes":12,
                               "required_initial_strlen_max":max_length_before_copy,
                               "actual_initial_strlen_bounded":False},
            "owner_symbols":symbols,
            "copy_bytes_immediate":12,
            "stack_local_source_candidate":"fp",
            "pre_copy_disassembly":[{"pc":f"{x.address:08x}",
                                     "mnemonic":x.mnemonic,
                                     "operands":x.op_str,
                                     "hex":x.bytes.hex()}
                                    for x in preceding],
            "context_after_copy":[{"pc":f"{x.address:08x}",
                                   "mnemonic":x.mnemonic,"operands":x.op_str}
                                  for x in ops if COPY_CALL<=x.address<=CALLSITE],
            "literal_source_bytes_verified":False,
            "nul_within_12_source_bytes_verified":False,
            "source_origin_bounds_verified":False,
            "reachable_path_verified":False}


def audit(binary):
    if hashlib.sha256(binary.read_bytes()).hexdigest()!=SHA:
        raise ValueError("Original ARM ELF SHA mismatch")
    return {"schema":1,"elf_sha256":SHA,
            "memcopy_import":import_identity(binary),
            "caller":surrounding(binary),
            "dynamic_copy_executed":False,
            "bounded_nul_proven":False,
            "new_certificates":0}


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--binary",required=True,type=Path)
    p.add_argument("--output",required=True,type=Path)
    a=p.parse_args()
    result=audit(a.binary)
    payload=json.dumps(result,sort_keys=True,indent=2)+"\n"
    a.output.parent.mkdir(parents=True,exist_ok=True)
    if a.output.exists() and a.output.read_text(encoding="utf-8")!=payload:
        raise ValueError("Original producer evidence changed")
    a.output.write_text(payload,encoding="utf-8")
    print("A04_SOURCE_COPY_IMPORT="+json.dumps(result["memcopy_import"]))
    print("A04_SOURCE_LITERAL="+json.dumps(result["caller"]["source_literal"]))
    print("A04_SOURCE_STACK_PRECONDITIONS="+json.dumps(result["caller"]["stack_geometry"]))
    for op in result["caller"]["pre_copy_disassembly"]:
        print("A04_SOURCE_PRECOPY "+op["pc"]+" "+op["mnemonic"]+" "+op["operands"])
    print("A04_SOURCE_NUL_PROVEN=0")


if __name__=="__main__":
    main()
