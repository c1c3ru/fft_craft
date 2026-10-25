#!/usr/bin/env python3
"""Audit the actual six-instruction ARM callee at houkoku_okng's first BL.

All claims here are static, instruction-level observations. In particular,
the callee's return-value contract and effects are UNKNOWN until measured.
"""
import argparse
import csv
import hashlib
from pathlib import Path

from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
from capstone.arm import ARM_INS_BL, ARM_INS_B, ARM_INS_BX, ARM_INS_POP, ARM_OP_IMM

import semantic_evidence

CALLSITE = 0x25A298
CALLEE = 0x2B7CCC
CALLEE_SIZE = 24
EXPECTED_SYMBOL = "iOS_getV2Icon(V2ICON_DATA)"


def decode(binary):
    md = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    md.detail = True
    call_bytes = semantic_evidence.read_function(binary, CALLSITE, 4)
    call = list(md.disasm(call_bytes, CALLSITE))
    if (len(call) != 1 or call[0].id != ARM_INS_BL
            or len(call[0].operands) != 1
            or call[0].operands[0].type != ARM_OP_IMM
            or call[0].operands[0].imm != CALLEE):
        raise ValueError("Real houkoku_okng callsite is not BL to expected callee")
    function = semantic_evidence.read_function(binary, CALLEE, CALLEE_SIZE)
    instructions = list(md.disasm(function, CALLEE))
    if len(instructions) != 6 or any(
            insn.address != CALLEE + i * 4 or insn.size != 4
            for i, insn in enumerate(instructions)):
        raise ValueError("V2Icon target is not exactly six aligned ARM instructions")
    return call[0], instructions


def inventory_match(inventory):
    with inventory.open(newline="", encoding="utf-8") as stream:
        rows = [row for row in csv.DictReader(stream)
                if int(row["address"], 16) == CALLEE]
    if len(rows) != 1 or rows[0]["demangled"] != EXPECTED_SYMBOL or (
            int(rows[0]["size"]) != CALLEE_SIZE):
        raise ValueError("ELF call target disagrees with inventory symbol and size")
    return rows[0]


def inspect(binary, inventory):
    digest = hashlib.sha256(binary.read_bytes()).hexdigest()
    call, instructions = decode(binary)
    item = inventory_match(inventory)
    table = []
    read_write = []
    for insn in instructions:
        try:
            read, written = insn.regs_access()
        except Exception:
            read, written = (), ()
        table.append(f"| `0x{insn.address:x}` | `{insn.mnemonic} {insn.op_str}` |")
        read_write.append(
            f"| `0x{insn.address:x}` | "
            f'{", ".join(insn.reg_name(reg) for reg in read) or "—"} | '
            f'{", ".join(insn.reg_name(reg) for reg in written) or "—"} |')
    outgoing = [(i.address, i.mnemonic, i.op_str) for i in instructions
                if i.id in (ARM_INS_BL, ARM_INS_B, ARM_INS_BX, ARM_INS_POP)]
    return "\n".join([
        "# ARM callee boundary: iOS_getV2Icon", "",
        f"ELF SHA-256: `{digest}`", "",
        f"Caller: `0x{CALLSITE:x}`: `{call.mnemonic} {call.op_str}`.",
        f'Callee: `0x{CALLEE:x}`, {CALLEE_SIZE} bytes, '
        f'`{item["demangled"]}` (inventory identifier only).', "",
        "## All six original ARM instructions", "",
        "| Address | Instruction |", "|---|---|",
        *table, "",
        "## Instruction-level register access (Capstone heuristic)", "",
        "| Address | Read registers | Written registers |",
        "|---|---|---|", *read_write, "",
        f"Observed branch/call/return-like instructions: **{len(outgoing)}**.", "",
        "## What remains unproven", "",
        "The argument passed to the callee, result in r0, global/heap "
        "memory access, external call side effects and conditional status "
        "after the BL are not inferred solely from a symbol name or six "
        "disassembled instructions. No full-function equivalence is claimed.", "",
    ])


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--binary", type=Path,
                   default=semantic_evidence.ROOT / "src/lib/armeabi/libgl2jni.so")
    p.add_argument("--inventory", type=Path,
                   default=semantic_evidence.ROOT / "docs/RE_FUNCTION_INVENTORY.csv")
    p.add_argument("--results", type=Path,
                   default=semantic_evidence.ROOT / "docs/re-results")
    args = p.parse_args()
    report = inspect(args.binary, args.inventory)
    dest = args.results / "SEMANTIC_V2ICON_CALLEE.md"
    dest.write_text(report, encoding="utf-8")
    print(report)
    print(f"Wrote {dest}")


if __name__ == "__main__":
    main()
