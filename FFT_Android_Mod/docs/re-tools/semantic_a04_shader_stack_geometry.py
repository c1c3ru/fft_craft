#!/usr/bin/env python3
"""Bounded original ARM shader stack-local buffer geometry, not runtime safety.

Confirms original A32 prologue, two local pointers, their BL callsites,
preservation of SP/local registers before the calls, and numeric frame bounds.
Does not execute shader or prove source NUL/length, exceptions, or JNI.
"""
import argparse
import hashlib
import json
from pathlib import Path
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
from capstone.arm import ARM_REG_SP, ARM_REG_R5, ARM_REG_R6, ARM_INS_BL
import semantic_evidence
from semantic_a04_714a0_slot import SHA

ENTRY = 0x000ab674
SITES = (0xab6a4,0xab6cc)
FRAME = 0x234
FIRST, SECOND = 0x14, 0x120
FIELD_END = 0x108
REQUIRED = {
    0xab674: ("push", "{r4, r5, r6, r7, r8, sb, sl, fp, lr}"),
    0xab67c: ("sub", "sp, sp, #0x234"),
    0xab680: ("add", "r5, sp, #0x14"),
    0xab694: ("mov", "r0, r5"),
    0xab6a4: ("bl", "#0xb6620"),
    0xab6c0: ("add", "r6, sp, #0x120"),
    0xab6c8: ("mov", "r0, r6"),
    0xab6cc: ("bl", "#0xb6620"),
}

def boundaries(frame=FRAME,first=FIRST,second=SECOND):
    if not (0 <= first < second < frame):
        raise ValueError("Invalid local buffer stack ordering")
    if first + FIELD_END > second or second + FIELD_END > frame:
        raise ValueError("A04 field extends beyond local stack partition")
    return {"frame_reserved_after_push":frame,
            "first_local_sp_offset":first,
            "first_max_to_second_local":second-first,
            "second_local_sp_offset":second,
            "second_max_to_frame_end":frame-second,
            "required_metadata_end":FIELD_END,
            "first_inside_frame":True,"second_inside_frame":True,
            "real_length_and_nul_proven":False}

def inspect(binary):
    if hashlib.sha256(binary.read_bytes()).hexdigest()!=SHA:
        raise ValueError("Original ELF SHA mismatch")
    data=semantic_evidence.read_function(binary,ENTRY,SITES[-1]-ENTRY+4)
    decoder=Cs(CS_ARCH_ARM,CS_MODE_ARM)
    decoder.detail=True
    inst=list(decoder.disasm(data,ENTRY))
    by={op.address:op for op in inst}
    if not inst or inst[-1].address != SITES[-1]:
        raise ValueError("Incomplete original ARM shader prologue disassembly")
    for addr,(m,o) in REQUIRED.items():
        if addr not in by or by[addr].mnemonic!=m or by[addr].op_str!=o:
            raise ValueError(f"Mutated original shader stack/call instruction 0x{addr:x}")

    # Track declared local registers as written by the exact ADD instructions,
    # and refuse other explicit changes before their respective callsite.
    for reg,start,site in ((ARM_REG_R5,0xab680,SITES[0]),
                           (ARM_REG_R6,0xab6c0,SITES[1])):
        for op in inst:
            if not (start < op.address < site):
                continue
            _,write=op.regs_access()
            if reg in write:
                raise ValueError(f"Original local pointer register overwritten: 0x{op.address:x}")

    # The local frame must keep the same SP between subtraction and both calls.
    for op in inst:
        if not (0xab67c < op.address < SITES[-1]):
            continue
        _,written=op.regs_access()
        if ARM_REG_SP in written:
            raise ValueError(f"Additional SP modification before shader BL: 0x{op.address:x}")

    return {"schema":1,"elf_sha256":SHA,
            "entry":f"{ENTRY:08x}",
            "calls":[{"site":f"{x:08x}","target":"000b6620",
                     "source_pointer":"r2" if x==SITES[0] else "sb",
                     "destination":"SP+0x14" if x==SITES[0] else "SP+0x120"}
                     for x in SITES],
            "geometry":boundaries(),
            "original_instructions_verified":len(REQUIRED),
            "candidate_pointer_registers_not_clobbered":True,
            "sp_constant_after_reservation_to_both_calls":True,
            "shader_runtime_executed":False,
            "actual_source_nul_or_max_proven":False,
            "stack_access_correct_for_all_cfg_paths":False,
            "new_certificates":0}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--binary",required=True,type=Path)
    p.add_argument("--checkpoint",required=True,type=Path)
    a=p.parse_args()
    result=inspect(a.binary)
    blob=json.dumps(result,sort_keys=True,indent=2)+"\n"
    a.checkpoint.parent.mkdir(parents=True,exist_ok=True)
    if a.checkpoint.exists() and a.checkpoint.read_text(encoding="utf-8")!=blob:
        raise ValueError("A04 shader stack geometry replay mismatch")
    a.checkpoint.write_text(blob,encoding="utf-8")
    print("A04_SHADER_STACK_GEOMETRY="+json.dumps(result["geometry"]))
    print("A04_SHADER_ORIGINAL_PREFIX_VERIFIED="+str(len(REQUIRED)))
    print("A04_SHADER_RUNTIME_NUL_BOUND_PROVEN=0")

if __name__=="__main__":
    main()
