#!/usr/bin/env python3
"""Read-only 40-task orchestration and ARM unknown-region/review prioritization."""
import argparse
import csv
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

import progress_report

ROOT = Path(__file__).resolve().parents[2]
SHA = "bf913415ab9458a83b14ac8c8a0fa3430d1f5d18bfbcd7c7472d6f5e8b4850bc"
PHASES = ((1, 5, "P0"), (6, 13, "P1"), (14, 26, "P2"),
          (27, 31, "P3"), (32, 34, "P4"), (35, 40, "P5"))
TASK = re.compile(r"^- \[([ xX])\] \*\*(T\d{2}) — (.+?)\*\*", re.M)
LOG = re.compile(r"^- \*\*(T\d{2})(.*?)\*\*", re.M)
STATE = re.compile("— " + re.escape(chr(96)) +
                   r"(pending|in_progress|blocked|ready_for_review|done)" +
                   re.escape(chr(96)))


def read_plan(raw):
    found = list(TASK.finditer(raw))
    expected = ["T%02d" % i for i in range(1, 41)]
    if [m.group(2) for m in found] != expected:
        raise ValueError("Expected T01..T40 exactly once, in order")
    if "## 7. Registro de execução" not in raw or "## 8. Referências" not in raw:
        raise ValueError("Missing official execution journal")
    journal = raw.split("## 7. Registro de execução", 1)[1].split(
        "## 8. Referências", 1)[0]
    primary, slices = {}, Counter()
    for m in LOG.finditer(journal):
        tid, annotation = m.groups()
        if tid not in expected:
            raise ValueError("Unrecognized task in journal")
        status = STATE.search(annotation)
        if not status:
            raise ValueError("Journal record without status")
        if "fatia" in annotation.split(" — ", 1)[0].lower():
            if status.group(1) == "done":
                raise ValueError("Partial slice cannot complete a task")
            slices[tid] += 1
        else:
            if tid in primary:
                raise ValueError("Duplicate primary journal state")
            primary[tid] = status.group(1)
    tasks, mismatches = [], []
    for m in found:
        checkbox, tid, title = m.groups()
        status = primary.get(tid, "partial_slice" if slices[tid] else "pending")
        if checkbox.lower() == "x" and status != "done":
            raise ValueError("Checkbox cannot override completion evidence")
        if checkbox == " " and status == "done":
            mismatches.append(tid)
        n = int(tid[1:])
        phase = next(code for low, high, code in PHASES if low <= n <= high)
        tasks.append({"id": tid, "title": title.rstrip("."),
                      "phase": phase, "status": status,
                      "partial_slices": slices[tid],
                      "original_checklist_checked": checkbox.lower() == "x"})
    return tasks, mismatches


def validated_gaps(doc, sha):
    if doc.get("elf_sha256") != sha:
        raise ValueError("T04 report is for a different ELF")
    rows = doc.get("gaps")
    if not isinstance(rows, list) or len(rows) != doc.get("gap_interval_count"):
        raise ValueError("Missing or truncated T04 gap population")
    section = doc["text_section"]
    start, end = int(section["start"], 16), int(section["end"], 16)
    previous = start
    for row in sorted(rows, key=lambda x: int(x["address"], 16)):
        addr, size = int(row["address"], 16), row["size"]
        if type(size) is not int or size <= 0 or addr < previous or addr + size > end:
            raise ValueError("Unsorted, overlapping or invalid T04 interval")
        previous = addr + size
    if sum(r["size"] for r in rows) != doc.get("text_bytes_uncovered"):
        raise ValueError("T04 byte count differs from individual intervals")
    return rows


