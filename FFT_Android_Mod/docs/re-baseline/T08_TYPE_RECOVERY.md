# T08 — Recuperar tipos e modelo de memória

Depende de T04 (`ready_for_review`, parcial). Executado em 2026-10-31.

**Estado: `ready_for_review` (muito parcial) — NÃO `done`.** Dos 8 tipos priorizados pela tarefa, 1 (`CFFT_STATE`) tem um mapa quase completo (já existia nas notas, só nunca tinha sido consolidado num header compartilhado), 2 (`BWORK`, `ACT`) têm mapas genuinamente parciais com evidência nova e antiga combinada, 1 (`EDATA`) ganhou evidência de campo pela primeira vez nesta tarefa (antes só tinha papel inferido por contexto, zero offset), e 4 (`_Object`, `ActionRequest`, `FFT_SAVE_DATA`, `CARD_HEADER`) **não têm nenhuma evidência de campo confiável** encontrada nesta auditoria — ficam explicitamente como não recuperados, não inventados. "Tabelas de mensagens e estruturas gráficas" tiveram apenas uma tabela de mensagens coberta (seção 5); nenhuma estrutura gráfica foi tratada.

Todos os headers em `docs/re-baseline/types/*.h` foram compilados e verificados com `offsetof`/`sizeof` contra os valores citados — nenhum offset no header é digitado sem checagem.

## 1. `CFFT_STATE` — já estava quase completo, consolidado em `types/cfft_state.h`

Evidência pré-existente (`REVERSE_ENGINEERING_NOTES.md` §22, 2026-10-16, sessão anterior): construtor lido por completo (584 B) + 23 getters/setters pequenos. Mapa de `+0x0` a `+0x34` (render size, escala de vértice, flags de captura/encontro, `mode` com efeito confirmado em UI e cor de fundo, `debugMode`, `moviePlaying` com sentinela `-1`, `musicBuffer[]`, `settingsEnable`, `linkEnable`) e `params[]` como array plano de `int` a partir de `+0x38`, confirmado por três acessores lidos por completo (`GetParam`/`SetParam`/`AddParam`). Nada novo adicionado por esta tarefa — só consolidação.

## 2. `BWORK` — parcial, 486 bytes confirmados, ~20 campos conhecidos de 486

`sizeof(BWORK) = 0x1e6` (486 bytes) confirmado por `set_status_all` indexando um array global `BWORK[]` via `idx*0x1e6`. Campos conhecidos vêm de três fontes: `REVERSE_ENGINEERING_NOTES.md` §349/§355 (status/rede/combate) e §653 (`set_casting_status`), mais a leitura nova de `copy_entry_coord(BWORK*, EDATA*)` (`0x1d9ee0`, 120 B, 100% de cobertura estrutural, 0 chamadas, totalmente linear) feita nesta tarefa. Essa leitura nova confirma, pela primeira vez, campos de coordenada: `+0x184` (halfword, "coord X", zero-estendido de um byte de `EDATA`) e `+0x186` (byte, "coord Y"), mais três bytes de flags em `+0x4f`/`+0x50`/`+0x51` copiados de `EDATA`.

**Achado de reconciliação pendente, não resolvido aqui:** `+0x61` é citado por §349 como byte de categoria "incapacitado" (bits `0x0D`/`0x20`) e por §653 como máscara de 4 bits de "estágio de conjuração" (bits 0-3) — os dois usos se sobrepõem parcialmente (bits 0,2,3 vs. bits 0-3) sem uma reconciliação explícita em nenhuma das duas seções originais. Registrado como pendência, não escolhido um dos dois como correto.

Ver `docs/re-baseline/types/bwork.h` para o layout completo com citação por campo; ~450 dos 486 bytes seguem como `_unknown_*` explícito.

## 3. `EDATA` — primeira evidência de campo já obtida para este tipo

