#!/usr/bin/env python3
"""A04: inspect original ELF prefix provider 0x002b04f0 for bounded NUL.

The caller 0x0020ca0c invokes this function, then passes its return to
strcpy. Static structural evidence only; no Android runtime, no libc
execution and no unsupported safety or reachability claim.
"""
import argparse
import hashlib
import json
from pathlib import Path

from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM, CS_MODE_THUMB
from capstone.arm import (ARM_INS_B, ARM_INS_BL, ARM_INS_BX, ARM_INS_BLX,
                          ARM_OP_IMM, ARM_OP_MEM, ARM_REG_PC)
from elftools.elf.elffile import ELFFile
from elftools.elf.sections import SymbolTableSection
import semantic_evidence
from semantic_a04_714a0_slot import SHA

ENTRY = 0x2b04f0
CALLSITE = 0x20ca0c
SCAN_BYTES = 256


def inspect(binary):
    if hashlib.sha256(binary.read_bytes()).hexdigest() != SHA:
        raise ValueError("Original A04 ELF SHA-256 mismatch")
    caller_data = semantic_evidence.read_function(binary, CALLSITE, 4)
    caller_cs = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    caller_cs.detail = True
    caller = list(caller_cs.disasm(caller_data, CALLSITE))
    if (len(caller) != 1 or caller[0].id != ARM_INS_BL or
            not caller[0].operands or
            caller[0].operands[0].type != ARM_OP_IMM or
            caller[0].operands[0].imm != ENTRY):
        raise ValueError("Original caller does not directly BL 0x2b04f0")
    functions = []
    owning_segments = []
    with binary.open("rb") as handle:
        elf = ELFFile(handle)
        if elf.elfclass != 32 or elf["e_machine"] != "EM_ARM":
            raise ValueError("Expected original 32-bit ARM ELF")
        for segment in elf.iter_segments():
            start = int(segment["p_vaddr"])
            size = int(segment["p_filesz"])
            if segment["p_type"] == "PT_LOAD" and start <= ENTRY < start+size:
                owning_segments.append({
                    "vaddr":f"{start:08x}", "p_filesz":size,
                    "p_flags":int(segment["p_flags"])})
        for section in elf.iter_sections():
            if not isinstance(section, SymbolTableSection):
                continue
            for symbol in section.iter_symbols():
                if symbol["st_info"]["type"] != "STT_FUNC":
                    continue
                start = int(symbol["st_value"]) & ~1
                size = int(symbol["st_size"])
                if start == ENTRY or (size and start <= ENTRY < start+size):
                    functions.append({
                        "name":symbol.name,"table":section.name,
                        "start":f"{start:08x}","size":size,
                        "st_value":f"{int(symbol['st_value']):08x}",
                        "thumb":bool(int(symbol["st_value"]) & 1)})
    modes = [bool(i["thumb"]) for i in functions if int(i["start"],16)==ENTRY]
    if modes and any(modes) and any(not m for m in modes):
        raise ValueError("Symbol mode ambiguity; refuse false A32 assumption")
    thumb = bool(modes and all(modes))
    if thumb:
        raise ValueError("Original prefix provider is Thumb; A32 audit must be redesigned")
    raw = semantic_evidence.read_function(binary, ENTRY, SCAN_BYTES)
    cs = Cs(CS_ARCH_ARM,CS_MODE_ARM)
    cs.detail=True
    decoded = list(cs.disasm(raw, ENTRY))
    if not decoded or decoded[0].address != ENTRY:
        raise ValueError("Original ARM provider could not be decoded")
    instructions=[]
    calls=[]
    branches=[]
    mem=[]
    pc_literals=[]
    for op in decoded:
        record={"pc":f"{op.address:08x}","hex":op.bytes.hex(),
                "mnemonic":op.mnemonic,"operands":op.op_str}
        instructions.append(record)
        if op.id in (ARM_INS_BL,ARM_INS_BLX):
            tgt=(int(op.operands[0].imm)&0xffffffff
                 if op.operands and op.operands[0].type==ARM_OP_IMM else None)
            calls.append({"pc":record["pc"],"kind":op.mnemonic,
                          "target":f"{tgt:08x}" if tgt is not None else None,
                          "called_semantics_verified":False})
        if op.id in (ARM_INS_B,ARM_INS_BX):
            tgt=(int(op.operands[0].imm)&0xffffffff
                 if op.operands and op.operands[0].type==ARM_OP_IMM else None)
            branches.append({"pc":record["pc"],"kind":op.mnemonic,
                             "target":f"{tgt:08x}" if tgt is not None else None})
        for operand in op.operands:
            if operand.type==ARM_OP_MEM:
                item={"pc":record["pc"],"mnemonic":op.mnemonic,
                      "base":op.reg_name(operand.mem.base),
                      "disp":operand.mem.disp}
                mem.append(item)
                if operand.mem.base==ARM_REG_PC and operand.mem.index==0:
                    literal=(op.address+8+int(operand.mem.disp))&0xffffffff
                    literal&=~3
                    try:
                        word=semantic_evidence.read_function(binary,literal,4)
                        pc_literals.append({"pc":record["pc"],"address":f"{literal:08x}",
                                            "raw":word.hex(),"word":f"{int.from_bytes(word,'little'):08x}"})
                    except ValueError:
                        pc_literals.append({"pc":record["pc"],"address":f"{literal:08x}",
                                            "raw":None,"unreadable_in_executable_PT_LOAD":True})
    return {
        "schema":1,"elf_sha256":SHA,"entry":f"{ENTRY:08x}",
        "original_callsite":f"{CALLSITE:08x}",
        "original_bl":caller[0].bytes.hex(),
        "provider_symbols":functions,
        "owning_segments":owning_segments,
        "static_decode_mode":"A32_only",
        "linear_window_bytes":SCAN_BYTES,
        "linear_instructions_not_cfg":instructions,
        "calls":calls,"branches":branches,"memory_candidates":mem,
        "pc_relative_literals":pc_literals,
        "source_pointer_is_nul_terminated_proven":False,
        "source_max_content_bytes_proven":None,
        "safe_prefix_248_bytes_proven":False,
        "provider_executed":False,
        "new_certificates":0}


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--binary",required=True,type=Path)
    p.add_argument("--checkpoint",required=True,type=Path)
    a=p.parse_args()
    record=inspect(a.binary)
    serialized=json.dumps(record,sort_keys=True,indent=2)+"\n"
    a.checkpoint.parent.mkdir(parents=True,exist_ok=True)
    if a.checkpoint.exists() and a.checkpoint.read_text(encoding="utf-8") != serialized:
        raise ValueError("Original prefix-provider structural checkpoint drift")
    a.checkpoint.write_text(serialized,encoding="utf-8")
    print("A04_PREFIX_SYMBOLS="+json.dumps(record["provider_symbols"]))
    print("A04_PREFIX_CALLS="+json.dumps(record["calls"]))
    print("A04_PREFIX_BRANCHES="+json.dumps(record["branches"]))
    print("A04_PREFIX_PC_LITERALS="+json.dumps(record["pc_relative_literals"]))
    for x in record["linear_instructions_not_cfg"][:64]:
        print("A04_PREFIX_DISASM "+x["pc"]+" "+x["mnemonic"]+" "+x["operands"])
    print("A04_PREFIX_NUL_BOUND_PROVEN=0")


if __name__=="__main__":
    main()
