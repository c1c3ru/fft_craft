# Plano de ação — Fase 3: cobertura total do `libgl2jni.so`

## Mudança de meta (2026-10-16)

As Fases 1 e 2 (`RE_BACKLOG_PLAN.md`/`RE_BACKLOG_PLAN_PHASE2.md`) tinham
critério de "zerado" deliberadamente modesto: fechar pontas concretas
e abrir alguns sistemas novos, sem meta de cobrir o binário inteiro.
**A partir desta sessão, a meta mudou**: o objetivo agora é **100% de
engenharia reversa concluída do binário `libgl2jni.so`** — toda função
real do jogo, lida linha a linha, não só as maiores ou as mais
convenientes. As Fases 1/2 continuam válidas como histórico e podem
seguir sendo fechadas em paralelo, mas a partir de agora **este
documento é a lista-mestra** que direciona o loop.

## A escala real (números medidos, não estimados)

```
$ readelf -W --dyn-syms libgl2jni.so | awk '$4=="FUNC" && $3>0'
6.455 funções com tamanho > 0, somando 1.837.392 bytes (~1,79 MB) de código real.
mediana = 56 B · p90 = 564 B · máxima = 17.156 B (battle())
```

**Cobertura real nesta data**, calculada função por função (não por
amostra), cruzando esta lista contra todas as seções já escritas nos
dois documentos de resultado:

| Status | Funções | % | Bytes | % |
|---|---|---|---|---|
| `read_full` (lidas linha a linha, confirmadas) | 77 | 1,19% | 43.104 | 2,35% |
| `mentioned_unverified` (nome aparece no texto, mas só citado como chamada/padrão — NÃO confirmado lido por dentro) | 608 | 9,42% | ~150.280 | ~8,18% |
| `unread` (nunca tocada, nem por nome) | 5.770 | 89,39% | 1.644.008 | 89,47% |

**Honestidade importante**: o número "10,6% mencionadas" que apareceu
numa passada inicial de análise é uma superestimativa — inclui toda
função só resolvida como alvo de `bl` de outra (ex.: `GsSortFastSprite`,
citada dezenas de vezes, mas nunca lida por dentro). A métrica que
importa pra "100% concluído" é a coluna `read_full`: **2,35% dos bytes
de código, 77 de 6.455 funções**. O trabalho real pela frente é enorme
— isto não é pessimismo, é a escala real do problema.

## Artefato mestre: `RE_FUNCTION_INVENTORY.csv`

Criado nesta sessão (`readelf --dyn-syms` + demangle + cruzamento
textual com os dois documentos), contém **as 6.455 funções**, uma por
linha: `address,size,mangled,demangled,status,section_ref`.

- `status` começa em `unread` ou `mentioned_unverified` (herdado da
  passada automática de cruzamento por nome — não é garantia de
  leitura, só um sinal de que a função já apareceu no texto) ou
  `read_full` (as 77 já confirmadas manualmente nesta sessão, com
  `section_ref` apontando pra seção exata).
- **Cada iteração futura do loop deve, ao terminar de ler uma função,
  atualizar a linha correspondente pra `status=read_full` e preencher
  `section_ref`** (ex.: `NOTES §12.15`) — isso substitui a necessidade
  de recalcular cobertura por busca textual a cada vez.
- Três funções confirmadas como lidas (`RecheckFlaggedTargets`,
  `sub_275e3c`, `sub_277f78`) não aparecem no CSV porque são símbolos
  **locais/estáticos**, sem entrada em `.dynsym` — `readelf --dyn-syms`
  só lista símbolos dinâmicos exportados. Ficam de fora da contagem
  de 6.455 (que é só o universo "exportado"); existem também
  funções locais sem nome dinâmico nenhum (os `sub_XXXXXX` que várias
  seções já encontraram) que **não estão neste inventário** — são
  descobertas à medida que aparecem como alvo de `bl` sem símbolo.

## Metodologia (mesma da Fase 1/2, com um ajuste de granularidade pra funções grandes)

