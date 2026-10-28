#!/usr/bin/env python3
"""Audit static ARM pilot outputs against the original ELF and exact manifests.

This is a pipeline integrity check, NOT an ARM execution or equivalence proof.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path

ORIGINAL_ELF_SHA256 = "bf913415ab9458a83b14ac8c8a0fa3430d1f5d18bfbcd7c7472d6f5e8b4850bc"
REQUIRED_UNVERIFIED = {
    "complete_control_flow", "register_effects", "runtime_memory_effects",
    "input_output_contract", "differential_tests", "semantic_equivalence",
}


def sha256_file(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def audit(binary, manifests_dir, pilot_dir, *, expected_workers=25,
          expected_tasks=250, expected_sha256=ORIGINAL_ELF_SHA256,
          reinspect=False, inspector=None):
    """Return a verified summary; reject omissions, substitutions and stale data."""
    binary, manifests_dir, pilot_dir = map(Path, (binary, manifests_dir, pilot_dir))
    if (not isinstance(expected_workers, int) or not 1 <= expected_workers <= 32
            or not isinstance(expected_tasks, int) or expected_tasks < 1):
        raise ValueError("invalid expected workers/tasks")
    digest = sha256_file(binary)
    if digest != expected_sha256:
        raise ValueError(f"original ELF SHA-256 mismatch: {digest}")
    paths = sorted(manifests_dir.glob("semantic-worker-*.json"))
    if len(paths) != expected_workers:
        raise ValueError(f"expected {expected_workers} manifests, found {len(paths)}")
    tasks = {}
    shards = []
    for index, path in enumerate(paths, 1):
        if path.name != f"semantic-worker-{index:02d}.json":
            raise ValueError(f"noncanonical or missing manifest: {path.name}")
        manifest = json.loads(path.read_text(encoding="utf-8"))
        if (manifest.get("schema") != 1 or manifest.get("worker") != index
                or manifest.get("elf_sha256") != digest
                or not isinstance(manifest.get("tasks"), list)):
            raise ValueError(f"invalid manifest identity: {path.name}")
        shard_tasks = manifest["tasks"]
        total_bytes = 0
        for task in shard_tasks:
            address = task.get("address")
            size = task.get("size")
            if (not isinstance(address, str) or len(address) != 8
                    or any(ch not in "0123456789abcdef" for ch in address)
                    or address in tasks or type(size) is not int
                    or not 1 <= size <= 20000
                    or not isinstance(task.get("name"), str)
                    or not task["name"]
                    or task.get("binary_sha256") != digest):
                raise ValueError(f"invalid or duplicate task in {path.name}: {address}")
            tasks[address] = task
            total_bytes += size
        if manifest.get("total_bytes") != total_bytes:
            raise ValueError(f"manifest byte accounting mismatch: {path.name}")
        shards.append(len(shard_tasks))
    if len(tasks) != expected_tasks:
        raise ValueError(f"expected {expected_tasks} unique tasks, found {len(tasks)}")
    output_paths = list(pilot_dir.glob("*.json"))
    outputs = {p.stem: p for p in output_paths}
    if (len(output_paths) != len(outputs) or set(outputs) != set(tasks)):
        missing = sorted(set(tasks) - set(outputs))[:5]
        extra = sorted(set(outputs) - set(tasks))[:5]
        raise ValueError(f"pilot output set mismatch: missing={missing}, extra={extra}")
    if reinspect and inspector is None:
        from semantic_pilot import inspect_task
        inspector = inspect_task
    rows = []
    for address, task in sorted(tasks.items()):
        result = json.loads(outputs[address].read_text(encoding="utf-8"))
        instruction_set = "thumb" if int(address, 16) & 1 else "arm"
        if (result.get("address") != address
                or result.get("name") != task["name"]
                or result.get("size") != task["size"]
                or result.get("binary_sha256") != digest
                or result.get("semantic_status") != "partial"
                or result.get("evidence_class") != "static_bounded"
                or result.get("instruction_set") != instruction_set
                or "certified" in result
                or type(result.get("decoded_instructions")) is not int
                or result["decoded_instructions"] < 1
                or type(result.get("unvisited_slots")) is not int
                or result["unvisited_slots"] < 0
                or type(result.get("resolved_jump_tables")) is not int
                or result["resolved_jump_tables"] < 0
                or not REQUIRED_UNVERIFIED.issubset(set(result.get("unverified", [])))):
            raise ValueError(f"invalid partial static evidence: {address}")
        for key in ("candidate_literal_addresses", "call_sites", "store_sites",
                    "unresolved_dispatches"):
            if not isinstance(result.get(key), list):
                raise ValueError(f"invalid {key} at {address}")
        if reinspect and inspector(task, binary, digest) != result:
            raise ValueError(f"reinspection of original ELF differs: {address}")
        rows.append((address, task["size"], result["decoded_instructions"],
                     result["unvisited_slots"]))
    return {"digest": digest, "workers": len(paths), "tasks": len(tasks),
            "outputs": len(outputs), "shard_sizes": shards, "rows": rows,
            "reinspected": bool(reinspect)}


def render(summary):
    tick = chr(96)
    lines = ["# Auditoria de integridade — 250 tarefas no ELF original", "",
             f"- ELF SHA-256: {tick}{summary['digest']}{tick}",
             f"- Execução GitHub Actions: {tick}{os.environ.get('GITHUB_RUN_ID', 'local')}{tick}",
             f"- Manifestos: **{summary['workers']}**; tarefas únicas: **{summary['tasks']}**",
             f"- Relatórios de evidência estática: **{summary['outputs']}**",
             f"- Reinspeção determinística do ELF: **{'sim' if summary['reinspected'] else 'não'}**",
             f"- Tarefas por manifesto: {tick}{', '.join(map(str, summary['shard_sizes']))}{tick}", "",
             "**Escopo:** integridade de manifestos e análise estática limitada, obtida do ELF original.",
             "Isto **não** é execução ARM/Unicorn, equivalência semântica, cobertura completa",
             "de fluxos de controle ou nova certificação. O ledger de certificados não foi alterado.",
             "", "## Evidência por endereço", "",
             "| Endereço | Bytes lidos | Instruções decodificadas | Slots não visitados |",
             "|---|---:|---:|---:|"]
    lines.extend(f"| {tick}{a}{tick} | {size} | {ins} | {gap} |"
                 for a, size, ins, gap in summary["rows"])
    return "\n".join(lines) + "\n"


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--binary", type=Path, required=True)
    p.add_argument("--manifests", type=Path, required=True)
    p.add_argument("--pilot", type=Path, required=True)
    p.add_argument("--expected-workers", type=int, default=25)
    p.add_argument("--expected-tasks", type=int, default=250)
    p.add_argument("--expected-sha256", default=ORIGINAL_ELF_SHA256)
    p.add_argument("--reinspect", action="store_true")
    p.add_argument("--report", type=Path, required=True)
    args = p.parse_args()
    summary = audit(args.binary, args.manifests, args.pilot,
                    expected_workers=args.expected_workers,
                    expected_tasks=args.expected_tasks,
                    expected_sha256=args.expected_sha256, reinspect=args.reinspect)
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(render(summary), encoding="utf-8")
    print(f"REAL_ELF_AUDIT_MANIFESTS={summary['workers']}")
    print(f"REAL_ELF_AUDIT_TASKS={summary['tasks']}")
    print(f"REAL_ELF_AUDIT_STATIC_REPORTS={summary['outputs']}")
    print(f"REAL_ELF_AUDIT_REINSPECTED={int(summary['reinspected'])}")
    print("REAL_ELF_AUDIT_CERTIFICATES_CREATED=0")


if __name__ == "__main__":
    main()
