#!/usr/bin/env python3
"""Track *verified ledger* velocity, never infer certificates from microtests.

A daily/CI snapshot is a measurement, not evidence of semantic equivalence.
A separate semantic_certificate_gate validates approved original-ELF contracts.
Python 3.11, standard library plus neighboring project modules.
"""
import argparse
import datetime as dt
import hashlib
import json
import os
from pathlib import Path

import progress_report
import semantic_coverage

HISTORY_SCHEMA = 1
MAX_RUNS = 120
UTC = dt.timezone.utc
STATUS = {"done", "in_progress", "planned", "blocked", "todo", "ready"}


def timestamp(value):
    if not isinstance(value, str) or not value.endswith("Z"):
        raise ValueError("UTC timestamp with trailing Z required")
    parsed = dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ValueError("timezone required")
    return parsed.astimezone(UTC)


def current_snapshot(rows, structural, tasks, elf, run_id, when):
    if (not isinstance(elf, str) or len(elf) != 64
            or any(c not in "0123456789abcdef" for c in elf)):
        raise ValueError("invalid ELF digest")
    if not isinstance(run_id, str) or not run_id.strip() or len(run_id) > 100:
        raise ValueError("run ID required")
    timestamp(when)
    if not isinstance(rows, list) or not rows:
        raise ValueError("empty semantic inventory")
    addresses = [r["address"] for r in rows]
    if len(set(addresses)) != len(addresses):
        raise ValueError("duplicate inventory address")
    certified = sorted(r["address"] for r in rows
                       if r["semantic_status"] == "certified")
    bytes_total = sum(r["size"] for r in rows)
    certified_bytes = sum(r["size"] for r in rows
                          if r["semantic_status"] == "certified")
    if any(type(r["size"]) is not int or r["size"] <= 0 for r in rows):
        raise ValueError("invalid function size")
    if (structural["digest"] != elf
            or structural["accepted_count"] > structural["checkpoints"]
            or structural["review_count"] > structural["checkpoints"]):
        raise ValueError("structural evidence not bound to same ELF")
    if not isinstance(tasks, list) or not tasks:
        raise ValueError("missing completion tracker")
    ids = {t.get("id") for t in tasks}
    if None in ids or len(ids) != len(tasks):
        raise ValueError("duplicate/invalid task IDs")
    for item in tasks:
        if item.get("status") not in STATUS:
            raise ValueError("invalid task status")
        if not isinstance(item.get("depends_on"), list):
            raise ValueError("invalid task dependencies")
        if any(dep not in ids or dep == item["id"] for dep in item["depends_on"]):
            raise ValueError("unknown or self-referential dependency")
    return {
        "run_id": run_id, "observed_at_utc": when, "elf_sha256": elf,
        "inventory_addresses": len(rows), "inventory_bytes": bytes_total,
        "certified_addresses": certified,
        "certified_bytes": certified_bytes,
        "structural_checkpoints": structural["checkpoints"],
        "structural_approved": structural["accepted_count"],
        "structural_review": structural["review_count"],
        "tasks_done": sum(t["status"] == "done" for t in tasks),
        "tasks_total": len(tasks),
    }


def update_history(history, sample):
    if history is None:
        history = {"schema": HISTORY_SCHEMA, "elf_sha256": sample["elf_sha256"], "runs": []}
    if (not isinstance(history, dict) or history.get("schema") != HISTORY_SCHEMA
            or history.get("elf_sha256") != sample["elf_sha256"]
            or not isinstance(history.get("runs"), list)):
        raise ValueError("history incompatible with original ELF; start a reviewed new baseline")
    old = history["runs"]
    for previous in old:
        if (not isinstance(previous, dict)
                or previous.get("elf_sha256") != sample["elf_sha256"]
                or previous.get("inventory_addresses") != sample["inventory_addresses"]
                or previous.get("inventory_bytes") != sample["inventory_bytes"]):
            raise ValueError("inconsistent historical inventory")
        if not isinstance(previous.get("certified_addresses"), list):
            raise ValueError("invalid historic certificate set")
        if len(previous["certified_addresses"]) != len(set(previous["certified_addresses"])):
            raise ValueError("duplicate certified address in history")
    if any(x["run_id"] == sample["run_id"] for x in old):
        prior = next(x for x in old if x["run_id"] == sample["run_id"])
        if prior != sample:
            raise ValueError("same run ID cannot silently replace measurement")
        return history
    if old and timestamp(sample["observed_at_utc"]) < timestamp(old[-1]["observed_at_utc"]):
        raise ValueError("history timestamps must be monotonic")
    return {"schema": HISTORY_SCHEMA, "elf_sha256": sample["elf_sha256"],
            "runs": (old + [sample])[-MAX_RUNS:]}


