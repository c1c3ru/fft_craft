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
| Equivalência semântica integral registrada | **0** | Certificados revisáveis vinculados ao ELF; microexecuções não são certificados |

O histórico CSV contém **5,932** registros de análise anterior, que podem se sobrepor aos checkpoints. **Não somamos esses conjuntos para criar um percentual global fictício.**

## Evidência e testes semânticos

89/89 relatórios estáticos de evidências. **Relatórios não são equivalência semântica certificada.**

Os relatórios abaixo apresentam **efeitos locais testados sob estados sintéticos** e seus limites. Testes passando não significam que a função inteira foi reconstruída:

- [Primeiros contratos locais BX LR com retornos ARM/Thumb verificados](SEMANTIC_BXLR_CONTRACT_PILOT.md)
- [Índice do acervo semântico acumulado e vinculado ao mesmo ELF](SEMANTIC_HISTORY_INDEX.md)
- [Candidatas ARM de retorno simples microexecutadas para contratos revisáveis](SEMANTIC_LEAF_BXLR.md)
- [Destinos ARM seguintes de houkoku_okng auditados sem executar ramos desconhecidos](SEMANTIC_HOUKOKU_NEXT_BOUNDARIES.md)
- [Três destinos de SysSE_Play e argumentos pós-GetScale verificados por máquina](SEMANTIC_POST_GETTER_PATHS.md)
- [GetParam/GetScale ARM: 96 microexecuções individuais e via BL original](SEMANTIC_GETPARAM_GETSCALE_MICROEXEC.md)
- [Instruções e destinos de chamada GetParam/GetScale auditados](SEMANTIC_GETPARAM_GETSCALE_AUDIT.md)
- [Próximas leituras globais de som e ícones verificadas até as primeiras chamadas BL](SEMANTIC_NEXT_POINTER_MICROEXEC.md)
- [Inventário dos opcodes ARM reais nos limites de som e ícones](SEMANTIC_NEXT_BOUNDARIES.md)
- [Som até 0x2b2b7c e prólogo de iOS_SetIconPosition até 0x2b8928](SEMANTIC_SOUND_ICON_MICROEXEC.md)
- [Três callees ARM e duas continuações controladas do chamador](SEMANTIC_THREE_CALLEES_EXECUTION.md)
- [BL/BX LR de V2Icon e seleção de três caminhos](SEMANTIC_V2ICON_CALL_FLOW.md)
- [Retorno ARM real e alterações de memória antes da primeira chamada](SEMANTIC_RETURN_CALL_BOUNDARY.md)

## Cobertura semântica e execução paralela

Os números certificados representam **registros formais válidos para este ELF**, não aprovação estrutural. Evidências parciais não certificam equivalência.

| Indicador | Resultado |
|---|---:|
| Entradas do inventário | 6,455 |
| Endereços únicos | 6,329 |
| Certificados semânticos registrados | 0 |
| Cobertura semântica por endereço | 0.00% |
| Cobertura semântica por bytes únicos | 0.00% |
| Registros parciais no ledger | 0 |
| Endereços com evidência parcial registrada ou gerada nesta execução | 309 |
| Documentos semânticos históricos do mesmo ELF | 24 |
| Documentos históricos com testes declarados | 13 |
| Candidatas BX LR verificadas, pendentes de revisão | 303 |
| Contratos locais BX LR com retorno ARM/Thumb verificado (revisão pendente) | 5 |
| Execuções ARM/Thumb adicionais dos contratos locais | 40 |
| Relatórios estáticos deste lote | 5 |
| Relatórios Unicorn deste lote | 309 |
| Microexecuções Unicorn verificadas neste lote (sem duplicar suítes) | 1,380 |
| Endereços distribuídos aos workers neste lote | 5 |
| Endereços aguardando certificação | 6,329 |

### Próximos contratos ainda não certificados (maiores primeiro)

| Endereço | Função | Bytes | Estado |
|---|---|---:|---|
| `00207e10` | battle() | 17156 | unknown |
| `0011173c` | Wmesputmain() | 16312 | unknown |
| `002c141c` | Main_FrameRender() | 16164 | unknown |
| `0017c27c` | BattleUnitList(unsigned char*, unsigned long*) | 15920 | unknown |
| `000e88c4` | mesputmain() | 15744 | unknown |
| `0016a6a4` | ASHURA_addPrim(MATRIX*) | 15412 | unknown |
| `001aeda0` | ItemMenu() | 13764 | unknown |
| `002bbb74` | Main_FrameMove() | 13272 | unknown |
| `0018aeec` | eItemMenu() | 12580 | unknown |
| `000c5148` | op_attackteam() | 12272 | unknown |
| `00184670` | CardAccess(int) | 11004 | unknown |
| `001506ec` | requireprinf() | 10976 | unknown |
| `00225ac8` | CreateObjectWithTable(short, int, int, _Object*) | 10724 | unknown |
| `0016fc90` | BattleCardAccess(int) | 10448 | unknown |
| `00128ed4` | disp_personalwindow() | 8756 | unknown |

O restante da fila permanece nos manifestos e no `SEMANTIC_COVERAGE.md`. Observações Unicorn limitadas e verificações estáticas não alteram automaticamente certificados.


## Próximas prioridades

### Lacunas semânticas conhecidas

- `0x2bf008`: Investigar o próximo BL de SysSE_Play depois do desvio condicionado.
- `0x0a7034`: Investigar o próximo BL de iOS_SetIconPosition com os argumentos já observados.

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

- [PR #321 — feat(re): iniciar contratos semânticos locais completos com retornos ARM/Thumb](https://github.com/c1c3ru/fft_craft/pull/321)
- [PR #320 — chore(re): automated structural batch 40388256641](https://github.com/c1c3ru/fft_craft/pull/320)
- [PR #319 — feat(re): reaproveitar evidências históricas e validar folhas ARM rumo aos contratos integrais](https://github.com/c1c3ru/fft_craft/pull/319)
- [PR #318 — chore(re): automated structural batch 40385077935](https://github.com/c1c3ru/fft_craft/pull/318)
- [PR #317 — feat(re): auditar destinos ARM pendentes de houkoku_okng e atualizar painel](https://github.com/c1c3ru/fft_craft/pull/317)

## Atualização automática e fontes

O workflow `re-batches.yml` regenera este arquivo **depois** de calcular progresso, revisar checkpoints v3 e executar os testes semânticos; publica os resultados no PR automático de checkpoints apenas se o CI passar.
O workflow `re-pipeline.yml` testa a geração em PRs sem publicar as alterações.
- [PROGRESS.md](PROGRESS.md) — dados estruturais do inventário.
- [STRUCTURAL_V3_REPORT.md](STRUCTURAL_V3_REPORT.md) — migração v3.
- [SEMANTIC_EVIDENCE_INDEX.md](SEMANTIC_EVIDENCE_INDEX.md) — evidência estática das pendências.
- [REVIEW_TRIAGE.md](REVIEW_TRIAGE.md) — critérios de priorização.
- [GitHub Actions](https://github.com/c1c3ru/fft_craft/actions) — execução e eventuais falhas de CI.

**Limitação:** o painel não é um contador de reconstrução semântica completa. Uma certificação desse tipo exigiria contratos e testes integrais por função; os registros parciais não constituem tais certificações.
