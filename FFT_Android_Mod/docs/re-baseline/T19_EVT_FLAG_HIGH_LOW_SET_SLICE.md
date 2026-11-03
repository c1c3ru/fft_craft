# T19 (fatia vertical) — Mundo e progressão: fecha a família `evt_flag*` por completo

Depende de T18 (`ready_for_review`). Executado em 2026-11-02, vigésima quarta fatia vertical de P2.

**Estado: `ready_for_review` (pequena fatia, não `done`).** Fecha os três membros remanescentes da família `evt_flag*` (`evt_flag_high`, `evt_flag_low`, `evt_flagset`) — com `evt_flag`/`evt_get_flgdt` já fechadas numa fatia anterior, **toda a família está agora completa**. Os alvos nominais de T19 (mapas, recrutamento, capítulos) seguem intocados.

## 1. Por que este grupo

A família `evt_flag*` foi identificada numa fatia anterior (seção 671), que fechou `evt_flag`/`evt_get_flgdt` mas deixou `evt_flag_high`/`evt_flag_low`/`evt_flagset` pendentes. Mesma estrutura, mesmos callees — fechar os três completa o grupo.

## 2. Reconstrução

```c
int32_t evt_flag_high(void) {
    int flagIndex, expectedValue;
    evt_get_flgdt(&flagIndex, &expectedValue);
    int32_t actualValue = Wread_eventflag(flagIndex);
    if (actualValue < expectedValue) g_vmCtx->status |= 2;
    return actualValue;
}

int32_t evt_flag_low(void) {
    int flagIndex, expectedValue;
    evt_get_flgdt(&flagIndex, &expectedValue);
    int32_t actualValue = Wread_eventflag(flagIndex);
    if (actualValue > expectedValue) g_vmCtx->status |= 2;
    return actualValue;
}

void evt_flagset(void) {
    int flagIndex, value;
    evt_get_flgdt(&flagIndex, &value);
    Wwrite_eventflag(flagIndex, value);
}
```

## 3. Achado: condição exata confirmada pela instrução, não pelo nome

`evt_flag_high` marca o bit de status quando `atual < esperado`
(`bge` pula o `orr`); `evt_flag_low` marca quando `atual > esperado`
(`ble` pula o `orr`). Na igualdade exata, nenhuma das duas marca o
bit — confirmado testando as três relações (`<`, `==`, `>`) nas duas
funções e cruzando os resultados. `evt_flagset` não tem condição
nenhuma — grava direto, sem tocar no bit de status.

## 4. Teste diferencial

`docs/re-tools/c-models/t19_evt_flag_high_low.c` + `test_t19_evt_flag_high_low.py`: 3 relações × 2 funções batem exatamente, mais 1 injeção de falha cruzando as duas funções nas três relações pra confirmar que disparam em lados opostos.

`docs/re-tools/c-models/t19_evt_flagset.c` + `test_t19_evt_flagset.py`: 4 valores (incluindo negativo e `INT32_MAX`) batem exatamente.

Suíte completa de `docs/re-tools`: de 620 pra (620 + 3 desta fatia) = **623 testes** (1.954 → **1.964 subtestes**), todos passando — confirmado em 2 execuções consecutivas.

## 5. Arquivos produzidos por esta tarefa

- `docs/REVERSE_ENGINEERING_NOTES.md` — seção 684.
- `docs/RE_FUNCTION_INVENTORY.csv` — as 3 funções promovidas a `read_full`.
- `docs/re-tools/c-models/t19_evt_flag_high_low.c`, `test_t19_evt_flag_high_low.py`.
- `docs/re-tools/c-models/t19_evt_flagset.c`, `test_t19_evt_flagset.py`.
- Este relatório.

## 6. Pendências que bloqueiam `done` de T19 completo

Mapas, movimento, recrutamento, capítulos não tocados; `Wread_eventflag`/`Wwrite_eventflag` caixa-preta; identidade semântica do global de contexto não estendida além do confirmado na fatia anterior.
