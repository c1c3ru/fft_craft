#!/usr/bin/env python3
"""A04 bounded callee CFG inventory from verified original ELF.

No emulation or semantic certification. Every indirect edge, unmatched
condition and memory effect remains unresolved until dynamic validation.
"""
import argparse
import hashlib
import json
from collections import deque
from pathlib import Path

from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
from capstone.arm import ARM_OP_IMM, ARM_OP_MEM, ARM_REG_PC
import semantic_evidence

SHA = "bf913415ab9458a83b14ac8c8a0fa3430d1f5d18bfbcd7c7472d6f5e8b4850bc"
CALLEES = (0x000b6620, 0x000b45d0)
MAX_WINDOW = 512
MAX_BLOCKS = 96
MAX_INSTRUCTIONS = 256


def inventory(data, entry, max_blocks=MAX_BLOCKS, max_instructions=MAX_INSTRUCTIONS):
    if entry % 4 or len(data) % 4:
        raise ValueError("ARM instruction alignment or window invalid")
    end = entry + len(data)
    dis = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    dis.detail = True
    pending = deque([entry])
    seen = {}
    edges = []
    memory = []
    calls = []
    unknown = []
    blocks = set()
    while pending:
        start = pending.popleft()
        if start in blocks:
            continue
        if len(blocks) >= max_blocks:
            unknown.append({"at": f"{start:08x}", "reason": "block_budget"})
            continue
        blocks.add(start)
        if not (entry <= start < end) or start % 4:
            unknown.append({"at": f"{start:08x}", "reason": "outside_window_or_unaligned"})
            continue
        pc = start
        while entry <= pc < end:
            if pc in seen:
                edges.append({"from": f"{pc:08x}", "to": f"{pc:08x}", "type": "join"})
                break
            if len(seen) >= max_instructions:
                unknown.append({"at": f"{pc:08x}", "reason": "instruction_budget"})
                break
            row = list(dis.disasm(data[pc-entry:pc-entry+4], pc, count=1))
            if len(row) != 1 or row[0].size != 4:
                unknown.append({"at": f"{pc:08x}", "reason": "decode_failure"})
                break
            ins = row[0]
            seen[pc] = {"pc": f"{pc:08x}", "bytes": ins.bytes.hex(),
                        "mnemonic": ins.mnemonic, "operands": ins.op_str}
            for op in ins.operands:
                if op.type == ARM_OP_MEM:
                    access = ("read_write_candidate" if ins.mnemonic.startswith(("swp", "ldrex", "strex"))
                              else "write_candidate" if ins.mnemonic.startswith(("str", "stm", "push", "vstr", "vstm"))
                              else "read_candidate" if ins.mnemonic.startswith(("ldr", "ldm", "pop", "vldr", "vldm"))
                              else "unknown_memory_effect")
                    memory.append({"pc": f"{pc:08x}", "access": access,
                                   "base": ins.reg_name(op.mem.base), "index": ins.reg_name(op.mem.index) if op.mem.index else None,
                                   "displacement": op.mem.disp, "instruction": ins.mnemonic})
            if ins.mnemonic.startswith(("push", "pop", "stm", "ldm")) and not any(x["pc"] == f"{pc:08x}" for x in memory):
                memory.append({"pc": f"{pc:08x}", "access": "register_list_memory_candidate", "instruction": ins.mnemonic})
            mnemonic = ins.mnemonic.split(".")[0]
            next_pc = pc + 4
            is_call = mnemonic.startswith("bl")
            is_branch = mnemonic == "b" or (mnemonic.startswith("b") and mnemonic not in ("bic", "bkpt") and not is_call)
            touches_pc = (("pc" in ins.op_str.lower().split(",")[0].split())
                          or (mnemonic in ("pop", "ldm", "ldmia") and "pc" in ins.op_str.lower()))
            if is_call:
                dest = ins.operands[0].imm if ins.operands and ins.operands[0].type == ARM_OP_IMM else None
                calls.append({"pc": f"{pc:08x}", "target": f"{dest & 0xffffffff:08x}" if dest is not None else None,
                              "kind": mnemonic, "effects": "unknown"})
                unknown.append({"at": f"{pc:08x}", "reason": "callee_effects_unresolved"})
                # Do not assume returning call; continuation is only a candidate.
                edges.append({"from": f"{pc:08x}", "to": f"{next_pc:08x}", "type": "post_call_candidate_unproven"})
                break
            if is_branch or touches_pc:
                dest = ins.operands[0].imm if is_branch and ins.operands and ins.operands[0].type == ARM_OP_IMM else None
                conditional = mnemonic not in ("b", "bx") and not touches_pc
                if dest is not None:
                    edges.append({"from": f"{pc:08x}", "to": f"{dest & 0xffffffff:08x}", "type": "conditional_candidate" if conditional else "branch"})
                    if entry <= dest < end and dest % 4 == 0:
                        pending.append(dest)
                    else:
                        unknown.append({"at": f"{pc:08x}", "reason": "branch_target_outside_window"})
                else:
                    unknown.append({"at": f"{pc:08x}", "reason": "indirect_pc_transfer_or_return"})
                if conditional:
                    edges.append({"from": f"{pc:08x}", "to": f"{next_pc:08x}", "type": "fallthrough_candidate"})
                    pending.append(next_pc)
                break
            # Unknown PC writes and nonstandard instructions are not modeled as effects.
            pc = next_pc
        else:
            unknown.append({"at": f"{pc:08x}", "reason": "window_end"})
    return {"entry": f"{entry:08x}", "window_bytes": len(data), "blocks_attempted": len(blocks),
            "instructions": [seen[x] for x in sorted(seen)], "edges": edges,
            "memory_candidates": memory, "calls": calls,
            "unresolved": unknown, "semantic_status": "static_candidates_only",
            "reimplementation_ready": False}


