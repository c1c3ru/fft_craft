#!/usr/bin/env python3
"""Fail-closed original-ELF A32 entry audit for SysSE_PlayDef (0x2b2cf8).

Static inspection only. No callee execution, sound effects or certification.
"""
import argparse
import hashlib
from pathlib import Path

from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM, CS_GRP_JUMP, CS_GRP_CALL, CS_GRP_RET
from capstone.arm import ARM_OP_MEM, ARM_OP_IMM, ARM_OP_REG

import semantic_evidence
import semantic_sound_three_entry_exec as upstream

ENTRY = 0x2B2CF8
WINDOW = 128
PREFIX = (0x26B374, 0x2168E0, 0x271314, ENTRY)


def inspect(binary):
    binary = Path(binary)
    if hashlib.sha256(binary.read_bytes()).hexdigest() != upstream.ELF_SHA256:
        raise ValueError("Original ELF SHA-256 mismatch")
    upstream.original_words(binary)  # verifies the entire predecessor chain
    code = semantic_evidence.read_function(binary, ENTRY, WINDOW)
    if len(code) != WINDOW:
        raise ValueError("Truncated destination window")
    dis = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    dis.detail = True
    instructions = list(dis.disasm(code, ENTRY))
    if (len(instructions) != WINDOW // 4 or
            [i.address for i in instructions] != list(range(ENTRY, ENTRY + WINDOW, 4))):
        raise ValueError("Unparseable original A32 window")
    return code, instructions


def classify(insn):
    tags = []
    if insn.group(CS_GRP_CALL):
        tags.append("call")
    if insn.group(CS_GRP_JUMP):
        tags.append("jump")
    if insn.group(CS_GRP_RET) or insn.mnemonic.startswith(("pop", "ldm")) and "pc" in insn.op_str:
        tags.append("possible-return")
    if any(op.type == ARM_OP_MEM for op in insn.operands):
        tags.append("memory")
    if any(op.type == ARM_OP_REG and insn.reg_name(op.reg) == "pc"
           for op in insn.operands):
        tags.append("pc-register")
    if insn.mnemonic.startswith(("b", "bl")):
        targets = [f"0x{op.imm:x}" for op in insn.operands if op.type == ARM_OP_IMM]
        tags.extend("target=" + t for t in targets)
    return ", ".join(tags) if tags else "ordinary/undetermined"


def render(binary):
    code, insns = inspect(binary)
    lines = [
        "# SysSE_PlayDef: auditoria estática da entrada A32 0x2b2cf8", "",
        f"ELF SHA-256: `{upstream.ELF_SHA256}`",
        f"Janela A32: `0x{ENTRY:x}..0x{ENTRY+WINDOW-1:x}` ({WINDOW} bytes).",
        f"SHA-256 da janela: `{hashlib.sha256(code).hexdigest()}`.", "",
        "## Proveniência", "",
        "A cadeia 0x26b374 -> 0x2168e0 -> 0x271314 -> 0x2b2cf8 "
        "foi previamente microexecutada **somente até antes da instrução no destino**.",
        "O script valida novamente os opcodes originais dos trampolins.", "",
        "## Desmontagem linear (não constitui CFG validado)", "",
        "| Endereço | Bytes | A32 | Marcadores conservadores |",
        "|---|---|---|---|",
    ]
    for i, insn in enumerate(insns):
        raw = code[i*4:i*4+4].hex()
        lines.append(f"| 0x{insn.address:x} | `{raw}` | "
                     f"`{insn.mnemonic} {insn.op_str}` | {classify(insn)} |")
    lines += [
        "", "## Limites de evidência", "",
        "- **Nenhuma instrução de SysSE_PlayDef foi executada** neste relatório.",
        "- Uma desmontagem linear pode conter dados inline; ramos condicionais, "
        "chamadas, acessos a memória e retornos exigem rastreamento separado.",
        "- Não se inferem parâmetros, semântica do áudio, estado global ou retornos.",
        "- Nenhuma função adicional é certificada; continuam 303 registros semânticos "
        "preexistentes, sujeitos à própria política de certificação.",
        "- Próximo experimento: executar bloco básico somente com memória mapeada "
        "do ELF e hooks de memória, parando **antes** de BL/BX/PC indireto, "
        "syscall, leitura não inicializada ou escrita externa.", "",
    ]
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--binary", type=Path, default=semantic_evidence.ROOT /
                        "src/lib/armeabi/libgl2jni.so")
    parser.add_argument("--output", type=Path, default=semantic_evidence.ROOT /
                        "docs/re-results/SEMANTIC_SOUND_PLAYDEF_ENTRY.md")
    args = parser.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(render(args.binary), encoding="utf-8")
    print("SOUND_PLAYDEF_STATIC_BYTES=128")
    print("SOUND_PLAYDEF_EXECUTED_INSTRUCTIONS=0")
    print("SOUND_PLAYDEF_NEW_CERTIFICATES=0")


if __name__ == "__main__":
    main()