def dependency_impact(tasks):
    by_id = {t["id"]: t for t in tasks}
    if len(by_id) != len(tasks):
        raise ValueError("duplicate task ID")
    children = {key: set() for key in by_id}
    for t in tasks:
        for dep in t["depends_on"]:
            if dep not in by_id:
                raise ValueError("unknown prerequisite")
            children[dep].add(t["id"])
    def descendants(start):
        found, stack = set(), list(children[start])
        while stack:
            item = stack.pop()
            if item == start:
                raise ValueError("cyclic task dependency")
            if item in found:
                continue
            found.add(item)
            stack.extend(children[item])
        return found
    return sorted(
        [{"task": t["id"], "status": t["status"],
          "downstream_not_done": sum(by_id[x]["status"] != "done"
                                      for x in descendants(t["id"]))}
         for t in tasks if t["status"] == "in_progress"],
        key=lambda x: (-x["downstream_not_done"], x["task"])
    )


def summarize(history, tasks):
    runs = history["runs"]
    if not runs:
        raise ValueError("no measurements")
    now, earlier = runs[-1], runs[-2] if len(runs) > 1 else None
    current = set(now["certified_addresses"])
    past = set(earlier["certified_addresses"]) if earlier else set()
    delta = None if earlier is None else {
        "new_certified_addresses": len(current - past),
        "removed_certified_addresses": len(past - current),
        "certified_bytes_delta": now["certified_bytes"] - earlier["certified_bytes"],
        "structural_approved_delta": now["structural_approved"] - earlier["structural_approved"],
        "structural_review_delta": now["structural_review"] - earlier["structural_review"],
        "new_tasks_done": now["tasks_done"] - earlier["tasks_done"],
    }
    cutoff = timestamp(now["observed_at_utc"]) - dt.timedelta(days=7)
    baseline = next((r for r in reversed(runs[:-1])
                     if timestamp(r["observed_at_utc"]) <= cutoff), None)
    seven = None
    if baseline:
        elapsed = (timestamp(now["observed_at_utc"]) -
                   timestamp(baseline["observed_at_utc"])).total_seconds() / 86400
        gain = len(current - set(baseline["certified_addresses"]))
        removed = len(set(baseline["certified_addresses"]) - current)
        seven = {"days_observed": round(elapsed, 2), "certificates_added": gain,
                 "certificates_removed": removed, "net_growth": gain - removed,
                 "net_per_day": round((gain - removed) / elapsed, 3)}
    return {"schema": 1, "elf_sha256": now["elf_sha256"],
            "last_run": now["run_id"], "last_observed_at_utc": now["observed_at_utc"],
            "certified": len(current), "certified_bytes": now["certified_bytes"],
            "uncertified": now["inventory_addresses"] - len(current),
            "inventory_addresses": now["inventory_addresses"],
            "inventory_bytes": now["inventory_bytes"], "structural_approved": now["structural_approved"],
            "structural_review": now["structural_review"], "tasks_done": now["tasks_done"],
            "tasks_total": now["tasks_total"], "previous_run_delta": delta,
            "rolling_7d": seven, "active_critical_dependencies": dependency_impact(tasks),
            "measurement_only_not_a_certificate": True}