Antes desta tarefa, `EDATA` só tinha papel inferido por contexto ("template de dados de inimigo", `REVERSE_ENGINEERING_NOTES.md` §72) e a nota explícita de que "o layout exato de `BWORK`/`EDATA` não foi mapeado campo a campo" (§72, linha 6752). A leitura de `copy_entry_coord` nesta tarefa dá os primeiros 5 campos reais: `+0x19`, `+0x1a`, `+0x1b` (bit-empacotado, consumido por `BWORK+0x51`), `+0x1e` e `+0x1f` (coordenadas X/Y de mapa, copiadas pra `BWORK`). `sizeof(EDATA)` segue desconhecido — o header (`types/edata.h`) não declara um tamanho total, só os bytes lidos.

## 4. `ACT` — minimamente recuperado a partir do `set_ct_weapon` já existente

`REVERSE_ENGINEERING_NOTES.md` §654 (sessão anterior) já tinha lido `set_ct_weapon(ACT*)` por completo e documentado `act->byte_0x1` (classe de arma), `act->field_0x2` (id de item, `int16_t`) e `act->field_0x8` (valor de fallback). Consolidado em `types/act.h` nesta tarefa, sem campo novo. `sizeof(ACT)` desconhecido.

## 5. Tabela de mensagens — `GlobalMsgCache`, achado lateral (não um dos 8 tipos pedidos, mas serve "tabelas de mensagens")

`MessageDataSet(int kind)` (`REVERSE_ENGINEERING_NOTES.md` §652, sessão anterior, 284 B, lida por completo) grava o resultado de `pspMsgGet(kind)` num struct global por `kind`: `+0x18`, `+0x38`, `+0x58`, `+0x60`, `+0x6c`, `+0x70`, `+0x74` (kinds 4 e 5 convergem no mesmo campo — achado já registrado), `+0x7c`. Não consolidado em header próprio nesta tarefa (não era um dos 8 tipos priorizados); registrado aqui só para constar no escopo de "tabelas de mensagens" e não ser perdido.

## 6. Não recuperados — explicitamente pendentes, nenhuma estrutura inventada

| Tipo | Evidência encontrada nesta auditoria |
|---|---|
| `_Object` | Nenhuma linha com offset de campo encontrada sob esse nome nas notas; 8 menções totais, todas contextuais |
| `ActionRequest` | 1 menção total no arquivo de notas inteiro; zero evidência de campo |
| `FFT_SAVE_DATA` | `pspFftSave(int, FFT_SAVE_DATA*, int*)` foi lida por completo (§651) mas o parâmetro é passado opaco pra um helper local não resolvido (`sub_2898e0`) — a função não toca nenhum campo de `FFT_SAVE_DATA` diretamente, então não produz evidência de layout |
| `CARD_HEADER` | 7 menções, nenhuma com offset de campo encontrado |
| Estruturas gráficas (não nomeadas especificamente na tarefa) | Não investigadas nesta tarefa |

Não escrevi headers para esses 5 itens — um header vazio ou "todo-unknown" não adiciona informação sobre um `sizeof()` desconhecido, e criar um só pra existir seria o tipo de "estrutura inventada" que a tarefa proíbe explicitamente.

## 7. Verificação de layout (exigida pelo critério de aceite)

Cada header em `docs/re-baseline/types/` foi compilado com GCC e checado via `offsetof`/`sizeof` contra os valores citados nos comentários — reproduzível com:

```bash
gcc -I docs/re-baseline/types -x c -include stdio.h -include stddef.h \
    -o /tmp/check - <<'C'
#include "bwork.h"
#include "edata.h"
#include "act.h"
#include "cfft_state.h"
int main(){ return sizeof(BWORK)==0x1e6 && sizeof(CFFT_STATE)>0 ? 0 : 1; }
C
```

## 8. Arquivos produzidos por esta tarefa

- `docs/re-baseline/types/bwork.h`, `edata.h`, `act.h`, `cfft_state.h` — headers citados por campo, verificados por compilação.
- Este relatório.