def review_queue(current, historical, core):
    previous = {x["address"]: x["category"] for x in historical["entries"]}
    if len(previous) != len(historical["entries"]):
        raise ValueError("Duplicate historical review")
    queue = []
    for size, address, name, state, coverage, unresolved, resolved in current["review_rows"]:
        if state != "needs_review":
            raise ValueError("Unexpected state in live review queue")
        category = previous.get(address, "not_in_old_triage")
        score = (250 if int(address, 16) & 1 else 0)
        score += (100 if address in core else 0)
        score += (50 if unresolved else 0)
        score += (25 if category == "not_in_old_triage" else 0)
        score += (20 if category == "A_already_read_full_history" else 0)
        score += min(50, size // 64)
        queue.append({"address": address, "name": name, "size": size,
                      "coverage_pct": coverage, "historical_category": category,
                      "unresolved_tables": unresolved, "core": address in core,
                      "priority_score": score, "proof": "needs_review",
                      "certified": False})
    if len(queue) != current["review_count"]:
        raise ValueError("Current T06 review queue incomplete")
    return sorted(queue, key=lambda x: (-x["priority_score"], x["address"]))


def gap_queue(doc, entries):
    init = [int(x, 16) for x in doc["init_array_fini_array_targets_not_in_inventory"]]
    queue = []
    for row in entries:
        addr, size = int(row["address"], 16), row["size"]
        inits = ["0x%x" % x for x in init if addr <= x < addr + size]
        classification = row["classification"]
        if classification not in ("plausible_function_start",
                                  "ambiguous_needs_structural_pass",
                                  "undecodable_at_arm32"):
            raise ValueError("Unknown gap classification")
        score = (250 if inits else 0)
        score += 60 if classification == "plausible_function_start" else 0
        score += 20 if 64 <= size <= 512 else 0
        score += 10 if size <= 4096 else 0
        queue.append({"address": row["address"], "size": size,
                      "classification": classification, "init_fini_targets": inits,
                      "priority_score": score, "instruction_hint": row.get("first_instruction"),
                      "is_confirmed_function": False, "certified": False})
    return sorted(queue, key=lambda x: (-x["priority_score"], x["size"],
                                         int(x["address"], 16)))


def assemble(plan, gaps, triage, current, core, sha, run_id):
    tasks, unchecked = read_plan(plan)
    unknowns = gap_queue(gaps, validated_gaps(gaps, sha))
    reviews = review_queue(current, triage, core)
    return {
        "schema": 1, "run_id": str(run_id), "elf_sha256": sha,
        "task_count": len(tasks),
        "task_states": dict(sorted(Counter(x["status"] for x in tasks).items())),
        "phase_states": {p: dict(Counter(x["status"] for x in tasks if x["phase"] == p))
                         for _, _, p in PHASES},
        "task_records": tasks, "unchecked_completed_task_ids": unchecked,
        "old_17_task_tracker_is_separate": True,
        "t04": {"interval_count": len(unknowns),
                "uncovered_bytes": gaps["text_bytes_uncovered"],
                "candidates": unknowns, "certified_functions_added": 0},
        "t05": {"canonical_ledger_reconciliation_still_needed": True},
        "t06": {"current_review_count": current["review_count"],
                "current_core_review_count": current["core_review"],
                "old_review_count": triage["total_needs_review"],
                "old_triage_outdated": triage["total_needs_review"] != current["review_count"],
                "without_old_triage_category": sum(
                    x["historical_category"] == "not_in_old_triage" for x in reviews),
                "candidates": reviews, "approved_automatically": 0},
        "safety": {"changes_task_state": False, "issues_semantic_certificate": False,
                   "links_original_game_binary": False,
                   "claims_full_app_completion": False}
    }


def markdown(data):
    lines = ["# FFT Craft — orquestrador T01–T40", "",
             "ELF SHA-256: " + data["elf_sha256"] + " | run: " + data["run_id"], "",
             "## Estados auditados", "", "| Estado | Quantidade |", "|---|---:|"]
    lines += [f"| {k} | {n} |" for k, n in data["task_states"].items()]
    lines += ["", "T11 concluída não é igual a app concluído. Checkboxes iniciais "
              "não substituem o registro de execução.", "",
              "Checklist a reconciliar: " +
              (", ".join(data["unchecked_completed_task_ids"]) or "nenhum"), "",
              "## T04 — intervalos não inventariados", "",
              f"Total: {data['t04']['interval_count']} intervalos / "
              f"{data['t04']['uncovered_bytes']} bytes.", "",
              "| Prioridade | Endereço | Bytes | Evidência de startup |",
              "|---:|---|---:|---|"]
    for x in data["t04"]["candidates"][:20]:
        lines.append(f"| {x['priority_score']} | {x['address']} | {x['size']} | "
                     f"{', '.join(x['init_fini_targets']) or '—'} |")
    lines += ["", "## T06 — revisões do ELF corrente", "",
              f"Fila atual: {data['t06']['current_review_count']} (núcleo: "
              f"{data['t06']['current_core_review_count']}); "
              f"fila histórica: {data['t06']['old_review_count']}.", "",
              "| Prioridade | Endereço | Função | Cobertura estrutural |",
              "|---:|---|---|---:|"]
    for x in data["t06"]["candidates"][:25]:
        lines.append(f"| {x['priority_score']} | {x['address']} | "
                     f"{x['name'].replace('|', '/')} | {x['coverage_pct']}% |")
    lines += ["", "## Critérios de segurança", "",
              "A fila é triagem apenas: não aprova checkpoints nem funções, "
              "não altera o ledger e não registra certificações semânticas.",
              "Resolver primeiro ARM/Thumb, limites e CFG, depois contratos "
              "e revisão independente.", ""]
    return "\n".join(lines)


def run(args):
    sha = hashlib.sha256(args.binary.read_bytes()).hexdigest()
    if sha != SHA:
        raise ValueError("ELF original não corresponde à linha de base")
    current = progress_report.summarize(args.inventory, args.results,
                                        args.binary, args.priority)
    with args.priority.open(encoding="utf-8", newline="") as f:
        core = {r["address"].lower() for r in csv.DictReader(f)}
    return assemble(args.plan.read_text(encoding="utf-8"),
                    json.loads(args.gaps.read_text(encoding="utf-8")),
                    json.loads(args.old_triage.read_text(encoding="utf-8")),
                    current, core, sha, args.run_id)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--binary", type=Path, default=ROOT / "src/lib/armeabi/libgl2jni.so")
    p.add_argument("--inventory", type=Path, default=ROOT / "docs/RE_FUNCTION_INVENTORY.csv")
    p.add_argument("--priority", type=Path, default=ROOT / "docs/alvos_prioritarios_nucleo.csv")
    p.add_argument("--results", type=Path, default=ROOT / "docs/re-results")
    p.add_argument("--plan", type=Path, default=ROOT / "docs/RE_COMPLETUDE_TASKS.md")
    p.add_argument("--gaps", type=Path, default=ROOT / "docs/re-baseline/text_coverage_gaps.json")
    p.add_argument("--old-triage", type=Path, default=ROOT / "docs/re-baseline/t06_checkpoint_triage.json")
    p.add_argument("--json-output", type=Path, required=True)
    p.add_argument("--md-output", type=Path, required=True)
    p.add_argument("--run-id", default="manual")
    a = p.parse_args()
    data = run(a)
    a.json_output.parent.mkdir(parents=True, exist_ok=True)
    a.md_output.parent.mkdir(parents=True, exist_ok=True)
    a.json_output.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n",
                             encoding="utf-8")
    a.md_output.write_text(markdown(data), encoding="utf-8")
    print("TASK40_DONE=" + str(data["task_states"].get("done", 0)))
    print("T04_GAPS=" + str(data["t04"]["interval_count"]))
    print("T06_REVIEW=" + str(data["t06"]["current_review_count"]))
    print("TASK40_AUTO_APPROVALS=0")


if __name__ == "__main__":
    main()
