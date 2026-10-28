#!/usr/bin/env python3
"""Generate a central, evidence-linked FFT Craft status dashboard.

Only same-ELF verified checkpoint records enter coverage metrics. A merged PR
is metadata, not evidence of semantic equivalence. The dashboard never
silently sums overlapping historical CSV and checkpoint populations.
"""
import argparse
import csv
import json
import re
from collections import Counter
from pathlib import Path

import progress_report
import central_semantic_summary
import re_completion_tracker

ROOT = Path(__file__).resolve().parents[2]
RESULTS = ROOT / "docs/re-results"
REPO = "c1c3ru/fft_craft"
MILESTONES = (
    ("CI_RELIABILITY_2026-10-28.md",
     "CI auditado: falhas históricas de fixture e Unicorn separadas do HEAD verde; cancelar apenas runs obsoletos de PR"),
    ("SEMANTIC_SOUND_GLOBAL_SLOT.md",
     "Som: slot global do ELF em 0x34615c, relocação e 512 leituras ARM com memória sintética"),
    ("SEMANTIC_SOUND_COMMON_PROLOGUE.md",
     "Corpo comum 0x2b2b7c: cinco instruções ARM e 128 testes diferenciais C com pilha e literal originais"),
    ("SEMANTIC_SOUND_COMMON_BODY_2B2B7C.md",
     "Corpo comum 0x2b2b7c: desmontagem original A32 e execução limitada antes de efeitos não modelados"),
    ("SEMANTIC_SOUND_FUNCTIONAL_RECONSTRUCTION.md",
     "sound_request: reconstrução parcial C do prefixo A32 e 128 comparações ARM/C"),
    ("SEMANTIC_SOUND_PLAYDEF_ENTRY.md",
     "SysSE_PlayDef 0x2b2cf8: auditoria estática A32 de 128 bytes; nenhuma instrução executada"),
    ("SEMANTIC_SOUND_THREE_ENTRY_EXEC.md",
     "sound_request: 384 microexecucoes em tres entradas ARM ate destinos de funcao nao executados"),
    ("SEMANTIC_A04_VENEERS.md",
     "A04: dois veneers ARM via GOT/PC com 64 microexecuções e zero alvos indiretos executados (run #40751407523)"),
    ("SEMANTIC_A04_DISPATCHER.md",
     "A04: dispatcher e getter originais microexecutados em 544 cenários, com memória controlada (run #40750531709)"),
    ("SEMANTIC_A04_DESTINATIONS.md",
     "A04: sete destinos ARM auditados estaticamente em 672 bytes do ELF original (run #40748750630); três destinos sem execução"),
    ("SEMANTIC_A02_BRANCHES.md",
     "A02 validada no ELF: 11 entradas, 352 microexecuções ARM e 0 destinos externos executados (run #40735782606); A04 investiga sete destinos"),
    ("SEMANTIC_A01_MEMORY.md",
     "A01 concluída: 10 rotinas STRB/LDRB/LDR no ELF real, 320 testes diferenciais (run #40730706242); 11 pendentes para A02"),
    ("SEMANTIC_REMAINING_34.md",
     "Issue #388: 34 endereços catalogados; 13 STR/BX LR e 416 testes Unicorn aprovados; 21 pendentes"),
    ("SEMANTIC_LOOP_250_FULL.md",
     "Loop ELF 250: 216 candidatos A32, 6.912 microexecuções e 14 checkpoints (run #40713115396); sem novos certificados"),
    ("SEMANTIC_LOOP_250.md",
     "Loop semântico A32: 24 funções-folha e 768 microexecuções do ELF (run #40710246666), zero novos certificados"),
    ("SEMANTIC_PIPELINE_RECOVERY.md",
     "Correção de 25 manifestos/250 tarefas e conflito do PR automatizado #362; sem novos certificados"),
    ("SEMANTIC_SOUND_DESTINATION_271314.md",
     "sound_request: destino 0x271314 e tres entradas ARM auditados no ELF original; execucao ainda pendente"),
    ("SEMANTIC_SOUND_TWO_HOP_EXEC.md",
     "sound_request: dois desvios ARM microexecutados ate destino ainda desconhecido"),
    ("SEMANTIC_BATCH_SCALING.md",
     "Lotes semânticos de 100/200 funções com revisão independente"),
    ("SEMANTIC_BXLR_REVIEW_BATCH.md",
     "Primeiro lote de cinco contratos BX LR preparados para revisão humana"),
    ("SEMANTIC_CERTIFICATION_POLICY.md",
     "Política de certificação: contrato integral, ELF, revisão independente e CI"),
    ("SEMANTIC_BXLR_CONTRACT_PILOT.md",
     "Primeiros contratos locais BX LR com retornos ARM/Thumb verificados"),
    ("SEMANTIC_HISTORY_INDEX.md",
     "Índice do acervo semântico acumulado e vinculado ao mesmo ELF"),
    ("SEMANTIC_LEAF_BXLR.md",
     "Candidatas ARM de retorno simples microexecutadas para contratos revisáveis"),
    ("SEMANTIC_HOUKOKU_NEXT_BOUNDARIES.md",
     "Destinos ARM seguintes de houkoku_okng auditados sem executar ramos desconhecidos"),
    ("SEMANTIC_POST_GETTER_PATHS.md",
     "Três destinos de SysSE_Play e argumentos pós-GetScale verificados por máquina"),
    ("SEMANTIC_GETPARAM_GETSCALE_MICROEXEC.md",
     "GetParam/GetScale ARM: 96 microexecuções individuais e via BL original"),
    ("SEMANTIC_GETPARAM_GETSCALE_AUDIT.md",
     "Instruções e destinos de chamada GetParam/GetScale auditados"),
    ("SEMANTIC_NEXT_POINTER_MICROEXEC.md",
     "Próximas leituras globais de som e ícones verificadas até as primeiras chamadas BL"),
    ("SEMANTIC_NEXT_BOUNDARIES.md",
     "Inventário dos opcodes ARM reais nos limites de som e ícones"),
    ("SEMANTIC_SOUND_ICON_MICROEXEC.md",
     "Som até 0x2b2b7c e prólogo de iOS_SetIconPosition até 0x2b8928"),
    ("SEMANTIC_THREE_CALLEES_EXECUTION.md",
     "Três callees ARM e duas continuações controladas do chamador"),
    ("SEMANTIC_V2ICON_CALL_FLOW.md",
     "BL/BX LR de V2Icon e seleção de três caminhos"),
    ("SEMANTIC_RETURN_CALL_BOUNDARY.md",
     "Retorno ARM real e alterações de memória antes da primeira chamada"),
)
CURRENT_SEMANTIC_BOUNDARIES = (
    ("0x34615c", "Investigar a inicialização/relocação em tempo de execução do slot de som; o ELF estático não prova seu valor em memória do processo"),
    ("0x2bf008", "Investigar o próximo BL de SysSE_Play depois do desvio condicionado"),
    ("0x0a7034", "Investigar o próximo BL de iOS_SetIconPosition com os argumentos já observados"),
)
EVIDENCE_RE = re.compile(r"Evidence collected:\s*\*\*(\d+)/(\d+)\*\*")
SHA_RE = re.compile(r"ELF SHA-256:\s*`([a-f0-9]{64})`")


