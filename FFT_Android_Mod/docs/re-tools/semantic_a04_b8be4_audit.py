#!/usr/bin/env python3
"""A04 nested path: original 0xb9454 -> 0xb8be4, with bounded CFG evidence."""
import argparse
import hashlib
import json
from pathlib import Path

from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
from capstone.arm import ARM_INS_BL, ARM_OP_IMM
import semantic_evidence
from semantic_a04_callee_cfg import inventory
from semantic_a04_714a0_slot import SHA

CALLSITE = 0x000b9454
CALLEE = 0x000b8be4
CONTINUATION = CALLSITE + 4


def verify_original_callsite(binary):
    raw = semantic_evidence.read_function(binary, CALLSITE, 4)
    md = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    md.detail = True
    ins = list(md.disasm(raw, CALLSITE))
    if (len(ins) != 1 or ins[0].id != ARM_INS_BL or
            len(ins[0].operands) != 1 or
            ins[0].operands[0].type != ARM_OP_IMM or
            ins[0].operands[0].imm != CALLEE):
        raise ValueError("Original nested callee target changed")
    return raw.hex()


def audit(binary):
    if hashlib.sha256(binary.read_bytes()).hexdigest() != SHA:
        raise ValueError("Original ARM ELF digest changed")
    original_opcode = verify_original_callsite(binary)
    raw = semantic_evidence.read_function(binary, CALLEE, 512)
    prefix = inventory(raw, CALLEE)
    tail = semantic_evidence.read_function(binary, CONTINUATION, 48)
    dis = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    following = [{"pc": f"{i.address:08x}", "hex": i.bytes.hex(),
                  "mnemonic": i.mnemonic, "operands": i.op_str}
                 for i in dis.disasm(tail, CONTINUATION)]
    if not prefix["instructions"] or not following:
        raise ValueError("Original continuation cannot be decoded")
    return {"schema": 1, "elf_sha256": SHA,
            "original_callsite": f"{CALLSITE:08x}", "original_opcode": original_opcode,
            "callee": f"{CALLEE:08x}", "callee_candidates": prefix,
            "post_call_static_candidates": following,
            "original_callee_executed": False,
            "unknown_dependent_calls_executed": False,
            "new_certificates": 0}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--binary", required=True, type=Path)
    p.add_argument("--output", required=True, type=Path)
    a = p.parse_args()
    result = audit(a.binary)
    payload = json.dumps(result, sort_keys=True, indent=2) + "\n"
    a.output.parent.mkdir(parents=True, exist_ok=True)
    if a.output.exists() and a.output.read_text(encoding="utf-8") != payload:
        raise ValueError("Nested callee original checkpoint drift")
    a.output.write_text(payload, encoding="utf-8")
    print("A04_NESTED_CALLEE=" + result["callee"])
    for r in result["callee_candidates"]["instructions"][:48]:
        print("A04_NESTED_ORIGINAL " + r["pc"] + " " + r["mnemonic"] + " " + r["operands"])
    for r in result["post_call_static_candidates"]:
        print("A04_NESTED_CONTINUATION " + r["pc"] + " " + r["mnemonic"] + " " + r["operands"])
    for field in ("edges", "memory_candidates", "calls", "unresolved"):
        print("A04_NESTED_" + field.upper() + "=" +
              json.dumps(result["callee_candidates"][field]))
    print("A04_NESTED_CALLEE_EXECUTED=0")


if __name__ == "__main__":
    main()
