# T14 (fatia vertical) — Boot e ciclo principal: reconstrução C diferencialmente testada de `Boot_FrameMove()`

Depende de T08–T10 (todas `ready_for_review`). Executado em 2026-11-01, oitava fatia vertical de P2.

**Estado: `ready_for_review` (fatia pequena, não `done`).** T14 completo exige fechar `Boot_Init` (já `read_full`, seção 650), `Main_Init`, `Main_FrameMove`, `Main_FrameRender` — os três últimos (300 B+ cada) não tocados aqui. Esta tarefa fecha o par `FrameMove` de `Boot_Init` e, no processo, cruza por endereço (não por nome) um global compartilhado entre as duas funções.

## 1. Por que esta função

Os alvos nominais de T14 continuam grandes. `Boot_FrameMove` (`0x2b3590`, 128 B, `read_structural` desde um lote em massa, NOTES §615) é o par natural de `Boot_Init` (já `read_full`), pequeno o bastante pra reconstrução completa nesta fatia.

## 2. Reconstrução

```c
int32_t Boot_FrameMove(void) {
    if (*g_bootFlag != 0) {
        return 0;
    }
    int32_t syncResult = CTHREAD::Sync(g_bootThread);
    if (syncResult != 0) {
        if (syncResult == 1) return -1;
        return 0;
    }
    CEGL2_IF::ClearBackdrop(g_glIf, 0.0f, 0.0f, 0.0f);
    onGotoNextMode(3);   // 3 = Logo, confirmado NOTES §640
    return 1;
}
```

## 3. Achado: mesmo global de `Boot_Init`, confirmado por endereço

A primeira guarda de `Boot_FrameMove` lê, via cadeia GOT (literal pool
→ slot GOT → endereço do global → valor), o endereço `.bss`
`0x19db208` (slot GOT `0x347cb4`). Resolvendo a MESMA cadeia dentro de
`Boot_Init` (que cacheia a base do GOT no registrador `r7` no próprio
prólogo, uma otimização que `Boot_FrameMove` não usa — cada acesso é
resolvido via `pc` direto), a instrução `*g_someBootFlag = 0` da
seção 650 resolve pro **mesmo** slot GOT (`0x347cb4`) e pro **mesmo**
endereço (`0x19db208`). Confirmado calculando os dois lados byte a
byte (immediate de cada `ldr`, não inferido por posição ou nome) — ver
seção 668 das notas pro cálculo completo.

**Nome do campo não inventado**: os dois usos observados (zerado por
`Boot_Init` no caminho assíncrono; guarda de "pronto pra continuar" em
`Boot_FrameMove`) são consistentes com um flag de "ainda carregando",
mas como o BSS já começa zerado por padrão e o caminho síncrono
(arquivo aberto de cara) nunca toca essa variável, a hipótese não está
confirmada o bastante pra virar nome oficial — mantido como
`g_bootFlag`, rótulo de conveniência. Os outros dois globais
(`g_bootThread`, cacheia o `CTHREAD*`; `g_glIf`, cacheia o
`CEGL2_IF*`) não foram cruzados contra nenhuma outra função nesta
sessão.

## 4. Teste diferencial

`docs/re-tools/c-models/t14_boot_framemove.c` + `test_t14_boot_framemove.py`: os 3 globais (`g_bootFlag`, `g_bootThread`, `g_glIf`) são passados ao modelo já resolvidos — mesmo recurso de largura de ponteiro de T24/T25 (host 64 bits vs. valor real de 32 bits), já que a cadeia GOT→valor é boilerplate PIC genérico, não lógica desta função. `CTHREAD::Sync`/`CEGL2_IF::ClearBackdrop`/`onGotoNextMode` são stubados via `callable` nos dois lados; os stubs do lado ELF real gravam os registradores observados na própria chamada, confirmando os argumentos exatos (`ClearBackdrop(this, 0.0f, 0.0f, 0.0f)`, `onGotoNextMode(3)`), não só que alguma chamada ocorreu.

4 cenários batem exatamente: saída antecipada (`g_bootFlag != 0`), sync "ainda rodando" (resultado nem 0 nem 1), sync erro (`== 1`), sync sucesso (`== 0`, dispara as duas chamadas finais e retorna 1). Mais 1 injeção de falha confirmando que um resultado de sync fora de `{0,1}` retorna `0`, não `-1` como uma simplificação ingênua ("qualquer coisa não-zero é erro") assumiria.

Suíte completa de `docs/re-tools`: de 576 pra (576 + 2 desta fatia) = **578 testes** (1.863 → **1.867 subtestes**), todos passando — confirmado em 2 execuções consecutivas (uma execução anterior da sessão, de outra fatia, teve uma falha isolada não reproduzível descartada por reexecução; esta fatia em si passou de primeira após o ajuste de mapeamento descrito na seção 5).

## 5. Achado de metodologia: endereços reais dentro do mesmo `.text` não precisam de página vazia extra

A primeira versão do teste mapeava páginas vazias explícitas nos três
endereços de `bl` reais (`CTHREAD::Sync`, `ClearBackdrop`,
`onGotoNextMode`) — o mesmo cuidado documentado no módulo do harness
pra ELFs sintéticos. Isso falhou com `UC_ERR_MAP` ("mapeamento
inválido"): diferente de um ELF sintético pequeno, esses três
endereços já caem dentro da MESMA seção `.text` real e gigante que
contém `Boot_FrameMove`, que o harness já mapeia por inteiro (por
`.text` se sobrepor ao intervalo `[start,end)` do alvo) — mapear de
novo colide com o mapeamento existente. Corrigido removendo as
páginas vazias extras; a peculiaridade do Unicorn documentada no
harness só se aplica quando o endereço de destino está **fora** de
qualquer seção já mapeada.

## 6. Arquivos produzidos por esta tarefa

- `docs/REVERSE_ENGINEERING_NOTES.md` — seção 668.
- `docs/RE_FUNCTION_INVENTORY.csv` — `Boot_FrameMove` promovida a `read_full`.
- `docs/re-tools/c-models/t14_boot_framemove.c`, `test_t14_boot_framemove.py`.
- Este relatório.

## 7. Pendências que bloqueiam `done` de T14 completo

`Main_Init`, `Main_FrameMove`, `Main_FrameRender` não tocadas; `CTHREAD::Sync`, `CEGL2_IF::ClearBackdrop` e `onGotoNextMode` tratadas como caixa-preta; identidade semântica de `g_bootFlag`/`g_bootThread`/`g_glIf` não confirmada além do cruzamento de endereço com `Boot_Init`; transições externas/internas de boot completo (settings, pausa) não revisitadas.