def percent(numerator, denominator):
    return "não mensurável" if not denominator else f"{100*numerator/denominator:.1f}%"


def current_v3(results, digest):
    """Only v3 records for the exact same binary with consistent metadata."""
    counts = Counter()
    for path in sorted(results.glob("*.json")):
        try:
            value = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        if (value.get("binary_sha256") != digest
                or value.get("pipeline_version") != 2
                or value.get("structural_version") != 3
                or path.stem.lower() != str(value.get("address", "")).lower()):
            continue
        counts["v3"] += 1
        counts[value.get("status", "unknown")] += 1
    return counts


def evidence_status(results, digest, pending_count):
    path = results / "SEMANTIC_EVIDENCE_INDEX.md"
    if not path.is_file():
        return "Relatório de evidências indisponível (não corresponde a aprovação semântica)."
    content = path.read_text(encoding="utf-8")
    match = EVIDENCE_RE.search(content)
    sha = SHA_RE.search(content)
    if not match or not sha or sha.group(1) != digest:
        return "Índice semântico ausente, incompleto ou referente a outro binário."
    found, total = (int(match.group(1)), int(match.group(2)))
    status = f"{found}/{total} relatórios estáticos de evidências"
    if total != pending_count:
        status += f" — desatualizado perante {pending_count} checkpoints pendentes"
    return status + ". **Relatórios não são equivalência semântica certificada.**"


def queue_rows(results):
    path = results / "REVIEW_QUEUE.csv"
    if not path.is_file():
        return []
    with path.open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream))


