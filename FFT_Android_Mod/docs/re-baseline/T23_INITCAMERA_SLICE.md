# T23 (fatia vertical) — Renderização e câmera: reconstrução C diferencialmente testada de `InitCamera()`

Depende de T08 e T14 (ambas `ready_for_review`). Executado em 2026-11-01, décima fatia vertical de P2.

**Estado: `ready_for_review` (fatia pequena, não `done`).** T23 completo exige fechar `GuEmu_libgu_to_gl`, `CEGL2_*`, buffers, blending, câmera completa e picking de toque — nenhum tocado aqui. Esta tarefa fecha uma função pequena e nominalmente relacionada a "câmera", achada por busca literal no cluster.

## 1. Por que esta função

`InitCamera()` (40 B, 0 `bl`) foi achada por busca de nome literal no cluster de câmera/renderização de T23. É minúscula e se resolve inteiramente em duas coisas: zerar 5 campos de um struct global e desviar (tail call) para outra função já catalogada.

## 2. Reconstrução

```c
void InitCamera(void) {
    g_camera->field_0xa0 = 0;
    g_camera->field_0xa4 = 0;
    g_camera->field_0xa8 = 0;
    g_camera->field_0xac = 0;
    g_camera->field_0xb0 = 0;
    SetDefaultCamera();   // *** TAIL CALL: `b`, não `bl` ***
}
```

## 3. Achado: segunda tail call real desta sessão, confirmada por endereço exato

`InitCamera` não tem prólogo (0 `push`) e termina num `b` incondicional
direto pra `0x218cf4` — não é uma suposição de "branch pra trás =
loop" (heurística que `jtable.py` aplica e que esta função também
dispara, da mesma forma que T20). O endereço de destino é **exatamente**
o início de `SetDefaultCamera()` (`0x218cf4`, 216 B, já catalogada):
`0x218cf4 + 216 = 0x218dcc`, o próprio endereço de `InitCamera`. As
duas funções são vizinhas contíguas no `.text`.

`g_camera` (`0x60593c`) é resolvido por um literal PC-relative direto, sem indireção via GOT — consistente com um dado local/estático que não precisa suportar interposição em tempo de execução (diferente dos globais de T14/T21, que usavam a cadeia GOT completa). Só os 5 campos (`+0xa0`–`+0xb0`) que esta função realmente escreve foram confirmados.

## 4. Teste diferencial

`docs/re-tools/c-models/t23_initcamera.c` + `test_t23_initcamera.py`: `SetDefaultCamera` tratada como caixa-preta via `stub_calls`, mesmo tratamento de tail-call-como-stub validado em T20. Diferente de um ELF sintético, o endereço de destino não precisa de página vazia extra mapeada (cai dentro do mesmo `.text` real já mapeado pelo harness — mesma lição de metodologia de T14).

Confirma que os 5 campos são zerados, que nenhum outro byte da struct é tocado (testado 1 byte antes do primeiro campo e 1 byte depois do último, com valores sentinela distintos byte a byte), e que a tail call é alcançada exatamente uma vez em cada lado.

Suíte completa de `docs/re-tools`: de 581 pra (581 + 2 desta fatia) = **583 testes** (1.871 subtestes — sem subtestes novos, os 2 testes desta fatia não usam `subTest`), todos passando — confirmado em 2 execuções consecutivas.

## 5. Arquivos produzidos por esta tarefa

- `docs/REVERSE_ENGINEERING_NOTES.md` — seção 670.
- `docs/RE_FUNCTION_INVENTORY.csv` — `InitCamera` promovida a `read_full`.
- `docs/re-tools/c-models/t23_initcamera.c`, `test_t23_initcamera.py`.
- Este relatório.

## 6. Pendências que bloqueiam `done` de T23 completo

`GuEmu_libgu_to_gl`, `CEGL2_*`, buffers, ordenação, blending, textura/CLUT, clipping e picking de toque não tocados; `SetDefaultCamera()` (98% estrutural, 3 `bl` — `getMapScrollXYZ`/`getMapScale`/`getMapAngle`) não lida; identidade semântica dos 5 campos e `sizeof` completo de `g_camera` não confirmados.
