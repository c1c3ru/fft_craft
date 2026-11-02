# T08 (fatia vertical) — Recuperação de tipos: primeira evidência de campo para `FFT_SAVE_DATA`

Depende de T04 (`ready_for_review`). Executado em 2026-11-02, décima quinta fatia vertical de P2.

**Estado: `ready_for_review` (pequena fatia, não `done`).** T08 completo exige headers/evidência pra `_Object`, `ActionRequest`, `FFT_SAVE_DATA`, `CARD_HEADER` e estruturas gráficas. Esta tarefa fecha o primeiro campo confirmado de `FFT_SAVE_DATA` — um dos quatro tipos que T08 (2026-10-31) listou como "sem nenhuma evidência de campo confiável".

## 1. Por que esta releitura

`pspSaveDataMissionRateSave`/`Load`/`GetOne` já estavam `read_full` desde o lote em massa 75 (NOTES §557), mas sem pseudocódigo individual nem teste diferencial — um fechamento por prefixo de subsistema, não a leitura rigorosa que este loop de fatias verticais aplica. Relendo individualmente por disassembly direto, as duas primeiras dão a primeira evidência de campo confiável pra `FFT_SAVE_DATA`.

## 2. Reconstrução

```c
void pspSaveDataMissionRateSave(FFT_SAVE_DATA* save) {
    void* missionBuffer = pspNetEntranceDataMissionBufferGet();
    memcpy(save->field_0x60, missionBuffer, 0x20);   // TAIL CALL pro memcpy real
}

void pspSaveDataMissionRateLoad(FFT_SAVE_DATA* save) {
    void* missionBuffer = pspNetEntranceDataMissionBufferGet();
    memcpy(missionBuffer, save->field_0x60, 0x20);   // direção INVERTIDA — TAIL CALL
}

int32_t pspSaveDataGetOne(int slot, FFT_SAVE_DATA* save) {
    return GetOne_0x2898e0(save, slot, 1);   // TAIL CALL, reordena os argumentos
}
```

## 3. Achado principal: primeira evidência de campo de `FFT_SAVE_DATA`

`Save`/`Load` terminam em tail call direto pro `memcpy` real
(`0x714b8`, já confirmado como `memcpy` glibc-style em outra seção das
notas, não um helper customizado). `Save` chama
`memcpy(dest=save+0x60, src=missionBuffer, 0x20)`; `Load` chama
`memcpy(dest=missionBuffer, src=save+0x60, 0x20)` — as direções são
**exatamente invertidas**, confirmado pelos registradores em cada
ponto de tail call. Dá `FFT_SAVE_DATA+0x60` (32 B) = um blob de "taxa
de missão", com direção save/load simétrica e confirmada — ver
[`types/fft_save_data.h`](types/fft_save_data.h).

## 4. Achado secundário: sexto tail call confirmado nesta sessão

`pspSaveDataGetOne` não tem prólogo e é puramente um shim de
reordenação de argumentos: troca `(slot, save)` por `(save, slot)`,
adiciona uma terceira constante (`1`), e desvia direto (`b`, não
`bl`) pra uma função local sem símbolo em `0x2898e0` — não lida nem
reivindicada aqui.

## 5. Teste diferencial

`docs/re-tools/c-models/t08_mission_rate_save_load.c` + `test_t08_mission_rate_save_load.py`: `pspNetEntranceDataMissionBufferGet` (já `read_full`) e o `memcpy` real são stubados via `callable` — o stub de `memcpy` executa a cópia de bytes de verdade dentro da memória do Unicorn. Confirma as duas direções e que nenhum outro byte de `save` é tocado, mais 1 injeção de falha confirmando que inverter as direções produz resultados diferentes.

`docs/re-tools/c-models/t08_pspsavedatagetone.c` + `test_t08_pspsavedatagetone.py`: confirma a reordenação exata de argumentos e que o valor de retorno é propagado sem alteração (3 cenários).

Suíte completa de `docs/re-tools`: de 596 pra (596 + 4 desta fatia) = **600 testes** (1.915 → **1.918 subtestes**), todos passando — confirmado em 2 execuções consecutivas.

## 6. Arquivos produzidos por esta tarefa

- `docs/REVERSE_ENGINEERING_NOTES.md` — seção 675.
- `docs/RE_FUNCTION_INVENTORY.csv` — `pspSaveDataMissionRateSave`/`Load`/`GetOne` com `section_ref` atualizado pra §675 (releitura individual, substitui a referência de lote).
- `docs/re-baseline/types/fft_save_data.h` — primeiro header do tipo, verificado por `static_assert`/`offsetof`.
- `docs/re-tools/c-models/t08_mission_rate_save_load.c`, `test_t08_mission_rate_save_load.py`.
- `docs/re-tools/c-models/t08_pspsavedatagetone.c`, `test_t08_pspsavedatagetone.py`.
- Este relatório.

## 7. Pendências que bloqueiam `done` de T08 completo

`_Object`, `ActionRequest`, `CARD_HEADER` e estruturas gráficas seguem sem nenhuma evidência de campo; `GetOne_0x2898e0` não lida; `sizeof(FFT_SAVE_DATA)` completo não conhecido; os outros ~28 campos de `FFT_SAVE_DATA` citados em `ConvTutoData`/`pspFftSave`/`pspFftLoad` (`read_structural`) não cruzados com este achado nem individualmente confirmados.
