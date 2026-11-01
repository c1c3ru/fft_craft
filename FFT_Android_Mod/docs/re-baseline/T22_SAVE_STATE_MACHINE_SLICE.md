# T22 (fatia vertical) — Persistência: reconstrução C diferencialmente testada de `pspFftSave`/`pspFftDelete`

Depende de T08–T10 (feitas) e T13 (feita). Executado em 2026-10-31/2026-11-01, como a "fatia vertical pequena de P2" escolhida nesta sessão.

**Estado: `ready_for_review` (fatia pequena, não `done`).** T22 completo exige fechar também `CardAccess`, `BattleCardAccess` (11–16 KB cada, não tocadas) e a família `iOS_RESUME_*` (vários KB cada, não tocada). Esta tarefa fecha só o par `pspFftSave`/`pspFftDelete` — a parte do escopo que já estava `read_full` e pequena o suficiente para uma reconstrução real e testada nesta sessão — e corrige dois erros reais encontrados no processo.

## 1. Por que esta fatia, não `CardAccess`/`iOS_RESUME_*`

Levantamento de todos os endereços citados nominalmente em T14–T26 do backlog (`docs/RE_COMPLETUDE_TASKS.md`) contra o CSV mostrou um padrão consistente: cada função citada está `read_full` e pequena (<600 B, já fechada) **ou** `read_structural` e enorme (6–16 KB, não tocada) — não há meio-termo "quase fechado". `pspFftSave` (288 B) e `pspFftDelete` (320 B) eram os dois já fechados e pequenos o bastante para reconstrução real nesta sessão; `Savedata_Load` (384 B) também estava fechada mas revelou um erro de leitura (seção 2) que a tirou de escopo pra reconstrução nesta passada.

## 2. Correção: `Savedata_Load` não tem "corrida de sequência" — é o epílogo padrão de stack canary

Releitura completa de `Savedata_Load` (`0x27fe84`, `NOTES §647`) mostrou que o "`bl` final sem retorno visível" que a seção original atribuiu a uma lógica de negócio de "contador de sequência" é, na verdade, o **epílogo clássico de stack canary** do GCC (`__stack_chk_guard` salvo no prólogo, comparado no epílogo, `bl __stack_chk_fail` — `0x715cc`, já confirmado como esse PLT stub em T09 — se divergir). Documentado em `NOTES §660`. Não é lógica do jogo; não há mais nenhum callee desconhecido nesse ponto, mas a seção 647 segue com uma lacuna real não resolvida nesta tarefa: a polaridade exata de `CFILE::Open` e o fluxo completo de sucesso/falha do resto da função não foram refeitos.

## 3. Correção verificada por execução real: `pspFftDelete` muda de estado na mesma chamada (`NOTES §661`)

A leitura original de `pspFftDelete` (`NOTES §641`) afirmava que, no estado 1, "o estado NÃO muda — continua 1 até a próxima chamada cair em state==2", e descrevia um `g_otherFlag` separado de `g_fftSaveState`. **Isso estava errado**, confirmado por execução real sob Unicorn (`differential_harness.py`, T10) contra os bytes originais — não só releitura manual:

- `g_fftSaveState` (`0xbab940`) é **realmente compartilhado** entre `pspFftSave` e `pspFftDelete` (confirmado).
- Cada função tem seu **próprio** slot de valor cacheado: `pspFftSave` em `0xbd3308`, `pspFftDelete` em `0xbd5e50` — endereços diferentes, não compartilhados (contrariando a hipótese inicial de que fosse um único `g_cachedArg`).
- No estado 1, `pspFftDelete` muda `g_fftSaveState` para `2` **na mesma chamada** em quase todos os casos (não existe `g_otherFlag`; era o próprio estado sendo escrito por uma segunda via de resolução de GOT). Só o caso `idx==13` (`result==0`) realmente deixa o estado em 1.
- `pspFftSave`, em contraste, **sempre** volta o estado pra `0` após processar o estado 1, qualquer que seja o resultado — comportamento genuinamente diferente do de `pspFftDelete`, apesar de ambos compartilharem o mesmo trio externo `xpLibapiSave{Start,Check,End}`.

## 4. Reconstrução: C compilável + teste diferencial contra o ELF original

`docs/re-tools/c-models/t22_fft_save_state_machine.c`: duas funções C (`pspFftSave_model`, `pspFftDelete_model`), cada uma refletindo o comportamento **real e corrigido** de sua contraparte ARM — não uma abstração compartilhada forçada (a primeira versão deste arquivo tentou unificar as duas num só helper e foi descartada ao notar, pela execução real, que os comportamentos de estado 1 diferem).

`docs/re-tools/test_t22_save_state_machine.py`: compila o modelo C, executa a implementação **original real** (via `differential_harness.py` de T10, bytes do ELF, não reimplementação) para os três estados × 6 valores representativos de `check_result` (incluindo fora da faixa `[0,15]` do índice), compara estado final e valor cacheado final entre original e modelo. **Todos batem exatamente**, incluindo o caminho de finalização (`state==2`, com sinal negativo testado). Mais um teste de injeção de falha, exigido pelo padrão de T10: confirma que o "modelo errado" (a crença pré-§661, que sempre reseta pra 0) realmente diverge do ELF real — prova que a suíte detectaria uma regressão de volta ao entendimento incorreto.

Suíte completa de `docs/re-tools`: **553 testes / 1.835 subtestes, todos passando** (548 antes + 5 novos).

## 5. O que isso prova e o que não prova

**Prova**: para as entradas testadas (3 estados, 6 valores de `check_result` cobrindo todos os ramos do índice de 16 vias incluindo fora de faixa), o modelo C reproduz exatamente o estado final e o valor de saída do binário ARM original. Isso é reconstrução real com teste diferencial, não documentação.

**Não prova**: equivalência para todo `int32` possível de `check_result` (testados só 6 valores representativos, não exaustivo); comportamento de `xpLibapiSaveStart/Check/End` em si (tratados como caixa-preta, stubados); interação com `Savedata_Load`/`CAUTOSAVE`/`CardAccess` (fora desta fatia); persistência real em arquivo (nenhum `CFILE` real tocado — este par de funções não faz I/O de arquivo diretamente, só orquestra o estado assíncrono).

## 6. Arquivos produzidos por esta tarefa

- `docs/REVERSE_ENGINEERING_NOTES.md` — seções 660 (correção `Savedata_Load`) e 661 (correção `pspFftDelete`, verificada por execução).
- `docs/re-tools/c-models/t22_fft_save_state_machine.c` — reconstrução C.
- `docs/re-tools/test_t22_save_state_machine.py` — teste diferencial contra o ELF original + injeção de falha.
- Este relatório.
