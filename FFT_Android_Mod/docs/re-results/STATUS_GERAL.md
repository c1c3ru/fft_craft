# FFT Craft — status geral

> Painel gerado automaticamente com dados do ELF, inventário e checkpoints. **Cobertura estrutural não demonstra equivalência semântica.**

**ELF SHA-256:** `bf913415ab9458a83b14ac8c8a0fa3430d1f5d18bfbcd7c7472d6f5e8b4850bc`

## Visão geral

| Indicador | Resultado | Origem / interpretação |
|---|---:|---|
| Funções no inventário | 6,455 | Inventário ARM |
| Checkpoints JSON válidos para este ELF | 3,002 | Status acompanhados |
| Aprovados estruturalmente | 2,913 | Aprovação automática de estrutura, não de comportamento |
| Precisam de revisão | 89 | Status `needs_review` |
| Aprovação estrutural entre checkpoints | **97.0%** | 2,913/3,002, **não** percentual de engenharia reversa completa |
| Checkpoints pendentes de criação | 0 | Não incluem funções cobertas apenas pelo histórico CSV |
| Metas de núcleo em revisão | 73 | De 2,345 checkpoints do núcleo |
| v3: checkpoints / aprovados / revisão | 1,213 / 1,169 / 44 | Subconjunto já analisado pelas regras v3 |
| Funções com **equivalência semântica integral certificada** | **não mensurado** | O pipeline atual não mantém certificações formais por função; microexecuções não substituem esse certificado |

O histórico CSV contém **5,932** registros de análise anterior, que podem se sobrepor aos checkpoints. **Não somamos esses conjuntos para criar um percentual global fictício.**

## Evidência e testes semânticos

89/89 relatórios estáticos de evidências. **Relatórios não são equivalência semântica certificada.**

Os relatórios abaixo apresentam **efeitos locais testados sob estados sintéticos** e seus limites. Testes passando não significam que a função inteira foi reconstruída:

- [Próximas leituras globais de som e ícones verificadas até as primeiras chamadas BL](SEMANTIC_NEXT_POINTER_MICROEXEC.md)
- [Inventário dos opcodes ARM reais nos limites de som e ícones](SEMANTIC_NEXT_BOUNDARIES.md)
- [Som até 0x2b2b7c e prólogo de iOS_SetIconPosition até 0x2b8928](SEMANTIC_SOUND_ICON_MICROEXEC.md)
- [Três callees ARM e duas continuações controladas do chamador](SEMANTIC_THREE_CALLEES_EXECUTION.md)
- [BL/BX LR de V2Icon e seleção de três caminhos](SEMANTIC_V2ICON_CALL_FLOW.md)
- [Retorno ARM real e alterações de memória antes da primeira chamada](SEMANTIC_RETURN_CALL_BOUNDARY.md)

## Próximas prioridades

### Lacunas semânticas conhecidas

- `0x28c320`: Investigar a chamada seguinte de SysSE_Play após validar seus argumentos.
- `0x0a6f28`: Investigar a primeira chamada de iOS_SetIconPosition com ponteiro controlado.

Estas duas prioridades são **curadas no gerador**; quando um limite for resolvido, a descrição deve ser atualizada no mesmo PR de análise.

### Revisão estrutural — fila atual do núcleo

| Endereço | Função | Cobertura | Motivo |
|---|---|---:|---|
| `0028179c` | iOS_v2menuSetType(V2MENU_TYPE) | 94.81% | coverage_below_95 |
| `00244200` | vEnd_rollproc() | 91.67% | coverage_below_95 |
| `000df864` | event_status_set(unsigned short, unsigned short) | 93.13% | coverage_below_95 |
| `0025a228` | houkoku_okng(CTLINFO*) | 93.7% | coverage_below_95 |
| `002b2448` | EnvSE_Play(int) | 77.17% | resolved_jump_table_check |
| `0028bb88` | TE_asmTaskEntry(int) | 91.27% | coverage_below_95 |

## Pull requests recentes

- [PR #297 — feat(re): auditar instruções reais nos próximos limites de som e ícones](https://github.com/c1c3ru/fft_craft/pull/297)
- [PR #296 — chore(re): automated structural batch 40295799498](https://github.com/c1c3ru/fft_craft/pull/296)
- [PR #295 — chore(re): automated structural batch 40246019946](https://github.com/c1c3ru/fft_craft/pull/295)
- [PR #294 — feat(re): gerar STATUS_GERAL.md automaticamente e destacá-lo no README](https://github.com/c1c3ru/fft_craft/pull/294)
- [PR #293 — chore(re): automated structural batch 40245079093](https://github.com/c1c3ru/fft_craft/pull/293)

## Atualização automática e fontes

O workflow `re-batches.yml` regenera este arquivo **depois** de calcular progresso, revisar checkpoints v3 e executar os testes semânticos; publica os resultados no PR automático de checkpoints apenas se o CI passar.
O workflow `re-pipeline.yml` testa a geração em PRs sem publicar as alterações.
- [PROGRESS.md](PROGRESS.md) — dados estruturais do inventário.
- [STRUCTURAL_V3_REPORT.md](STRUCTURAL_V3_REPORT.md) — migração v3.
- [SEMANTIC_EVIDENCE_INDEX.md](SEMANTIC_EVIDENCE_INDEX.md) — evidência estática das pendências.
- [REVIEW_TRIAGE.md](REVIEW_TRIAGE.md) — critérios de priorização.
- [GitHub Actions](https://github.com/c1c3ru/fft_craft/actions) — execução e eventuais falhas de CI.

**Limitação:** o painel não é um contador de reconstrução semântica completa. Uma certificação desse tipo exigiria contratos e testes integrais por função que ainda não são registrados pelo pipeline.
