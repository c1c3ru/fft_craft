# FFT Craft — status geral

> Painel gerado automaticamente com dados do ELF, inventário e checkpoints. **Cobertura estrutural não demonstra equivalência semântica.**

**ELF SHA-256:** `bf913415ab9458a83b14ac8c8a0fa3430d1f5d18bfbcd7c7472d6f5e8b4850bc`

## Visão geral

| Indicador | Resultado | Origem / interpretação |
|---|---:|---|
| Funções no inventário | 6,455 | Inventário ARM |
| Checkpoints JSON válidos para este ELF | 3,002 | Status acompanhados |
| Aprovados estruturalmente | 2,952 | Aprovação automática de estrutura, não de comportamento |
| Precisam de revisão | 50 | Status `needs_review` |
| Aprovação estrutural entre checkpoints | **98.3%** | 2,952/3,002, **não** percentual de engenharia reversa completa |
| Checkpoints pendentes de criação | 0 | Não incluem funções cobertas apenas pelo histórico CSV |
| Metas de núcleo em revisão | 34 | De 2,345 checkpoints do núcleo |
| v3: checkpoints / aprovados / revisão | 1,258 / 1,208 / 50 | Subconjunto já analisado pelas regras v3 |
| Equivalência semântica integral registrada | **303** | Certificados revisáveis vinculados ao ELF; microexecuções não são certificados |

O histórico CSV contém **5,932** registros de análise anterior, que podem se sobrepor aos checkpoints. **Não somamos esses conjuntos para criar um percentual global fictício.**

## Fluxo de reconstrução funcional

A prioridade é reconstruir comportamento verificável (estrutura, semântica, C/C++, diferencial), não aumentar certificados.
[Etapas, gates e prioridades](../RECONSTRUCTION_WORKFLOW.md)

## Plano de conclusão da engenharia reversa do app

[Plano e critérios de aceite](../RE_COMPLETION_PLAN.md) · [Fila e evidências versionadas](RE_COMPLETION_TRACKER.json)

**Escopo:** engenharia reversa funcional, C/C++, JNI/Smali, APK/OBB e execução em Android suportado.

**Atividades:** 17 totais; **2 concluídas com evidência**; **2 em andamento**; **0 prontas para iniciar**; **0 bloqueadas**. Dependências pendentes não contam como prontas.

| Etapa | Gate de saída | Concluídas / total |
|---|---|---:|
| F0 — Linha de base e escopo | Inventario e artefatos de referencia versionados, areas descobertas/dados separadas, riscos/alcancabilidade documentados | 0/1 |
| F1 — Contratos de instrucao e CFG | 21 alvos ARM restantes classificados e testados quando seguros; CFG e pendencias estruturais auditados | 2/4 |
| F2 — Reconstrucao semantica de subsistemas | Fluxos nativos relevantes com contratos completos, memoria/calls/branch e traces com limites | 0/4 |
| F3 — Reimplementacao funcional independente | Modulos compilaveis com diferencial original x C/C++ sem divergencias do gate | 0/2 |
| F4 — Integracao APK/Android/OBB | ABI e JNI integrados, APK assinado reproduzivel, instalacao/carregamento em dispositivos suportados | 0/2 |
| F5 — Validacao funcional e regressao | Matriz real Android/OBB com zero divergencias criticas e evidencias de teste | 0/2 |
| F6 — Aceite final e documentacao | Todos fluxos do escopo com disposition validada e nenhuma lacuna funcional relevante | 0/2 |

### Próximas atividades executáveis

- **A04 (P1, em andamento)** — A04: sete destinos auditados; dispatcher (512 casos), getter (32) e dois veneers GOT (64) microexecutados com checkpoints — total 608 testes locais. Restam 0x000ab674 (prólogo, estado global e BL 0x000b6620), 0x000b461c (prólogo e BL 0x000b45d0), 0x002b1bb0 (retorno condicional) e a reachability do autoloop 0x002a1268. Não promover certificados nem marcar A04 done até CFG/efeitos integrais verificados. **Aceite:** CFG e contratos por destino com testes diferenciais completos até próximas fronteiras; fluxo do autoloop classificado com evidência de reachability ou lacuna explícita.
- **B01 (P1, em andamento)** — Consolidar inventario unico ELF (ARM/Thumb), JNI/Smali e assets OBB, deduplicar aliases e apontar manifestos, erros e exclusoes. **Aceite:** Relatorio de inventario com total unico, cobertura de bytes e origem de cada entrada, sem dupla contagem.

### Próximas dependências não liberadas

