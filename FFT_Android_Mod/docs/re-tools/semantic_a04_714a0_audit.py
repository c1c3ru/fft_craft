#!/usr/bin/env python3
"""Audit 0x714a0 in the original ELF without assuming callee effects."""
import argparse
import hashlib
import json
from pathlib import Path

from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
from capstone.arm import ARM_INS_B, ARM_INS_BL, ARM_INS_BLX, ARM_INS_BX, ARM_OP_IMM
import semantic_evidence
from semantic_a04_callee_cfg import inventory

SHA = "bf913415ab9458a83b14ac8c8a0fa3430d1f5d18bfbcd7c7472d6f5e8b4850bc"
CALLSITE = 0xb6630
TARGET = 0x714a0
SCAN = 512

def verify_bl(binary):
    data = semantic_evidence.read_function(binary, CALLSITE, 4)
    dis = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    dis.detail = True
    ins = list(dis.disasm(data, CALLSITE))
    if len(ins) != 1 or ins[0].id != ARM_INS_BL or len(ins[0].operands) != 1:
        raise ValueError("Expected original direct BL missing")
    if ins[0].operands[0].type != ARM_OP_IMM or ins[0].operands[0].imm != TARGET:
        raise ValueError("BL destination differs from expected original target")
    return data.hex()

def audit(binary):
    if hashlib.sha256(binary.read_bytes()).hexdigest() != SHA:
        raise ValueError("Original ELF SHA changed")
    opcode = verify_bl(binary)
    raw = semantic_evidence.read_function(binary, TARGET, SCAN)
    state = inventory(raw, TARGET)
    return {"schema": 1, "elf_sha256": SHA,
            "callsite": f"{CALLSITE:08x}", "callee": f"{TARGET:08x}",
            "callsite_opcode": opcode, "candidate_cfg": state,
            "dynamic_execution": False, "whole_function_equivalent": False,
            "new_certificates": 0}

def report(state):
    cfg = state["candidate_cfg"]
    lines = ["# A04 — investigação do destino externo 0x000714a0", "",
             f"ELF SHA-256: `{SHA}`", "",
             "O BL em 0x000b6630 aponta para 0x000714a0, confirmado por bytes do ELF.",
             "As instruções abaixo são somente hipóteses A32 dentro de janela de 512 bytes.",
             "Desvios, dados inline, chamadas e efeitos desconhecidos impedem equivalência integral.",
             "", "## Instruções candidatas", "", "```asm"]
    lines += [r["pc"] + ": " + r["mnemonic"] + " " + r["operands"]
              for r in cfg["instructions"]]
    lines += ["```", "", "## Grafo, memória e chamadas candidatas", "",
              "```json", json.dumps({k: cfg[k] for k in
              ("edges", "memory_candidates", "calls", "unresolved")}, indent=2),
              "```", "", "## Próximos gates", "",
              "1. Resolver código/dados e saltos indiretos no callee; confirmar limites do corpo.",
              "2. Identificar argumentos reais e globais; não usar valores sintéticos como runtime Android.",
              "3. Modelar caminho seguro até o primeiro efeito desconhecido com Unicorn.",
              "4. Somente então criar modelo C e diferencial de efeitos completo.",
              "5. Não declarar A04 concluída nem certificar automaticamente.", ""]
    return "\n".join(lines)

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--binary", type=Path, required=True)
    p.add_argument("--checkpoint", type=Path, required=True)
    p.add_argument("--report", type=Path, required=True)
    args = p.parse_args()
    state = audit(args.binary)
    payload = json.dumps(state, sort_keys=True, indent=2) + "\n"
    if args.checkpoint.exists() and args.checkpoint.read_text(encoding="utf-8") != payload:
        raise ValueError("Previous checkpoint differs: do not overwrite")
    args.checkpoint.parent.mkdir(parents=True, exist_ok=True)
    args.checkpoint.write_text(payload, encoding="utf-8")
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(report(state), encoding="utf-8")
    print("A04_CALLER_BL_VERIFIED=1")
    print("A04_EXTERNAL_CALLEE_STATIC_INSTRUCTIONS=" + str(len(state["candidate_cfg"]["instructions"])))
    print("A04_EXTERNAL_CALLEE_EXECUTED=0")
    print("A04_NEW_CERTIFICATES=0")

if __name__ == "__main__":
    main()
