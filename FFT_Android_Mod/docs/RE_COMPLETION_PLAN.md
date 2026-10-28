# Plano executivo para concluir a engenharia reversa e reconstrução do FFT Craft

**Escopo:** aplicativo Android *Final Fantasy Tactics: The War of the Lions* estudado no repositório privado `c1c3ru/fft_craft`, incluindo código nativo ELF ARM, JNI/Smali, recursos/OBB, compilação, integração e testes no dispositivo. O plano não autoriza distribuir material de terceiros; manter binários e assets originais privados e validar direitos de uso.

**Fonte única de prioridades e andamento:** [RE_COMPLETION_TRACKER.json](re-results/RE_COMPLETION_TRACKER.json), exibido automaticamente em [STATUS_GERAL.md](re-results/STATUS_GERAL.md). Esta página define os critérios de saída; o rastreador registra execução, dependências e evidências. Atualizar os dois quando mudar o plano; a cada entrega atualizar o rastreador **no mesmo PR** que adiciona o código e o relatório.

## Estado real de partida — 28/10/2026

- ELF nativo de referência SHA-256: `bf913415ab9458a83b14ac8c8a0fa3430d1f5d18bfbcd7c7472d6f5e8b4850bc`. Qualquer alteração de binário exige nova linha de base.
- Inventário: **6.455 entradas / 6.329 endereços únicos**; 3.002 checkpoints estruturais, dos quais 2.952 aceitos e 50 em revisão. Os 5.932 registros históricos podem se sobrepor e não são somáveis.
- **303 certificados semânticos** de escopo específico ARM BX LR: **4,79% dos endereços únicos** e somente **0,07% dos bytes únicos** do relatório. Certificados de um retorno e testes de prefixo não são equivalência de uma rotina extensa, de um subsistema, do aplicativo ou de uma versão Android executável.
- Lote recente de 250 entradas: 216 candidatas A32 com 6.912 microexecuções locais + 13 `STR/BX LR` com 416 cenários. Restam **21 entradas não executadas nesse lote** — issue [#388](https://github.com/c1c3ru/fft_craft/issues/388). Esses números descrevem um subconjunto, **não** cobertura global de 229/6.329.
- Fronteiras já registradas: slot de som `0x34615c` sem valor real de runtime, próximo `BL` de `SysSE_Play` em `0x2bf008`, próximo `BL` de `iOS_SetIconPosition` em `0x0a7034`. Revisar saltos/tabelas e 50 checkpoints estruturais.
- O projeto documenta scripts de build/assinatura do APK e OBB, mas **não há evidência aqui de equivalência integral, integração da reimplementação C/C++ ou matriz final de execução Android concluída**.

## Engenharia de loop — regra para toda atividade

1. **Selecionar:** escolher um endereço, bloco, contrato ou fluxo priorizado por impacto no jogo, dependência, cobertura desconhecida e capacidade de validação; marcar a atividade `em andamento` no JSON central.
2. **Desmontar:** verificar SHA do ELF e bytes; identificar A32/Thumb, código vs dados, CFG, branches, BL/BLX, retornos, ponteiros, tabelas e fronteiras desconhecidas.
3. **Modelar:** escrever pré-condições, entradas, saídas, aliasing, pilha, R0–R15/CPSR, memória, efeitos globais, exceções e invariantes. Manter o desconhecido como `needs_review`.
4. **Executar:** usar Unicorn no **ELF original** para casos delimitados, flags/caminhos extremos, memória controlada e sentinelas; seguir chamadas somente quando os contratos dos callees forem conhecidos. Parar em qualquer efeito não modelado.
5. **Reimplementar:** traduzir comportamento compreendido para módulos C/C++ (ou outra linguagem justificada), com testes independentes e instrumentação de interfaces JNI/Android.
6. **Comparar:** testar original × modelo × implementação com estados idênticos, traces, registradores, memória, arquivos, efeitos e caminhos. Registrar divergências com reprodutor e reabrir hipóteses.
7. **Persistir e repetir:** salvar relatório por endereço e hash ELF, checkpoint idempotente, matriz de testes, commit, run e PR; reexecutar até gates verdes. Somente então marcar tarefa concluída com **evidência verificável**, atualizar o JSON e regenerar `STATUS_GERAL.md`. Nunca certificar automaticamente.
8. **Escalar:** usar jobs/manifestos em lotes de 100–250 para descoberta e pequenos sublotes para validação de efeitos. Concorrência só em alvos independentes; não fazer merge com CI pendente/falho. Em regressão, usar `git revert` e testes, sem supor que rollback evita impacto prévio.

## Etapas e critérios de saída

| Etapa | Foco e atividades obrigatórias | Gate de saída verificável |
|---|---|---|
| **F0 — linha de base** | Consolidar inventário ELF e APK/DEX/JNI/OBB; resolver aliases e alvos de 32-bit/Thumb, contabilizar bytes únicos, funções realmente alcançáveis e áreas ainda desconhecidas | Inventário versionado com SHA, proveniência, cobertura deduplicada, lista de lacunas e relatório de riscos |
| **F1 — instruções e CFG** | Encerrar 21 pendências ARM (#388): `STRB`, `LDRB`, LDR com offsets maiores, prefixos antes de B, auto-loop; revisar os 50 checkpoints estruturais, jump tables, exceções, literais e fronteiras de chamada | Toda entrada rastreada como executada com contrato limitado **ou** classificada em lacuna objetiva; CFG auditável por função; zero opcodes silenciosamente ignorados |
| **F2 — semântica end-to-end** | Reconstruir o fluxo de inicialização, `Main_FrameMove/Render`, `battle`, menus, input, áudio, save/load, sistemas/serviços do Android, estado global e dependências; capturar traces reais quando o modelo sintético não basta | Entradas/saídas, efeitos, chamados e caminhos alcançáveis cobertos por contrato por subsistema; todo comportamento desconhecido impede a aprovação desse subsistema |
| **F3 — reimplementação** | Produzir C/C++ (ou equivalente) modular e compatível com o ABI/JNI; definir interfaces e substituições semânticas, estado persistente, exceções, arquivos e sincronização | Módulos compiláveis, contrato documentado e testes original × reimplementação sem divergência nos cenários do gate; cobertura funcional reportada por subsistema |
| **F4 — integração Android** | Integrar nativo, JNI, Smali/Manifest e recursos/OBB; manter assinatura própria e rastreabilidade de artefatos; auditar requisitos de armazenamento, 32-bit e versões Android suportadas | Build e instalação reproduzíveis; smoke do APK+OBB na matriz declarada; nenhuma dependência desconhecida bloqueando abertura, tela, entrada ou carregamento |
| **F5 — validação funcional** | Comparar o app com a referência em inicialização, menus, batalhas, eventos, save/load, áudio, gráficos, touch, desempenho e ciclos de vida; testar dispositivos compatíveis, falhas, limites e regressões | Matriz funcional assinada com **zero divergência crítica**; incompatibilidades explicitamente fora de escopo aceitas por decisão registrada; relatórios, logs e reproduções |
| **F6 — encerramento** | Revisar todo endereço/fluxo alcançável e declarar disposition (`reimplementado+testado`, `componente original mantido sob escopo`, `inalcançável provado`, `não resolvido`); revisar licença/uso/distribuição e documentação final | **Nenhum fluxo necessário com status desconhecido**; artefato versionado reproduzível, documentação final e checklist aprovado. Afirmar engenharia reversa **total** somente se não houver lacunas de comportamento relevantes; caso contrário, publicar como reconstrução parcial/compatível |

**Critério global:** o objetivo não é obter 100% por simples contagem de microexecuções. Para declarar reconstrução completa, é preciso fechar as dependências reais entre componentes, explicar todo código/fluxo relevante (inclusive entradas inalcançáveis com justificativa), construir e executar o APK integrado e demonstrar equivalência funcional no escopo declarado. Se a meta for **reimplementação nativa integral sem reutilizar nenhuma rotina original**, cada função nativa necessária deve ter reimplementação independente, não somente comportamento preservado por biblioteca original.

## Próximas ações, nesta ordem

1. **L01 — #388:** modelos com testes `STRB`/`LDRB` e leituras com offsets maiores, sob memória sintética e rastreio de efeitos. Não executar o auto-loop `0x002a1268` de forma ilimitada.
2. **L02 — #388:** nove prefixos com operação+B e um LDR+B: comparar estado antes do destino e mapear cada callee/destino sem extrapolar a função inteira.
3. **L03 — CFG:** resolver 50 pendências estruturais; priorizar `EnvSE_Play`, `iOSsetCursorByTouch`, `Savedata_Load`, `pspFftSave`, `initMap` e `Boot_Init`, pois conectam subsistemas observáveis.
4. **L04 — runtime:** obter traces do slot de som `0x34615c`, `SysSE_Play` em `0x2bf008` e `iOS_SetIconPosition` em `0x0a7034`, diferenciando valores reais de memória sintética.
5. **L05 — fluxo principal:** reconstruir `Boot_Init → Main_FrameMove/Render → menus/battle/save` e contratos entre callers/callees. Priorizar interações efetivas em vez de funções isoladas por tamanho.
6. **L06 — execução comparativa:** estabelecer suíte original × C/C++ e matriz Android para cada fluxo concluído; nenhum gate de subsistema se satisfaz apenas por testes do prólogo.
7. **L07 — integração final:** build nativo/JNI/APK/OBB assinado em ambiente reproduzível e testes completos em dispositivo de ABI suportada; corrigir toda divergência.

## Operação e atualização do documento central

- [Rastreador estruturado](re-results/RE_COMPLETION_TRACKER.json): IDs estáveis, fase, prioridade, estado, dependências, evidências e `next_action`. Estados permitidos: `planned`, `in_progress`, `blocked`, `done`. Tarefas `done` exigem ao menos uma evidência verificável e critério de aceite.
- [STATUS_GERAL.md](re-results/STATUS_GERAL.md) é gerado por `docs/re-tools/status_geral.py`, que lê o rastreador em cada execução; não editar só o Markdown gerado. A mudança de estado e a prova correspondente precisam aparecer no **mesmo PR**.
- Rodar `python3 FFT_Android_Mod/docs/re-tools/re_completion_tracker.py --tracker FFT_Android_Mod/docs/re-results/RE_COMPLETION_TRACKER.json --expected-sha bf913415ab9458a83b14ac8c8a0fa3430d1f5d18bfbcd7c7472d6f5e8b4850bc` e o gerador central; CI rejeita inconsistências de identificadores, dependências, hashes ou conclusão sem evidência.
- Reportar semanalmente (ou por PR/lote) tarefas concluídas por etapa, tarefas em curso, blockers, hashes/CI, divergências, próximos três alvos e evolução **real** dos gates funcionais. Sem estimar percentual total de engenharia reversa a partir da cobertura estrutural.
