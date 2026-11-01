# T09 — Resolver dispatch indireto e grafo de dependências

Depende de T07–T08 (`ready_for_review`, parciais). Executado em 2026-10-31.

**Estado: `ready_for_review` (parcial) — NÃO `done`.** Consolida, pela primeira vez num só artefato, as 38 tabelas de salto já resolvidas em todos os checkpoints existentes, e constrói o grafo de chamadas conhecido (3.820 arestas `bl` entre funções com checkpoint). Resolve o ponto de chamada indireta por registrador (`blx r3`) encontrado em T07 (`__cxa_type_match`). Não cobre callbacks/vtables fora do que já estava checkpointado, nem schedulers `asm`/`wasm` em detalhe — ver pendências.

## 1. Registro consolidado de dispatch (38 tabelas de salto)

Nenhum artefato único reunia as tabelas de salto já resolvidas espalhadas pelos 3.002 checkpoints. `docs/re-baseline/dispatch_registry.json` consolida as **38 tabelas resolvidas** (guarda `cmp`, endereço de dispatch, número de casos, lista de alvos) extraídas diretamente dos logs de checkpoint existentes.

**Verificação de integridade feita nesta tarefa:** para cada uma das 38 tabelas, confirmei que **todos os alvos caem dentro do intervalo de bytes declarado da própria função dona da tabela** (nenhum alvo "escapa" para outra função ou para uma região não relacionada) — 0 anomalias em 38 tabelas. Isso é esperado (alvos de tabela de salto são rótulos de `case` dentro da mesma função), mas não tinha sido verificado em lote antes; agora está confirmado para as 38 conhecidas.

## 2. Grafo de chamadas conhecido e busca de ciclos (componentes fortemente conectados)

Construído a partir do campo `bl_targets` dos 3.002 checkpoints, restrito a arestas onde **os dois lados** (chamador e alvo) já têm um endereço no inventário de 6.329 entradas:

| Métrica | Valor |
|---|---:|
| Checkpoints com dados de `bl_targets` | 3.002 |
| Arestas `bl` totais registradas | 3.820 |
| Nós com pelo menos uma aresta conhecido→conhecido | 1.235 |
| Componentes fortemente conectados com >1 nó (ciclos reais) | **0** |

Executado Tarjan's SCC sobre o grafo dirigido. **Nenhum ciclo de chamada mútua foi encontrado** entre funções já checkpointadas — tratamento de ciclos por SCC foi aplicado (não pulado), resultado é "nenhum ciclo nesta sub-rede", não "não verificado". Isso não prova que o binário inteiro é acíclico — só que a fatia já analisada não tem recursão mútua detectável por essa aresta.

## 3. Alvos de chamada "desconhecidos" (fora do inventário de 6.329) — todos explicados

233 endereços de alvo de `bl` não batem com nenhum dos 6.329 endereços do CSV. Classificados em `docs/re-baseline/call_graph_analysis.json`:

| Categoria | Quantidade | Explicação |
|---|---:|---|
| Dentro de um dos 303 intervalos de `.text` sem inventário (T04) | 162 | **Confirma, por evidência independente de chamada real, que esses intervalos de T04 são código genuinamente alcançado em runtime** — não apenas bytes não-zero coincidentes |
| Dentro de `.plt` (`0x71468`–`0x71c50`) | 70 | Trampolins padrão de PLT (confirmado por desmontagem: `add ip, pc, #...; add ip, ip, #...; ldr pc, [ip, #...]!`, o idioma clássico de PLT ARM) — comportamento esperado, `.plt` nunca fez parte do inventário de `.text` |
| Chamada para endereço no meio de uma função já inventariada | 1 | `0x2ca7a4` — 8 bytes dentro de `__divsi3` (`0x2ca79c`, 220 B, `mentioned_unverified`); é um ponto de entrada secundário da rotina de divisão (comum em `libgcc`, ex. pular tratamento de sinal), não uma função nova. Correção de precisão do meu próprio script de correspondência (compara por endereço exato de entrada, não por intervalo) — não é uma lacuna real. |

**Nenhum dos 233 fica sem explicação.** Isso satisfaz o critério de aceite "todo call site tem alvo/conjunto justificado ou pendência explícita" para este subconjunto — os 162 em gaps de T04 ficam com pendência EXPLÍCITA (são código real, ainda não resolvido estruturalmente; resolver isso é T06/T04 continuado, não reaberto aqui).

## 4. Chamada indireta por registrador resolvida: `__cxa_type_match` (`blx r3`)

T07 deixou pendente um `blx r3` em `__cxa_type_match` (`0x2ca17e`). Lendo o Thumb completo da função (modo já corrigido em T07):

```
ldr r3, [r6]       ; r3 = *catch_type        (vtable pointer, offset 0 do objeto)
ldr r3, [r3, #8]   ; r3 = vtable[2]          (slot de 3ª função virtual)
...
blx r3             ; chamada virtual
```

Esse é exatamente o padrão do ABI Itanium C++ (código-fonte público do `libsupc++`/`eh_personality.cc`): `__cxa_type_match` despacha para `catch_type->__do_catch(thrown_type, thrown_object, throw_flags)` por chamada virtual via a `vtable` de `std::type_info` — o alvo concreto depende do tipo RTTI em tempo de execução (`catch_type`), não é um único endereço fixo. **Justificativa do alvo: dispatch polimórfico documentado pelo ABI público, não um desconhecido não investigado** — não é um caso que precise de observação em runtime pra ser considerado resolvido, porque o mecanismo (não o alvo concreto) é o que se explica aqui, conforme o padrão já confirmado por fonte pública.

## 5. O que fica pendente (bloqueia `done`)

1. Os 162 endereços dentro de gaps de T04 confirmados como alcançados por chamada real seguem sem análise estrutural (T06/T04 continuado).
2. Schedulers `asm_function`/`wasm_function` (citados no próprio T06 como alvos, com tabela de salto já resolvida — ver `dispatch_registry.json`) não tiveram os handlers individuais lidos nesta tarefa, só a tabela.
3. Vtables C++ do motor gráfico/engine (fora do runtime de exceção) não foram procuradas nesta tarefa — só a de `std::type_info` via `__cxa_type_match`.
4. Chamadas de retorno Java↔JNI (`getCommand`, `dialogOnClose`, etc.) não mapeadas aqui — pertence a T27.
5. Grafo de chamadas cobre só os 1.235 nós com checkpoint em ambas as pontas; os ~5.094 endereços restantes do inventário (sem checkpoint estrutural com `bl_targets`, ou cujo `bl_targets` está vazio) não entram nesta análise de ciclos.

## 6. Arquivos produzidos por esta tarefa

- `docs/re-baseline/dispatch_registry.json` — as 38 tabelas de salto resolvidas, consolidadas, com verificação de intervalo.
- `docs/re-baseline/call_graph_analysis.json` — grafo de chamadas conhecido, resultado de SCC, e classificação completa dos 233 alvos "desconhecidos".
- Este relatório.
