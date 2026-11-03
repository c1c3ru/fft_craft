# T23 (fatia vertical) — Renderização: reconstrução C diferencialmente testada de `Winitsprt`

Depende de T08 e T14 (ambas `ready_for_review`). Executado em 2026-11-02, vigésima terceira fatia vertical de P2.

**Estado: `ready_for_review` (pequena fatia, não `done`).** Continua o cluster `tagSPRT` fechado na fatia anterior (`initsprt` + 5 setters), agora com a variante `Winitsprt`.

## 1. Por que esta função

`Winitsprt(tagSPRT*)` foi achada por busca de nome no mesmo cluster `tagSPRT` de `initsprt`. Mesma assinatura, mesmo tamanho (100 B), mesmos dois `bl` (`SetSprt`, `SetShadeTex`) e mesma tail call final (`SetSemiTrans`) — um candidato natural pra comparar diretamente com `initsprt`.

## 2. Reconstrução

```c
void Winitsprt(tagSPRT* sprt) {
    SetSprt(sprt);
    SetShadeTex(sprt, 0);   // única diferença de initsprt: 0, não 1
    sprt->field_0x8 = sprt->field_0x9 = sprt->field_0xa = 0x80;
    sprt->field_0x10 = sprt->field_0x11 = 0;
    sprt->field_0xc  = 0x200;
    sprt->field_0x12 = 0x7c3c;
    sprt->field_0x14 = sprt->field_0x16 = sprt->field_0xe = 0;
    SetSemiTrans(sprt, 1);   // TAIL CALL, idêntica à de initsprt
}
```

## 3. Achado: diferença de um único argumento, confirmada por diff de disassembly

`Winitsprt` é byte-idêntica a `initsprt` em toda a estrutura, com
**uma única diferença**: `SetShadeTex(sprt, 0)` em vez de
`SetShadeTex(sprt, 1)`. Isso foi confirmado por diff de disassembly
instrução a instrução (`mov r1,#0` vs. `mov r1,#1`), não assumido
pela convenção de nome "W" — o prefixo não implica automaticamente
uma variante menor/diferente sem verificação.

## 4. Teste diferencial

Reaproveita `docs/re-tools/c-models/t23_initsprt.c`: fatorado num
helper comum `initsprt_common` parametrizado pela flag de
`SetShadeTex`, sem alterar o comportamento já testado de
`initsprt_model`. `test_t23_winitsprt.py`: confirma ordem e
argumentos exatos das 3 chamadas (incluindo a flag `0`), mais 1
injeção de falha confirmando que a flag não é `1` (não é uma cópia
desatenta de `initsprt`).

Suíte completa de `docs/re-tools`: de 618 pra (618 + 2 desta fatia) = **620 testes** (1.954 subtestes, sem novos), todos passando — confirmado em 2 execuções consecutivas.

## 5. Arquivos produzidos por esta tarefa

- `docs/REVERSE_ENGINEERING_NOTES.md` — seção 683.
- `docs/RE_FUNCTION_INVENTORY.csv` — `Winitsprt` promovida a `read_full`.
- `docs/re-tools/c-models/t23_initsprt.c` (estendido com `Winitsprt_model`), `test_t23_winitsprt.py`.
- Este relatório.

## 6. Pendências que bloqueiam `done` de T23 completo

Nenhuma nova além das já registradas pra `initsprt`/`SetSprt`/`SetShadeTex`/`SetSemiTrans` (fatia anterior); `GuEmu_libgu_to_gl`, `CEGL2_*`, picking de toque seguem intocados.
