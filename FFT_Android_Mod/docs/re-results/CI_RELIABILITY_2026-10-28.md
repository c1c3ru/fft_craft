# Diagnóstico e estabilização do CI — 28/10/2026

## Situação verificada

- **Nenhum PR aberto** durante a auditoria, após o merge do [PR #394](https://github.com/c1c3ru/fft_craft/pull/394).
- O último lote automático da `main`, [run #40731929672](https://github.com/c1c3ru/fft_craft/actions/runs/40731929672) (merge `bc6cfa3144c15730460c60cdc5fad23c94d3ead8`), terminou **success**.
- O PR #394 na revisão final `03e155b4175942d7dfcd0ae76fb1b9da95547e3d` passou em `unit-tests`, `structural-smoke`, `manifests`, `real-elf-250` e `GitGuardian Security Checks`.
- As três falhas recentes de [run #40730586589](https://github.com/c1c3ru/fft_craft/actions/runs/40730586589), [#40730586637](https://github.com/c1c3ru/fft_craft/actions/runs/40730586637) e [#40730586739](https://github.com/c1c3ru/fft_craft/actions/runs/40730586739) referiam-se **ao mesmo commit intermediário** `8eab5a0d9bce` e tinham a **mesma causa**: `KeyError: 'status'` em uma fixture de teste do analisador A01. A correção `a6a2670d1ad1717135a92516840b123595fd1e2d` adicionou a classificação; as revisões posteriores passaram. Não são falhas correntes da `main`.
- Falhas históricas distintas: o [run #40710012447](https://github.com/c1c3ru/fft_craft/actions/runs/40710012447) exibiu `UC_ERR_FETCH_UNMAPPED` no loop Unicorn, tratado em [PR #382](https://github.com/c1c3ru/fft_craft/pull/382). Já o [run #40560964817](https://github.com/c1c3ru/fft_craft/actions/runs/40560964817) falhou por conflito no merge automático de checkpoints, não por falha de equivalência ARM; o workflow atual tem verificações contra mudança da `main` e o último lote automático passou.

**Regra de leitura:** verificar o SHA do PR antes de interpretar checks. Um workflow vermelho de SHA antigo não indica falha da `main`; tampouco um CI verde de outra revisão substitui o gate no SHA atual. Histórico vermelho não pode nem deve ser apagado para fabricar estabilidade.

## Prevenção implantada neste PR

Os três workflows de validação de PR usam agora um grupo de concorrência isolado pelo nome do workflow e número do PR. **Somente execuções de `pull_request` são canceladas quando substituídas por uma revisão mais recente do mesmo PR.** Execuções manuais permanecem independentes; `re-batches.yml` mantém `cancel-in-progress: false`, protegendo checkpoints e publicação serializada na `main`.

Isso reduz gasto de minutos e ruído por múltiplos pushes, mas não corrige nem mascara falhas reais. Execuções antigas poderão aparecer como `cancelled`, e isso é esperado; todo PR novo continua precisando de checks verdes no HEAD exato.

## Gates da engenharia de loop

1. Para cada alteração, rodar regressões Python e os gates de certificados; falha no lint, teste ou Unicorn bloqueia merge.
2. Registrar SHA do commit, run ID, motivo técnico e correção por erro; reproduzir localmente quando necessário.
3. Após novo commit no PR, conferir que os jobs pendentes/cancelados são de revisões **anteriores** e que os checks da revisão atual ficam verdes antes de integrar.
4. Nos workflows automáticos da `main`, nunca cancelar jobs em execução só porque houve novo commit; preservar artifacts e deixar PR aberto caso surja conflito de merge.
5. Atualizar [STATUS_GERAL.md](STATUS_GERAL.md) e este relatório quando surgir **uma nova classe de falha** ou mitigação; falhas antigas não são reabertas sem regressão no HEAD.

## Limite

O CI testa as evidências ARM nas condições estabelecidas; CI verde não prova que a engenharia reversa ou o aplicativo completo estejam concluídos. A fila de reconstrução permanece em [RE_COMPLETION_TRACKER.json](RE_COMPLETION_TRACKER.json).
