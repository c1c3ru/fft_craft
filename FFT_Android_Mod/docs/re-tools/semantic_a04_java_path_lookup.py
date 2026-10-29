#!/usr/bin/env python3
"""Locate Java JNI class/method signatures behind Android_GetSystemPath.

Read original file-backed ELF literals and seven-entry method selector table.
File words are not assumed to be relocated runtime pointers. Does not
validate any runtime Java path length or execute JNI.
"""
import argparse
import hashlib
import json
from pathlib import Path
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
from elftools.elf.elffile import ELFFile
from elftools.elf.relocation import RelocationSection
import semantic_evidence
from semantic_a04_714a0_slot import SHA

LOOKUPS=((0x72a24,0x72a30,"class_candidate"),
         (0x72a54,0x72a64,"signature_candidate"))
TABLE_LDR=0x72a04
TABLE_ADD=0x72a0c
NAMES=7


def file_bytes(binary,address,size):
    with binary.open("rb") as stream:
        elf=ELFFile(stream)
        for seg in elf.iter_segments():
            if seg["p_type"]!="PT_LOAD":
                continue
            v=int(seg["p_vaddr"]);length=int(seg["p_filesz"])
            if v<=address and address+size<=v+length:
                stream.seek(int(seg["p_offset"])+address-v)
                data=stream.read(size)
                if len(data)!=size:
                    raise ValueError("Truncated ELF load segment")
                return data
    raise ValueError(f"Original file-backed ELF address unavailable: {address:08x}")


def static_string(binary,address):
    try:
        raw=file_bytes(binary,address,128)
    except ValueError:
        return {"address":f"{address:08x}","file_backed":False}
    ending=raw.find(b"\x00")
    if ending<0:
        return {"address":f"{address:08x}","file_backed":True,
                "nul_in_first_128_bytes":False}
    content=raw[:ending]
    return {"address":f"{address:08x}","file_backed":True,
            "nul_offset":ending,"bytes_hex":content.hex(),
            "ascii_escaped":content.decode("utf-8","backslashreplace"),
            "string_is_static_identifier_not_runtime_path":True}


def resolve_pc_relative(binary,ldr,add):
    dis=Cs(CS_ARCH_ARM,CS_MODE_ARM)
    seq=list(dis.disasm(semantic_evidence.read_function(binary,ldr,4),ldr))
    second=list(dis.disasm(semantic_evidence.read_function(binary,add,4),add))
    if len(seq)!=1 or len(second)!=1 or not seq[0].mnemonic.startswith("ldr"):
        raise ValueError(f"Original JNI literal LDR changed at {ldr:x}")
    if second[0].mnemonic!="add":
        raise ValueError(f"Original JNI literal ADD changed at {add:x}")
    dis.detail=True
    from capstone.arm import ARM_OP_MEM, ARM_REG_PC
    detail=list(dis.disasm(semantic_evidence.read_function(binary,ldr,4),ldr))[0]
    ops=detail.operands
    if len(ops)!=2 or ops[1].type!=ARM_OP_MEM or ops[1].mem.base!=ARM_REG_PC:
        raise ValueError("JNI literal address is no longer PC-relative")
    addr=ldr+8+int(ops[1].mem.disp)
    word=file_bytes(binary,addr,4)
    result=(add+8+int.from_bytes(word,"little"))&0xffffffff
    return {"load":f"{ldr:08x}","add":f"{add:08x}",
            "literal":f"{addr:08x}","word_hex":word.hex(),
            "resolved":f"{result:08x}"}


def get_table_relocs(binary,base):
    hits=[]
    with binary.open("rb") as stream:
        elf=ELFFile(stream)
        for section in elf.iter_sections():
            if not isinstance(section,RelocationSection):
                continue
            symbol_table=elf.get_section(int(section["sh_link"]))
            for r in section.iter_relocations():
                off=int(r["r_offset"])
                if not (base<=off<base+NAMES*4):
                    continue
                sym=symbol_table.get_symbol(int(r["r_info_sym"]))
                hits.append({"offset":f"{off:08x}","reloc_type":int(r["r_info_type"]),
                             "section":section.name,"symbol":sym.name})
    return hits


def audit(binary):
    if hashlib.sha256(binary.read_bytes()).hexdigest()!=SHA:
        raise ValueError("Original ELF SHA mismatch")
    lookups=[]
    for ldr,add,label in LOOKUPS:
        row=resolve_pc_relative(binary,ldr,add)
        row["role"]=label
        row["static_identifier"]=static_string(binary,int(row["resolved"],16))
        lookups.append(row)
    table=resolve_pc_relative(binary,TABLE_LDR,TABLE_ADD)
    base=int(table["resolved"],16)
    raw=file_bytes(binary,base,NAMES*4)
    reloc=get_table_relocs(binary,base)
    entries=[]
    for i in range(NAMES):
        word=int.from_bytes(raw[i*4:i*4+4],"little")
        entries.append({"selector":i,"file_word":f"{word:08x}",
                        "runtime_relocation_may_change":True,
                        "static_word_as_possible_pointer":static_string(binary,word),
                        "relocations_at_entry":[r for r in reloc if int(r["offset"],16)==base+i*4]})
    return {"schema":1,"elf_sha256":SHA,
            "jni_literals":lookups,
            "selector_table_pointer":table,
            "selector_table_file_bytes":raw.hex(),
            "selector_entries":entries,
            "selector_relocations":reloc,
            "jni_method_resolution_executed":False,
            "java_runtime_path_length_known":False,
            "max_242_java_bytes_proven":False,
            "new_certificates":0}


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--binary",type=Path,required=True)
    p.add_argument("--checkpoint",type=Path,required=True)
    a=p.parse_args()
    record=audit(a.binary)
    body=json.dumps(record,sort_keys=True,indent=2)+"\n"
    a.checkpoint.parent.mkdir(parents=True,exist_ok=True)
    if a.checkpoint.exists() and a.checkpoint.read_text(encoding="utf-8")!=body:
        raise ValueError("Original Java path symbol checkpoint drift")
    a.checkpoint.write_text(body,encoding="utf-8")
    print("A04_JAVA_LOOKUPS="+json.dumps(record["jni_literals"]))
    print("A04_JAVA_SELECTOR_TABLE="+json.dumps(record["selector_table_pointer"]))
    print("A04_JAVA_SELECTOR_ENTRIES="+json.dumps(record["selector_entries"]))
    print("A04_JAVA_RELCS="+json.dumps(record["selector_relocations"]))
    print("A04_JAVA_RUNTIME_PATH_BOUND_PROVEN=0")


if __name__=="__main__":
    main()
