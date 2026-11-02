# T08 (fatia vertical) — Recuperação de tipos: primeira evidência de campo para `_Object`

Depende de T04 (`ready_for_review`). Executado em 2026-11-02, décima sétima fatia vertical de P2.

**Estado: `ready_for_review` (pequena fatia, não `done`).** Esta tarefa fecha o quarto e ÚLTIMO dos tipos que T08 (2026-10-31) listou como "sem nenhuma evidência de campo confiável" (`_Object`, `ActionRequest`, `FFT_SAVE_DATA`, `CARD_HEADER`) — os outros três já foram fechados nas duas fatias anteriores desta sessão. `CARD_HEADER` continua sem evidência.

## 1. Por que esta função

`DisposeObject(short, _Object*)` foi achada por busca de nome pelo tipo `_Object*`. Tem 196 B e 2 `bl` — moderada, mas o valor (4 campos de `_Object` de uma vez, mais 2 campos de uma struct de tabela associada) justificou a leitura completa nesta fatia.

## 2. Reconstrução

```c
void DisposeObject(int16_t tableId, _Object* obj) {
    ObjTableEntry* entry = &g_objTable[tableId];   // stride 0xf8, base já confirmado em outra seção

    if (obj->next != NULL) {
        obj->next->prev = obj->prev;
    }
    if (obj->prev != NULL) {
        obj->prev->next = obj->next;
    } else {
        entry->headPtr = obj->next;   // obj ERA a cabeça da lista do slot
    }

    int16_t category = obj->categoryFlags & 0xf000;
    entry->liveCount -= 1;

    if (category == 0x4000) {
        Free(obj->payload);
    } else if (category == 0 || category == 0x1000 || category == 0x2000 || category == 0x3000) {
        DisposeEffectAnimation(obj->payload);
    }
    // qualquer outra categoria: nem Free nem DisposeEffectAnimation são chamadas

    g_liveObjCount -= 1;
    obj->next = g_freeListHead;   // reaproveita o campo `next` como link da free-list
    g_freeListHead = obj;
}
```

## 3. Achado: lista duplamente encadeada intrusiva, 4 campos de `_Object` confirmados de uma vez

`+0x00` = `prev`, `+0x04` = `next` (dentro da lista do slot da
tabela; reaproveitado depois como link da free-list global), `+0x4c`
= `categoryFlags` (int16, nibble alto seleciona o caminho de
descarte), `+0x54` = `payload` (ponteiro opaco, repassado pra
`Free()` ou `DisposeEffectAnimation()` conforme a categoria). Ver
[`types/_object.h`](types/_object.h).

Também dá a primeira evidência de 2 campos da entrada da tabela de
objetos por slot (stride `0xf8`, base já confirmado em outra seção):
`+0x1c` = contador de objetos vivos do slot (decrementado), `+0xd0` =
ponteiro de cabeça de lista do slot (só escrito quando o objeto
descartado não tinha `prev`).

## 4. Teste diferencial

`docs/re-tools/c-models/t08_disposeobject.c` + `test_t08_disposeobject.py`: `next`/`prev` passados ao modelo como ponteiros nativos já resolvidos (mesmo recurso de largura de ponteiro de T14/T21/T25). 6 cenários cobrem as 5 categorias cruzadas com presença/ausência de `next`/`prev`, todos batendo exatamente — inclusive a decisão de `g_freeListHead` virar o próprio `obj`, verificada contra o próprio espaço de endereço de cada lado (não por igualdade numérica cross-side, já que um endereço ARM de 32 bits e um endereço `ctypes` do host de 64 bits não são comparáveis bit a bit). Mais 2 injeções de falha: a escrita da cabeça de lista depende de `prev` ausente, não de `next`; e o valor de `obj->next` propaga corretamente pra `prev->next` mesmo quando `next` em si está ausente.

Suíte completa de `docs/re-tools`: de 602 pra (602 + 2 desta fatia) = **604 testes** (1.923 → **1.929 subtestes**), todos passando — confirmado em 2 execuções consecutivas.

## 5. Arquivos produzidos por esta tarefa

- `docs/REVERSE_ENGINEERING_NOTES.md` — seção 677.
- `docs/RE_FUNCTION_INVENTORY.csv` — `DisposeObject` promovida a `read_full`.
- `docs/re-baseline/types/_object.h` — primeiro header do tipo, verificado por `static_assert`/`offsetof`.
- `docs/re-tools/c-models/t08_disposeobject.c`, `test_t08_disposeobject.py`.
- Este relatório.

## 6. Pendências que bloqueiam `done` de T08 completo

`CARD_HEADER` segue sem nenhuma evidência de campo (único dos quatro tipos ainda não fechado); `Free()`/`DisposeEffectAnimation()` não lidas; `sizeof(_Object)` completo não conhecido; nome exato de `categoryFlags`/`payload` não afirmado além do que os bytes mostram.