def render(summary):
    d, week = summary["previous_run_delta"], summary["rolling_7d"]
    lines = [
        "# Produtividade verificável por execução — FFT Craft", "",
        f"ELF SHA-256: `{summary['elf_sha256']}`", "",
        f"Último run: `{summary['last_run']}` · {summary['last_observed_at_utc']}", "",
        "| Indicador | Valor |", "|---|---:|",
        f"| Certificados do ledger | {summary['certified']}/{summary['inventory_addresses']} |",
        f"| Bytes certificados | {summary['certified_bytes']}/{summary['inventory_bytes']} |",
        f"| Checkpoints aprovados estruturalmente | {summary['structural_approved']} |",
        f"| Checkpoints a revisar | {summary['structural_review']} |",
        f"| Atividades concluídas | {summary['tasks_done']}/{summary['tasks_total']} |", "",
        "## Variação da última execução", "",
    ]
    if d is None:
        lines.append("Primeira medição: **linha de base, sem crescimento atribuível a este run**.")
    else:
        lines.extend([
            f"- Novos endereços certificados: **{d['new_certified_addresses']}**.",
            f"- Certificados removidos: **{d['removed_certified_addresses']}**.",
            f"- Variação de bytes certificados: **{d['certified_bytes_delta']:+}**.",
            f"- Variação de aprovação estrutural: **{d['structural_approved_delta']:+}**.",
            f"- Variação de revisões pendentes: **{d['structural_review_delta']:+}**.",
            f"- Atividades concluídas adicionais: **{d['new_tasks_done']:+}**.",
        ])
    lines.extend(["", "## Janela móvel de sete dias", ""])
    if week is None:
        lines.append("**Dados históricos insuficientes (menos de sete dias): sem taxa e sem ETA.**")
    else:
        lines.append(f"- Crescimento líquido: **{week['net_growth']}** certificados em "
                     f"{week['days_observed']} dias (média **{week['net_per_day']}/dia**).")
        if week["net_growth"] <= 0:
            lines.append("- **Sem ETA inferível**: ritmo líquido não positivo.")
        else:
            lines.append("- Essa taxa não prediz a conclusão funcional do app, "
                         "nem substitui a avaliação de complexidade por bytes.")
    lines.extend(["", "## Dependências ativas e impacto no plano", ""])
    for item in summary["active_critical_dependencies"]:
        lines.append(f"- **{item['task']}**: {item['downstream_not_done']} "
                     "atividades descendentes ainda não concluídas.")
    lines.extend(["", "**Metodologia:** certificados contabilizados somente a partir "
                  "do ledger vinculado ao mesmo ELF e sujeitos ao gate independente "
                  "já existente. Endereços são conjuntos únicos; microexecuções, "
                  "documentos estáticos e builds C/C++ não acrescentam certificados. "
                  "O timestamp é do job de medição, não prova execução do código-alvo. "
                  "Ritmo de certificação por endereço não mede equivalência do APK/JNI/OBB.", ""])
    return "\n".join(lines)


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    root = semantic_coverage.ROOT
    p.add_argument("--binary", type=Path, default=semantic_coverage.BINARY)
    p.add_argument("--inventory", type=Path, default=semantic_coverage.INVENTORY)
    p.add_argument("--certificates", type=Path,
                   default=semantic_coverage.RESULTS / "semantic-certificates.json")
    p.add_argument("--tracker", type=Path,
                   default=root / "docs/re-results/RE_COMPLETION_TRACKER.json")
    p.add_argument("--results", type=Path, default=semantic_coverage.RESULTS)
    p.add_argument("--priority", type=Path,
                   default=root / "docs/alvos_prioritarios_nucleo.csv")
    p.add_argument("--history", type=Path,
                   default=semantic_coverage.RESULTS / "SEMANTIC_VELOCITY_HISTORY.json")
    p.add_argument("--report", type=Path,
                   default=semantic_coverage.RESULTS / "SEMANTIC_VELOCITY.md")
    p.add_argument("--run-id", default=os.environ.get("GITHUB_RUN_ID", "manual"))
    p.add_argument("--when", default=dt.datetime.now(UTC).isoformat(timespec="seconds")
                   .replace("+00:00", "Z"))
    args = p.parse_args(argv)
    digest = hashlib.sha256(args.binary.read_bytes()).hexdigest()
    certificates = json.loads(args.certificates.read_text(encoding="utf-8"))
    rows = semantic_coverage.ledger(args.inventory, digest, certificates)
    structural = progress_report.summarize(
        args.inventory, args.results, args.binary, args.priority)
    task_data = json.loads(args.tracker.read_text(encoding="utf-8"))
    if task_data.get("elf_sha256") != digest:
        raise ValueError("tracker references another ELF")
    tasks = task_data["tasks"]
    sample = current_snapshot(rows, structural, tasks, digest, args.run_id, args.when)
    old = (json.loads(args.history.read_text(encoding="utf-8"))
           if args.history.exists() else None)
    history = update_history(old, sample)
    report = render(summarize(history, tasks))
    args.history.parent.mkdir(parents=True, exist_ok=True)
    args.history.write_text(json.dumps(history, indent=2) + "\n", encoding="utf-8")
    args.report.write_text(report, encoding="utf-8")
    print("SEMANTIC_VELOCITY_CERTIFIED=" + str(len(sample["certified_addresses"])))
    print("SEMANTIC_VELOCITY_HISTORY_RUNS=" + str(len(history["runs"])))
    print("SEMANTIC_VELOCITY_NEW_CERTIFICATES=" +
          str((summarize(history, tasks)["previous_run_delta"] or {})
              .get("new_certified_addresses", 0)))


if __name__ == "__main__":
    main()