def inspect(binary):
    if hashlib.sha256(binary.read_bytes()).hexdigest() != SHA:
        raise ValueError("original ELF SHA256 mismatch")
    result = []
    for address in CALLEES:
        raw = semantic_evidence.read_function(binary, address, MAX_WINDOW)
        result.append(inventory(raw, address))
    return {"schema": 1, "elf_sha256": SHA, "callees": result,
            "new_certificates": 0, "dynamic_executions": 0}


def markdown(result):
    lines = ["# A04 — investigação estrutural dos callees ARM originais", "",
             "ELF SHA-256: `" + result["elf_sha256"] + "`", "",
             "**Somente candidatos estáticos:** o grafo é limitado a 512 bytes por entrada,",
             "não é prova de alcançabilidade, retorno, segurança de acesso ou equivalência.", ""]
    for row in result["callees"]:
        lines += ["## `0x" + row["entry"] + "`", "",
                  f"- Blocos tentados: {row['blocks_attempted']}; instruções decodificadas: {len(row['instructions'])}",
                  f"- Candidatos de acesso à memória: {len(row['memory_candidates'])}; chamadas: {len(row['calls'])}",
                  f"- Fronteiras desconhecidas: {len(row['unresolved'])}", "",
                  "### Instruções", "", "```asm"]
        lines += [x["pc"] + ": " + x["mnemonic"] + " " + x["operands"] for x in row["instructions"]]
        lines += ["```", "", "### Chamadas e efeitos desconhecidos", "",
                  "```json", json.dumps({"calls": row["calls"], "memory": row["memory_candidates"],
                                           "unknown": row["unresolved"], "edges": row["edges"]}, indent=2),
                  "```", ""]
    lines += ["## Próximo gate", "",
              "Definir invariantes, conferir código/dados e semântica das instruções,",
              "executar apenas blocos seguros no Unicorn, comparar com oráculo C independente,",
              "e nunca promover o status sem resolver efeitos externos.", ""]
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--binary", type=Path, required=True)
    parser.add_argument("--checkpoint", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    a = parser.parse_args()
    result = inspect(a.binary)
    serialized = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if a.checkpoint.exists() and a.checkpoint.read_text(encoding="utf-8") != serialized:
        raise ValueError("A04 callee CFG checkpoint changed")
    a.checkpoint.parent.mkdir(parents=True, exist_ok=True)
    a.checkpoint.write_text(serialized, encoding="utf-8")
    a.report.write_text(markdown(result), encoding="utf-8")
    print("A04_CALLEE_ENTRIES=2")
    print("A04_CALLEE_NEW_CERTIFICATES=0")
    print("A04_CALLEE_DYNAMIC_EXECUTIONS=0")


if __name__ == "__main__":
    main()
