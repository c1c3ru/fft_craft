#!/usr/bin/env python3
"""Build a traceable human-review batch from same-run original-ELF proof records.

Consumes the 303 per-address local BX LR contracts *already executed* by the
current CI run. Never creates full certificates, forges review metadata, or
counts these reused machine samples as new executions.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path

import semantic_coverage
import semantic_evidence
import semantic_bxlr_contract_pilot as local
import semantic_certificate_gate as gate

MAX_BATCH = 20


def build(binary, inventory, contracts_dir, limit=5,
          reader=semantic_evidence.read_function, run_id=None):
    if type(limit) is not int or not 1 <= limit <= MAX_BATCH:
        raise ValueError("review batch size must be between 1 and 20")
    binary, inventory = Path(binary), Path(inventory)
    digest = hashlib.sha256(binary.read_bytes()).hexdigest()
    ledger = semantic_coverage.ledger(inventory, digest, {})
    by_address = {r["address"]: r for r in ledger}
    contracts_dir = Path(contracts_dir)
    paths = sorted(contracts_dir.glob("*.json"))
    if not paths:
        raise ValueError("no same-run machine-verified contract files provided")
    candidates = []
    seen = set()
    for path in paths:
        record = json.loads(path.read_text(encoding="utf-8"))
        address = str(record.get("address", "")).lower().removeprefix("0x")
        if (path.stem.lower() != address or address in seen
                or address not in by_address
                or record.get("binary_sha256") != digest
                or record.get("size") != by_address[address]["size"]
                or record.get("size") != 4
                or record.get("instruction_word") != "1eff2fe1"
                or record.get("semantic_status") != "partial"
                or record.get("certified") is not False
                or record.get("reviewer") is not None
                or record.get("contract_stage") !=
                   "local_isa_contract_checked_review_pending"
                or record.get("machine_samples_passed") != 32
                or record.get("machine_samples_failed") != 0
                or record.get("verified_return_modes") != ["ARM", "Thumb"]
                or record.get("contract") != local.isa_contract(local.leaf.BX_LR)
                or record.get("preconditions") != list(gate.PRECONDITIONS)
                or record.get("postconditions") != list(gate.POSTCONDITIONS)
                or record.get("memory_effects") != list(gate.MEMORY_EFFECTS)
                or record.get("control_flow") != list(gate.CONTROL_FLOW)
                or record.get("test_evidence") != list(gate.REQUIRED_EVIDENCE)):
            raise ValueError(f"unverified or stale contract candidate: {path}")
        seen.add(address)
        original = reader(binary, int(address, 16), 4)
        if (original != local.leaf.BX_LR
                or record.get("instruction_sha256") !=
                   hashlib.sha256(original).hexdigest()):
            raise ValueError(f"original ELF bytes changed for candidate: {address}")
        candidates.append((address, record))
    if len(candidates) < limit:
        raise ValueError("insufficient validated proof candidates")
    result = []
    for address, source in candidates[:limit]:
        result.append({
            "address": address,
            "name": by_address[address]["name"],
            "status": "partial",
            "certified": False,
            "review_stage": "independent_human_review_pending",
            "proof_class": gate.SCOPE,
            "scope": "normal_a32_valid_abi_return",
            "binary_sha256": digest,
            "size": 4,
            "instruction_encoding": source["instruction_word"],
            "instruction_sha256": source["instruction_sha256"],
            "contract": source["contract"],
            "preconditions": list(gate.PRECONDITIONS),
            "postconditions": list(gate.POSTCONDITIONS),
            "control_flow": list(gate.CONTROL_FLOW),
            "memory_effects": list(gate.MEMORY_EFFECTS),
            "test_evidence": list(gate.REQUIRED_EVIDENCE),
            "verified_return_modes": ["ARM", "Thumb"],
            "same_run_machine_samples": 32,
            "new_machine_samples_in_this_step": 0,
            "source_artifact": "contract-pilot/" + address + ".json",
            "reviewer": None,
            "blocking_review_items": [
                "independent human assessment of ARM ISA scope and assumptions",
                "GitHub APPROVED review on the eventual certificate-ledger PR",
                "certification gate rerun against original ELF after approval",
            ],
        })
    batch = {
        "schema": 1,
        "elf_sha256": digest,
        "source_ci_run_id": str(run_id or os.environ.get("GITHUB_RUN_ID") or "local"),
        "status": "review_pending",
        "sample_accounting": "reuses previous 32 samples per function; adds zero",
        "certified_functions": 0,
        "candidates": result,
    }
    return batch


def render(batch):
    lines = [
        "# Primeira fila de revisão formal: contratos BX LR", "",
        f"ELF SHA-256: `{batch['elf_sha256']}`", "",
        f"Execução de origem do CI: `{batch['source_ci_run_id']}`", "",
        f"- Contratos locais preparados para revisão: **{len(batch['candidates'])}**",
        "- Microexecuções **novas neste passo**: **0** "
        "(reutiliza as 32 observações ARM/Thumb por candidato).",
        "- Certificados integrais emitidos automaticamente: **0**.", "",
        "**Nenhuma função está certificada por este pacote.** "
        "A revisão independente deve avaliar o escopo de execução normal, "
        "interworking, preservação dos registradores, efeitos de memória, "
        "alinhamento do LR e casos de exceção excluídos.", "",
        "| Endereço | Função | Opcode original | Testes anteriores | Estado |",
        "|---|---|---|---:|---|",
    ]
    for r in batch["candidates"]:
        lines.append(
            f"| `{r['address']}` | {r['name'].replace('|','/')} | "
            f"`{r['instruction_encoding']}` | "
            f"{r['same_run_machine_samples']} | revisão pendente |"
        )
    lines += [
        "", "## Como concluir a revisão", "",
        "1. Conferir os registros individuais em "
        "`SEMANTIC_BXLR_REVIEW_BATCH.json` com o ELF original.",
        "2. Verificar as pré/pós-condições e documentar ressalvas; "
        "o escopo **não** cobre o programa completo.",
        "3. Submeter proposta explícita de certificados ao ledger em PR "
        "separado; jamais copiar aprovação fictícia de uma fixture.",
        "4. Obter revisão independente registrada no GitHub. "
        "O gate verifica PR, identidade, commit, endereço e bytes do ELF "
        "antes de contar qualquer certificado.", "",
        "Este arquivo é uma fila de revisão e não uma declaração "
        "de equivalência semântica integral.", "",
    ]
    return "\n".join(lines)


def write(batch, manifest, report):
    manifest, report = Path(manifest), Path(report)
    manifest.parent.mkdir(parents=True, exist_ok=True)
    report.parent.mkdir(parents=True, exist_ok=True)
    manifest.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n",
                        encoding="utf-8")
    report.write_text(render(batch), encoding="utf-8")
    print(f"BXLR_REVIEW_BATCH_PREPARED={len(batch['candidates'])}")
    print("BXLR_REVIEW_BATCH_NEW_SAMPLES=0")
    print("BXLR_REVIEW_BATCH_CERTIFIED=0")


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--binary", type=Path, default=semantic_coverage.BINARY)
    p.add_argument("--inventory", type=Path, default=semantic_coverage.INVENTORY)
    p.add_argument("--contracts-dir", type=Path, required=True)
    p.add_argument("--limit", type=int, default=5)
    p.add_argument("--manifest", type=Path,
                   default=semantic_coverage.RESULTS / "SEMANTIC_BXLR_REVIEW_BATCH.json")
    p.add_argument("--report", type=Path,
                   default=semantic_coverage.RESULTS / "SEMANTIC_BXLR_REVIEW_BATCH.md")
    a = p.parse_args()
    write(build(a.binary, a.inventory, a.contracts_dir, a.limit),
          a.manifest, a.report)


if __name__ == "__main__":
    main()