1. **Escolher a próxima função não lida**, priorizando por tamanho
   (maior primeiro) — mesma lógica já validada nas Fases 1/2, porque
   concentra o esforço onde há mais lógica real por byte de leitura.
   Consultar `RE_FUNCTION_INVENTORY.csv` ordenado por `size` com
   `status != read_full`.
2. **Ajuste pra funções muito grandes (>~2 KB)**: "lida por completo"
   pode significar, nesta fase, um **passe estrutural completo**
   (grafo de controle, todos os `bl` resolvidos por nome, todos os
   switches/tabelas de salto identificados, cada bloco principal
   descrito) em vez de pseudocódigo instrução-a-instrução de cada
   byte — mesmo espírito já usado na Fase 1 pras ~50 funções `wld_*`
   pequenas (seção 12.1: "caracterizadas por chamada/padrão, não
   byte-a-byte"), só que invertido (aqui é a função GRANDE que recebe
   o tratamento mais leve primeiro, com a opção de aprofundar depois).
   Isso é necessário pra `battle()` (17 KB) ser viável em iterações
   razoáveis. **Marcar explicitamente no `REVERSE_ENGINEERING_NOTES.md`
   qual dos dois níveis foi usado**, pra não inflar a cobertura.
3. **Desmontar via Capstone**, resolver `bl` contra `.dynsym`, ler,
   documentar, marcar `[x]`/`read_full`, comitar e dar push — mesmo
   ciclo de sempre.
4. **Escalonar, não forçar**, quando um alvo resistir.

## Atualização (2026-10-17): primeira função grande processada

`battle()` recebeu o primeiro passe estrutural da Fase 3 (ver
`REVERSE_ENGINEERING_NOTES.md` §32). Dois ajustes à infraestrutura
desta sessão:

- `status` no CSV agora tem um terceiro valor possível,
  **`read_structural`** — grafo de chamadas + blocos principais +
  tabelas de salto resolvidos, mas os corpos dos blocos individuais
  não lidos. Só `read_full` conta como "100% concluído" de verdade;
  `read_structural` é um estado intermediário explícito, não
  "terminado".
- Ferramenta nova no scratch da sessão, `struct_pass.py` (descida
  recursiva por branches como o `disasm_cfg.py`, mas resumindo em bl
  resolvidos + branches de retrocesso + pontos de convergência em vez
  de despejar cada instrução) — usar nas próximas funções grandes
  (`Wmesputmain`, `Main_FrameRender`, `Main_FrameMove`, etc.) antes de
  decidir se vale a leitura linha-a-linha completa.
- **Atualização (2026-10-17, `ItemMenu`, §39)**: existe uma tentativa
  `struct_pass2.py` de auto-resolver tabelas de salto em cascata —
  **não confiar nela sem verificar**; em `ItemMenu` ela gerou 3 falsos
  positivos (endereços que não eram tabelas de verdade). Pra tabelas
  de salto, continuar extraindo à mão (achar o `cmp`/`addls`, calcular
  `instr+8+offset`, decodificar os words como `b`) e só então semear
  a descida recursiva com os alvos reais — é mais lento mas confiável.

Trabalho pendente de maior valor identificado: os **70 handlers de
estado do switch de `battle()`** (endereços na seção 32.2 do
`REVERSE_ENGINEERING_NOTES.md`) — nenhum lido por dentro ainda.

## Fila prioritária imediata (as 30 maiores funções nunca tocadas)

Lista completa em `RE_FUNCTION_INVENTORY.csv` — aqui só o topo, pra
não duplicar 6.455 linhas neste arquivo:

