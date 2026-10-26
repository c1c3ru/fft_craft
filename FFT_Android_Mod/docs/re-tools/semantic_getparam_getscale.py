#!/usr/bin/env python3
"""Original ARM instruction/word audit for the next two callable targets.

Never interpret a function name, unconditional linear decode, or a trailing
word after BX LR as a verified semantic effect.
"""
import argparse
import csv
import hashlib
from pathlib import Path

from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
from capstone.arm import ARM_INS_BL, ARM_OP_IMM, ARM_OP_MEM
import semantic_evidence

TARGETS = (
    (0x28C320, 12, "CFFT_STATE::GetParam(int)", 0x2B2B98),
    (0x0A6F28, 16, "CGX_SCREEN_CORRECT::GetScale(float*)", 0x2B8938),
)


def inventory_check(path):
    with path.open(newline="", encoding="utf-8") as f:
        rows = {int(r["address"],16):r for r in csv.DictReader(f)}
    for address,size,symbol,_ in TARGETS:
        row=rows.get(address)
        if row is None or int(row["size"])!=size or row["demangled"]!=symbol:
            raise ValueError(f"Inventory target drift at 0x{address:x}")
    return True


def decode(binary, address, size, callsite):
    md=Cs(CS_ARCH_ARM,CS_MODE_ARM)
    md.detail=True
    call=list(md.disasm(
        semantic_evidence.read_function(binary,callsite,4),callsite))
    if (len(call)!=1 or call[0].id!=ARM_INS_BL
            or len(call[0].operands)!=1
            or call[0].operands[0].type!=ARM_OP_IMM
            or call[0].operands[0].imm!=address):
        raise ValueError(f"Caller BL at 0x{callsite:x} has a different destination")
    raw=semantic_evidence.read_function(binary,address,size)
    insns=list(md.disasm(raw,address))
    if len(insns)!=size//4 or any(
            x.size!=4 or x.address!=address+4*i
            for i,x in enumerate(insns)):
        raise ValueError(f"Target ARM words are truncated at 0x{address:x}")
    return raw,insns


def audit(binary, inventory):
    inventory_check(inventory)
    digest=hashlib.sha256(binary.read_bytes()).hexdigest()
    report=[
        "# First-level ARM call contracts: GetParam / GetScale","",
        f"ELF SHA-256: `{digest}`","",
        "Original executable ELF words are **linearly decoded**; "
        "a trailing word may be literal data even if Capstone gives it a mnemonic. "
        "No runtime call results or function-wide equivalence are asserted.","",
    ]
    for address,size,symbol,callsite in TARGETS:
        raw, insns = decode(binary,address,size,callsite)
        report += [
            f"## {symbol}","",
            f"- Callsite: `0x{callsite:x}` (verified ARM BL).",
            f"- ELF span: `0x{address:x}`, {size} bytes.",
            "", "| Word address | Raw ELF word | Linear ARM decoding | Memory/flow hints |",
            "|---|---|---|---|",
        ]
        for k,x in enumerate(insns):
            word=int.from_bytes(raw[k*4:k*4+4],"little")
            hints=[]
            for op in x.operands:
                if op.type==ARM_OP_MEM:
                    hints.append(f"mem via {x.reg_name(op.mem.base)} displacement {op.mem.disp}")
            if x.mnemonic.startswith(("b","pop")):
                hints.append("candidate control transfer")
            report.append(f"| `0x{x.address:x}` | `0x{word:08x}` | "
                          f"`{x.mnemonic} {x.op_str}` | "
                          f"{'; '.join(hints) or '—'} |")
        report += ["", "Reachability and literal-vs-code classification "
                   "require a separate control-flow check.",""]
    report += [
        "## Next reproducible step","",
        "Verify exact opcode signatures and original PC-relative data. "
        "Emulate locally bounded inputs with Unicorn, checking reads, writes, "
        "registers, original return PC, memory neighbors and call boundaries.",
        "Stop before indirect or external callees not yet modeled.","",
        "**Not proven:** true application state, pointer validity, actual sound "
        "output, UI placement, or complete semantic equivalence.","",
    ]
    return "\n".join(report)


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--binary",type=Path,
                   default=semantic_evidence.ROOT/"src/lib/armeabi/libgl2jni.so")
    p.add_argument("--inventory",type=Path,
                   default=semantic_evidence.ROOT/"docs/RE_FUNCTION_INVENTORY.csv")
    p.add_argument("--results",type=Path,
                   default=semantic_evidence.ROOT/"docs/re-results")
    a=p.parse_args()
    dest=a.results/"SEMANTIC_GETPARAM_GETSCALE_AUDIT.md"
    result=audit(a.binary,a.inventory)
    dest.write_text(result,encoding="utf-8")
    print(result)
    print(f"Updated {dest}")

if __name__=="__main__":
    main()
