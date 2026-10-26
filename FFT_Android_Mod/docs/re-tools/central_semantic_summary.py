"""Conservative semantic metrics for the centralized FFT Craft dashboard.

Read the current ELF ledger and same-run worker evidence. Never promote
microexecution or structural coverage to full semantic certification.
"""
import json
from collections import Counter
from pathlib import Path

import semantic_coverage
import semantic_history


def summarize(inventory, digest, certificates_path, pilot_dir=None,
              dynamic_dir=None, manifests_dir=None, history_dir=None,
              contracts_dir=None):
    certificates_path = Path(certificates_path)
    certificates = (json.loads(certificates_path.read_text(encoding="utf-8"))
                    if certificates_path.is_file() else {})
    rows = semantic_coverage.ledger(Path(inventory), digest, certificates)
    mapped = {r["address"]: r for r in rows}
    counts = Counter(r["semantic_status"] for r in rows)
    total_bytes = sum(r["size"] for r in rows)
    certified_bytes = sum(r["size"] for r in rows
                          if r["semantic_status"] == "certified")
    partial = set(r["address"] for r in rows if r["semantic_status"] == "partial")
    sources = {}
    dynamic_samples = 0
    shared_samples = {}
    leaf_candidates = 0
    for source, folder, glob in (
        ("static", pilot_dir, "*.json"),
        ("unicorn", dynamic_dir, "*.json"),
    ):
        observed = set()
        if folder is not None:
            for path in sorted(Path(folder).glob(glob)):
                record = json.loads(path.read_text(encoding="utf-8"))
                address = str(record["address"]).lower().removeprefix("0x")
                if (address not in mapped or path.stem.lower() != address
                        or record.get("binary_sha256") != digest
                        or record.get("semantic_status") != "partial"):
                    raise ValueError(f"invalid or stale {source} evidence: {path}")
                if address in observed:
                    raise ValueError(f"duplicate evidence: {path}")
                observed.add(address)
                if source == "unicorn":
                    if record.get("contract_candidate"):
                        if record.get("size") != 4 or record.get("instruction_encoding") != "1eff2fe1":
                            raise ValueError(f"invalid BX LR candidate: {path}")
                        leaf_candidates += 1
                    if record.get("certified") is not False:
                        raise ValueError(f"dynamic evidence cannot certify: {path}")
                    if "machine_samples_passed" in record:
                        n = record["machine_samples_passed"]
                        if type(n) is not int or n <= 0:
                            raise ValueError(f"invalid machine sample count: {path}")
                        dynamic_samples += n
                    elif "suite_samples_passed" in record:
                        n = record["suite_samples_passed"]
                        scope = record.get("suite_sample_count_scope")
                        if type(n) is not int or n <= 0 or not scope:
                            raise ValueError(f"invalid shared sample count: {path}")
                        if scope in shared_samples and shared_samples[scope] != n:
                            raise ValueError(f"inconsistent shared machine suite: {path}")
                        shared_samples[scope] = n
                    else:
                        raise ValueError(f"missing machine sample count: {path}")
                if mapped[address]["semantic_status"] != "certified":
                    partial.add(address)
        sources[source] = len(observed)
    dynamic_samples += sum(shared_samples.values())
    checked_contracts = set()
    contract_samples = 0
    if contracts_dir is not None:
        for path in sorted(Path(contracts_dir).glob("*.json")):
            record = json.loads(path.read_text(encoding="utf-8"))
            address = str(record.get("address", "")).lower().removeprefix("0x")
            if (address not in mapped or address in checked_contracts
                    or path.stem.lower() != address
                    or record.get("binary_sha256") != digest
                    or mapped[address]["size"] != 4
                    or record.get("instruction_word") != "1eff2fe1"
                    or record.get("contract_stage") != "local_isa_contract_checked_review_pending"
                    or record.get("certified") is not False
                    or record.get("semantic_status") != "partial"
                    or record.get("machine_samples_failed") != 0
                    or record.get("machine_samples_passed") != 8
                    or record.get("reviewer") is not None):
                raise ValueError(f"invalid or stale local contract: {path}")
            checked_contracts.add(address)
            contract_samples += 8
    assigned = set()
    if manifests_dir is not None:
        for path in sorted(Path(manifests_dir).glob("semantic-worker-*.json")):
            manifest = json.loads(path.read_text(encoding="utf-8"))
            if manifest.get("elf_sha256") != digest:
                raise ValueError(f"stale worker manifest: {path}")
            for task in manifest["tasks"]:
                address = str(task["address"]).lower().removeprefix("0x")
                if (address in assigned or address not in mapped
                        or task.get("binary_sha256") != digest
                        or task.get("size") != mapped[address]["size"]):
                    raise ValueError(f"invalid or duplicate worker address: {address}")
                assigned.add(address)
    pending = [r for r in rows if r["semantic_status"] != "certified"]
    history, stale_history = (semantic_history.discover(history_dir, digest)
                              if history_dir is not None else ([], 0))
    return {
        "historic_reports": len(history),
        "historic_machine_report_documents": sum(
            item["kind"] == "microexecution_report" for item in history),
        "historic_stale_reports": stale_history,
        "leaf_candidates": leaf_candidates,
        "checked_local_contracts": len(checked_contracts),
        "contract_samples": contract_samples,
        "symbols": sum(len(r["symbols"]) for r in rows),
        "unique": len(rows), "certified": counts["certified"],
        "certified_bytes": certified_bytes, "total_bytes": total_bytes,
        "partial_certificate_records": counts["partial"],
        "partial_evidence_unique": len(partial),
        "static_reports": sources["static"], "unicorn_reports": sources["unicorn"],
        "assigned": len(assigned), "pending": pending,
        "dynamic_samples": dynamic_samples,
    }


