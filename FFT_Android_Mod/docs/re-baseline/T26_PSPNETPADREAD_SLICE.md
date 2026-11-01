# T26 (fatia vertical) — Integrações legadas: reconstrução C diferencialmente testada de `pspNetPadRead()`

Depende de T08–T10 (feitas). Executado em 2026-11-01, terceira fatia vertical de P2.

**Estado: `ready_for_review` (fatia pequena, não `done`).** T26 completo exige mapear toda a família `pspNet*`/`iCloud_*`/`NetBattleJudge` e distinguir caminhos ativos de herdados. Esta tarefa fecha e reconstrói uma função do cluster, com um achado central: o nome não corresponde à função real.

## 1. Por que esta função

A maioria das funções `pspNet*` já é `read_full` e trivial (BX LR de 4-8 bytes, cobertas pelo lote de certificação de T11). `pspNetPadRead` (140 B, `mentioned_unverified`) era a maior ainda não lida do cluster e pequena o bastante para reconstrução real.

## 2. Achado central: "`pspNet`" não significa rede aqui

Leitura completa (`NOTES §663`) mostra que `pspNetPadRead()` **combina dois buffers de estado de botões, aplica uma máscara de desabilitação de um-tiro e sobrepõe uma leitura de modo tutorial** — nenhuma chamada de rede, nenhum pacote, nenhum estado compartilhado entre jogadores. Confirma a cautela já registrada na própria T26: "símbolo de rede isolado não vira afirmação de funcionalidade ativa." O prefixo `pspNet` aqui é resíduo de nomenclatura herdada do módulo de rede original (provavelmente porque a leitura combinada de pad é consumida também pelo código de sincronização de rede em batalhas online), não evidência de que esta função específica faz algo de rede.

```c
uint32_t pspNetPadRead(void) {
    void** ptrSlot0 = xpPadKeyBufGet(0);
    void** ptrSlot1 = xpPadKeyBufGet(1);
    uint8_t* buf0 = *ptrSlot0;   // dupla indireção
    uint8_t* buf1 = *ptrSlot1;
    uint16_t v0 = buf0[3] | (buf0[2] << 8);
    uint16_t v1 = buf1[3] | (buf1[2] << 8);
    uint32_t combined = v0 | (v1 << 16);
    combined &= ~g_padMask;
    g_padMask = 0;
    int tutorialActive = iOSTutoCheck();
    combined = ~combined;
    if (!tutorialActive) return combined;
    if (iOS_getTutorialPad() != 0) combined |= iOS_getTutorialPad();
    return combined;
}
```

## 3. A primeira tentativa de teste falhou — e isso revelou a dupla indireção real

A primeira configuração do teste diferencial supôs que `xpPadKeyBufGet(n)` retorna o buffer de botões diretamente. Rodar contra o ELF real deu **falha imediata de acesso a memória não mapeada**. Em vez de contornar isso ajustando o teste, investiguei a causa: o disassembly mostra `ldr r1,[r0]` logo após a chamada — uma desreferência extra. `xpPadKeyBufGet` retorna o **endereço de uma variável-ponteiro** (dupla indireção, provavelmente porque o buffer real alterna de slot a cada frame). Corrigido, a execução passou a funcionar e bater exatamente com a aritmética esperada.

## 4. Extensão do harness: `stub_calls` aceita `callable(uc) -> int`

`pspNetPadRead` chama `xpPadKeyBufGet` duas vezes com argumentos diferentes (`0`, depois `1`) e precisa de retornos diferentes por chamada — o mecanismo anterior de T10 só suportava um valor fixo por endereço. `docs/re-tools/differential_harness.py` agora aceita, em `stub_calls`, um `callable` que recebe a engine `Uc` (podendo ler `r0` da chamada real) além do `int` fixo anterior — mudança retrocompatível, confirmada pela suíte completa sem regressão. `test_differential_harness_stub_callable.py` (2 testes novos) cobre o caso fixo (ainda funciona) e o caso `callable` (vê o `r0` real de cada chamada).

## 5. Reconstrução C + teste diferencial

`docs/re-tools/c-models/t26_pspnetpadread.c` + `test_t26_pspnetpadread.py`: compila o modelo, executa a implementação original real via `differential_harness.py` para 6 cenários (sem tutorial; tutorial com pad zero; tutorial com bit de pad setado; máscara não-zero; buffers zerados; máscara `0xffffffff`) — **tudo bate exatamente**. Mais um teste de injeção de falha confirmando que a interpretação "sem dupla indireção" (o erro original) produziria um resultado diferente do ELF real, não coincidentemente igual.

Suíte completa de `docs/re-tools`: **561 testes / 1.846 subtestes, todos passando** (557 antes + 2 da extensão do harness + 2 desta fatia).

## 6. O que isso prova e o que não prova

**Prova**: para os 6 cenários testados, o modelo C reproduz exatamente o valor de retorno do binário ARM original, incluindo a máscara de um-tiro e a sobreposição de tutorial.

**Não prova**: `xpPadKeyBufGet` em si (caixa-preta); quem define `g_padMask` antes desta função rodar; se esta função é realmente chamada em contexto de rede em algum lugar do código (não investigado — só a função em si, não seus chamadores).

## 7. Arquivos produzidos por esta tarefa

- `docs/REVERSE_ENGINEERING_NOTES.md` — seção 663.
- `docs/RE_FUNCTION_INVENTORY.csv` — `pspNetPadRead` promovida a `read_full`.
- `docs/re-tools/differential_harness.py` — `stub_calls` aceita `callable`.
- `docs/re-tools/test_differential_harness_stub_callable.py` — 2 testes de regressão da extensão.
- `docs/re-tools/c-models/t26_pspnetpadread.c`, `test_t26_pspnetpadread.py`.
- Este relatório.
