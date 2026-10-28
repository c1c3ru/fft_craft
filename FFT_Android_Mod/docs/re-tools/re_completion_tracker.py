#!/usr/bin/env python3
"""Strict and reproducible RE completion tracker. Never promotes certificates."""
import argparse
import json
import re
from pathlib import Path

STATUSES = {"planned", "in_progress", "blocked", "done"}
SHA = re.compile(r"^[a-f0-9]{64}$")
TASK = re.compile(r"^[A-Z][0-9]{2}$")


def validate(obj, sha):
    if not isinstance(obj, dict) or obj.get("schema") != 1:
        raise ValueError("Invalid completion schema")
    if not isinstance(sha, str) or not SHA.fullmatch(sha) or obj.get("elf_sha256") != sha:
        raise ValueError("Stale or invalid original ELF SHA-256")
    if obj.get("scope") != "end_to_end_android_app":
        raise ValueError("Invalid app completion scope")
    phases = obj.get("phases")
    tasks = obj.get("tasks")
    if not isinstance(phases, list) or len(phases) != 7 or any(
            not isinstance(p, dict) or p.get("id") != f"F{i}"
            or not isinstance(p.get("title"), str) or not p["title"].strip()
            or not isinstance(p.get("exit_gate"), str) or not p["exit_gate"].strip()
            for i, p in enumerate(phases)):
        raise ValueError("Expected F0-F6 with nonempty exit gates")
    if not isinstance(tasks, list) or not tasks:
        raise ValueError("Empty task queue")
    by_id = {}
    for t in tasks:
        if not isinstance(t, dict) or not TASK.fullmatch(str(t.get("id", ""))):
            raise ValueError("Invalid task ID")
        k = t["id"]
        if k in by_id or t.get("phase") not in {x["id"] for x in phases}:
            raise ValueError(f"Duplicate task or unknown stage: {k}")
        if t.get("status") not in STATUSES:
            raise ValueError(f"Invalid status: {k}")
        if type(t.get("priority")) is not int or t["priority"] not in (1, 2, 3):
            raise ValueError(f"Invalid priority: {k}")
        for field in ("title", "next_action", "acceptance"):
            if not isinstance(t.get(field), str) or not t[field].strip():
                raise ValueError(f"Missing {k}.{field}")
        deps, evidence = t.get("depends_on"), t.get("evidence")
        if not isinstance(deps, list) or len(set(deps)) != len(deps):
            raise ValueError(f"Invalid dependencies: {k}")
        if not isinstance(evidence, list) or any(
                not isinstance(e, str) or not e.strip() for e in evidence):
            raise ValueError(f"Invalid evidence: {k}")
        if t["status"] == "done" and not evidence:
            raise ValueError(f"Completed task without evidence: {k}")
        by_id[k] = t
    visited, visiting = set(), set()

    def check(k):
        if k in visiting:
            raise ValueError("Cyclic dependencies")
        if k in visited:
            return
        visiting.add(k)
        t = by_id[k]
        for dep in t["depends_on"]:
            if dep == k or dep not in by_id:
                raise ValueError(f"Unknown/self dependency: {k}")
            check(dep)
            if t["status"] == "done" and by_id[dep]["status"] != "done":
                raise ValueError(f"Completed before dependency: {k}")
        visiting.remove(k)
        visited.add(k)
    for k in by_id:
        check(k)
    return obj


def safe(s):
    return s.replace("|", "/").replace("\n", " ").replace("[", "(").replace("]", ")")


def render(obj):
    by_id = {t["id"]: t for t in obj["tasks"]}
    tasks = obj["tasks"]
    running = [t for t in tasks if t["status"] == "in_progress"]
    ready = [t for t in tasks if t["status"] == "planned" and all(
        by_id[k]["status"] == "done" for k in t["depends_on"])]
    done = [t for t in tasks if t["status"] == "done"]
    blocked = [t for t in tasks if t["status"] == "blocked"]
    lines = [
        "## Plano de conclusão da engenharia reversa do app", "",
        "[Plano e critérios de aceite](../RE_COMPLETION_PLAN.md) · "
        "[Fila e evidências versionadas](RE_COMPLETION_TRACKER.json)", "",
        "**Escopo:** engenharia reversa funcional, C/C++, JNI/Smali, "
        "APK/OBB e execução em Android suportado.", "",
        f"**Atividades:** {len(tasks)} totais; **{len(done)} concluídas com evidência**; "
        f"**{len(running)} em andamento**; **{len(ready)} prontas para iniciar**; "
        f"**{len(blocked)} bloqueadas**. Dependências pendentes não contam como prontas.",
        "", "| Etapa | Gate de saída | Concluídas / total |",
        "|---|---|---:|",
    ]
    for p in obj["phases"]:
        group = [t for t in tasks if t["phase"] == p["id"]]
        count = sum(t["status"] == "done" for t in group)
        lines.append(f"| {p['id']} — {safe(p['title'])} | "
                     f"{safe(p['exit_gate'])} | {count}/{len(group)} |")
    lines.extend(["", "### Próximas atividades executáveis", ""])
    selection = sorted(running + ready, key=lambda t: (
        t["priority"], t["status"] != "in_progress", t["id"]))
    for t in selection[:8]:
        state = "em andamento" if t["status"] == "in_progress" else "pronta"
        lines.append(f"- **{t['id']} (P{t['priority']}, {state})** — "
                     f"{safe(t['next_action'])} **Aceite:** {safe(t['acceptance'])}")
    if not selection:
        lines.append("Nenhuma atividade pronta; verificar bloqueios no rastreador.")
    lines.extend(["", "### Próximas dependências não liberadas", ""])
    dependent = [t for t in tasks if t["status"] == "planned" and t not in ready]
    for t in sorted(dependent, key=lambda t: (t["priority"], t["id"]))[:8]:
        outstanding = [k for k in t["depends_on"] if by_id[k]["status"] != "done"]
        lines.append(f"- **{t['id']}**: aguarda {', '.join(outstanding)}.")
    if not dependent:
        lines.append("Nenhuma dependência planejada pendente.")
    lines.extend(["", "**Regra por PR:** mudar estado, ação seguinte, dependências "
                  "e evidências no JSON; atualizar o relatório técnico; "
                  "regenerar este painel; exigir CI verde. "
                  "Somente marcar done com provas e todas as dependências concluídas.",
                  "**Gate global:** nenhuma lacuna funcional relevante; fluxos "
                  "originais comparados à reimplementação, APK/OBB instalado e "
                  "matriz de testes Android aprovada. Microexecuções e "
                  "certificados de BX LR não satisfazem esse gate.", ""])
    return "\n".join(lines)


def render_file(path, sha):
    if not path.is_file():
        return ("## Plano de conclusão da engenharia reversa do app\n\n"
                "**Rastreador não encontrado:** nenhum andamento foi validado.")
    return render(validate(json.loads(path.read_text(encoding="utf-8")), sha))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tracker", type=Path, required=True)
    parser.add_argument("--expected-sha", required=True)
    args = parser.parse_args()
    obj = json.loads(args.tracker.read_text(encoding="utf-8"))
    validate(obj, args.expected_sha)
    print("RE_COMPLETION_TRACKER_VALID=1")
    print(f"RE_COMPLETION_TRACKER_TASKS={len(obj['tasks'])}")
    print(f"RE_COMPLETION_TRACKER_DONE={sum(t['status']=='done' for t in obj['tasks'])}")


if __name__ == "__main__":
    main()
