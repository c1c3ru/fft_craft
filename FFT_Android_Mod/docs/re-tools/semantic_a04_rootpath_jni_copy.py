#!/usr/bin/env python3
"""Original-ELF JNI system-path string copy and CAPP_INFO suffix literals.

This statically verifies A32 instructions and literal bytes. It does not
execute JNI, libc or unsafe copies and does not prove the Java path length.
"""
import argparse
import hashlib
import json
from pathlib import Path

from capstone import Cs,CS_ARCH_ARM,CS_MODE_ARM
from capstone.arm import ARM_OP_MEM,ARM_REG_PC
from semantic_a04_714a0_slot import SHA,decoded_slot,elf_provenance
import semantic_evidence

JNI_GET = 0x72a94
COPY=0x72aac
JNI_RELEASE=0x72abc
FIRST=0x2b05e4
SECOND=0x2b0680


def verify_jni_copy(binary):
    raw=semantic_evidence.read_function(binary,0x714a0,12)
    slot=decoded_slot(raw)
    if slot["slot"]!="00347d70":
        raise ValueError("Original strcpy GOT slot changed")
    p=elf_provenance(binary)["exact_relocations"]
    if (len(p)!=1 or p[0]["type"]!="R_ARM_JUMP_SLOT" or
            p[0]["symbol"]["name"]!="strcpy"):
        raise ValueError("Original strcpy import changed")
    cs=Cs(CS_ARCH_ARM,CS_MODE_ARM)
    instructions=list(cs.disasm(semantic_evidence.read_function(binary,0x72a88,0x40),0x72a88))
    by={i.address:i for i in instructions}
    required={
        0x72a88:("ldr","r3, [r5]"),
        0x72a8c:("mov","r2, #0"),
        0x72a90:("mov","r1, r4"),
        JNI_GET:("ldr","r3, [r3, #0x2a4]"),
        0x72a98:("mov","r0, r5"),
        0x72a9c:("blx","r3"),
        0x72aa0:("mov","r8, r0"),
        0x72aa4:("mov","r1, r8"),
        0x72aa8:("mov","r0, r6"),
        COPY:("bl","#0x714a0"),
        0x72ab0:("ldr","r3, [r5]"),
        0x72ab4:("mov","r2, r8"),
        0x72ab8:("mov","r1, r4"),
        JNI_RELEASE:("ldr","r3, [r3, #0x2a8]"),
        0x72ac0:("mov","r0, r5"),
        0x72ac4:("blx","r3"),
    }
    for pc,(name,operands) in required.items():
        i=by.get(pc)
        if not i or i.mnemonic!=name or i.op_str!=operands:
            raise ValueError(f"Original JNI-to-strcpy chain changed at {pc:x}")
    return [{"pc":f"{i.address:08x}","hex":i.bytes.hex(),
             "mnemonic":i.mnemonic,"operands":i.op_str}
            for i in instructions if i.address in required]


def original_suffix(binary,ldr_pc,add_pc):
    dis=Cs(CS_ARCH_ARM,CS_MODE_ARM)
    dis.detail=True
    i=list(dis.disasm(semantic_evidence.read_function(binary,ldr_pc,4),ldr_pc))
    j=list(dis.disasm(semantic_evidence.read_function(binary,add_pc,4),add_pc))
    if (len(i)!=1 or i[0].mnemonic!="ldr" or len(i[0].operands)!=2
            or i[0].operands[1].type!=ARM_OP_MEM
            or i[0].operands[1].mem.base!=ARM_REG_PC):
        raise ValueError("Original PC-relative literal LDR changed")
    if len(j)!=1 or j[0].mnemonic!="add" or j[0].op_str!="r1, pc, r1":
        raise ValueError("Original PC-relative literal ADD changed")
    lit=ldr_pc+8+int(i[0].operands[1].mem.disp)
    word=semantic_evidence.read_function(binary,lit,4)
    src=(add_pc+8+int.from_bytes(word,"little"))&0xffffffff
    text=semantic_evidence.read_function(binary,src,7)
    return {"ldr_pc":f"{ldr_pc:08x}",
            "offset_at":f"{lit:08x}","offset_word":word.hex(),
            "source_address":f"{src:08x}","source_bytes":text.hex(),
            "nul_at":text.find(b"\x00"),
            "ascii":text.decode("latin-1"),
            "nbytes":7,"original_bytes_verified":True}


def audit(binary):
    if hashlib.sha256(binary.read_bytes()).hexdigest()!=SHA:
        raise ValueError("Original ELF SHA changed")
    ops=verify_jni_copy(binary)
    suffixes=[original_suffix(binary,FIRST,0x2b05f0),
              original_suffix(binary,SECOND,0x2b068c)]
    return {"schema":1,"elf_sha256":SHA,
            "verified_jni_copy_instructions":ops,
            "candidate_jni_get_utf_chars_vtable_index":0x2a4//4,
            "candidate_jni_release_utf_chars_vtable_index":0x2a8//4,
            "initializer_suffixes":suffixes,
            "rootpath_object_field_offset":0x98,
            "following_object_field_offset":0x19c,
            "field_span_bytes":0x19c-0x98,
            "downstream_fftpack_prefix_max_bytes":248,
            "java_input_string_size_and_nul_proven":False,
            "android_jni_executed":False,
            "original_strcpy_executed":False,
            "new_certificates":0}


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--binary",type=Path,required=True)
    p.add_argument("--checkpoint",type=Path,required=True)
    a=p.parse_args()
    record=audit(a.binary)
    content=json.dumps(record,sort_keys=True,indent=2)+"\n"
    a.checkpoint.parent.mkdir(parents=True,exist_ok=True)
    if a.checkpoint.exists() and a.checkpoint.read_text(encoding="utf-8")!=content:
        raise ValueError("Original JNI rootpath copy checkpoint drift")
    a.checkpoint.write_text(content,encoding="utf-8")
    print("A04_JNI_STRING_SLOTS="+json.dumps([
          record["candidate_jni_get_utf_chars_vtable_index"],
          record["candidate_jni_release_utf_chars_vtable_index"]]))
    print("A04_ROOTPATH_INIT_SUFFIXES="+json.dumps(record["initializer_suffixes"]))
    print("A04_ROOTPATH_FIELD_SPAN="+str(record["field_span_bytes"]))
    print("A04_JNI_PREFIX_NUL_BOUND_PROVEN=0")


if __name__=="__main__":
    main()
