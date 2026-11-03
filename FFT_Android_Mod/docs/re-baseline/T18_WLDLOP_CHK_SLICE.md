# T18 (fatia vertical) — VM de eventos: reconstrução C diferencialmente testada de `wldlop_chk`

Depende de T08–T10 (todas `ready_for_review`). Executado em 2026-11-02, vigésima sétima fatia vertical de P2.

**Estado: `ready_for_review` (pequena fatia, não `done`).** `event_call`, `worldmap_call`, `op_attackteam` (os alvos nominais de T18) seguem intocados — o dispatcher central de bytecode de evento segue fechado.

## 1. Por que esta função

`wldlop_chk()` foi achada por busca de nome no cluster `wld*`/`op_*` de T18. 88 B, 1 `bl` (`frmbuf_get`, já `read_full`).

## 2. Reconstrução

```c
void wldlop_chk(void) {
    int32_t src = g_srcFlags;
    if ((src & 2) == 0) {
        int32_t dst = g_dstFlags;
        if ((dst & 2) != 0) {
            frmbuf_get();
            src = g_srcFlags;    // RE-LEITURA real após a chamada
        }
    }
    g_dstFlags = src;
}
```

## 3. Achado: releitura pós-chamada confirmada pelos bytes, não assumida

`ldr r2,[r5]` aparece DUAS vezes no disassembly — antes do `tst`
inicial e de novo depois do `bl` — não é o mesmo valor de registrador
reaproveitado. O efeito final só usa o valor PRÉ-chamada de
`g_srcFlags` quando o `bl` não acontece; quando acontece, usa o valor
PÓS-chamada. Em todos os casos, o efeito NETO visível (ignorando o
`bl`) é `g_dstFlags = g_srcFlags` — uma "sincronização" condicional
de bit que, antes de limpar o bit no destino, dá a `frmbuf_get()` a
chance de reagir (e possivelmente mudar `g_srcFlags`) antes da cópia
final.

## 4. Teste diferencial

`docs/re-tools/c-models/t18_wldlop_chk.c` + `test_t18_wldlop_chk.py`: `frmbuf_get` stubada via `callable` capaz de mutar `g_srcFlags` durante a chamada. 5 cenários (cobrindo as combinações de bit de `src`/`dst`, com e sem mutação) batem exatamente, mais 1 injeção de falha confirmando que a mutação durante `frmbuf_get()` é observada no resultado final.

Suíte completa de `docs/re-tools`: de 628 pra (628 + 2 desta fatia) = **630 testes** (1.973 → **1.978 subtestes**), todos passando — confirmado em 2 execuções consecutivas.

## 5. Arquivos produzidos por esta tarefa

- `docs/REVERSE_ENGINEERING_NOTES.md` — seção 687.
- `docs/RE_FUNCTION_INVENTORY.csv` — `wldlop_chk` promovida a `read_full`.
- `docs/re-tools/c-models/t18_wldlop_chk.c`, `test_t18_wldlop_chk.py`.
- Este relatório.

## 6. Pendências que bloqueiam `done` de T18 completo

`event_call`, `worldmap_call`, `op_attackteam` não tocadas; `frmbuf_get()` não relida nesta fatia; identidade semântica de `g_srcFlags`/`g_dstFlags`/bit 2 não confirmada.
