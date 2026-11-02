# T22 (fatia vertical) — Persistência: reconstrução C diferencialmente testada de `iOS_ResumeMusic`

Depende de T08–T10 e T20 (todas `ready_for_review`). Executado em 2026-11-02, vigésima segunda fatia vertical de P2.

**Estado: `ready_for_review` (pequena fatia, não `done`).** Com esta tarefa, os dois itens remanescentes do cluster `iOS_Resume*` que T22 ainda tinha em aberto ficam fechados (`iOS_ResumeGetData` na fatia anterior, `iOS_ResumeMusic` aqui). `CardAccess`/`BattleCardAccess` seguem intocadas.

## 1. Por que esta função

`iOS_ResumeMusic()` era a última função `read_structural` do cluster `iOS_Resume*` ainda não individualmente lida. 100 B, 2 `bl` + 1 tail call, compõe duas funções já fechadas em outras seções.

## 2. Reconstrução

```c
void iOS_ResumeMusic(void) {
    g_lastBgm0 = (uint16_t)CFFT_STATE::GetMusicBuffer(g_cfftState, 0);
    g_lastBgm1 = (uint16_t)CFFT_STATE::GetMusicBuffer(g_cfftState, 1);

    iOS_SetLastBGMFromResumeData(&g_lastBgm0, &g_lastBgm1);  // SOBRESCREVE os dois, incondicional

    tailTarget_0xbebec(g_lastBgm0, g_lastBgm1);   // TAIL CALL
}
```

## 3. Achado: resultados de `GetMusicBuffer` descartados antes de serem lidos

Disassembly de `iOS_SetLastBGMFromResumeData` (já `read_full`)
confirma que ela sempre sobrescreve os dois parâmetros de saída com
valores lidos de offsets fixos de uma struct de dados de resume
(`+0x47c`/`+0x47e`), sem checar nem misturar com o que já estava lá.
Os dois valores que `GetMusicBuffer` calculou são imediatamente
substituídos, nunca chegando ao tail call final — os valores
realmente passados vêm inteiramente da struct de resume. Confirmado
por injeção de falha com valores de `GetMusicBuffer` e de resume
deliberadamente diferentes.

## 4. Achado secundário: oitava tail call desta sessão

`iOS_ResumeMusic` termina com `b` direto pra uma função local sem
símbolo (`0xbebec`) — mais uma confirmação do padrão já visto em
T20/T23/T17/T08.

## 5. Teste diferencial

`docs/re-tools/c-models/t22_ios_resumemusic.c` + `test_t22_ios_resumemusic.py`: as duas chamadas e o alvo da tail call stubados via `callable`, confirmando ordem exata, argumentos de cada uma, e que os valores finais vêm de `SetLastBGMFromResumeData`, não de `GetMusicBuffer`.

3 cenários batem exatamente, mais 1 injeção de falha. Suíte completa de `docs/re-tools`: de 616 pra (616 + 2 desta fatia) = **618 testes** (1.951 → **1.954 subtestes**), todos passando — confirmado em 2 execuções consecutivas.

## 6. Arquivos produzidos por esta tarefa

- `docs/REVERSE_ENGINEERING_NOTES.md` — seção 682.
- `docs/RE_FUNCTION_INVENTORY.csv` — `iOS_ResumeMusic` promovida a `read_full`.
- `docs/re-tools/c-models/t22_ios_resumemusic.c`, `test_t22_ios_resumemusic.py`.
- Este relatório.

## 7. Pendências que bloqueiam `done` de T22 completo

`CardAccess`, `BattleCardAccess` não tocadas; alvo da tail call (`0xbebec`) não lido; por que `GetMusicBuffer` é chamada se seu resultado é descartado (efeito colateral relevante na própria `CFFT_STATE`?) não investigado.