| Endereço | Bytes | Função | Categoria provável |
|---|---|---|---|
| `0x207e10` | 17156 | `battle()` | ✅ passe estrutural feito (`REVERSE_ENGINEERING_NOTES.md` §32, 2026-10-17): switch de 102 estados / 70 endereços distintos, tabela completa extraída, 94 chamadas catalogadas. **Os 70 handlers de estado ainda não foram lidos por dentro** — maior trabalho pendente de toda a Fase 3. |
| `0x11173c` | 16312 | `Wmesputmain()` | ✅ passe estrutural feito (§33, 2026-10-17): confirma o subsistema `W*` de janelas/mensagens inteiro (nunca citado antes) e revela um sistema de tasks "wasm" novo. Corpo do laço principal e das 7 locais sem símbolo não lido. |
| `0x2c141c` | 16164 | `Main_FrameRender()` | ✅ passe estrutural feito (§34, 2026-10-17): confirma o chamador real do motor `CEGL2_*` (fecha seções 13–15), revela `CGX_SCREEN_CORRECT` (correção de proporção por dispositivo) e um padrão "screen manager" (delega pra `NowLoading_FrameRender`/`SettingsWnd_FrameRender`). Corpos dos blocos individuais não lidos. |
| `0x17c27c` | 15920 | `BattleUnitList(uchar*, ulong*)` | ✅ passe estrutural feito (§36, 2026-10-17): revela uma família `b*` inteira (~30 funções) de primitivas de desenho PS1 dedicada à UI 2D de batalha (`bDB_init`/`bSwapDB` = um 3º sistema de buffer, além de `GsOT` e `CEGL2_*`), com semi-transparência real confirmada. 3 tabelas de salto (toque) extraídas. Corpos não lidos. |
| `0xe88c4` | 15744 | `mesputmain()` | ✅ passe estrutural feito (§37, 2026-10-17): confirma que `W*`/sem-prefixo são duas variantes paralelas do MESMO sistema (quase 1:1 função por função — hipótese: texto largo/Shift-JIS vs. 1 byte), não dois sistemas diferentes. Generaliza provavelmente pra família `disp_personalwindow`. |
| `0x16a6a4` | 15412 | `ASHURA_addPrim(MATRIX*)` | ✅ passe estrutural feito (§38, 2026-10-17): confirma pilha de matrizes GTE real (`PushMatrix`/`PopMatrix`), iluminação real (`SetLightMatrix`), ray-picking (`RayPick_GT4/GT3`) e uso pesado de `ps_rand` (29×, partículas/efeitos). Corpos não lidos. |
| `0x1aeda0` | 13764 | `ItemMenu()` | ✅ passe estrutural feito (§39, 2026-10-17): revela o sistema real de itens/equipamento (`GetItemList`/`ItemEquip`/`AutoEquip`/`ChrPowerCompare`) e uma biblioteca completa de widgets de janela/menu (`WindowInit`/`SetBitStream`/`SetMenuSelVertical`), compartilhada. 1 tabela de salto real extraída. |
| `0x2bbb74` | 13272 | `Main_FrameMove()` | ✅ passe estrutural feito (§35, 2026-10-17): 2 switches de estado aninhados (9 casos externo, 43 interno) extraídos por completo; catálogo de 116 chamadas, maior desta fase — API de polling de toque completa, chamadas de plataforma Android diretas. Corpos dos 7+32 casos não lidos. |
| `0x18aeec` | 12580 | `eItemMenu()` | ✅ passe estrutural feito (§40, 2026-10-17): confirma a tela de EQUIPAR item (sufixo `_equip` paralelo ao `_unitlist`), terceira cópia paralela do padrão de duplicação por tela. **Corrige** a hipótese de idioma da §37: parece ser duplicação por tela/contexto, não por charset. |
| `0xc5148` | 12272 | `op_attackteam()` | ✅ passe estrutural feito (§41, 2026-10-17): confirma suporte real a batalha em rede (`pspNetGetBattleModeFlag`) e fecha a ponte bytecode↔task (opcode cria/espera uma task real pra UI de seleção de time). 3 tabelas de salto extraídas. |
| `0x184670` | 11004 | `CardAccess(int)` | ✅ passe estrutural feito (§42, 2026-10-17): "Card" = memory card do PS1 — revela o sistema REAL de save/load (`pspFftSave`/`pspFftLoad`/`pspSaveDataGetOne`, distinto do dump de heap de `CAUTOSAVE`), com suporte a **iCloud** (`iCloud_GetSlotCount`, nunca visto). |
| `0x1506ec` | 10976 | `requireprinf()` | ✅ passe estrutural feito (§43, 2026-10-17): liga com `op_attackteam` (§41) no cluster de configuração de batalha; confirma julgamento real de batalha em rede (`NetBattleJudge`/`getNetBattleJudge`) e um sistema "binpack" de dados binários de batalha (`__bpInitBinpackData`). |
| `0x225ac8` | 10724 | `CreateObjectWithTable(short,int,int,_Object*)` | ✅ passe estrutural feito (§44, 2026-10-17): confirma ser o gerador de partículas/efeitos variados (`_ParticleParameter*`, `getVariationData`), 99,7% de cobertura. `ps_rand()` chamada 103×, a maior contagem de toda a investigação. |
| `0x16fc90` | 10448 | `BattleCardAccess(int)` | ✅ passe estrutural feito (§45, 2026-10-17): confirma a tela de save/load acessível DE DENTRO da batalha, quarta cópia paralela (prefixo `c`) do padrão das seções 36/40/42. Revela `CARD_HEADER` (formato real de cabeçalho de save) e mais funções `pspSaveData*`. |
| `0x128ed4` | 8756 | `disp_personalwindow()` | ✅ passe estrutural feito (§46, 2026-10-17): confirma a janela de status pessoal real, com texto kanji (`statuskanjiprint`) e sombreamento PS1 real (`SetShadeTex`, nunca visto). Desenha via primitivas soltas, um 4º caminho de desenho distinto de `GsOT`/`CEGL2_*`/`DB`. Variantes `A/C/D/E/W` ainda não lidas. |
| `0x23e29c` | 8616 | `Mdl0024(short,int,int,int)` | ✅ passe estrutural feito (§48, 2026-10-17): confirma que a família `Mdl*` é o conjunto de rotinas de desenho de efeito/animação numeradas, construídas direto sobre `ASHURA` (§38) e o gerador de partículas (§44) — fecha o ciclo entre os dois. 99,4% de cobertura. |
| `0x1b2ea8` | 6216 | `JobChange()` | troca de classe/job |
| `0x1a486c` | 6908 | `AbilityMenu()` | menu de habilidades |
| `0x1bde2c` | 6976 | `UnitTable(...)` | ✅ passe estrutural feito (§55, 2026-10-17): rotina GENÉRICA parametrizada por 2 callbacks (não tabela de salto — eram chamadas via ponteiro de função dos próprios parâmetros). Explica o `iOSUnitList*` compartilhado entre telas. |
| `0x1c0930` | 6956 | `UnitList(int,int)` | ⚠️ passe estrutural PARCIAL (§56, 2026-10-17, só 58%): tem uma tabela de ponteiros de função real em memória (não um `addls` extraível), escalonado. 69 `bl` resolvidos mesmo assim. |

