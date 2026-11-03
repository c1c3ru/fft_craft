# T16 (fatia vertical) — Regras de combate: reconstrução C diferencialmente testada de `getFontIDFormBattleWork`

Depende de T08–T10 (todas `ready_for_review`). Executado em 2026-11-02, vigésima sexta fatia vertical de P2.

**Estado: `ready_for_review` (pequena fatia, não `done`).** Fecha uma função pequena do cluster de batalha de T16, com um cruzamento de endereço genuíno pra `BWORK`, já parcialmente documentada em T08. `calc_result`, `getskillrange`, `getskilleffect`, `setskillresult` (os alvos nominais de T16) seguem intocados.

## 1. Por que esta função

`getFontIDFormBattleWork(int)` foi achada por busca de nome no cluster de batalha de T16. 64 B, 0 `bl`, totalmente auto-contida.

## 2. Reconstrução

```c
int32_t getFontIDFormBattleWork(int target) {
    Node* node = g_listHead;             // GOT, dupla indireção padrão
    while (node != NULL) {
        BWORK* bwork = node->bwork;       // +0x134, pode ser NULL
        if (bwork != NULL && bwork->byte_0x1ac == target) {
            return node->fontId;          // +0x5, byte zero-extendido
        }
        node = node->next;                 // +0x0
    }
    return -1;
}
```

## 3. Achado de cruzamento por endereço com T08

Esta função lê `BWORK+0x1ac`, um campo JÁ CONFIRMADO em
`docs/re-baseline/types/bwork.h` (T08, NOTES §653 — "`origByte1ac`
em `set_casting_status`, alimenta `dir` em
`_changeAnimationStatus_`"). Isso confirma independentemente, numa
função totalmente diferente, que `BWORK+0x1ac` é um campo real e
significativo — sem assumir o significado da outra leitura, só
reaproveitando o offset já estabelecido. Não se afirma que o
parâmetro `target` desta função seja literalmente uma "direção" — só
que é comparado contra o mesmo campo já confirmado como tal em outro
contexto.

## 4. Achado estrutural

Percorre uma lista ligada simples global (cabeça resolvida via GOT,
dupla indireção padrão), cada nó com `next` em `+0x0`, `fontId`
(byte) em `+0x5`, e um ponteiro `BWORK*` em `+0x134` — primeira
evidência de campo pra essa struct de nó. Nós com `bwork==NULL` são
pulados sem comparar nada. Se a lista se esgota sem bater, retorna
`-1`.

## 5. Teste diferencial

`docs/re-tools/c-models/t16_getfontidformbattlework.c` + `test_t16_getfontidformbattlework.py`: 5 cenários (nó único, segundo nó bate, nenhum bate, primeiro nó sem `BWORK`, lista vazia) batem exatamente, mais 1 injeção de falha confirmando que nós sem `BWORK` nunca batem.

Suíte completa de `docs/re-tools`: de 626 pra (626 + 2 desta fatia) = **628 testes** (1.968 → **1.973 subtestes**), todos passando — confirmado em 2 execuções consecutivas.

## 6. Arquivos produzidos por esta tarefa

- `docs/REVERSE_ENGINEERING_NOTES.md` — seção 686.
- `docs/RE_FUNCTION_INVENTORY.csv` — `getFontIDFormBattleWork` promovida a `read_full`.
- `docs/re-tools/c-models/t16_getfontidformbattlework.c`, `test_t16_getfontidformbattlework.py`.
- Este relatório.

## 7. Pendências que bloqueiam `done` de T16 completo

`calc_result`, `getskillrange`, `getskilleffect`, `setskillresult` (2,7–3,8 KB cada) não tocadas — a fórmula de combate real segue fechada; nome/sizeof real da struct de nó não conhecido; identidade exata de `target`/`fontId` não confirmada além do cruzamento com `BWORK+0x1ac`.
