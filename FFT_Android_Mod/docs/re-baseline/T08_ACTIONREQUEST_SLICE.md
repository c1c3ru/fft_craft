# T08 (fatia vertical) — Recuperação de tipos: primeira evidência de campo para `ActionRequest`

Depende de T04 (`ready_for_review`). Executado em 2026-11-02, décima sexta fatia vertical de P2.

**Estado: `ready_for_review` (pequena fatia, não `done`).** Esta tarefa fecha o segundo campo confirmado entre os quatro tipos que T08 (2026-10-31) listou como "sem nenhuma evidência de campo confiável" — o primeiro foi `FFT_SAVE_DATA+0x60` (fatia anterior); este é `ActionRequest+0x0`.

## 1. Por que esta função

`iOSCurSameProcs(ActionRequest*)` foi achada por busca de nome direta pelo tipo `ActionRequest*` no inventário. É pequena (44 B, 1 `bl`) e toca diretamente o campo `+0x0` do parâmetro.

## 2. Reconstrução

```c
void iOSCurSameProcs(ActionRequest* req) {
    if (req->field_0x0 != 0xfe) {
        return;
    }
    if (iOSCurSameOK() != 0) {
        req->field_0x0 = 7;
    }
}
```

## 3. Achado de cruzamento com pesquisa independente

`AI_DIFFICULTY_RESEARCH.md` seção 14.4 — uma linha de investigação
diferente desta, sobre o dispatcher de `BattleRoutine` — já tinha
observado que o bloco de finalização de `BattleRoutine` "grava um
código em `*out` (valores `0` ou `2` observados)". `*out` é
precisamente `ActionRequest+0x0`, o MESMO campo que esta função lê e
condicionalmente sobrescreve. As duas leituras confirmam
independentemente que esse offset é um código de status/requisição,
sem que nenhum lado tenha assumido o significado do outro — agora com
um conjunto mais amplo de valores observados (`0`, `2`, `0xfe`, `7`).

## 4. Teste diferencial

`docs/re-tools/c-models/t08_ioscursameprocs.c` + `test_t08_ioscursameprocs.py`: `iOSCurSameOK` stubada via `callable`. 5 cenários batem exatamente, incluindo os códigos `0`/`2`/`7` já observados pela pesquisa de IA (confirmando que são ignorados por esta função — só `0xfe` dispara o caminho). Mais 1 injeção de falha confirmando que `iOSCurSameOK` nunca é chamada para nenhum código diferente de `0xfe` — uma guarda frouxa poderia sobrescrever códigos que pertencem à lógica de `BattleRoutine`.

Suíte completa de `docs/re-tools`: de 600 pra (600 + 2 desta fatia) = **602 testes** (1.918 → **1.923 subtestes**), todos passando — confirmado em 2 execuções consecutivas.

## 5. Arquivos produzidos por esta tarefa

- `docs/REVERSE_ENGINEERING_NOTES.md` — seção 676.
- `docs/RE_FUNCTION_INVENTORY.csv` — `iOSCurSameProcs` promovida a `read_full`.
- `docs/re-baseline/types/action_request.h` — primeiro header do tipo, verificado por `static_assert`/`offsetof`.
- `docs/re-tools/c-models/t08_ioscursameprocs.c`, `test_t08_ioscursameprocs.py`.
- Este relatório.

## 6. Pendências que bloqueiam `done` de T08 completo

`_Object`, `CARD_HEADER`, estruturas gráficas seguem sem nenhuma evidência de campo; `iOSCurSameOK()` não lida; `sizeof(ActionRequest)` e os demais campos (preenchidos pelo bloco de finalização de `BattleRoutine`, "pacote de 24 bytes" por `MemCpyW`, AI seção 14.4) não confirmados; significado semântico exato de `0xfe`/`7` não afirmado além do que os bytes mostram.
