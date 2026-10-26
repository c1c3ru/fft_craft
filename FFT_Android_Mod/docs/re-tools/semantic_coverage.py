#!/usr/bin/env python3
"""Per-function semantic evidence ledger, without converting microtests into proof.

All inventory addresses are retained. Certificates are manually reviewable
JSON objects bound to the exact ELF, range and explicit evidence.
"""
import argparse
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
INVENTORY = ROOT / "docs/RE_FUNCTION_INVENTORY.csv"
BINARY = ROOT / "src/lib/armeabi/libgl2jni.so"
RESULTS = ROOT / "docs/re-results"
ALLOWED = {"certified", "partial", "unknown"}
REQUIRED_CERT = ("contract", "preconditions", "postconditions", "control_flow",
                 "memory_effects", "test_evidence", "reviewer")


def ledger(inventory, digest, certificates):
    if not isinstance(certificates, dict):
        raise ValueError("certificates must be an address-keyed JSON object")
    with inventory.open(newline="", encoding="utf-8") as file:
        inventory_rows = list(csv.DictReader(file))
    rows = []
    by_address = {}
    symbol_count = 0
    for item in inventory_rows:
        address = item["address"].strip().lower().removeprefix("0x")
        symbol_count += 1
        size = int(item["size"])
        if address in by_address:
            prior = by_address[address]
            if prior["size"] != size:
                raise ValueError(f"conflicting sizes for aliased address: {address}")
            prior["symbols"].append(item["demangled"])
            continue
        cert = certificates.get(address)
        status = "unknown"
        if cert is not None:
            if not isinstance(cert, dict):
                raise ValueError(f"invalid certificate for {address}")
            status = cert.get("status", "unknown")
            if status not in ALLOWED:
                raise ValueError(f"invalid semantic status for {address}")
            if cert.get("binary_sha256") != digest or cert.get("size") != size:
                raise ValueError(f"stale certificate for {address}")
            if status == "certified" and any(not cert.get(key) for key in REQUIRED_CERT):
                raise ValueError(f"incomplete certification for {address}")
        record = {"address": address, "name": item["demangled"],
                  "symbols": [item["demangled"]], "size": size,
                  "semantic_status": status,
                  "evidence": cert.get("test_evidence", []) if cert else []}
        rows.append(record)
        by_address[address] = record
    extra = set(certificates) - set(by_address)
    if extra:
        raise ValueError(f"certificates outside inventory: {sorted(extra)[:5]}")
    rows.sort(key=lambda x: (-x["size"], x["address"]))
    return rows


def report(rows, digest):
    counts = Counter(r["semantic_status"] for r in rows)
    total_bytes = sum(r["size"] for r in rows)
    symbol_count = sum(len(r["symbols"]) for r in rows)
    certified_bytes = sum(r["size"] for r in rows if r["semantic_status"] == "certified")
    certified = counts["certified"]
    lines = ["# Cobertura semântica verificável — FFT Craft", "",
             f"ELF SHA-256: `{digest}`", "",
             "> **Regra:** aprovação estrutural, análise estática e microexecuções "
             "parciais não significam equivalência semântica integral.", "",
             "| Métrica | Quantidade |", "|---|---:|",
             f"| Entradas/símbolos no inventário | {symbol_count:,} |",
             f"| Endereços de execução únicos | {len(rows):,} |",
             f"| Semântica integral certificada por registro | {certified:,} |",
             f"| Evidência parcial registrada | {counts['partial']:,} |",
             f"| Sem certificação registrada | {counts['unknown']:,} |",
             f"| Progresso certificado por endereço | {certified / max(len(rows),1):.2%} |",
             f"| Progresso certificado por bytes | {certified_bytes / max(total_bytes,1):.2%} |",
             "", "Contagens medem **certificados registrados no ledger**, "
             "não a ausência de conhecimento em relatórios anteriores.",
             "Um certificado revisado e testes diferenciais são necessários "
             "antes de afirmar equivalência. O esquema não prova completude por si.", "",
             "## Fila por bytes ainda sem certificação", "",
             "| Endereço | Função | Bytes | Estado |",
             "|---|---|---:|---|"]
    for row in (r for r in rows if r["semantic_status"] != "certified"):
        lines.append(f"| `{row['address']}` | {row['name'].replace('|', '/')} | "
                     f"{row['size']} | {row['semantic_status']} |")
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--inventory", type=Path, default=INVENTORY)
    parser.add_argument("--binary", type=Path, default=BINARY)
    parser.add_argument("--certificates", type=Path, default=RESULTS / "semantic-certificates.json")
    parser.add_argument("--output", type=Path, default=RESULTS / "SEMANTIC_COVERAGE.md")
    args = parser.parse_args()
    digest = hashlib.sha256(args.binary.read_bytes()).hexdigest()
    certificates = (json.loads(args.certificates.read_text(encoding="utf-8"))
                    if args.certificates.exists() else {})
    rows = ledger(args.inventory, digest, certificates)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(report(rows, digest), encoding="utf-8")
    print(f"SEMANTIC_CERTIFIED={sum(r['semantic_status']=='certified' for r in rows)}")
    print(f"INVENTORY_COUNT={sum(len(r[\u0027symbols\u0027]) for r in rows)}")
    print(f"UNIQUE_ENTRYPOINTS={len(rows)}")


if __name__ == "__main__":
    main()