def recent_prs(raw, repository=REPO):
    """Filter to merged PRs in this repo and expose normalized safe links."""
    if not isinstance(raw, list):
        raise ValueError("GitHub PR metadata must be a JSON array")
    results = []
    for pr in raw:
        if not isinstance(pr, dict) or not pr.get("merged_at"):
            continue
        number = pr.get("number")
        if type(number) is not int or number <= 0:
            continue
        # Construct destination from authenticated repository context, not
        # an arbitrary URL embedded in the metadata.
        title = str(pr.get("title") or "PR sem título").replace("|", "/")
        title = title.replace("\n", " ").replace("[", "(").replace("]", ")")
        results.append((str(pr["merged_at"]), number, title,
                        f"https://github.com/{repository}/pull/{number}"))
    results.sort(reverse=True)
    return results[:5]


def render(data, results, prs=None, semantic=None):
    accepted, review, total = (data["accepted_count"], data["review_count"],
                               data["checkpoints"])
    if accepted + review > total:
        raise ValueError("Invalid checkpoint status accounting")
    v3 = current_v3(results, data["digest"])
    open_rows = queue_rows(results)
    lines = [
        "# FFT Craft — status geral", "",
        "> Painel gerado automaticamente com dados do ELF, inventário e "
        "checkpoints. **Cobertura estrutural não demonstra equivalência semântica.**", "",
        f"**ELF SHA-256:** `{data['digest']}`", "",
        "## Visão geral", "",
        "| Indicador | Resultado | Origem / interpretação |",
        "|---|---:|---|",
        f"| Funções no inventário | {data['rows']:,} | Inventário ARM |",
        f"| Checkpoints JSON válidos para este ELF | {total:,} | Status acompanhados |",
        f"| Aprovados estruturalmente | {accepted:,} | "
        "Aprovação automática de estrutura, não de comportamento |",
        f"| Precisam de revisão | {review:,} | Status `needs_review` |",
        f"| Aprovação estrutural entre checkpoints | "
        f"**{percent(accepted,total)}** | {accepted:,}/{total:,}, "
        "**não** percentual de engenharia reversa completa |",
        f"| Checkpoints pendentes de criação | {data['pending_count']:,} | "
        "Não incluem funções cobertas apenas pelo histórico CSV |",
        f"| Metas de núcleo em revisão | {data['core_review']:,} | "
        f"De {data['core_checkpointed']:,} checkpoints do núcleo |",
        f"| v3: checkpoints / aprovados / revisão | {v3['v3']:,} / "
        f"{v3['auto_structural']:,} / {v3['needs_review']:,} | "
        "Subconjunto já analisado pelas regras v3 |",
        "| Equivalência semântica integral registrada | "
        f"**{semantic['certified']:,}** | Certificados revisáveis vinculados ao ELF; "
        "microexecuções não são certificados |" if semantic is not None
        else "| Equivalência semântica integral registrada | **não mensurada** | "
             "Dados de certificados não disponíveis nesta geração |",
        "", "O histórico CSV contém "
        f"**{data['historical_count']:,}** registros de análise anterior, "
        "que podem se sobrepor aos checkpoints. "
        "**Não somamos esses conjuntos para criar um percentual global fictício.**",
        "", "## Fluxo de reconstrução funcional", "",
        "A prioridade é reconstruir comportamento verificável (estrutura, semântica, C/C++, diferencial), não aumentar certificados.",
        "[Etapas, gates e prioridades](../RECONSTRUCTION_WORKFLOW.md)",
        "", re_completion_tracker.render_file(
            results / "RE_COMPLETION_TRACKER.json", data["digest"]),
        "## Evidência e testes semânticos", "",
        evidence_status(results, data["digest"], review), "",
        "Os relatórios abaixo apresentam **efeitos locais testados sob estados "
        "sintéticos** e seus limites. Testes passando não significam que "
        "a função inteira foi reconstruída:", "",
    ]
    for filename, description in MILESTONES:
        if (results / filename).is_file():
            lines.append(f"- [{description}]({filename})")
    if semantic is not None:
        lines.extend(["", central_semantic_summary.render(semantic)])
    lines.extend(["", "## Próximas prioridades", "",
                  "### Lacunas semânticas conhecidas", ""])
    for address, description in CURRENT_SEMANTIC_BOUNDARIES:
        lines.append(f"- `{address}`: {description}.")
    lines += ["", "Estas prioridades são **curadas no gerador**; "
              "quando um limite for resolvido, a descrição deve ser "
              "atualizada no mesmo PR de análise.", "",
              "### Revisão estrutural — fila atual do núcleo", "",
              "| Endereço | Função | Cobertura | Motivo |",
              "|---|---|---:|---|"]
    if open_rows:
        for item in open_rows[:6]:
            addr = str(item.get("address", "")).lower()
            name = str(item.get("name", "")).replace("|", "/").replace("\n", " ")
            lines.append(f"| `{addr}` | {name} | "
                         f"{item.get('coverage_pct', '—')}% | "
                         f"{item.get('review_reason', '—')} |")
    else:
        lines.append("| — | Fila ausente ou sem itens | — | — |")
    lines.extend(["", "## Pull requests recentes", ""])
    if prs is None:
        lines += ["Metadados dos PRs indisponíveis nesta execução local; "
                  f"[consultar merges]("
                  f"https://github.com/{REPO}/pulls?q=is%3Apr+is%3Amerged)."]
    else:
        verified = recent_prs(prs)
        if verified:
            for _, number, title, url in verified:
                lines.append(f"- [PR #{number} — {title}]({url})")
        else:
            lines.append("Nenhum PR mesclado encontrado nos metadados fornecidos.")
    lines.extend(["", "## Atualização automática e fontes", "",
                  "O workflow `re-batches.yml` regenera este arquivo "
                  "**depois** de calcular progresso, revisar checkpoints v3 "
                  "e executar os testes semânticos; publica os resultados "
                  "no PR automático de checkpoints apenas se o CI passar.",
                  "O workflow `re-pipeline.yml` testa a geração em PRs "
                  "sem publicar as alterações.",
                  "- [PROGRESS.md](PROGRESS.md) — dados estruturais do inventário.",
                  "- [STRUCTURAL_V3_REPORT.md](STRUCTURAL_V3_REPORT.md) — migração v3.",
                  "- [SEMANTIC_EVIDENCE_INDEX.md](SEMANTIC_EVIDENCE_INDEX.md) "
                  "— evidência estática das pendências.",
                  "- [REVIEW_TRIAGE.md](REVIEW_TRIAGE.md) — critérios de priorização.",
                  f"- [GitHub Actions](https://github.com/{REPO}/actions) "
                  "— execução e eventuais falhas de CI.",
                  "", "**Limitação:** o painel não é um contador de "
                  "reconstrução semântica completa. Uma certificação "
                  "desse tipo exigiria contratos e testes integrais "
                  "por função; os registros parciais não constituem tais certificações.",
                  ""])
    return "\n".join(lines)


