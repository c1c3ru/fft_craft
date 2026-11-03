# T24 (fatia vertical) — Modelos, animações e efeitos: reconstrução C diferencialmente testada de 5 callbacks do cluster `_EffectTCB`/`_Object`

Depende de T23 (`ready_for_review`). Executado em 2026-11-02, vigésima oitava fatia vertical de P2.

**Estado: `ready_for_review` (pequena fatia, não `done`).** `ASHURA_addPrim`, `CreateObjectWithTable`, `NewAnimation`, `executeShape` (os alvos nominais de T24) seguem intocados.

## 1. Por que este grupo

5 funções do cluster de callbacks `_EffectTCB`/`_Object` achadas por busca de nome: `dmyFnc`, `CreateObjectWithTableWithParentData`, `system_error`, `objectLG2`, `dmyFnc2`. Todas minúsculas (4–24 B), fechar o grupo inteiro de uma vez revelou uma distinção honesta entre duas categorias de "placeholder".

## 2. Reconstrução

```c
void system_error(int category, int code) { /* bx lr isolado -- nada */ }

int32_t dmyFnc(_EffectTCB* tcb) {
    system_error(1, 0x22);   // ignora completamente tcb
    return 0;
}

int32_t CreateObjectWithTableWithParentData(short a0, int a1, int a2, int a3, _Object* obj) {
    system_error(1, 0x50);   // ignora completamente todos os parâmetros
    return 0;
}

void objectLG2(_EffectTCB* tcb, _Object* obj) { /* bx lr isolado -- nada */ }
void dmyFnc2(_EffectTCB* tcb, _Object* obj)   { /* bx lr isolado -- nada */ }
```

## 3. Achado: duas categorias de "placeholder" genuinamente diferentes

`objectLG2`/`dmyFnc2` são `bx lr` isolados — no-ops puros, idênticos
em espírito aos 5 stubs de NetBattle/iCloud (seção 674). `dmyFnc`/
`CreateObjectWithTableWithParentData`, apesar do nome sugerir a
mesma categoria, ignoram os próprios parâmetros e chamam
`system_error(1, código)` antes de retornar `0` — com um código fixo
DIFERENTE pra cada uma (`0x22`/`0x50`), confirmado por injeção de
falha. Só que `system_error` em si é TAMBÉM um `bx lr` isolado,
ignorando os dois argumentos — todo o mecanismo de "reportar um
erro" está, neste build, completamente inerte. O efeito observável
final das 5 funções acaba sendo o mesmo, mas por DUAS formas de
código genuinamente distintas.

## 4. Teste diferencial

`docs/re-tools/c-models/t24_stub_callbacks.c` + `test_t24_stub_callbacks.py`: `system_error` stubada via `callable` pra confirmar os argumentos exatos de cada chamador, mais os 3 no-ops puros testados diretamente (confirmando que `r0` nunca é escrito, mesmo teste de dois valores de entrada distintos já usado pra `NetBattleJudge`), mais 1 injeção de falha confirmando que os dois códigos de erro são distintos.

Suíte completa de `docs/re-tools`: de 630 pra (630 + 4 desta fatia) = **634 testes** (1.978 subtestes, sem novos), todos passando — confirmado em 2 execuções consecutivas.

## 5. Arquivos produzidos por esta tarefa

- `docs/REVERSE_ENGINEERING_NOTES.md` — seção 688.
- `docs/RE_FUNCTION_INVENTORY.csv` — as 5 funções promovidas a `read_full`.
- `docs/re-tools/c-models/t24_stub_callbacks.c`, `test_t24_stub_callbacks.py`.
- Este relatório.

## 6. Pendências que bloqueiam `done` de T24 completo

`ASHURA_addPrim`, `CreateObjectWithTable`, `NewAnimation`, `executeShape` não tocados; alcançabilidade real de `dmyFnc`/`CreateObjectWithTableWithParentData` não investigada.