- **A03**: aguarda B01.
- **C01**: aguarda R01, R02.
- **C02**: aguarda R03, R04.
- **I01**: aguarda C01, C02.
- **Q01**: aguarda I02.
- **R01**: aguarda B01.
- **R02**: aguarda B01.
- **R03**: aguarda A03.

**Regra por PR:** mudar estado, ação seguinte, dependências e evidências no JSON; atualizar o relatório técnico; regenerar este painel; exigir CI verde. Somente marcar done com provas e todas as dependências concluídas.
**Gate global:** nenhuma lacuna funcional relevante; fluxos originais comparados à reimplementação, APK/OBB instalado e matriz de testes Android aprovada. Microexecuções e certificados de BX LR não satisfazem esse gate.

## Evidência e testes semânticos

50/50 relatórios estáticos de evidências. **Relatórios não são equivalência semântica certificada.**

Os relatórios abaixo apresentam **efeitos locais testados sob estados sintéticos** e seus limites. Testes passando não significam que a função inteira foi reconstruída:

- [CI auditado: falhas históricas de fixture e Unicorn separadas do HEAD verde; cancelar apenas runs obsoletos de PR](CI_RELIABILITY_2026-10-28.md)
- [Som: slot global do ELF em 0x34615c, relocação e 512 leituras ARM com memória sintética](SEMANTIC_SOUND_GLOBAL_SLOT.md)
- [Corpo comum 0x2b2b7c: cinco instruções ARM e 128 testes diferenciais C com pilha e literal originais](SEMANTIC_SOUND_COMMON_PROLOGUE.md)
- [Corpo comum 0x2b2b7c: desmontagem original A32 e execução limitada antes de efeitos não modelados](SEMANTIC_SOUND_COMMON_BODY_2B2B7C.md)
- [sound_request: reconstrução parcial C do prefixo A32 e 128 comparações ARM/C](SEMANTIC_SOUND_FUNCTIONAL_RECONSTRUCTION.md)
- [SysSE_PlayDef 0x2b2cf8: auditoria estática A32 de 128 bytes; nenhuma instrução executada](SEMANTIC_SOUND_PLAYDEF_ENTRY.md)
- [sound_request: 384 microexecucoes em tres entradas ARM ate destinos de funcao nao executados](SEMANTIC_SOUND_THREE_ENTRY_EXEC.md)
- [A04: dois veneers ARM via GOT/PC com 64 microexecuções e zero alvos indiretos executados (run #40751407523)](SEMANTIC_A04_VENEERS.md)
- [A04: dispatcher e getter originais microexecutados em 544 cenários, com memória controlada (run #40750531709)](SEMANTIC_A04_DISPATCHER.md)
- [A04: sete destinos ARM auditados estaticamente em 672 bytes do ELF original (run #40748750630); três destinos sem execução](SEMANTIC_A04_DESTINATIONS.md)
- [A02 validada no ELF: 11 entradas, 352 microexecuções ARM e 0 destinos externos executados (run #40735782606); A04 investiga sete destinos](SEMANTIC_A02_BRANCHES.md)
- [A01 concluída: 10 rotinas STRB/LDRB/LDR no ELF real, 320 testes diferenciais (run #40730706242); 11 pendentes para A02](SEMANTIC_A01_MEMORY.md)
- [Issue #388: 34 endereços catalogados; 13 STR/BX LR e 416 testes Unicorn aprovados; 21 pendentes](SEMANTIC_REMAINING_34.md)
- [Loop ELF 250: 216 candidatos A32, 6.912 microexecuções e 14 checkpoints (run #40713115396); sem novos certificados](SEMANTIC_LOOP_250_FULL.md)
- [Loop semântico A32: 24 funções-folha e 768 microexecuções do ELF (run #40710246666), zero novos certificados](SEMANTIC_LOOP_250.md)
- [Correção de 25 manifestos/250 tarefas e conflito do PR automatizado #362; sem novos certificados](SEMANTIC_PIPELINE_RECOVERY.md)
- [sound_request: destino 0x271314 e tres entradas ARM auditados no ELF original; execucao ainda pendente](SEMANTIC_SOUND_DESTINATION_271314.md)
- [sound_request: dois desvios ARM microexecutados ate destino ainda desconhecido](SEMANTIC_SOUND_TWO_HOP_EXEC.md)
- [Lotes semânticos de 100/200 funções com revisão independente](SEMANTIC_BATCH_SCALING.md)
- [Primeiro lote de cinco contratos BX LR preparados para revisão humana](SEMANTIC_BXLR_REVIEW_BATCH.md)
- [Política de certificação: contrato integral, ELF, revisão independente e CI](SEMANTIC_CERTIFICATION_POLICY.md)
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

Evidências geradas e verificadas nesta execução do pipeline.

| Indicador | Resultado |
|---|---:|
| Entradas do inventário | 6,455 |
| Endereços únicos | 6,329 |
| Certificados semânticos registrados | 303 |
| Cobertura semântica por endereço | 4.79% |
| Cobertura semântica por bytes únicos | 0.07% |
| Registros parciais no ledger | 0 |
| Endereços com evidência parcial no lote de referência | 11 |
| Documentos semânticos históricos do mesmo ELF | 26 |
| Documentos históricos com testes declarados | 13 |
| Candidatas BX LR verificadas, pendentes de revisão | 303 |
| Contratos BX LR preparados para revisão humana (não certificados) | 0 |
| Contratos locais BX LR com retorno ARM/Thumb verificado (revisão pendente) | 303 |
| Execuções ARM/Thumb adicionais dos contratos locais | 9,696 |
| Relatórios estáticos deste lote | 5 |
| Relatórios Unicorn deste lote | 309 |
| Microexecuções Unicorn verificadas neste lote (sem duplicar suítes) | 1,380 |
| Endereços distribuídos aos workers neste lote | 5 |
| Endereços aguardando certificação | 6,026 |

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

- `0x34615c`: Investigar a inicialização/relocação em tempo de execução do slot de som; o ELF estático não prova seu valor em memória do processo.
- `0x2bf008`: Investigar o próximo BL de SysSE_Play depois do desvio condicionado.
- `0x0a7034`: Investigar o próximo BL de iOS_SetIconPosition com os argumentos já observados.

Estas prioridades são **curadas no gerador**; quando um limite for resolvido, a descrição deve ser atualizada no mesmo PR de análise.

### Revisão estrutural — fila atual do núcleo

| Endereço | Função | Cobertura | Motivo |
|---|---|---:|---|
| `002b2448` | EnvSE_Play(int) | 77.17% | resolved_jump_table_check |
| `0015813c` | unittoface(int) | 69.35% | resolved_jump_table_check |
| `001ccc3c` | getTrapResultDamage(BWORK*, int) | 88.71% | resolved_jump_table_check |
| `00159aac` | asm_function(unsigned long, unsigned long, unsigned long, unsigned long, unsigned long, unsigned long) | 80.2% | resolved_jump_table_check |
| `00162080` | wasm_function(unsigned long, unsigned long, unsigned long, unsigned long, unsigned long, unsigned long) | 80.2% | resolved_jump_table_check |
| `002031a4` | iOSsetCursorByTouch(int, int, int, int, int) | 57.14% | resolved_jump_table_check |

## Pull requests recentes

- [PR #410 — docs(re): centralizar evidências A04 e manter três destinos pendentes](https://github.com/c1c3ru/fft_craft/pull/410)
- [PR #411 — chore(re): automated structural batch 40752057494](https://github.com/c1c3ru/fft_craft/pull/411)
- [PR #408 — feat(re): A04 validar dois saltos indiretos ARM PC/GOT sem executar os alvos](https://github.com/c1c3ru/fft_craft/pull/408)
- [PR #409 — chore(re): automated structural batch 40751245753](https://github.com/c1c3ru/fft_craft/pull/409)
- [PR #407 — feat(re): validar dispatcher ARM e getter A04 em 544 cenários](https://github.com/c1c3ru/fft_craft/pull/407)

## Atualização automática e fontes

O workflow `re-batches.yml` regenera este arquivo **depois** de calcular progresso, revisar checkpoints v3 e executar os testes semânticos; publica os resultados no PR automático de checkpoints apenas se o CI passar.
O workflow `re-pipeline.yml` testa a geração em PRs sem publicar as alterações.
- [PROGRESS.md](PROGRESS.md) — dados estruturais do inventário.
- [STRUCTURAL_V3_REPORT.md](STRUCTURAL_V3_REPORT.md) — migração v3.
- [SEMANTIC_EVIDENCE_INDEX.md](SEMANTIC_EVIDENCE_INDEX.md) — evidência estática das pendências.
- [REVIEW_TRIAGE.md](REVIEW_TRIAGE.md) — critérios de priorização.
- [GitHub Actions](https://github.com/c1c3ru/fft_craft/actions) — execução e eventuais falhas de CI.

**Limitação:** o painel não é um contador de reconstrução semântica completa. Uma certificação desse tipo exigiria contratos e testes integrais por função; os registros parciais não constituem tais certificações.
