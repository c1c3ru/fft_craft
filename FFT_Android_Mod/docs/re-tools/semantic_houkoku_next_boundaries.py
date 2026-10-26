#!/usr/bin/env python3
"""Audit the first ARM instructions at two unresolved houkoku call boundaries.

This is a static entry-window audit, not execution beyond a branch or
proof of full caller/callee behavior.
"""
import argparse
import hashlib
from pathlib import Path

from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
import semantic_evidence
import semantic_three_callees_exec as caller

BOUNDARIES = (
    ("sound_request branch destination", caller.SOUND_TARGET, caller.SOUND),
    ("iOS_setV2Icon special destination", caller.SPECIAL_TARGET, 0x2B9CC4),
)


def inspect(binary, window=32):
    if window <= 0 or window > 256 or window % 4:
        raise ValueError("ARM window must be aligned and between 4 and 256 bytes")
    # Fails closed when the audited three-callee machine-code signature changed.
    caller.read_code(binary)
    md = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    output = []
    for title, target, source in BOUNDARIES:
        source_code = semantic_evidence.read_function(binary, source, 4)
        insns = list(md.disasm(source_code, source))
        if len(insns) != 1 or insns[0].size != 4:
            raise ValueError(f"Source ARM branch not decodable: {source:x}")
        expected = f"#0x{target:x}"
        if not insns[0].mnemonic.startswith("b") or insns[0].op_str != expected:
            raise ValueError(f"Branch target changed at {source:x}")
        raw = semantic_evidence.read_function(binary, target, window)
        decoded = list(md.disasm(raw, target))
        if not decoded or sum(i.size for i in decoded) != window:
            raise ValueError(f"Undecodable entry window at {target:x}")
        output.append({"title": title, "source": source, "target": target,
                       "source_opcode": f"{insns[0].mnemonic} {insns[0].op_str}",
                       "window_sha256": hashlib.sha256(raw).hexdigest(),
                       "instructions": [(i.address, i.mnemonic, i.op_str)
                                        for i in decoded]})
    return output


def render(records, digest):
    lines = ["# Próximos destinos ARM de houkoku_okng — auditoria estática", "",
             f"ELF SHA-256: `{digest}`", "",
             "> Esta auditoria apenas decodifica janelas de instruções do ELF "
             "original. **Não executa os destinos nem certifica contratos**.", ""]
    for r in records:
        lines += [f"## {r['title']}", "",
                  f"- Origem do desvio: `0x{r['source']:x}` — `{r['source_opcode']}`",
                  f"- Próximo destino: `0x{r['target']:x}`",
                  f"- SHA-256 da janela: `{r['window_sha256']}`",
                  "", "| Endereço | Instrução ARM |", "|---|---|"]
        for address, name, operands in r["instructions"]:
            lines.append(f"| `0x{address:x}` | `{name} {operands}` |")
        lines += ["", "Continuação da execução, estados de entrada, "
                  "efeitos indiretos e valores de retorno **não verificados**.", ""]
    return "\n".join(lines) + "\n"


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--binary", type=Path,
                   default=semantic_evidence.ROOT / "src/lib/armeabi/libgl2jni.so")
    p.add_argument("--output", type=Path,
                   default=semantic_evidence.ROOT / "docs/re-results/SEMANTIC_HOUKOKU_NEXT_BOUNDARIES.md")
    args = p.parse_args()
    digest = hashlib.sha256(args.binary.read_bytes()).hexdigest()
    records = inspect(args.binary)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(render(records, digest), encoding="utf-8")
    print(f"HOUKOKU_BOUNDARIES_AUDITED={len(records)}")
    print("HOUKOKU_BOUNDARIES_EXECUTED=0")


if __name__ == "__main__":
    main()
