#!/usr/bin/env python3
"""Fail-closed R_ARM_JUMP_SLOT strcpy provenance and caller continuation audit."""
import argparse
import hashlib
import json
from pathlib import Path
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
from capstone.arm import ARM_INS_BL, ARM_INS_B, ARM_OP_IMM

import semantic_evidence
import semantic_a04_714a0_slot as slot

CALLER = 0x000b6620
BL = 0x000b6630
BEQ = 0x000b662c
BRANCH_TARGET = 0x000b6644


def verify_strcpy_provenance(meta):
    exact = meta.get("exact_relocations", [])
    if len(exact) != 1:
        raise ValueError("Expected exactly one original GOT relocation")
    row = exact[0]
    symbol = row.get("symbol") or {}
    if (row.get("offset") != f"{slot.SLOT:08x}"
            or row.get("rel_section") != ".rel.plt"
            or row.get("type_id") != 22
            or row.get("type") != "R_ARM_JUMP_SLOT"
            or symbol.get("name") != "strcpy"
            or symbol.get("shndx") != "SHN_UNDEF"
            or symbol.get("kind") != "STT_FUNC"):
        raise ValueError("Original GOT slot no longer points to external strcpy symbol")
    if "libc.so" not in meta.get("needed_libraries", []):
        raise ValueError("Expected external library dependency libc.so missing")
    file_word = meta.get("file_word") or {}
    if file_word.get("le32") != "00071468":
        raise ValueError("Original unrelocated slot word changed")
    if not any(x.get("name") == ".got" for x in meta.get("sections", [])):
        raise ValueError("Original slot must belong to .got")
    return {"symbol": "strcpy", "relocation": "R_ARM_JUMP_SLOT",
            "binding": "STB_GLOBAL", "symbol_definition": "SHN_UNDEF",
            "provider_library_candidate": "libc.so",
            "resolved_android_runtime_address": None}


def scan_caller(binary):
    raw = semantic_evidence.read_function(binary, CALLER, 0x60)
    dis = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    dis.detail = True
    rows = list(dis.disasm(raw, CALLER))
    ins = {i.address: i for i in rows}
    if len(ins) < 20 or BEQ not in ins or BL not in ins:
        raise ValueError("Caller body no longer disassembles at expected boundaries")
    beq, call = ins[BEQ], ins[BL]
    if (beq.id != ARM_INS_B or len(beq.operands) != 1
            or beq.operands[0].type != ARM_OP_IMM
            or beq.operands[0].imm != BRANCH_TARGET
            or call.id != ARM_INS_BL or len(call.operands) != 1
            or call.operands[0].type != ARM_OP_IMM
            or call.operands[0].imm != slot.ENTRY):
        raise ValueError("Original strcpy callsite/branch not established")
    return {"entry": f"{CALLER:08x}", "branch_to_skip_strcpy": f"{BRANCH_TARGET:08x}",
            "strcpy_bl": f"{BL:08x}", "veneer": f"{slot.ENTRY:08x}",
            "post_bl": f"{BL+4:08x}", "linear_candidate_not_executed": [
                {"pc": f"{i.address:08x}", "bytes": i.bytes.hex(),
                 "mnemonic": i.mnemonic, "operands": i.op_str}
                for i in rows if CALLER <= i.address <= CALLER+0x5c]}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--binary", required=True, type=Path)
    p.add_argument("--output", required=True, type=Path)
    a = p.parse_args()
    if hashlib.sha256(a.binary.read_bytes()).hexdigest() != slot.SHA:
        raise ValueError("ELF digest mismatch")
    meta = slot.elf_provenance(a.binary)
    proven = verify_strcpy_provenance(meta)
    caller = scan_caller(a.binary)
    result = {"elf_sha256": slot.SHA, "schema": 1, "slot": f"{slot.SLOT:08x}",
              "import": proven, "caller": caller,
              "strcpy_runtime_implementation_executed": False,
              "caller_nonzero_path_executed": False, "new_certificates": 0}
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    a.output.parent.mkdir(parents=True, exist_ok=True)
    if a.output.exists() and a.output.read_text(encoding="utf-8") != payload:
        raise ValueError("A04 strcpy provenance checkpoint drift")
    a.output.write_text(payload, encoding="utf-8")
    print("A04_IMPORT_STRCPY_CONFIRMED=1")
    print("A04_IMPORT_RUNTIME_PROVIDER_NOT_PROVEN=1")
    for item in caller["linear_candidate_not_executed"]:
        print("A04_CALLER_DISASM " + item["pc"] + " " + item["mnemonic"] + " " + item["operands"])
    print("A04_R1_NONZERO_EXECUTED=0")


if __name__ == "__main__":
    main()
