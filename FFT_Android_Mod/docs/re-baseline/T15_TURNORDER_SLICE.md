# T15 (fatia vertical) — Máquina de estados de batalha: reconstrução C diferencialmente testada de `nextTurnOrder`/`resetTurnOrder`

Depende de T14 e dos contratos necessários de T16–T19 (todas `ready_for_review`). Executado em 2026-11-02, décima terceira fatia vertical de P2.

**Estado: `ready_for_review` (fatia pequena, não `done`).** T15 completo exige revalidar `battle()` (102 estados declarados, 70 destinos distintos no plano histórico) e todos os handlers reais — nada disso tocado aqui. Esta tarefa fecha um par pequeno achado por busca de nome no cluster de turnos.

## 1. Por que este par

`nextTurnOrder()`/`resetTurnOrder()` foram achadas por busca literal no cluster de turnos de T15 ("início/turnos/vitória/derrota/recompensa cobertos"). Ambas são minúsculas (36 B/24 B, 0 `bl`) e compartilham o mesmo global — fechar as duas juntas dá uma confirmação cruzada que fechar uma isolada não daria.

## 2. Reconstrução

```c
void nextTurnOrder(void) {
    int32_t next = *g_turnIndex + 1;
    if (next > 39) {       // comparação é sobre o valor NOVO, não o antigo
        next = 0;
    }
    *g_turnIndex = next;
}

void resetTurnOrder(void) {
    *g_turnIndex = 0;
}
```

## 3. Achado: limite checado sobre o valor novo, com comparação estrita

`nextTurnOrder` compara `old+1 > 39` (não `old >= 39`, nem `old+1 >= 40`
embora sejam equivalentes aritmeticamente — a instrução real é
`movgt`, estritamente maior). Isso significa que o valor armazenado
nunca passa por `40`: de `old=39` vai direto pra `0`; `old=38` avança
normalmente pra `39` sem resetar. Um modelo que comparasse o valor
antigo, ou usasse o limite errado por um, teria resetado um passo
adiantado — confirmado por injeção de falha testando exatamente
`old=38` vs. `old=39`.

## 4. Achado de cruzamento por endereço

As duas funções resolvem, independentemente (cada uma com sua própria
cadeia literal pool → GOT → endereço), o **mesmo** slot GOT
(`0x3475dc`) pro **mesmo** endereço global (`0x5dd8e0`). Confirmado
calculando as duas cadeias separadamente, não por nome.
`setTurnOrder()` (120 B, mesma família nominal) não foi verificada
nesta fatia.

## 5. Teste diferencial

`docs/re-tools/c-models/t15_nextturnorder.c` + `test_t15_nextturnorder.py`: 7 cenários (incluindo `0`, `38`, `39`, `40`, `INT32_MAX`) batem exatamente com o ELF original, mais 1 injeção de falha isolando a transição exata `38→39` (sem reset) vs. `39→0` (reset).

`docs/re-tools/c-models/t15_resetturnorder.c` + `test_t15_resetturnorder.py`: 5 cenários (incluindo valor negativo e `INT32_MAX` de entrada) confirmam reset incondicional pra `0`.

Suíte completa de `docs/re-tools`: de 591 pra (591 + 3 desta fatia) = **594 testes** (1.878 → **1.890 subtestes**), todos passando — confirmado em 2 execuções consecutivas.

## 6. Arquivos produzidos por esta tarefa

- `docs/REVERSE_ENGINEERING_NOTES.md` — seção 673.
- `docs/RE_FUNCTION_INVENTORY.csv` — `nextTurnOrder` e `resetTurnOrder` promovidas a `read_full`.
- `docs/re-tools/c-models/t15_nextturnorder.c`, `test_t15_nextturnorder.py`.
- `docs/re-tools/c-models/t15_resetturnorder.c`, `test_t15_resetturnorder.py`.
- Este relatório.

## 7. Pendências que bloqueiam `done` de T15 completo

`battle()` (102 estados, 70 destinos, não revalidados nesta fatia) e os demais handlers reais não tocados; `setTurnOrder()` não lida; identidade semântica de `g_turnIndex` (ordem de iniciativa vs. round-robin simples) não confirmada além do que os bytes mostram.
