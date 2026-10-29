#!/usr/bin/env python3
"""Prove the next A04 external import and scan post-return original instructions.

Does not execute libc or assume that candidate linear disassembly is a proven
full CFG. All original-ELF evidence is guarded by SHA-256.
"""
import argparse
import hashlib
import json
from pathlib import Path

from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
from capstone.arm import (ARM_INS_ADD, ARM_INS_LDR, ARM_OP_REG, ARM_OP_IMM,
                          ARM_OP_MEM, ARM_REG_IP, ARM_REG_PC)
from elftools.elf.elffile import ELFFile
from elftools.elf.relocation import RelocationSection
import semantic_evidence
from semantic_a04_callee_cfg import inventory
from semantic_a04_714a0_slot import SHA

VENEER = 0x00071494
NEXT_CALLER = 0x000b942c
NEXT_BL = 0x000b9440
CONTINUATION = NEXT_BL+4


def veneer_slot(binary):
    raw = semantic_evidence.read_function(binary, VENEER, 12)
    cs = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    cs.detail = True
    op = list(cs.disasm(raw, VENEER))
    if len(op) != 3 or [x.id for x in op] != [ARM_INS_ADD, ARM_INS_ADD, ARM_INS_LDR]:
        raise ValueError("Original second imported veneer changed")
    a, b, c = op
    def add_value(ins, source):
        parts = ins.operands
        if (len(parts) != 3 or parts[0].type != ARM_OP_REG or parts[0].reg != ARM_REG_IP
                or parts[1].type != ARM_OP_REG or parts[1].reg != source
                or parts[2].type != ARM_OP_IMM):
            raise ValueError("Original second veneer ADD operands changed")
        return int(parts[2].imm)
    d1 = add_value(a, ARM_REG_PC)
    d2 = add_value(b, ARM_REG_IP)
    parts = c.operands
    if (len(parts) != 2 or parts[0].type != ARM_OP_REG or parts[0].reg != ARM_REG_PC
            or parts[1].type != ARM_OP_MEM or parts[1].mem.base != ARM_REG_IP
            or parts[1].mem.index or not c.writeback):
        raise ValueError("Original second veneer must use LDR PC with writeback")
    slot = (VENEER+8 + d1+d2 + int(parts[1].mem.disp)) & 0xffffffff
    if slot % 4:
        raise ValueError("Unaligned second imported GOT slot")
    return {"veneer": f"{VENEER:08x}", "slot": f"{slot:08x}",
            "instructions": [{"address": f"{x.address:08x}", "hex": x.bytes.hex(),
                              "mnemonic": x.mnemonic, "operands": x.op_str} for x in op]}


def slot_relocation(binary, slot):
    with binary.open("rb") as fh:
        elf = ELFFile(fh)
        owners = [s for s in elf.iter_segments() if s["p_type"] == "PT_LOAD"
                  and int(s["p_vaddr"]) <= slot < int(s["p_vaddr"])+int(s["p_memsz"])]
        if len(owners) != 1:
            raise ValueError("No unique PT_LOAD segment owns second GOT slot")
        rels = []
        for section in elf.iter_sections():
            if not isinstance(section, RelocationSection):
                continue
            symbols = elf.get_section(int(section["sh_link"]))
            for r in section.iter_relocations():
                if int(r["r_offset"]) != slot:
                    continue
                index = int(r["r_info_sym"])
                if not hasattr(symbols, "get_symbol"):
                    raise ValueError("Missing GOT relocation symbol table")
                symbol = symbols.get_symbol(index)
                rels.append({"section": section.name,
                             "type": int(r["r_info_type"]), "offset": f"{slot:08x}",
                             "name": symbol.name,
                             "shndx": str(symbol["st_shndx"]),
                             "kind": str(symbol["st_info"]["type"])})
        if len(rels) != 1:
            raise ValueError(f"Expected one exact second veneer relocation, found {len(rels)}")
        return rels[0]


def check_import(veneer, rel):
    if (veneer["slot"] != "00347d6c" or rel["offset"] != veneer["slot"]
            or rel["section"] != ".rel.plt" or rel["type"] != 22
            or rel["name"] != "strlen" or rel["shndx"] != "SHN_UNDEF"
            or rel["kind"] != "STT_FUNC"):
        raise ValueError("Second external callee is not proven strlen")
    return {"import": "strlen", "relocation": "R_ARM_JUMP_SLOT",
            "got_slot": veneer["slot"], "runtime_address_unknown": True}


def inspect(binary):
    if hashlib.sha256(binary.read_bytes()).hexdigest() != SHA:
        raise ValueError("A04 original ARM ELF SHA changed")
    callee_raw = semantic_evidence.read_function(binary, NEXT_CALLER, 24)
    dis = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    rows = list(dis.disasm(callee_raw, NEXT_CALLER))
    if len(rows) != 6 or [i.mnemonic for i in rows] != [
            "push", "mov", "mov", "mov", "mov", "bl"]:
        raise ValueError("Caller prefix before second import changed")
    dis.detail = True
    check = list(dis.disasm(callee_raw[-4:], NEXT_BL))
    if len(check) != 1 or not check[0].op_str.endswith("0x71494"):
        raise ValueError("Original 0xb9440 BL destination changed")
    v = veneer_slot(binary)
    relocation = slot_relocation(binary, int(v["slot"], 16))
    imp = check_import(v, relocation)
    after = inventory(semantic_evidence.read_function(binary, CONTINUATION, 256),
                      CONTINUATION)
    return {"schema": 1, "elf_sha256": SHA, "next_import": imp,
            "veneer": v, "relocation": relocation,
            "post_strlen_static_candidates": after,
            "executed_external_callee": False,
            "executed_post_call": False, "new_certificates": 0}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--binary", required=True, type=Path)
    p.add_argument("--output", required=True, type=Path)
    a = p.parse_args()
    result = inspect(a.binary)
    payload = json.dumps(result, sort_keys=True, indent=2)+"\n"
    a.output.parent.mkdir(parents=True, exist_ok=True)
    if a.output.exists() and a.output.read_text(encoding="utf-8") != payload:
        raise ValueError("Post-strlen original ELF checkpoint drift")
    a.output.write_text(payload, encoding="utf-8")
    print("A04_SECOND_IMPORT=" + json.dumps(result["next_import"]))
    print("A04_SECOND_IMPORT_RELOC=" + json.dumps(result["relocation"]))
    for i in result["post_strlen_static_candidates"]["instructions"][:42]:
        print("A04_AFTER_STRLEN " + i["pc"] + " " + i["mnemonic"] + " " + i["operands"])
    for key in ("calls", "memory_candidates", "edges", "unresolved"):
        print("A04_AFTER_STRLEN_" + key.upper() + "=" +
              json.dumps(result["post_strlen_static_candidates"][key]))
    print("A04_POST_STRLEN_EXECUTED=0")


if __name__ == "__main__":
    main()