**Observação honesta**: `battle()`, `Main_FrameMove()` e
`Main_FrameRender()` — literalmente o **loop principal do jogo e o
loop principal de batalha** — nunca foram abertos nesta investigação
inteira, apesar de serem as 1ª/3ª/8ª maiores funções do binário. Todo
o trabalho até aqui (IA de batalha, mapa mundi, motores gráfico/áudio)
foi sobre sistemas DE SUPORTE chamados por essas três funções, não
sobre elas mesmas. Fechar essas três é provavelmente o item de maior
valor de toda a Fase 3.

## Critério de "zerado" desta fase

Diferente das Fases 1/2 (que tinham um critério modesto e alcançável),
**Fase 3 não tem critério de parada antecipada**: "zerado" = as 6.455
funções do `.dynsym` com `status=read_full` (no nível de detalhe
apropriado ao tamanho, seção "Metodologia" acima), mais o x86
(`libgl2jni.so` da pasta `x86/`) comparado função a função onde a
lógica diverge do ARM. Dado o tamanho (quase 1.800 iterações no ritmo
atual de ~1 função grande por iteração, mais um número grande de
funções pequenas que podem ser varridas em lote), isto é trabalho de
muitas centenas de iterações do loop — compatível com um `/loop`
contínuo, não com uma sessão só.
