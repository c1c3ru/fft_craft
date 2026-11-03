# T21 (fatia vertical) — Texto e janelas: reconstrução C diferencialmente testada de `Wdisposewindowbytask`

Depende de T08 e T20 (ambas `ready_for_review`). Executado em 2026-11-02, vigésima quinta fatia vertical de P2.

**Estado: `ready_for_review` (pequena fatia, não `done`).** Primeira evidência de struct de slots de janela nesta sessão. Os alvos nominais de T21 (`mesputmain`, `Wmesputmain`, variantes A/C/D/E/W) seguem intocados.

## 1. Por que esta função

`Wdisposewindowbytask(int)` foi achada por busca de nome no cluster de janelas de T21. 112 B, 0 `bl`, totalmente auto-contida.

## 2. Reconstrução

```c
void Wdisposewindowbytask(int taskId) {
    int slotPair;
    if (g_base->ownerTask0 == taskId)      slotPair = 0;   // +0x5e8
    else if (g_base->ownerTask1 == taskId) slotPair = 2;   // +0x968
    else if (g_base->ownerTask2 == taskId) slotPair = 4;   // +0xce8
    else return;                                            // nenhum bate: no-op real

    g_base->slots[slotPair].field_0x5e4     = 0;   // stride 0x1c0 por slot
    g_base->slots[slotPair + 1].field_0x5e4 = 0;
}
```

## 3. Achado: mesmo endereço base para os rastreadores e o array de slots

As duas cadeias de literal PC-relative (sem GOT) resolvem pro mesmo
endereço base (`0x4711fc`), confirmado calculando as duas
separadamente. É literalmente a mesma struct contendo tanto os 3
rastreadores de "task dono" (`+0x5e8`/`+0x968`/`+0xce8`, 0x380 bytes
entre si) quanto o array de slots de janela (stride `0x1c0`=448 B,
indexado em pares: 0&1, 2&3, 4&5). Primeira evidência de campo pra
esse array de slots (campo `+0x5e4` de cada entrada, zerado no
descarte) e pros 3 rastreadores.

## 4. Achado: caso sem correspondência é um no-op real

Se `taskId` não bate com nenhum dos três rastreadores, a função é um
no-op real — confirmado pelo `bxne lr` direto na terceira
comparação, não assumido.

## 5. Teste diferencial

`docs/re-tools/c-models/t21_wdisposewindowbytask.c` + `test_t21_wdisposewindowbytask.py`: 4 cenários (um pra cada rastreador batendo, mais um que não bate com nenhum) batem exatamente, mais 2 injeções de falha: confirma que o caso "não bate com nenhum" é um no-op completo; e que AMBOS os slots do par são zerados, não só um.

Suíte completa de `docs/re-tools`: de 623 pra (623 + 3 desta fatia) = **626 testes** (1.964 → **1.968 subtestes**), todos passando — confirmado em 2 execuções consecutivas.

## 6. Arquivos produzidos por esta tarefa

- `docs/REVERSE_ENGINEERING_NOTES.md` — seção 685.
- `docs/RE_FUNCTION_INVENTORY.csv` — `Wdisposewindowbytask` promovida a `read_full`.
- `docs/re-tools/c-models/t21_wdisposewindowbytask.c`, `test_t21_wdisposewindowbytask.py`.
- Este relatório.

## 7. Pendências que bloqueiam `done` de T21 completo

`mesputmain`, `Wmesputmain`, variantes A/C/D/E/W não tocadas; identidade semântica exata dos 3 rastreadores e do campo `field_0x5e4` não confirmada; `sizeof` real da struct de slot e número total de slots não conhecido além do mínimo exigido.
