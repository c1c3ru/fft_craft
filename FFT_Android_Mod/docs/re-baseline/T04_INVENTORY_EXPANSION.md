# T04 — Expandir inventário além de `.dynsym`

Depende de T01–T03 (todas `ready_for_review`, parciais). Executado em 2026-10-31.

**Estado: `ready_for_review` (parcial) — NÃO `done`.** Esta tarefa produziu um achado central e bem evidenciado (seção 2): **26,31% do `.text` do ARM (651.216 bytes, em 303 intervalos) não está coberto pelo inventário de 6.329 endereços**, que é inteiramente derivado de `.dynsym`. O inventário x86 simplesmente não existe (seção 4). Classificação completa dos 303 intervalos está em `text_coverage_gaps.json`; resolução função-a-função de cada um é trabalho de T06 em diante, fora do escopo desta tarefa.

## 1. Fontes de símbolo disponíveis — confirmação direta

| Fonte | Presente? | Entradas |
|---|---|---|
| `.dynsym` | Sim | 9.158 símbolos `FUNC`/`OBJECT` (muito mais que os 6.329 endereços únicos do CSV — o CSV já filtra/deduplica por algum critério não documentado aqui; não investigado a fundo nesta tarefa) |
| `.symtab` | **Não existe** (confirmado via `readelf -S`, ARM e x86) | — |
| `.rel.dyn` | Sim | 6.832 relocations (não enumeradas função a função nesta tarefa) |
| `.init_array` | Sim | 13 ponteiros de função + terminador nulo |
| `.fini_array` | Sim | 1 ponteiro de função |

## 2. Achado principal: 26,31% do `.text` (ARM) não está no inventário

Cálculo: somar os intervalos declarados no CSV (6.329 endereços, deduplicados por endereço — aliases usam o maior tamanho declarado) dentro dos limites reais da seção `.text` (`0x71c50`–`0x2ce23c`, 2.475.500 bytes via `readelf -S`), e listar o que sobra.

| Métrica | Valor |
|---|---:|
| Bytes de `.text` cobertos pelo inventário | 1.826.552 (73,79%) |
| Bytes de `.text` **não cobertos** | 651.216 (26,31%) |
| Número de intervalos não cobertos | 303 |
| Intervalos >1024 bytes (quase certamente várias funções cada) | 132, somando 586.117 bytes |

**Nenhum dos 303 intervalos é padding/zero** — todos têm bytes não-nulos (verificado byte a byte). Amostra de três dos maiores intervalos (`0x2a39c8` 31.748 B, `0x1f75c4` 22.572 B, `0xf6058` 21.584 B), desmontados com Capstone: todos começam com prólogo ARM reconhecível (`push {r4-fp}`/`push {..., lr}` + `sub sp, sp, #N`) e contêm chamadas (`bl`) para endereços que já estão no inventário — ou seja, são funções reais, chamando código conhecido, mas nunca symbolizadas elas mesmas.

Classificação de todos os 303 intervalos pelo primeiro byte decodificado como ARM32 (ver `text_coverage_gaps.json`):

| Classificação | Quantidade | Interpretação |
|---|---:|---|
| `plausible_function_start` (começa com `push`/`stmdb`/`stmfd`) | 226 (74,6%) | Evidência forte de início de função real não inventariada |
| `ambiguous_needs_structural_pass` | 76 (25,1%) | Pode ser função *leaf* sem frame de pilha, pode ser literal pool mal-delimitado no fim da função anterior, ou código Thumb num endereço que este passe decodificou como ARM32 por padrão — **requer passe estrutural (T06+), não decidido aqui** |
| `undecodable_at_arm32` | 1 (0,3%) | Byte inicial não forma instrução ARM32 válida — candidato a região Thumb ou offset desalinhado |

## 3. `.init_array`/`.fini_array` — 14 endereços de código executados automaticamente no load, nenhum no inventário

Todos os 13 ponteiros de `.init_array` e o 1 ponteiro de `.fini_array` do ARM apontam para endereços **ausentes do CSV de 6.329 entradas**:

