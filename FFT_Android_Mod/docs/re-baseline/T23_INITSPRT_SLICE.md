# T23 (fatia vertical) — Renderização: reconstrução C diferencialmente testada do cluster `tagSPRT`

Depende de T08 e T14 (ambas `ready_for_review`). Executado em 2026-11-02, décima nona fatia vertical de P2.

**Estado: `ready_for_review` (pequena fatia, não `done`).** Esta tarefa fecha 6 funções do cluster de sprites PS1/PSX (`tagSPRT*`), dando a primeira evidência de campo para esse tipo. Os alvos nominais de T23 (`GuEmu_libgu_to_gl`, `CEGL2_*`, picking de toque) seguem intocados.

## 1. Por que este grupo

`initsprt(tagSPRT*)` chama/desvia pras outras cinco funções do mesmo cluster (`SetSprt`, `SetSprt8`, `SetSprt16`, `SetSemiTrans`, `SetShadeTex`) — todas pequenas (24–100 B, 0–2 `bl`), achadas por busca de nome. Fechar o grupo inteiro de uma vez dá uma confirmação cruzada natural (as funções de flag tocam exatamente o mesmo offset que as de inicialização escrevem).

## 2. Reconstrução

```c
void SetSprt(tagSPRT* s)   { s->field_0x4=4; s->field_0xb=0x64; s->field_0x5=s->field_0x6=s->field_0x7=0; }
void SetSprt16(tagSPRT* s) { s->field_0x4=3; s->field_0xb=0x7c; s->field_0x5=s->field_0x6=s->field_0x7=0; }
void SetSprt8(tagSPRT* s)  { s->field_0x4=3; s->field_0xb=0x74; s->field_0x5=s->field_0x6=s->field_0x7=0; }

void SetSemiTrans(tagSPRT* s, int flag) {
    if (flag) s->field_0xb |= 2; else s->field_0xb &= ~2;
}
void SetShadeTex(tagSPRT* s, int flag) {
    if (flag) s->field_0xb |= 1; else s->field_0xb &= ~1;
}

void initsprt(tagSPRT* s) {
    SetSprt(s);
    SetShadeTex(s, 1);
    s->field_0x8 = s->field_0x9 = s->field_0xa = 0x80;   // RGB cinza médio
    s->field_0x10 = s->field_0x11 = 0;
    s->field_0xc  = 0x200;
    s->field_0x12 = 0x7c3c;
    s->field_0x14 = s->field_0x16 = s->field_0xe = 0;
    SetSemiTrans(s, 1);   // TAIL CALL
}
```

## 3. Achado: `+0xb` é o byte de código de primitiva GPU estilo PS1

`SetSprt`/`SetSprt8`/`SetSprt16` escrevem `+0xb` com um valor base
fixo (`0x64`/`0x74`/`0x7c`, bits baixos já zerados); `SetSemiTrans`/
`SetShadeTex` leem-modificam-escrevem O MESMO `+0xb` via `|=`/`&=~`
nos bits 1/0. Confirmado por endereço (ambas as funções de flag
tocam exatamente o offset que as três de inicialização escrevem) —
não por semelhança com a convenção de hardware real. Ver
[`types/tagsprt.h`](types/tagsprt.h).

## 4. Achado secundário: sétima tail call desta sessão

`initsprt` termina com um `b` direto pra `SetSemiTrans(s, 1)`, não
`bl` — mais uma confirmação do padrão já visto em T20/T23/T17/T08.

## 5. Teste diferencial

`docs/re-tools/c-models/t23_sprt_setters.c` + `test_t23_sprt_setters.py`: 5 funções testadas com variações de valor inicial e flag, mais injeção de falha confirmando que só o bit próprio é tocado (nunca o byte inteiro nem outro offset).

`docs/re-tools/c-models/t23_initsprt.c` + `test_t23_initsprt.py`: `SetSprt`/`SetShadeTex`/`SetSemiTrans` stubadas, confirma ordem e argumentos exatos das 3 chamadas, mais os campos escritos diretamente.

Suíte completa de `docs/re-tools`: de 607 pra (607 + 5 desta fatia) = **612 testes** (1.933 → **1.946 subtestes**), todos passando — confirmado em 2 execuções consecutivas.

## 6. Arquivos produzidos por esta tarefa

- `docs/REVERSE_ENGINEERING_NOTES.md` — seção 679.
- `docs/RE_FUNCTION_INVENTORY.csv` — as 6 funções promovidas a `read_full`.
- `docs/re-baseline/types/tagsprt.h` — primeiro header do tipo, verificado por `static_assert`/`offsetof`.
- `docs/re-tools/c-models/t23_sprt_setters.c`, `test_t23_sprt_setters.py`.
- `docs/re-tools/c-models/t23_initsprt.c`, `test_t23_initsprt.py`.
- Este relatório.

## 7. Pendências que bloqueiam `done` de T23 completo

`GuEmu_libgu_to_gl`, `CEGL2_*`, buffers, blending, clipping, picking de toque não tocados; identidade semântica exata dos demais campos de `tagSPRT` (`+0x4`, RGB, coordenadas/dimensões) não confirmada além do que os bytes mostram; `sizeof(tagSPRT)` não conhecido além de `0x18`.
