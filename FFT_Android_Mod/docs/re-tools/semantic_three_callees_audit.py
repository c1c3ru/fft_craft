#!/usr/bin/env python3
"""Audit actual ARM opcodes for three callees reached from houkoku_okng.

No semantic claims from a name. A return may leave trailing PC-relative
literal data. Decoding a word does not prove that word is reachable code.
"""
import argparse
import csv
import hashlib
from pathlib import Path

from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
from capstone.arm import ARM_INS_LDR, ARM_OP_MEM, ARM_REG_PC
import semantic_evidence

TARGETS = (
    (0x2B9CAC, 32, "iOS_setV2Icon(V2ICON_DATA, int)", 0x25A2BC),
    (0x26B374, 4, "sound_request(int)", 0x25A310),
    (0x282268, 12, "iOS_clearOkNg()", 0x25A328),
)


def validate_inventory(inventory):
    with inventory.open(newline="", encoding="utf-8") as file:
        rows = {int(r["address"], 16): r for r in csv.DictReader(file)}
    for address, size, symbol, _ in TARGETS:
        row = rows.get(address)
        if not row or int(row["size"]) != size or row["demangled"] != symbol:
            raise ValueError(f"Inventory mismatch at 0x{address:x}")
    return True


def audit(binary, inventory):
    validate_inventory(inventory)
    md = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    md.detail = True
    lines = ["# Three real ARM callees — initial machine-code audit", "",
             f"ELF SHA-256: `{hashlib.sha256(binary.read_bytes()).hexdigest()}`", "",
             "Static instruction decoding alone does not establish reachability, "
             "effects of calls, ABI postconditions or equivalence.", ""]
    for address, size, symbol, callsite in TARGETS:
        code = semantic_evidence.read_function(binary, address, size)
        call = list(md.disasm(semantic_evidence.read_function(binary, callsite, 4),
                              callsite))
        if len(call) != 1 or call[0].mnemonic != "bl" or (
                call[0].op_str != f"#0x{address:x}"):
            raise ValueError(f"Expected BL destination not present at 0x{callsite:x}")
        instructions = list(md.disasm(code, address))
        if len(instructions) != size // 4 or any(
                insn.address != address + index * 4 or insn.size != 4
                for index, insn in enumerate(instructions)):
            raise ValueError(f"Malformed ARM words at 0x{address:x}")
        lines += [f"## {symbol}", "",
                  f"- Callsite: `0x{callsite:x}` — `{call[0].mnemonic} {call[0].op_str}`",
                  f"- Candidate span: `0x{address:x}` through "
                  f"`0x{address + size - 4:x}` ({size} bytes).", "",
                  "| Address | Original word | ARM decoding | Memory / flow observations |",
                  "|---|---|---|---|"]
        for i, insn in enumerate(instructions):
            word = int.from_bytes(code[4*i:4*i+4], "little")
            memory = []
            for op in insn.operands:
                if op.type == ARM_OP_MEM:
                    base = insn.reg_name(op.mem.base)
                    memory.append(f"mem[{base},disp={op.mem.disp}]")
                    if op.mem.base == ARM_REG_PC and insn.id == ARM_INS_LDR:
                        literal_addr = insn.address + 8 + op.mem.disp
                        memory.append(f"PC-relative literal at 0x{literal_addr:x}")
            if insn.mnemonic.startswith(("bl", "b")) or insn.mnemonic.startswith("pop"):
                memory.append("control-flow candidate")
            lines.append(f"| `0x{insn.address:x}` | `0x{word:08x}` | "
                         f"`{insn.mnemonic} {insn.op_str}` | "
                         f'{"; ".join(memory) or "—"} |')
        lines += ["", "Decoded entries can include embedded data after a return; "
                  "the next phase must distinguish reachable code from literals "
                  "and dynamically check memory reads/writes.", ""]
    lines += ["## Planned bounded tests", "",
              "Emulate each callee with controlled registers and memory. "
              "Verify the exact PC trace, link register, returns, read/write "
              "addresses, neighboring canaries and unresolved branch/call "
              "destinations. Compose only effects actually established by "
              "individual tests into the caller.", "",
              "## Limitations", "",
              "No full-function semantic equivalence, real runtime global "
              "state, caller effects or legitimate argument domains proven.", ""]
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--binary", type=Path,
                        default=semantic_evidence.ROOT / "src/lib/armeabi/libgl2jni.so")
    parser.add_argument("--inventory", type=Path,
                        default=semantic_evidence.ROOT / "docs/RE_FUNCTION_INVENTORY.csv")
    parser.add_argument("--results", type=Path,
                        default=semantic_evidence.ROOT / "docs/re-results")
    args = parser.parse_args()
    out = args.results / "SEMANTIC_THREE_CALLEES_AUDIT.md"
    text = audit(args.binary, args.inventory)
    out.write_text(text, encoding="utf-8")
    print(text)
    print(f"Published {out}")


if __name__ == "__main__":
    main()
