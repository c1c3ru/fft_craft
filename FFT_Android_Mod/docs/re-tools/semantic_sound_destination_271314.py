#!/usr/bin/env python3
"""Conservative entry-window audit for next ARM sound_request destination.

The original ELF must match the established SHA-256, all incoming branches
must match their intended targets, and each 32-bit word must decode.
A linear decode is NOT a proven executable path or a full semantic proof.
"""
import argparse
import hashlib
from pathlib import Path

from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
from capstone.arm import ARM_OP_IMM, ARM_OP_MEM, ARM_OP_REG

import semantic_evidence
import semantic_sound_two_hop_exec as prior

START = 0x271314
WINDOW = 96
ENTRIES = (0x271314, 0x271318, 0x27131C)
INCOMING = (
    (0x26B374, 0x2168E0),
    (0x2168E0, 0x271314),
    (0x2168E4, 0x27131C),
    (0x2168F4, 0x271318),
)


def inspect(binary):
    binary = Path(binary)
    digest = hashlib.sha256(binary.read_bytes()).hexdigest()
    if digest != prior.ELF_SHA256:
        raise ValueError("Original ELF hash changed")
    md = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    md.detail = True
    incoming = []
    for addr, target in INCOMING:
        code = semantic_evidence.read_function(binary, addr, 4)
        insns = list(md.disasm(code, addr))
        if (len(insns) != 1 or insns[0].mnemonic != "b"
                or insns[0].op_str != f"#0x{target:x}"):
            raise ValueError(f"Changed ARM branch at 0x{addr:x}")
        incoming.append((addr, target, code.hex()))
    code = semantic_evidence.read_function(binary, START, WINDOW)
    insns = list(md.disasm(code, START))
    if (len(insns) != WINDOW // 4
            or [i.address for i in insns] != list(range(START, START + WINDOW, 4))):
        raise ValueError("Destination window is not a complete A32 decoding")
    return digest, code, incoming, insns


def operand_types(insn):
    categories = []
    for op in insn.operands:
        if op.type == ARM_OP_MEM:
            categories.append(
                f"memory base={insn.reg_name(op.mem.base)}, offset={op.mem.disp}")
        elif op.type == ARM_OP_IMM and insn.mnemonic.startswith(("b", "bl")):
            categories.append(f"direct target=0x{op.imm:x}")
        elif op.type == ARM_OP_REG and insn.mnemonic.startswith(("bx", "blx")):
            categories.append(f"indirect={insn.reg_name(op.reg)}")
    return "; ".join(categories) or "no explicitly classified control/data operand"


def render(binary):
    digest, code, incoming, insns = inspect(binary)
    lines = [
        "# sound_request: auditoria da entrada 0x271314", "",
        "ELF SHA-256: " + digest,
        f"ARM code window: 0x{START:x}..0x{START+WINDOW-1:x}, "
        f"{WINDOW} bytes; window SHA-256: {hashlib.sha256(code).hexdigest()}", "",
        "## Desvios de entrada confirmados no ELF", "",
        "| Origem ARM | Destino ARM | Opcode (4 bytes) |",
        "|---|---|---|",
    ]
    for addr, target, raw in incoming:
        lines.append(f"| 0x{addr:x} | 0x{target:x} | {raw} |")
    lines += [
        "", "## Decodificacao linear A32 (nao equivale a alcance de fluxo)", "",
        "As entradas 0x271314 / 0x271318 / 0x27131c podem "
        "ter precondicoes diferentes. Dados inline podem decodificar como ARM.",
        "",
        "| Endereco | Opcode (4 bytes) | Instrucao ARM | Operand classification |",
        "|---|---|---|---|",
    ]
    for index, insn in enumerate(insns):
        raw = code[index * 4:index * 4 + 4].hex()
        mark = " (entry)" if insn.address in ENTRIES else ""
        lines.append(
            f"| 0x{insn.address:x}{mark} | {raw} | "
            f"{insn.mnemonic} {insn.op_str} | {operand_types(insn)} |")
    lines += [
        "",
        "## Estado dos contratos e limites", "",
        "- Confirmado: entradas e opcodes A32 originais e janela de 96 bytes.",
        "- Ainda NAO executado: qualquer instrucao deste destino.",
        "- Nao conhecido: efeitos em dados, retorno, acessos indiretos, "
        "outros sucessores e comportamento do subsistema de som.",
        "- Proxima etapa: microexecucao limitada e rastreada de caminhos reais, "
        "com estado controlado; parar ANTES de chamadas ou destinos desconhecidos.",
        "- Novas certificacoes: 0. As 303 provas BX LR ja aprovadas permanecem validas.", "",
    ]
    return "\n".join(lines)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--binary", type=Path, default=semantic_evidence.ROOT /
                   "src/lib/armeabi/libgl2jni.so")
    p.add_argument("--output", type=Path, default=semantic_evidence.ROOT /
                   "docs/re-results/SEMANTIC_SOUND_DESTINATION_271314.md")
    a = p.parse_args()
    a.output.parent.mkdir(parents=True, exist_ok=True)
    a.output.write_text(render(a.binary), encoding="utf-8")
    print("SOUND_DESTINATION_ENTRY_TARGETS=3")
    print("SOUND_DESTINATION_A32_WORDS_DISASSEMBLED=24")
    print("SOUND_DESTINATION_INSTRUCTIONS_EXECUTED=0")
    print("SOUND_DESTINATION_NEW_CERTIFICATES=0")


if __name__ == "__main__":
    main()
