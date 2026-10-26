#!/usr/bin/env python3
"""Index accumulated semantic reports from the same ELF without inventing proof.

This preserves years of existing reports as discoverable evidence while
separating historical observations from machine tests executed *this run*.
"""
import argparse
import hashlib
import re
from pathlib import Path

import semantic_coverage

SHA = re.compile(r"ELF SHA-256:\s*`([0-9a-f]{64})`")
PASS = re.compile(r"(?<![0-9])(\d+)/(\d+)\s+PASS\b")
EXCLUDE = {"SEMANTIC_COVERAGE.md", "SEMANTIC_HISTORY_INDEX.md",
           "SEMANTIC_EVIDENCE_INDEX.md"}


def discover(results, digest):
    records = []
    mismatched = 0
    for path in sorted(Path(results).glob("SEMANTIC_*.md")):
        if path.name in EXCLUDE:
            continue
        content = path.read_text(encoding="utf-8")
        match = SHA.search(content)
        if match is None:
            continue  # unbound texts are not countable as same-binary evidence
        if match.group(1) != digest:
            mismatched += 1
            continue
        declared = [(int(a), int(b)) for a, b in PASS.findall(content)]
        # Do not sum nested subtotals or repeated sample groups from reports.
        records.append({
            "file": path.name, "title": content.splitlines()[0].lstrip("# ").strip(),
            "kind": "microexecution_report" if declared else "static_or_boundary_audit",
            "complete_pass_claims": sum(1 for passed, total in declared
                                        if total > 0 and passed == total),
        })
    return records, mismatched


def render(records, mismatched, digest):
    machine = sum(r["kind"] == "microexecution_report" for r in records)
    lines = [
        "# Acervo histórico de evidências semânticas — FFT Craft", "",
        f"ELF SHA-256: `{digest}`", "",
        f"- Relatórios históricos vinculados a este ELF: **{len(records)}**",
        f"- Documentos com contagens de microexecuções declaradas: **{machine}**",
        f"- Documentos de auditoria estática / limites: **{len(records)-machine}**",
        f"- Documentos com outro SHA-256 excluídos: **{mismatched}**", "",
        "**Importante:** os relatórios abaixo foram gerados em etapas anteriores. "
        "Suas contagens podem se sobrepor e não são somadas às microexecuções "
        "deste lote. A presença de um relatório e um texto PASS não é "
        "certificação integral nem reexecução do teste.", "",
        "| Documento histórico | Tipo | PASS declarados completos |",
        "|---|---|---:|",
    ]
    for r in records:
        label = r["title"].replace("|", "/").replace("[", "(").replace("]", ")")
        lines.append(f"| [{label}]({r['file']}) | {r['kind']} | "
                     f"{r['complete_pass_claims']} |")
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--binary", type=Path, default=semantic_coverage.BINARY)
    parser.add_argument("--results", type=Path, default=semantic_coverage.RESULTS)
    parser.add_argument("--output", type=Path,
                        default=semantic_coverage.RESULTS / "SEMANTIC_HISTORY_INDEX.md")
    args = parser.parse_args()
    digest = hashlib.sha256(args.binary.read_bytes()).hexdigest()
    records, stale = discover(args.results, digest)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(render(records, stale, digest), encoding="utf-8")
    print(f"HISTORIC_SEMANTIC_REPORTS={len(records)}")
    print(f"HISTORIC_REPORTS_WITH_TEST_CLAIMS={sum(r['kind']=='microexecution_report' for r in records)}")
    print(f"HISTORIC_STALE_REPORTS={stale}")


if __name__ == "__main__":
    main()
