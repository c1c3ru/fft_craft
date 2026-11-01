# T21 (fatia vertical) — Texto e janelas: reconstrução C diferencialmente testada de `pagenext_cursor(PAGEWININFO*)`

Depende de T08 e T20 (ambas `ready_for_review`). Executado em 2026-11-01, nona fatia vertical de P2.

**Estado: `ready_for_review` (fatia pequena, não `done`).** T21 completo exige fechar `mesputmain`, `Wmesputmain` e as variantes de janela com prefixos A/C/D/E/W — nenhuma tocada aqui. Esta tarefa fecha uma função pequena já citada por nome (mas nunca lida) no framework `PAGEWININFO` já documentado na seção 381 das notas.

## 1. Por que esta função

Os alvos nominais de T21 continuam grandes. O framework `PAGEWININFO` (janela paginada genérica, seção 381) já cita `pagenext_cursor`/`pageupdown_cursor` por nome como callees de `pagewin_main` ("navegação de página"), mas nenhuma das duas tinha sido lida individualmente. `pagenext_cursor` (88 B, 0 `bl`) é a mais simples das duas.

## 2. Reconstrução

```c
void pagenext_cursor(PAGEWININFO* info) {
    uint32_t* entry = &g_cursorFlags[info->field_0x38];   // array real, stride 0x24
    if (info->field_0x54 >= info->field_0x50) {            // curPage >= maxPage: última página
        *entry |= 0x10;
    } else {
        *entry &= ~0x10;
    }
}
```

Os três campos de `PAGEWININFO` que esta função toca (`+0x38` índice, `+0x50` "página máxima", `+0x54` "página atual") são lidos diretamente dos bytes; `PAGEWININFO` ainda não tem um header de struct consolidado (não é um dos tipos priorizados em T08), então estes offsets não herdam confirmação de nenhuma outra fonte. O limite é confirmado **inclusivo** (`curPage >= maxPage`) por execução real com igualdade exata, não assumido pela leitura do mnemônico `bge`/`blt`.

## 3. Achado: mesmo array global nos dois ramos, confirmado por endereço

Os dois ramos da função (ainda há próxima página / já é a última) leem,
via cadeias GOT independentes, o **mesmo** slot (`0x3479a4`) resolvendo
pro **mesmo** array global (base `0x67e390`, stride `0x24`=36 B,
indexado por `info->field_0x38`). Confirmado calculando os dois ramos
separadamente e comparando o endereço final, não assumido pela
semelhança do padrão de instruções. Só os primeiros 4 bytes de cada
entrada (um campo de flags de 32 bits) são tocados; os outros 32 bytes
permanecem opacos a esta leitura.

## 4. Teste diferencial

`docs/re-tools/c-models/t21_pagenext_cursor.c` + `test_t21_pagenext_cursor.py`: sem `bl` pra stubar — a única indireção é o array global, passado ao modelo como ponteiro nativo já resolvido (mesmo recurso de T14/T25, pela mesma razão de largura de ponteiro host×ARM). 4 cenários batem exatamente com o ELF original: não-última-página com a flag já setada (precisa limpar), última página por igualdade exata, última página por excesso, e não-última-página preservando outros bits do campo de flags.

Mais 2 injeções de falha: uma confirma que os outros bits do campo de flags sobrevivem à operação (não é uma atribuição direta `=0x10`/`=0`, é `|=`/`&= ~`); outra confirma que o limite é inclusivo (`curPage == maxPage` já conta como última página).

Suíte completa de `docs/re-tools`: de 578 pra (578 + 3 desta fatia) = **581 testes** (1.867 → **1.871 subtestes**), todos passando — confirmado em 2 execuções consecutivas.

## 5. Arquivos produzidos por esta tarefa

- `docs/REVERSE_ENGINEERING_NOTES.md` — seção 669.
- `docs/RE_FUNCTION_INVENTORY.csv` — `pagenext_cursor` promovida a `read_full`.
- `docs/re-tools/c-models/t21_pagenext_cursor.c`, `test_t21_pagenext_cursor.py`.
- Este relatório.

## 6. Pendências que bloqueiam `done` de T21 completo

`mesputmain`, `Wmesputmain` e variantes A/C/D/E/W não tocadas; `PAGEWININFO` ainda sem header de struct consolidado (campos confirmados só para esta função); `pageupdown_cursor` (citada junto na seção 381, mesmo framework) não lida.
