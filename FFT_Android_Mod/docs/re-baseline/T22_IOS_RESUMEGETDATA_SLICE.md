# T22 (fatia vertical) — Persistência: reconstrução C diferencialmente testada de `iOS_ResumeGetData`

Depende de T08–T10 e T20 (todas `ready_for_review`). Executado em 2026-11-02, vigésima primeira fatia vertical de P2.

**Estado: `ready_for_review` (pequena fatia, não `done`).** T22 completo exige `CardAccess`, `BattleCardAccess` e toda a família `iOS_RESUME_*` — a maior parte já estava `read_full` desde lotes anteriores (NOTES §555/§565). Esta tarefa fecha uma das duas funções remanescentes do cluster (`iOS_ResumeGetData`); `iOS_ResumeMusic()` segue intocada.

## 1. Por que esta função

`iOS_ResumeGetData` já era citada por nome na leitura de `CAUTOSAVE::Save` (chama `iOS_ResumeGetData(&buf,&size)` pra tirar um snapshot de "resume" de batalha pro autosave), mas nunca foi lida individualmente — o tamanho real do buffer nunca tinha sido confirmado numericamente. 32 B, 0 `bl`, totalmente auto-contida.

## 2. Reconstrução

```c
void iOS_ResumeGetData(unsigned char** outBuf, unsigned int* outSize) {
    *outBuf = (unsigned char*)g_battleResumeBuffer;   // endereço fixo, PC-relative direto
    *outSize = 0x84558;                                 // 542.040 B (~529,9 KiB), constante fixa
}
```

## 3. Achado: tamanho exato do snapshot de resume de batalha, nunca documentado numericamente antes

`g_battleResumeBuffer` é um endereço fixo resolvido por literal
PC-relative direto (sem GOT). O tamanho é uma constante `0x84558` =
542.040 bytes. Consistente com a matemática já vista em
`CAUTOSAVE::Save`: `memcpy(scratch+0x20, buf, size)` seguido de
`CFFT_STATE::Suspend(..., scratch+0xc0020)` — a diferença
(`0xc0000`=786.432 B reservados vs. `0x84558`=542.040 B copiados)
deixa ~244 KB de margem, consistente com alocação conservadora.

## 4. Teste diferencial

`docs/re-tools/c-models/t22_ios_resumegetdata.c` + `test_t22_ios_resumegetdata.py`: confirma que a função sempre retorna o endereço fixo e o tamanho fixo, independente de qualquer entrada, mais 1 injeção de falha executando a função duas vezes com ponteiros de saída completamente diferentes e confirmando que os valores escritos são idênticos.

Suíte completa de `docs/re-tools`: de 614 pra (614 + 2 desta fatia) = **616 testes** (1.951 subtestes, sem novos), todos passando — confirmado em 2 execuções consecutivas.

## 5. Arquivos produzidos por esta tarefa

- `docs/REVERSE_ENGINEERING_NOTES.md` — seção 681.
- `docs/RE_FUNCTION_INVENTORY.csv` — `iOS_ResumeGetData` promovida a `read_full`.
- `docs/re-tools/c-models/t22_ios_resumegetdata.c`, `test_t22_ios_resumegetdata.py`.
- Este relatório.

## 6. Pendências que bloqueiam `done` de T22 completo

`CardAccess`, `BattleCardAccess` não tocadas; layout interno do buffer de 542.040 bytes não investigado; `iOS_WorldMapResumeGetData` (par citado na mesma seção de `CAUTOSAVE::Save`) não lida individualmente; `iOS_ResumeMusic()` segue `read_structural`.
