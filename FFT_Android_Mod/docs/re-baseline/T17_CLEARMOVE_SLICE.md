# T17 (fatia vertical) — IA de batalha e movimento: reconstrução C diferencialmente testada de `ClearMove`/`ClearForBattleRoutine`

Depende de T16 (`ready_for_review`). Executado em 2026-11-02, décima segunda fatia vertical de P2.

**Estado: `ready_for_review` (fatia pequena, não `done`).** T17 completo exige fechar `BattleRoutine` (`0x274764`) e `FundamentalRoutine` (`0x278f84`), seleção de alvos, prioridades, desempates e pathfinding — nada disso tocado aqui. Esta tarefa fecha um par pequeno (uma função + seu tail call) achado por busca de nome direta no cluster "Routine"/"Battle".

## 1. Por que este par

`ClearForBattleRoutine()` foi achada por busca literal no cluster de T17 — o nome cita "BattleRoutine" diretamente. É minúscula (24 B) e se resolve inteiramente num tail call pra `ClearMove(MOVE*)` (40 B, mesma família "mentioned_unverified"), então fechar as duas dá valor incremental genuíno.

## 2. Reconstrução

```c
void ClearMove(MOVE* move) {
    move->field_0x1 = 0;
    move->field_0x3 = 5;
    move->field_0x1c = 0;
    move->field_0x1d = 0;
    move->field_0x1e = 0x8001;   // halfword -- provável sentinela de "sem direção"
    // field_0x0, field_0x2 e tudo a partir de +0x4 NÃO são tocados
}

void ClearForBattleRoutine(void) {
    MOVE* m = (MOVE*)(g_someBase + 0x17c0 + 0x3c);
    ClearMove(m);   // *** TAIL CALL: `b`, não `bl` ***
}
```

## 3. Achado #1: `ClearMove` é um reset parcial, não total

Só 5 bytes do struct `MOVE` são escritos (`+0x1`, `+0x3`, `+0x1c`, `+0x1d`, meia-palavra `+0x1e`); `+0x0`, `+0x2` e tudo a partir de `+0x4` ficam intocados. Confirmado por injeção de falha com bytes sentinela distintos em cada posição — um modelo que "limpasse tudo" teria divergido visivelmente.

## 4. Achado #2: terceira tail call real desta sessão

`ClearForBattleRoutine` não tem prólogo e termina num `b` direto cujo
destino é exatamente o início de `ClearMove` — a terceira tail call
real confirmada nesta sessão (depois de T20/`iOSUnitListWinOnOff` e
T23/`InitCamera`). Calcula o ponteiro `MOVE*` a partir de um global
resolvido via GOT (`0x347bb8`) somado a `+0x17c0+0x3c`, e delega a
limpeza real inteiramente pra `ClearMove`.

## 5. Teste diferencial

`docs/re-tools/c-models/t17_clearmove.c` + `test_t17_clearmove.py`: sem `bl`, 1 cenário bate exatamente mais 1 injeção de falha confirmando que `+0x0`/`+0x2` sobrevivem à chamada.

`docs/re-tools/c-models/t17_clearforbattleroutine.c` + `test_t17_clearforbattleroutine.py`: `ClearMove` tratada como caixa-preta via o mesmo tratamento de tail-call-como-stub já validado em T20/T23 — sem página vazia extra no alvo (mesma lição de metodologia de T14). Confirma que o endereço exato esperado (`g_someBase+0x17fc`) é passado como argumento e que a tail call ocorre exatamente uma vez.

Suíte completa de `docs/re-tools`: de 588 pra (588 + 3 desta fatia) = **591 testes** (1.878 subtestes, sem novos — os 3 testes desta fatia não usam `subTest`), todos passando — confirmado em 2 execuções consecutivas.

## 6. Arquivos produzidos por esta tarefa

- `docs/REVERSE_ENGINEERING_NOTES.md` — seção 672.
- `docs/RE_FUNCTION_INVENTORY.csv` — `ClearMove` e `ClearForBattleRoutine` promovidas a `read_full`.
- `docs/re-tools/c-models/t17_clearmove.c`, `test_t17_clearmove.py`.
- `docs/re-tools/c-models/t17_clearforbattleroutine.c`, `test_t17_clearforbattleroutine.py`.
- Este relatório.

## 7. Pendências que bloqueiam `done` de T17 completo

`BattleRoutine`, `FundamentalRoutine`, seleção de alvos, prioridades, desempates e pathfinding não tocados; identidade semântica dos 5 campos de `MOVE` e do global de contexto (`g_someBase`) não confirmada; `sizeof(MOVE)` completo não conhecido.