def generate(inventory, results, priority, binary, pulls_json=None,
             pilot_dir=None, dynamic_dir=None, manifests_dir=None,
             contracts_dir=None):
    data = progress_report.summarize(inventory, results, binary, priority)
    prs = None
    if pulls_json is not None and pulls_json.is_file():
        prs = json.loads(pulls_json.read_text(encoding="utf-8"))
    semantic = central_semantic_summary.summarize(
        inventory, data["digest"], results / "semantic-certificates.json",
        pilot_dir, dynamic_dir, manifests_dir, history_dir=results,
        contracts_dir=contracts_dir,
        snapshot_path=results / "SEMANTIC_RUN_SNAPSHOT.json", binary=binary,
        review_batch_path=results / "SEMANTIC_BXLR_REVIEW_BATCH.json")
    return render(data, results, prs, semantic)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--inventory", type=Path,
                        default=ROOT / "docs/RE_FUNCTION_INVENTORY.csv")
    parser.add_argument("--results", type=Path, default=RESULTS)
    parser.add_argument("--priority", type=Path,
                        default=ROOT / "docs/alvos_prioritarios_nucleo.csv")
    parser.add_argument("--binary", type=Path,
                        default=ROOT / "src/lib/armeabi/libgl2jni.so")
    parser.add_argument("--pulls-json", type=Path,
                        help="Optional GitHub REST merged-PR list saved by workflow")
    parser.add_argument("--pilot-dir", type=Path)
    parser.add_argument("--dynamic-dir", type=Path)
    parser.add_argument("--manifests-dir", type=Path)
    parser.add_argument("--contracts-dir", type=Path)
    args = parser.parse_args()
    text = generate(args.inventory, args.results, args.priority, args.binary,
                    args.pulls_json, args.pilot_dir, args.dynamic_dir,
                    args.manifests_dir, args.contracts_dir)
    dest = args.results / "STATUS_GERAL.md"
    temporary = dest.with_suffix(".md.tmp")
    temporary.write_text(text, encoding="utf-8")
    temporary.replace(dest)
    print(f"Updated {dest}")
    print(f"Structural checkpoint completion: {text.split('Aprovação estrutural entre checkpoints | ', 1)[1].split(' |',1)[0]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