```
0x71d50 (fini) · 0x71d60 · 0x71d9c · 0x71dd8 · 0x71e18 · 0x71e80 · 0x71e90 ·
0x71fb8 · 0x72114 · 0x721a4 · 0x721e0 · 0x72280 · 0x722e0 · 0x72345
```

São candidatos típicos de inicializadores estáticos de C++ (`_GLOBAL__sub_I_*`), que o linker chama automaticamente antes de `JNI_OnLoad` — ou seja, **código que roda garantidamente em todo load da lib**, sem nenhum call site visível em `.dynsym`. Tamanhos entre os ponteiros consecutivos variam de 16 a 348 bytes — grande o suficiente para serem funções reais, não apenas trampolins vazios. Não foram analisados semanticamente nesta tarefa (isso é T06+); ficam registrados como alvo prioritário porque já se sabe que executam sempre.

## 4. x86 — não há inventário formal, 0% comparável ao ARM

`RE_FUNCTION_INVENTORY.csv` é indexado inteiramente por endereços do ELF **ARM** (`bf913415...`, confirmado em `b01_inventory_audit.py` e em `progress_report.py`). Não existe nenhum CSV, JSON ou ledger equivalente para `src/lib/x86/libgl2jni.so` nesta auditoria. O x86 tem `.init_array`/`.fini_array` com a mesma contagem de entradas que o ARM (13+1), consistente com vir do mesmo código-fonte, mas os endereços são diferentes e não comparáveis diretamente sem um mapeamento (que é o objetivo de **T31**, ainda `pending`). Não calculei aqui um "percentual de cobertura" para x86 porque não há numerador nem denominador confiável sem esse inventário — reportar 73,79% só para o ARM evita misturar os dois universos, conforme T02 §8.

## 5. Reconciliação dos exemplos citados no próprio `RE_COMPLETUDE_TASKS.md`

A tarefa cita `sub_275e3c` e `sub_277f78` como funções locais a reconciliar. Confirmado:

| Endereço | Está no CSV? | Está num gap desta auditoria? | Nota |
|---|---|---|---|
| `0x275e3c` | Não | Sim — gap de 2.232 bytes | Citado em `REVERSE_ENGINEERING_NOTES.md` como chamador de `__stack_chk_fail` (`0x715cc`) — ou seja, já tinha sido observado indiretamente, mas nunca ganhou entrada própria no inventário |
| `0x277f78` | Não | Sim — gap de 1.224 bytes | Sem menção anterior encontrada em `REVERSE_ENGINEERING_NOTES.md` |

Essa reconciliação confirma que a metodologia desta tarefa (cobertura por intervalo dentro de `.text`) identifica exatamente o tipo de lacuna que `RE_COMPLETUDE_TASKS.md` pedia para encontrar.

## 6. O que NÃO foi feito (pendências que bloqueiam `done`)

1. **Resolução função a função dos 303 intervalos** — isso é T06 (estrutural) e além, não T04. T04 entrega a classificação por intervalo, não a análise semântica.
2. **Vtables, tabelas de callback, PLT como alvo de chamada indireta** — `.plt`/`.got` não foram auditados em detalhe nesta tarefa (são trampolins padrão do linker, mas não confirmei que todas as entradas são triviais).
3. **x86**: nenhuma expansão de inventário, porque não há inventário base (seção 4) — T31 precisa ser feito antes ou em conjunto.
4. **`.rel.dyn`/`.rel.plt` (6.832 relocations)** não foram enumeradas e cruzadas contra os gaps individualmente — poderiam ajudar a confirmar quais endereços de gap são realmente referenciados (reduzindo a incerteza da categoria `ambiguous_needs_structural_pass`).

## 7. Arquivos produzidos por esta tarefa

- `docs/re-baseline/text_coverage_gaps.json` — os 303 intervalos, classificados, mais os 14 alvos de `.init_array`/`.fini_array` e o resumo numérico.
- Este relatório.
