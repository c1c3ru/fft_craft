# T23 (fatia vertical) — Renderização: reconstrução C diferencialmente testada de `addlocalprim2`

Depende de T08 e T14 (ambas `ready_for_review`). Executado em 2026-11-02, vigésima fatia vertical de P2.

**Estado: `ready_for_review` (pequena fatia, não `done`).** Fecha mais uma função pequena do cluster de primitivas gráficas PS1/PSX, continuando o trabalho de T23 iniciado com `InitCamera` e o cluster `tagSPRT`.

## 1. Por que esta função

`addlocalprim2(tagPOLY_FT4*)` foi achada por busca de nome no cluster `addlocalprim*`/`POLY_FT4`. 112 B, 0 `bl`, totalmente auto-contida.

## 2. Reconstrução

```c
void addlocalprim2(tagPOLY_FT4* prim) {
    uint32_t oldTag = ctx->otHead[0] | (ctx->otHead[1]<<8) | (ctx->otHead[2]<<16) | (ctx->otHead[3]<<24);
    prim->tagByte0 = (uint8_t)(oldTag);
    prim->tagByte1 = (uint8_t)(oldTag>>8);
    prim->tagByte2 = (uint8_t)(oldTag>>16);
    prim->tagByte3 = (uint8_t)(oldTag>>24);

    uint32_t primAddr = (uint32_t)(uintptr_t)prim;
    ctx->otHead[0] = (uint8_t)(primAddr);
    ctx->otHead[1] = (uint8_t)(primAddr>>8);
    ctx->otHead[2] = (uint8_t)(primAddr>>16);
    ctx->otHead[3] = (uint8_t)(primAddr>>24);
}
```

## 3. Achado: inserção clássica de PS1 na ordering table, byte a byte

Os 4 `ldrb` seguidos de 4 `strb` (em cada direção) são deliberados,
não um artefato de alinhamento. Apesar do parâmetro ser tipado
`tagPOLY_FT4*`, só os primeiros 4 bytes são tocados — o campo `tag`
universal compartilhado por QUALQUER primitiva da GPU do PS1 (link
pra próxima primitiva na ordering table), não algo específico de
`POLY_FT4`. Confirma: `prim->tag = *otHead; *otHead = prim;`
(inserção na cabeça da lista) — o padrão `addPrim` clássico da
PSYQ/libgpu.

## 4. Achado de metodologia

A escrita final (`ctx->otHead` virando o próprio endereço de `prim`)
não é comparável como número bruto entre o lado ELF real (endereço
ARM de 32 bits) e o lado do modelo (endereço `ctypes` do host) — mesmo
tratamento já usado em T08 (`DisposeObject`'s `free_list_head`): cada
lado é verificado contra o próprio endereço de `prim`.

## 5. Teste diferencial

`docs/re-tools/c-models/t23_addlocalprim2.c` + `test_t23_addlocalprim2.py`: 5 cenários (incluindo `oldTag=0`, `0xffffffff`, um valor coincidindo com o próprio endereço de teste) batem exatamente, mais 1 injeção de falha confirmando que os 4 bytes não são trocados de ordem (little-endian preservado).

Suíte completa de `docs/re-tools`: de 612 pra (612 + 2 desta fatia) = **614 testes** (1.946 → **1.951 subtestes**), todos passando — confirmado em 2 execuções consecutivas.

## 6. Arquivos produzidos por esta tarefa

- `docs/REVERSE_ENGINEERING_NOTES.md` — seção 680.
- `docs/RE_FUNCTION_INVENTORY.csv` — `addlocalprim2` promovida a `read_full`.
- `docs/re-tools/c-models/t23_addlocalprim2.c`, `test_t23_addlocalprim2.py`.
- Este relatório.

## 7. Pendências que bloqueiam `done` de T23 completo

Identidade exata do contexto (`ctx`, resolvido via GOT) não confirmada além de "tem um campo em `+0x8` usado como cabeça de OT"; `addlocalprim`/`add_anmpac`/`add_winpac` não lidas; campos reais de `tagPOLY_FT4` além do `tag` universal não tocados por esta função; `GuEmu_libgu_to_gl`, `CEGL2_*`, picking de toque seguem intocados.