def render(summary):
    s = summary
    lines = [
        "## Cobertura semântica e execução paralela", "",
        "Os números certificados representam **registros formais válidos para este ELF**, "
        "não aprovação estrutural. Evidências parciais não certificam equivalência.", "",
        "| Indicador | Resultado |", "|---|---:|",
        f"| Entradas do inventário | {s['symbols']:,} |",
        f"| Endereços únicos | {s['unique']:,} |",
        f"| Certificados semânticos registrados | {s['certified']:,} |",
        f"| Cobertura semântica por endereço | {100*s['certified']/max(1,s['unique']):.2f}% |",
        f"| Cobertura semântica por bytes únicos | {100*s['certified_bytes']/max(1,s['total_bytes']):.2f}% |",
        f"| Registros parciais no ledger | {s['partial_certificate_records']:,} |",
        f"| Endereços com evidência parcial registrada ou gerada nesta execução | {s['partial_evidence_unique']:,} |",
        f"| Documentos semânticos históricos do mesmo ELF | {s.get('historic_reports', 0):,} |",
        f"| Documentos históricos com testes declarados | {s.get('historic_machine_report_documents', 0):,} |",
        f"| Candidatas BX LR verificadas, pendentes de revisão | {s.get('leaf_candidates', 0):,} |",
        f"| Contratos locais BX LR com retorno ARM/Thumb verificado (revisão pendente) | {s.get('checked_local_contracts', 0):,} |",
        f"| Execuções ARM/Thumb adicionais dos contratos locais | {s.get('contract_samples', 0):,} |",
        f"| Relatórios estáticos deste lote | {s['static_reports']:,} |",
        f"| Relatórios Unicorn deste lote | {s['unicorn_reports']:,} |",
        f"| Microexecuções Unicorn verificadas neste lote (sem duplicar suítes) | {s['dynamic_samples']:,} |",
        f"| Endereços distribuídos aos workers neste lote | {s['assigned']:,} |",
        f"| Endereços aguardando certificação | {len(s['pending']):,} |",
        "", "### Próximos contratos ainda não certificados (maiores primeiro)", "",
        "| Endereço | Função | Bytes | Estado |",
        "|---|---|---:|---|",
    ]
    for r in s["pending"][:15]:
        name = r["name"].replace("|", "/").replace("\n", " ")
        lines.append(f"| `{r['address']}` | {name} | {r['size']} | {r['semantic_status']} |")
    lines += ["", "O restante da fila permanece nos manifestos e no "
              "`SEMANTIC_COVERAGE.md`. Observações Unicorn limitadas e "
              "verificações estáticas não alteram automaticamente certificados.", ""]
    return "\n".join(lines)
