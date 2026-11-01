# T19 (fatia vertical) — Mundo e progressão: reconstrução C diferencialmente testada de `evt_get_flgdt`/`evt_flag`

Depende de T18 (`ready_for_review`). Executado em 2026-11-01, décima primeira fatia vertical de P2.

**Estado: `ready_for_review` (fatia pequena, não `done`).** T19 completo exige seleção/transição de mapas, movimento no mundo, encontros, recrutamento, capítulos e condições de desbloqueio — nada disso tocado aqui. Esta tarefa fecha um par de funções pequenas da família "flags de história" (`evt_flag*`), achada por busca de nome, cruzando por endereço um global de contexto antes não identificado.

## 1. Por que este par

A família `evt_flag()`/`evt_flag_high()`/`evt_flag_low()`/`evt_flagset()` (todas `mentioned_unverified`) chama uma função auxiliar comum, `evt_get_flgdt(int*, int*)` (`read_structural`, nunca lida por completo). Fechar o par (o auxiliar + um consumidor) dá valor incremental genuíno: o auxiliar fica disponível como dependência já fechada pras outras três funções da família.

## 2. Reconstrução

```c
void evt_get_flgdt(int* out1, int* out2) {
    uint16_t v1 = g_vmCtx->buf[g_vmCtx->pos];
    g_vmCtx->pos += 1;                          // gravação intermediária
    uint16_t v2 = g_vmCtx->buf[g_vmCtx->pos];
    *out1 = v1;
    *out2 = v2;
    g_vmCtx->pos += 2;   // soma final a partir do pos ORIGINAL
}

int32_t evt_flag(void) {
    int flagIndex, expectedValue;
    evt_get_flgdt(&flagIndex, &expectedValue);
    int32_t actualValue = Wread_eventflag(flagIndex);
    if (actualValue != expectedValue) {
        g_vmCtx->status |= 2;
    }
    return actualValue;
}
```

## 3. Achado #1: `evt_get_flgdt` grava o cursor duas vezes, com truncamento de 16 bits explícito

Lê dois tokens `uint16` consecutivos a partir do cursor de leitura
(campo de 16 bits), mas grava o cursor **duas vezes** — uma vez
`pos+1` (intermediária, entre ler o primeiro e o segundo token), outra
`pos+2` (final, a partir do `pos` original, não do intermediário). O
truncamento pra 16 bits é explícito nos bytes (`lsl #0x10; lsr
#0x10`) e confirmado por injeção de falha com `pos=0xffff` (vira `0`,
não `0x10000`).

## 4. Achado #2: `evt_flag` não é um predicado puro

`r0` nunca é reescrito depois do `bl Wread_eventflag`, nos dois
ramos — o retorno real é **sempre o valor lido de verdade da flag**,
não um booleano. O efeito de "bate/não bate o valor esperado do
script" é só um bit (`0x2`) marcado condicionalmente num status
global, sem afetar o retorno. Confirmado por teste de injeção de
falha: um modelo "predicado puro" teria divergido.

## 5. Achado de cruzamento por endereço

O status global que `evt_flag` escreve (`+0x0`) e o buffer/cursor que
`evt_get_flgdt` usa (`+0x8`/`+0xc`) resolvem pro mesmo slot GOT
(`0x347a80`) e pro mesmo endereço base (`0x67b35c`) — confirmado
calculando as duas cadeias independentemente, não por nome. É uma
struct de contexto de VM antes não identificada; **não** se afirma
ligação com a struct de `event_call`/`worldmap_call` (seções 66/80),
que recebem `script`/`pc` como argumentos explícitos.

## 6. Teste diferencial

`docs/re-tools/c-models/t19_evt_get_flgdt.c` + `test_t19_evt_get_flgdt.py`: sem `bl` pra stubar, 3 cenários batem exatamente mais 1 injeção de falha confirmando o truncamento de 16 bits.

`docs/re-tools/c-models/t19_evt_flag.c` + `test_t19_evt_flag.py`: `evt_get_flgdt`/`Wread_eventflag` stubados via `callable`, 4 cenários batem exatamente mais 2 injeções de falha (retorno não é booleano; bit de status sobrevive quando os valores batem — não é uma limpeza incondicional).

Suíte completa de `docs/re-tools`: de 583 pra (583 + 5 desta fatia) = **588 testes** (1.871 → **1.878 subtestes**), todos passando — confirmado em 2 execuções consecutivas.

## 7. Arquivos produzidos por esta tarefa

- `docs/REVERSE_ENGINEERING_NOTES.md` — seção 671.
- `docs/RE_FUNCTION_INVENTORY.csv` — `evt_get_flgdt` e `evt_flag` promovidas a `read_full`.
- `docs/re-tools/c-models/t19_evt_get_flgdt.c`, `test_t19_evt_get_flgdt.py`.
- `docs/re-tools/c-models/t19_evt_flag.c`, `test_t19_evt_flag.py`.
- Este relatório.

## 8. Pendências que bloqueiam `done` de T19 completo

Seleção/transição de mapas, movimento no mundo, encontros, recrutamento, capítulos e condições de desbloqueio não tocados; `Wread_eventflag`/`Wwrite_eventflag` tratadas como caixa-preta; `evt_flag_high`, `evt_flag_low`, `evt_flagset` (mesma família) não lidas; identidade semântica do global de contexto não estendida além dos 3 campos usados aqui.
