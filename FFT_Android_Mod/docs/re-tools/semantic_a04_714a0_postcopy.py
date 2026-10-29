#!/usr/bin/env python3
"""A04 strcpy continuation: verify call to 0xb942c and scan original callee."""
import argparse
import hashlib
import json
from pathlib import Path
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
from capstone.arm import ARM_INS_BL, ARM_INS_MOV, ARM_OP_IMM, ARM_OP_REG, ARM_REG_R2, ARM_REG_R4

import semantic_evidence
from semantic_a04_callee_cfg import inventory
from semantic_a04_714a0_slot import SHA
from semantic_a04_714a0_strcpy import scan_caller

EXTERNAL_CALL = 0x000b942c
POST_BL = 0x000b6634
STRCPY_CALL = 0x000b6630


def verify_sequence(rows):
    by_pc = {int(row["pc"], 16): row for row in rows}
    for pc, mnemonic in ((0xb6634, "mov"), (0xb6638, "mov"),
                         (0xb663c, "mov"), (0xb6640, "bl"),
                         (0xb6644, "mov"), (0xb6648, "str"),
                         (0xb664c, "mov"), (0xb6650, "pop")):
        if pc not in by_pc or by_pc[pc]["mnemonic"] != mnemonic:
            raise ValueError(f"Original A04 strcpy continuation changed at 0x{pc:x}")
    # Check independent ARM decoding of operands rather than trusting display strings.
    raw = b"".join(bytes.fromhex(by_pc[pc]["bytes"])
                   for pc in (0xb6634, 0xb6638, 0xb663c, 0xb6640))
    cs = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    cs.detail = True
    ins = list(cs.disasm(raw, POST_BL))
    if len(ins) != 4 or any(ins[i].id != ARM_INS_MOV for i in range(3)) or ins[3].id != ARM_INS_BL:
        raise ValueError("A04 post-strcpy instruction family changed")
    if ([ins[0].operands[1].imm, ins[1].operands[1].imm] != [0x2f, 0x5c]
            or ins[2].operands[0].reg != ARM_REG_R2
            or ins[2].operands[1].reg != ARM_REG_R4
            or ins[3].operands[0].type != ARM_OP_IMM
            or ins[3].operands[0].imm != EXTERNAL_CALL):
        raise ValueError("A04 post-strcpy arguments or next callee changed")
    return {"character_arguments": [0x2f, 0x5c], "pointer_reg": "r4",
            "next_callee": f"{EXTERNAL_CALL:08x}",
            "external_implementation_executed": False}


def audit(binary):
    if hashlib.sha256(binary.read_bytes()).hexdigest() != SHA:
        raise ValueError("Original ARM ELF SHA changed")
    caller = scan_caller(binary)
    verified = verify_sequence(caller["linear_candidate_not_executed"])
    raw = semantic_evidence.read_function(binary, EXTERNAL_CALL, 256)
    cfg = inventory(raw, EXTERNAL_CALL)
    return {"schema": 1, "elf_sha256": SHA,
            "caller_post_strcpy": verified, "next_callee_cfg": cfg,
            "next_callee_executed": False, "new_certificates": 0}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--binary", required=True, type=Path)
    p.add_argument("--output", required=True, type=Path)
    a = p.parse_args()
    result = audit(a.binary)
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    a.output.parent.mkdir(parents=True, exist_ok=True)
    if a.output.exists() and a.output.read_text(encoding="utf-8") != payload:
        raise ValueError("A04 post-strcpy checkpoint changed")
    a.output.write_text(payload, encoding="utf-8")
    print("A04_POST_STRCPY_CALLEE=" + result["caller_post_strcpy"]["next_callee"])
    for ins in result["next_callee_cfg"]["instructions"][:48]:
        print("A04_POST_COPY_SCAN " + ins["pc"] + " " + ins["mnemonic"] + " " + ins["operands"])
    print("A04_POST_COPY_EDGES=" + json.dumps(result["next_callee_cfg"]["edges"]))
    print("A04_POST_COPY_CALLS=" + json.dumps(result["next_callee_cfg"]["calls"]))
    print("A04_POST_COPY_MEMORY=" + json.dumps(result["next_callee_cfg"]["memory_candidates"]))
    print("A04_POST_COPY_UNRESOLVED=" + json.dumps(result["next_callee_cfg"]["unresolved"]))
    print("A04_POST_COPY_EXECUTED=0")


if __name__ == "__main__":
    main()
