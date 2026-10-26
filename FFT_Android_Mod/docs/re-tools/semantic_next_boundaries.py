#!/usr/bin/env python3
"""Read the next 96 ARM bytes at two stopped semantic boundaries.

Linear decoding is *not* proof of reachability. The observations are used to
design a separately validated bounded Unicorn experiment.
"""
import argparse
import hashlib
from pathlib import Path
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
from capstone.arm import ARM_OP_MEM, ARM_OP_IMM, ARM_INS_BL, ARM_INS_B
import semantic_evidence

SOUND = 0x2B2B7C
ICON = 0x2B8928
BYTES = 96
TARGETS = (("SysSE_Play(int,int)", SOUND), ("iOS_SetIconPosition() after prologue", ICON))


def inspect(binary):
    md = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    md.detail = True
    reports = []
    for label, start in TARGETS:
        code = semantic_evidence.read_function(binary, start, BYTES)
        decoded = list(md.disasm(code, start))
        if len(decoded) != BYTES // 4 or any(
                insn.size != 4 or insn.address != start + k*4
                for k, insn in enumerate(decoded)):
            raise ValueError(f"Unaligned or undecodable ARM region at 0x{start:x}")
        rows=[]
        for insn in decoded:
            word = int.from_bytes(code[insn.address-start:insn.address-start+4],"little")
            effects=[]
            for operand in insn.operands:
                if operand.type == ARM_OP_MEM:
                    effects.append(f"memory through `{insn.reg_name(operand.mem.base)}` "
                                   f"(disp={operand.mem.disp})")
            if insn.id in (ARM_INS_B, ARM_INS_BL) and insn.operands and (
                    insn.operands[0].type == ARM_OP_IMM):
                effects.append(f"transfer to `0x{insn.operands[0].imm:x}`")
            rows.append(f"| `0x{insn.address:x}` | `0x{word:08x}` | "
                        f"`{insn.mnemonic} {insn.op_str}` | "
                        f"{'; '.join(effects) or '—'} |")
        reports += [f"## {label} at `0x{start:x}`", "",
                    "| PC | ELF word | Decoded ARM candidate | Operand hints |",
                    "|---|---|---|---|",*rows,""]
    digest=hashlib.sha256(binary.read_bytes()).hexdigest()
    return "\n".join([
        "# ARM next-boundary inspection — sound and icon", "",
        f"ELF SHA-256: `{digest}`", "",
        "These are file-backed ARM **linear decoding candidates**, not "
        "a demonstrated control-flow graph, dynamic executions or verified "
        "memory effects. Embedded data may be decoded as instructions.", "",
        *reports,
        "## Safety constraints for next step", "",
        "- Only test verified entry-to-boundary instruction sequences.",
        "- Model each indirect pointer and adjacent canary explicitly.",
        "- Stop before an unmodeled BL, indirect branch or side effect.",
        "- Do not claim complete-function semantic equivalence.", "",
    ])


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--binary",type=Path,
                        default=semantic_evidence.ROOT/"src/lib/armeabi/libgl2jni.so")
    parser.add_argument("--results",type=Path,
                        default=semantic_evidence.ROOT/"docs/re-results")
    args=parser.parse_args()
    result=inspect(args.binary)
    dest=args.results/"SEMANTIC_NEXT_BOUNDARIES.md"
    dest.write_text(result,encoding="utf-8")
    print(result)
    print(f"Wrote {dest}")


if __name__=="__main__":
    main()
