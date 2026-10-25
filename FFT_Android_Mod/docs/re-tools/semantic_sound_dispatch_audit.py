#!/usr/bin/env python3
"""Inspect the first non-trampoline sound function and the special icon setter.

Read original executable ELF bytes, distinguish reachable instructions from
potential literal data, and do not assign semantic effects from symbol names.
"""
import argparse
import csv
import hashlib
from pathlib import Path
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
from capstone.arm import ARM_OP_MEM, ARM_OP_IMM, ARM_INS_B, ARM_INS_BL
import semantic_evidence
import semantic_sound_chain as chain

SOUND_DISPATCH = (0x2B2CF8, 12, "SysSE_PlayDef(int)")
ICON_POSITION = (0x2B8900, 5036, "iOS_SetIconPosition()")
ICON_PREFIX_BYTES = 96
SOUND_FOLLOWING_BYTES = 32


def matching_symbol(inventory, record):
    with inventory.open(newline="", encoding="utf-8") as stream:
        hits = [r for r in csv.DictReader(stream)
                if int(r["address"], 16) == record[0]]
    if (len(hits) != 1 or int(hits[0]["size"]) != record[1]
            or hits[0]["demangled"] != record[2]):
        raise ValueError(f"Inventory mismatch for 0x{record[0]:x}")
    return hits[0]


def disassemble(binary, address, size):
    data = semantic_evidence.read_function(binary, address, size)
    md = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    md.detail = True
    instructions = list(md.disasm(data, address))
    if (len(instructions) != size // 4 or
            [i.address for i in instructions] !=
            list(range(address, address + size, 4))):
        raise ValueError(f"Original ELF not fully ARM word-aligned at 0x{address:x}")
    return data, instructions


def detail_rows(data, instructions, start):
    out = []
    for i, insn in enumerate(instructions):
        observed = []
        for op in insn.operands:
            if op.type == ARM_OP_MEM:
                observed.append(f"memory base {insn.reg_name(op.mem.base)} "
                                f"displacement {op.mem.disp}")
        if insn.id in (ARM_INS_B, ARM_INS_BL):
            if len(insn.operands) == 1 and insn.operands[0].type == ARM_OP_IMM:
                observed.append(f"direct branch/call 0x{insn.operands[0].imm:x}")
        word = int.from_bytes(data[i*4:i*4+4], "little")
        out.append(f"| `0x{insn.address:x}` | `0x{word:08x}` | "
                   f"`{insn.mnemonic} {insn.op_str}` | "
                   f'{"; ".join(observed) or "—"} |')
    return out


def report(binary, inventory):
    matching_symbol(inventory, SOUND_DISPATCH)
    matching_symbol(inventory, ICON_POSITION)
    direct, sound_boundary, reason = chain.follow(binary)
    if sound_boundary != SOUND_DISPATCH[0]:
        raise ValueError(
            f"Sound branch sequence unexpectedly ends at 0x{sound_boundary:x}")
    sound_data, sound_insns = disassemble(binary, SOUND_DISPATCH[0], SOUND_DISPATCH[1])
    next_data, next_insns = disassemble(
        binary, SOUND_DISPATCH[0] + SOUND_DISPATCH[1], SOUND_FOLLOWING_BYTES)
    icon_data, icon_insns = disassemble(
        binary, ICON_POSITION[0], ICON_PREFIX_BYTES)
    digest = hashlib.sha256(binary.read_bytes()).hexdigest()
    lines = ["# Original ARM boundaries — sound dispatcher and icon positioning", "",
             f"ELF SHA-256: `{digest}`", "",
             "This report is a **static audit**, not a behavioral or equivalence "
             "claim. Linear disassembly can decode embedded data as code.", "",
             "## Verified sound trampoline", "",
             "| Address | Target |", "|---|---|"]
    for address, (_, target) in direct.items():
        lines.append(f"| `0x{address:x}` | `0x{target:x}` |")
    lines.extend(["", f"Stops at `0x{sound_boundary:x}`: {reason}.", "",
                  "## SysSE_PlayDef(int) — 12-byte symbol", "",
                  "| Address | ELF word | ARM decoding | Observable operand category |",
                  "|---|---|---|---|",
                  *detail_rows(sound_data, sound_insns, SOUND_DISPATCH[0]), "",
                  "## Following 32 bytes, not assumed part of SysSE_PlayDef", "",
                  "| Address | ELF word | ARM decoding | Observable operand category |",
                  "|---|---|---|---|",
                  *detail_rows(next_data, next_insns, SOUND_DISPATCH[0] + SOUND_DISPATCH[1]),
                  "", "## iOS_SetIconPosition() — first 96 bytes only", "",
                  "| Address | ELF word | ARM decoding | Observable operand category |",
                  "|---|---|---|---|",
                  *detail_rows(icon_data, icon_insns, ICON_POSITION[0]), "",
                  "## Next verification gate", "",
                  "Only emulate paths after checking direct and indirect "
                  "transfers, stack setup and memory operands. Do not "
                  "execute unresolved callees or branch targets. "
                  "Do not classify a whole function by its entry prefix.", "",
                  "A bounded instruction sequence may be correct under "
                  "controlled inputs without proving complete function "
                  "behavior, runtime effects, or semantic equivalence.", ""])
    return "\n".join(lines)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--binary", type=Path,
                   default=semantic_evidence.ROOT/"src/lib/armeabi/libgl2jni.so")
    p.add_argument("--inventory", type=Path,
                   default=semantic_evidence.ROOT/"docs/RE_FUNCTION_INVENTORY.csv")
    p.add_argument("--results", type=Path,
                   default=semantic_evidence.ROOT/"docs/re-results")
    a = p.parse_args()
    text = report(a.binary, a.inventory)
    target = a.results/"SEMANTIC_SOUND_DISPATCH_AUDIT.md"
    target.write_text(text, encoding="utf-8")
    print(text)
    print(f"Wrote {target}")


if __name__ == "__main__":
    main()
