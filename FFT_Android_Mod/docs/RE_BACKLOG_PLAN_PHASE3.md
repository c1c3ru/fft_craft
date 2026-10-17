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

Trabalho pendente de maior valor identificado: os **70 handlers de
estado do switch de `battle()`** (endereços na seção 32.2 do
`REVERSE_ENGINEERING_NOTES.md`) — nenhum lido por dentro ainda.

## Fila prioritária imediata (as 30 maiores funções nunca tocadas)

Lista completa em `RE_FUNCTION_INVENTORY.csv` — aqui só o topo, pra
não duplicar 6.455 linhas neste arquivo:

| Endereço | Bytes | Função | Categoria provável |
|---|---|---|---|
| `0x207e10` | 17156 | `battle()` | ✅ passe estrutural feito (`REVERSE_ENGINEERING_NOTES.md` §32, 2026-10-17): switch de 102 estados / 70 endereços distintos, tabela completa extraída, 94 chamadas catalogadas. **Os 70 handlers de estado ainda não foram lidos por dentro** — maior trabalho pendente de toda a Fase 3. |
| `0x11173c` | 16312 | `Wmesputmain()` | sistema de mensagens/diálogo (variante "W") |
| `0x2c141c` | 16164 | `Main_FrameRender()` | **loop principal do jogo inteiro** |
| `0x17c27c` | 15920 | `BattleUnitList(uchar*, ulong*)` | lista de unidades em batalha |
| `0xe88c4` | 15744 | `mesputmain()` | sistema de mensagens/diálogo (base) |
| `0x16a6a4` | 15412 | `ASHURA_addPrim(MATRIX*)` | motor gráfico "ASHURA" (nome nunca visto antes) |
| `0x1aeda0` | 13764 | `ItemMenu()` | menu de itens |
| `0x2bbb74` | 13272 | `Main_FrameMove()` | **loop principal do jogo inteiro** |
| `0x18aeec` | 12580 | `eItemMenu()` | variante de `ItemMenu` |
| `0xc5148` | 12272 | `op_attackteam()` | opcode de bytecode (time de ataque) |
| `0x184670` | 11004 | `CardAccess(int)` | sistema de "cartas" (nunca mencionado antes) |
| `0x1506ec` | 10976 | `requireprinf()` | nome não identificável só pelo nome |
| `0x225ac8` | 10724 | `CreateObjectWithTable(short,int,int,_Object*)` | fábrica de objetos do motor |
| `0x16fc90` | 10448 | `BattleCardAccess(int)` | variante de batalha de `CardAccess` |
| `0x128ed4` | 8756 | `disp_personalwindow()` | janela de status pessoal (+ variantes `A/C/D/E/W` prefixadas, provável localização por idioma) |
| `0x23e29c` | 8616 | `Mdl0024(short,int,int,int)` | handler de modelo/animação por unidade (há uma família `Mdl0001`–`Mdl0028`+) |
| `0x1b2ea8` | 6216 | `JobChange()` | troca de classe/job |
| `0x1a486c` | 6908 | `AbilityMenu()` | menu de habilidades |
| `0x1bde2c` | 6976 | `UnitTable(...)` | tabela de unidades |
| `0x1c0930` | 6956 | `UnitList(int,int)` | lista de unidades |

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
