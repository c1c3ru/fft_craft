#!/usr/bin/env python3
"""Verify original ARM V2Icon getter and distinguish code from literal pool.

Five reachable ARM instructions and one PC-relative literal occupy the
24-byte symbol. Static evidence is NOT complete semantic equivalence.
"""
import argparse
import csv
import hashlib
from pathlib import Path

from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
from capstone.arm import ARM_INS_BL, ARM_OP_IMM

import semantic_evidence

CALLSITE = 0x25A298
CALLEE = 0x2B7CCC
CALLEE_SIZE = 24
LITERAL_ADDR = CALLEE + 20
EXPECTED_SYMBOL = "iOS_getV2Icon(V2ICON_DATA)"
OPCODES = (
    ("ldr", "r3, [pc, #0xc]"),
    ("add", "r3, pc, r3"),
    ("add", "r0, r3, r0, lsl #2"),
    ("ldr", "r0, [r0, #0xd04]"),
    ("bx", "lr"),
)


def decode(binary):
    """Read BL and five opcodes plus literal; refuse changed opcode signatures."""
    md = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    md.detail = True
    call_bytes = semantic_evidence.read_function(binary, CALLSITE, 4)
    call = list(md.disasm(call_bytes, CALLSITE))
    if (len(call) != 1 or call[0].id != ARM_INS_BL
            or len(call[0].operands) != 1
            or call[0].operands[0].type != ARM_OP_IMM
            or call[0].operands[0].imm != CALLEE):
        raise ValueError("Real houkoku_okng callsite is not BL to expected callee")
    body = semantic_evidence.read_function(binary, CALLEE, CALLEE_SIZE)
    if len(body) != CALLEE_SIZE:
        raise ValueError("V2Icon code/literal bytes truncated")
    instructions = list(md.disasm(body[:20], CALLEE))
    if ([i.address for i in instructions] != list(range(CALLEE, LITERAL_ADDR, 4))
            or [(i.mnemonic, i.op_str) for i in instructions] != list(OPCODES)):
        raise ValueError("V2Icon target no longer matches five known ARM opcodes")
    literal = int.from_bytes(body[20:], "little")
    return call[0], instructions, literal


def inventory_match(inventory):
    with inventory.open(newline="", encoding="utf-8") as stream:
        rows = [row for row in csv.DictReader(stream)
                if int(row["address"], 16) == CALLEE]
    if (len(rows) != 1 or rows[0]["demangled"] != EXPECTED_SYMBOL
            or int(rows[0]["size"]) != CALLEE_SIZE):
        raise ValueError("ELF call target disagrees with inventory symbol and size")
    return rows[0]


def indexed_address(literal, index):
    """32-bit ARM PC-relative base plus unsigned element index and 0xd04."""
    if not 0 <= index <= 0xFFFFFFFF:
        raise ValueError("Index must be a 32-bit integer")
    base = ((CALLEE + 4 + 8) + literal) & 0xFFFFFFFF
    return (base + ((index << 2) & 0xFFFFFFFF) + 0xD04) & 0xFFFFFFFF


def inspect(binary, inventory):
    digest = hashlib.sha256(binary.read_bytes()).hexdigest()
    call, instructions, literal = decode(binary)
    item = inventory_match(inventory)
    table = []
    access = []
    for insn in instructions:
        try:
            read, written = insn.regs_access()
        except Exception:
            read, written = (), ()
        table.append(f"| `0x{insn.address:x}` | `{insn.mnemonic} {insn.op_str}` |")
        access.append(
            f"| `0x{insn.address:x}` | "
            f'{", ".join(insn.reg_name(r) for r in read) or "—"} | '
            f'{", ".join(insn.reg_name(r) for r in written) or "—"} |')
    return "\n".join([
        "# ARM callee: iOS_getV2Icon — verified instruction/data split", "",
        f"ELF SHA-256: `{digest}`", "",
        f"Caller: `0x{CALLSITE:x}`: `{call.mnemonic} {call.op_str}`.",
        f'Callee: `0x{CALLEE:x}`, {CALLEE_SIZE} bytes, '
        f'`{item["demangled"]}`.', "",
        "## Five executable ARM instructions", "",
        "| Address | Instruction |", "|---|---|", *table, "",
        "## One PC-relative literal (data, not an executable opcode)", "",
        f"- Literal at `0x{LITERAL_ADDR:x}`: `0x{literal:08x}`.",
        f"- Indexed data address for argument `r0 = 0`: "
        f"`0x{indexed_address(literal,0):x}`.",
        "- The final 4-byte word must not be counted as a sixth "
        "ARM instruction simply because it decodes as one.", "",
        "## Register accesses for five ARM instructions", "",
        "| Address | Read registers | Written registers |",
        "|---|---|---|", *access, "",
        "The code calculates a PC-relative base, adds `r0 * 4`, "
        "loads a word at an additional `0xd04` displacement, "
        "and returns via `BX LR`. No store instruction is present.", "",
        "## Evidence boundary", "",
        "The actual table contents, valid index bounds, aliasing, "
        "caller argument provenance and complete function behavior are "
        "not established by disassembly. No semantic equivalence claimed.", "",
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
