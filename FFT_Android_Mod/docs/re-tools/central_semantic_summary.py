"""Conservative semantic metrics for the centralized FFT Craft dashboard.

Read the current ELF ledger and same-run worker evidence. Never promote
microexecution or structural coverage to full semantic certification.
"""
import json
from collections import Counter
from pathlib import Path

import semantic_coverage


def summarize(inventory, digest, certificates_path, pilot_dir=None,
              dynamic_dir=None, manifests_dir=None):
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
                if mapped[address]["semantic_status"] != "certified":
                    partial.add(address)
        sources[source] = len(observed)
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
    return {
        "symbols": sum(len(r["symbols"]) for r in rows),
        "unique": len(rows), "certified": counts["certified"],
        "certified_bytes": certified_bytes, "total_bytes": total_bytes,
        "partial_certificate_records": counts["partial"],
        "partial_evidence_unique": len(partial),
        "static_reports": sources["static"], "unicorn_reports": sources["unicorn"],
        "assigned": len(assigned), "pending": pending,
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
        f"| Relatórios estáticos deste lote | {s['static_reports']:,} |",
        f"| Relatórios Unicorn deste lote | {s['unicorn_reports']:,} |",
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
