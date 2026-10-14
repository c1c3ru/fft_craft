# Pesquisa: IA de batalha e opção de dificuldade

Investigação inicial sobre como a IA dos inimigos funciona dentro de
`libgl2jni.so` e o que seria necessário para (a) torná-la "mais esperta" e
(b) expor um seletor de dificuldade ao jogador.

## 1. Achado principal: o módulo de IA tem nomes de função legíveis

Diferente das classes C++ de engine (gráfico, som, input — ver
`libgl2jni_analysis_report.md`), a lógica de **IA de batalha** foi escrita em
C puro (não C++) e, por isso, os nomes das funções sobrevivem no
`.dynsym` mesmo num binário "stripped" (linkage `extern "C"` não é mangled
da mesma forma, então o símbolo não é removido pelo strip de debug info).
Os nomes batem exatamente com a nomenclatura conhecida do código-fonte
original de Final Fantasy Tactics (PSX/PSP) documentada pela comunidade de
engenharia reversa do jogo (FFHacktics e afins) — ou seja, **este port
Android reaproveita o C original quase sem alteração**.

Funções confirmadas (endereços no `.so` ARM, versão deste repositório):

| Função | Endereço | Papel (pelo nome + pseudocódigo) |
|---|---|---|
| `MainBattleRoutine` | `0x27426c` | Laço principal de IA por turno |
| `BattleRoutine` | `0x274764` | Executa a rotina de IA de uma unidade |
| `BattleRoutineInit` | `0x27a974` | Inicialização do estado de IA da batalha |
| `ClearForBattleRoutine` | `0x279ed4` | Reset de estado entre turnos |
| `FundamentalRoutine` | `0x278f84` | **Dispatcher central da IA** (150 blocos básicos — ver seção 3) |
| `EvaluateAllUnitAction` | `0x271da0` | Itera as 34 unidades do campo chamando `FundamentalRoutine` |
| `ForAbnormalStatus` | `0x272254` | Decide ação quando a unidade está sob status alterado |
| `GetNearestUnit` | `0x27207c` | Busca unidade mais próxima (alvo) |
| `GetCountToDeath` | `0x27b240` | Estima turnos até a morte de uma unidade (heurística de prioridade de alvo) |
| `SetDestUnit` / `GetPanelUnderUnit` | `0x27334c` / `0x278440` | Define/lê painel de destino do movimento |
| `IsNullUnit` / `IsAlmostNullUnit` | `0x273d20` / `0x273cc8` | Filtros de unidade inválida/morta ao varrer a lista |
| `CheckUnitActionOK` / `CheckUnitActionEffective` | `0x276788` / `0x276e4c` | Validam se uma ação é possível/eficaz |
| `GetDirectionOfAutoUnit` | `0x279cc0` | Direção de movimento automático |
| `SetUnitParameter` | `0x27a3bc` | (não decompilado ainda — ver limitações) |

## 2. Como a IA decide (confirmado via pseudocódigo)

- **Loop de topo:** `EvaluateAllUnitAction` percorre uma tabela global de até
  34 unidades (`*dword_347bb8`, provavelmente a struct `BWORK`/lista de
  batalha) e chama `FundamentalRoutine()` para cada uma que não está
  marcada como inválida (`campo[0x2] != 0xff`).
- **`GetCountToDeath(unit)`** calcula `turnos_para_morrer ≈ ceil((100*dano_por_turno) / HP_atual)`
  via `smlabb` (multiply-accumulate) seguido de divisão inteira — e retorna
  "infinito" (`0x7fffffff`) se a unidade está sob efeitos que a tornam
  imortal/irrelevante no momento. Isso é a heurística clássica de
  "prioridade de alvo" (IA prefere matar quem ela consegue matar rápido).
- **`ForAbnormalStatus`** (ação quando a unidade tem status alterado) usa
  `ps_rand()` para **sortear entre candidatos com a mesma pontuação** quando
  há múltiplas opções igualmente boas de alvo/painel — ou seja, parte da
  "burrice" percebida da IA vem de desempate aleatório deliberado, não de
  erro de cálculo.
- `IsNullUnit`/`IsAlmostNullUnit` são apenas filtros de validade (unidade
  morta, fora do campo, etc.), confirmando a estrutura normal de uma lista
  de atores de batalha.

## 3. Limitação encontrada: Hopper não descompila as funções mais complexas

`FundamentalRoutine` (o dispatcher central, 150 blocos básicos / 2792 bytes)
e várias outras (`CheckUnitActionEffective`, `SetUnitParameter`,
`BattleRoutine`, `GetHightDistance`, `GetUnitOnPanel`, `JudgeStatus`,
`GetPanelUnderUnit`, `GetDirectionOfAutoUnit`, `ClearForBattleRoutine`,
`BattleRoutineInit`) retornaram pseudocódigo vazio — o decompilador do
Hopper não dá conta de reconstruir C legível para elas (provavelmente por
causa de saltos/switch complexos típicos de código PSX-ASM-para-C
"source-to-source" direto). Num lote (`batch_decompile`) o processo do
Hopper ficou instável e precisou ser reiniciado (`close_binary` +
`open_binary` de novo) depois de travar em `BattleRoutine`.

**Essas são justamente as funções que decidem qual ação/skill a IA escolhe**
— ou seja, o núcleo real da "inteligência" da IA ainda não foi exposto como
pseudocódigo legível. Dá para ler a montagem ARM bruta
(`procedure_assembly`) função por função, mas é um trabalho manual lento;
ou tentar o Ghidra (que em geral lida melhor com CFGs grandes/switch), que
ficou bloqueado nesta máquina por configuração de `JAVA_HOME` (ver
`libgl2jni_analysis_report.md`, seção 7).

## 4. Duas rotas possíveis a partir daqui

### Rota A — "IA mais esperta" (reescrever a decisão real)
Exige decompilar/entender `FundamentalRoutine`, `BattleRoutine` e
`CheckUnitActionEffective` em detalhe (provavelmente via leitura de
assembly bruto ou resolvendo o Ghidra), e então **patchear bytes de
instrução ARM e x86 separadamente** dentro do `.so` para alterar pesos de
decisão/thresholds — sem poder recompilar a partir de fonte. Risco alto,
esforço grande, resultado incerto; cada ajuste exige reteste manual em
jogo.

### Rota B — "Dificuldade selecionável" via escala de stats (recomendada)
Em vez de alterar a decisão da IA, aplicar um multiplicador de HP/Ataque/
Velocidade dos inimigos no início da batalha, configurável pelo jogador.
Não exige entender `FundamentalRoutine` — só achar onde os stats da unidade
são carregados/inicializados (candidatos a investigar a seguir:
`_Z12set_unitdatai` `0x1dbcec`, `_Z18set_startingstatusP5BWORK` `0x1dc908`,
`_Z19adjust_entry_statusP5BWORK` `0x1dc44c`, todos vistos na mesma busca).
Ganho prático de dificuldade percebida (inimigos mais tanky/letais) com uma
fração do esforço e risco da Rota A, e dá pra expor como opção de UI
(smali + layout, no mesmo estilo dos patches de licença/OBB já feitos no
projeto).

## 5. Atualização: o Hopper se revelou pouco confiável neste ambiente

Em sessão posterior, tentamos continuar a Rota A usando o Hopper (via REA)
para obter o grafo de chamadas de `FundamentalRoutine`. O lançamento do
Hopper passou a travar consistentemente na fase de inicialização (sempre
~120s, sempre no mesmo ponto do log, "not_started"). Investigamos várias
hipóteses (diálogo de licença, travas antigas em `/tmp/Hopper*`, pressão de
memória/swap do sistema, contenção com uma sessão paralela que também usa
REA) — todas tinham evidência parcial, mas nenhuma resolveu o problema de
forma definitiva, e o timeout de 120s do lado do REA mata o processo do
Hopper antes dele terminar a análise inicial, então nem "ter paciência"
ajuda: cada tentativa reinicia do zero.

**Solução: abandonar o Hopper para este tipo de consulta e desmontar o ARM
diretamente**, usando a biblioteca Python `capstone` (instalada num
virtualenv isolado em `/tmp`, fora do repositório) direto sobre os bytes do
`.so`. Isso não depende de GUI, bridge, nem do Hopper — só precisa saber o
offset no arquivo (que, para este binário, é igual ao endereço virtual
dentro da seção `.text`, confirmado via `readelf -WS`: `.text` tem
`Addr == Offset == 0x71c50`, delta zero).

## 6. Mapeamento manual de `FundamentalRoutine` (via Capstone, sem Hopper)

`FundamentalRoutine` (`0x278f84`) é confirmada como uma **máquina de
estados**: lê uma "fase" de IA (0–8) guardada em `unit[0xc70]` e despacha via
tabela de salto (`addls pc, pc, r3, lsl #2` em `0x278fc8`) para um handler
por fase:

| Fase | Endereço do handler |
|---|---|
| 0 | `0x279464` |
| 1 | `0x27969c` |
| 2 | `0x279684` |
| 3 | `0x27955c` |
| 4 | `0x279580` |
| 5 | `0x27938c` |
| 6 | `0x279464` (mesmo handler da fase 0) |
| 7 | `0x2795e0` |
| 8 (fora da tabela / "else") | `0x278ff4` — chama `VSync()`, compara a um limite de 440 "ticks" (`0x1b8`); é um estado de **espera com timeout** (provavelmente aguardando animação/efeito terminar) |

Isso bate exatamente com a estrutura clássica de IA tática por turnos:
fases distintas para "pensar" (escolher ação), "mover", "executar
ação/animação", "esperar" etc. — cada fase um pequeno sub-programa.

### `sub_271628` — validador/"comprometer-se" com a ação escolhida
Função estática sem nome exportado (entre `CountMap` e
`SetBaseTargetGroup`), chamada por `ForAbnormalStatus` para decidir se uma
ação candidata deve ser executada. Desmontagem manual mostrou que ela:
- Chama `GetDestinationsAndMakeMaskTG()` — calcula o conjunto de painéis de
  destino válidos ("TG" = Target Group) e uma máscara de alcance.
- Decrementa um contador de tentativas em `unit[0xcbc]`.
- Chama `SetThisDestination()` para confirmar o painel de destino escolhido.

Ou seja, `sub_271628` é a etapa de **validação de movimento/caminho** da
ação já escolhida — não é onde a IA decide *qual* habilidade usar (isso
deve estar nas fases 0/1 da máquina de estados acima, ainda não mapeadas em
detalhe).

## 6.1 Fase 0 da máquina de estados — achado principal: aqui está o "cérebro"

Desmontagem manual de `0x279464` (handler da fase 0, que também é a fase 6)
revela chamadas a uma sequência de funções com nomes extremamente
reveladores:

| Função chamada | Endereço | Papel |
|---|---|---|
| `SetBestMoveAnywhereOK` | `0x273ea0` | Marca se mover para qualquer painel é aceitável |
| `SetBMList` | `0x273f4c` | Monta a lista de "Best Move" (BM = melhor jogada) candidatos |
| `GetTargetBaseArea(int,int)` | `0x276930` | Calcula área/alcance em torno do alvo |
| `CheckUnitActionOK` | `0x276788` | Valida se a ação é permitida |
| `CheckUnitActionEffective` | `0x276e4c` | Valida se a ação teria efeito (ex.: não é imune) |
| `JudgeMovable(int)` | `0x2775dc` | Julga se a unidade pode se mover para o painel |
| `SetThisDestination` | `0x277640` | Confirma o destino escolhido |
| estática dentro de `SetBestMove` (+0x5c) | `0x277f78` | Parte interna de `SetBestMove` |
| estática dentro de `GetDestinationsAndMakeMaskTG` (+0x78c) | `0x278c0c` | Chamada no início de várias fases — provável "está pronto para agir?" |

**Esta é a rotina real de "escolher a melhor jogada"** — o nome `SetBMList`
("Best Move List") deixa pouca dúvida. Para realmente tornar a IA "mais
esperta" (Rota A), o próximo nível de detalhe seria desmontar `SetBMList` e
`SetBestMove` por completo para achar a fórmula de pontuação (provavelmente
envolvendo `GetCountToDeath`, dano estimado, distância, e thresholds fixos)
e então decidir o que ajustar — ex.: aumentar o peso dado a alvos
vulneráveis, reduzir a dependência de `ps_rand()` nos empates, ou ampliar
quantos candidatos `SetBMList` considera antes de decidir.

## 6.2 Dentro de `SetBMList`: a fórmula de comparação de jogadas

`SetBMList` (`0x273f4c`, 204 bytes, desmontada por completo) mantém uma
**lista ordenada das 8 melhores jogadas candidatas** (`BM` = "Best Move"),
8 slots de 32 bytes cada, e insere um novo candidato nessa lista por
inserção ordenada (shift dos elementos piores para abrir espaço),
comparando sempre contra o candidato atual via `CompareMove`.

As duas funções de comparação, reconstruídas por completo a partir da
desmontagem (nomes de tipo `SCORE`/`MOVE` vêm do próprio símbolo mangled
C++, preservados no binário):

```c
// CompareScore(SCORE* a, SCORE* b) — retorna 0 (a melhor), 1 (empate), 2 (a pior)
// struct SCORE { uint8_t f0; uint8_t f1; int16_t f2; ... };
int CompareScore(SCORE* a, SCORE* b) {
    if (a->f0 > b->f0) return 2;
    if (a->f0 < b->f0) return 0;
    // f0 empatado — critério de desempate 1: f2 (16 bits, com sinal)
    if (a->f2 > b->f2) return 2;
    if (a->f2 < b->f2) return 0;
    // f2 empatado — critério de desempate 2: f1 (8 bits)
    if (a->f1 > b->f1) return 2;
    return (a->f1 < b->f1) ? 0 : 1;   // 1 = empate total
}

// CompareMove(MOVE* a, MOVE* b) — struct MOVE tem um SCORE embutido no offset 0x1c
int CompareMove(MOVE* a, MOVE* b) {
    int c = CompareScore(&a->score, &b->score);  // score em MOVE+0x1c
    if (c == 2) return 1;   // a pior que b
    if (c == 0) return 0;   // a melhor que b
    // c == 1: score EXATAMENTE igual — usa uma tabela de terreno/posição
    // como desempate final (lookup indexado por (f5,f6) de cada MOVE,
    // stride 0x12*16, campo final em +0x174 da tabela)
    return (a->terrain_tiebreak >= b->terrain_tiebreak) ? 0 : 1;
}
```

**Leitura prática:** a IA ordena jogadas candidatas por 3 critérios em
cascata — (1) uma categoria/prioridade de 1 byte, (2) uma pontuação de 16
bits com sinal (provavelmente a estimativa de valor/dano da jogada — ainda
não localizamos onde esse campo é *calculado*, só onde é *comparado*), e
(3) um segundo byte de desempate — e em empate total cai num lookup de
tabela de terreno/posição. Isso é uma IA determinística e bem estruturada,
não aleatória: a "burrice" percebida não vem dessa comparação (que é sã),
e sim de **quantos candidatos ela avalia** (só os que entram na lista de 8,
montada antes de chegar aqui) e de onde o campo de pontuação (`f2`) é
preenchido — essa é a peça que falta mapear para achar o verdadeiro
"quão inteligente" a avaliação é.

## 6.3 `EvaluationFunction` — achado grande: a IA simula antes de pontuar

`SetBestMove` (`0x277f1c`, 1316 bytes) é quem monta cada candidato a
jogada e o insere na lista de `SetBMList`. A primeira chamada que ela faz,
antes de qualquer comparação, é para **`EvaluationFunction()`**
(`0x277720`, 2044 bytes — nome exato preservado no símbolo mangled).

Desmontagem (parcial, nível de "quais funções ela chama") de
`EvaluationFunction` mostra algo mais sofisticado do que uma fórmula fixa
de dano/distância: ela chama funções que **aplicam efeitos de habilidade
de verdade**, como se estivesse simulando a ação até o fim antes de
avaliar o resultado:

| Chamada | Papel |
|---|---|
| `setskilldata(ACT*)` | Prepara os dados da habilidade a ser "executada" |
| `setskillresult()` | Aplica o resultado da habilidade (dano, status, etc.) |
| `set_turn_end(int)` | Marca fim de turno |
| `time_flies(int)` | Avança o relógio interno do jogo |
| `set_guard_status(int)` | Ajusta status de guarda |
| `__aeabi_idiv` (3 chamadas) | Divisões inteiras — proporções tipo "benefício / custo" |
| 3 funções estáticas internas de `BattleRoutine` (sem nome próprio) | Provavelmente cálculo de dano/acerto específico pra avaliação |

**Hipótese de trabalho:** a IA de FFT não usa só uma fórmula estática — ela
parece **simular a execução da habilidade** (aplicando dano/status
hipotético) e só então pontua o estado resultante, usando `CompareScore`/
`CompareMove` (seção 6.2) pra decidir qual candidato simulado é melhor.
Isso é uma arquitetura de IA bem mais sofisticada do que normalmente se
credita ao jogo — mas também significa que entender o detalhe fino da
pontuação (os campos `f0`/`f1`/`f2` do struct `SCORE`) exige ler as 502
linhas de assembly de `EvaluationFunction` com calma, incluindo as 3
funções estáticas internas de `BattleRoutine` que ela usa.

## 6.4 `EvaluationFunction` completa (502 linhas de ARM lidas por completo)

Leitura integral confirma a hipótese da seção anterior e revela uma
arquitetura mais sofisticada do que o esperado:

**É uma simulação em corrotina espalhada por vários frames reais.** A
função usa um campo de estado (`sb+0xeee`, onde `sb` = `*dword_347bb8`, a
mesma struct global de sempre) com 3 valores: `0` = iniciar simulação do
zero, `1` = retomar após 1 frame de espera, `2` = simulação concluída,
pronta pra extrair o resultado. Isso bate com o padrão de jogos da época:
rodar uma animação de ataque hipotética exige vários frames reais de
`VSync()`, então a função "pausa" e é chamada de novo no frame seguinte —
não dá pra simular tudo de uma vez numa única chamada.

**Checkpoint/rollback de estado global:** antes de simular, salva 3
palavras de 32 bits de variáveis globais (prováveis candidatas: semente do
RNG e/ou estado do motor de física/animação) em `sb+0xee0/0xee4/0xee8`. Se
a simulação não terminar dentro de um limite de tempo (~312 ou ~440
"frames" dependendo do caminho — `cmp r0,#0x138` / `#0x1b8`), a função
**restaura essas 3 palavras** e aborta com sentinela -1, marcando um sinal
de "tentar de novo" (`sb+0xeee`). Ou seja, o motor garante que uma
simulação hipotética de IA nunca "vaza" para o estado real do jogo se
precisar ser cancelada.

**Cálculo real da pontuação (quando a simulação termina a tempo):** itera
sobre as unidades afetadas pela área de efeito da habilidade (laço de 40
posições, índices 0–0x27, com uma tabela de salto de 27 casos para
diferentes formatos de área) e acumula em `r6`/`r8`:
- Dano/efeito base de cada painel afetado, vindo de uma tabela indexada
  por posição (via `__aeabi_idiv`, ou seja, com alguma divisão/proporção
  envolvida, não só multiplicação direta).
- **+51 de bônus por fraqueza elemental explorada** — um laço de 7
  elementos compara a tabela de afinidade elemental da habilidade com a do
  alvo e soma `0x33` (51) a cada acerto. Isso é literalmente "a IA valoriza
  explorar o elemento fraco do inimigo", de forma bem concreta e com peso
  fixo.
- Um termo escalado por `(HP atual × 64) / algo`, reduzido à metade se a
  habilidade atinge uma linha/fileira específica — plausivelmente
  relacionado a priorizar acabar com unidades já fracas (reforça o padrão
  de `GetCountToDeath` visto antes).
- **Inversão de sinal aliado/inimigo**: no fim do cálculo por alvo, se uma
  flag indicar "este alvo é aliado", o score daquele alvo é **negativo**
  (`rsbne r0, r0, #0`); se for inimigo, fica positivo. Confirma
  explicitamente que a IA penaliza acertar os próprios aliados (fogo
  amigo) e recompensa acertar inimigos — e soma tudo num único total.

**Gravação do resultado:** o total acumulado (`r8`) é salvo em
`unit[0x32]` (`strh r8, [sb, #0x32]`, linha `0x277d4c`) — este é, com alta
confiança, o mesmo campo de 16 bits com sinal que `CompareScore` lê como
`f2` (critério de desempate principal entre jogadas candidatas, seção
6.2). **Isso fecha o ciclo completo**: `EvaluationFunction` calcula →
grava em `unit+0x32` → `SetBestMove` copia pro campo `score` do `MOVE` →
`SetBMList`/`CompareMove`/`CompareScore` decidem qual candidato é melhor.

### O que ainda fica impreciso
- A tabela de 27 "formatos de área" (jump table em `0x277bb0`) não foi
  decodificada painel-por-painel — sabemos que existe e que ela filtra
  quais das 40 posições contam, mas não o desenho exato de cada formato.
- As 3 funções estáticas internas de `BattleRoutine` chamadas por
  `EvaluationFunction` (dano base, tabela elemental, lookup de HP) não
  foram desmontadas linha a linha — inferimos o papel pelo contexto
  (operandos, ordem das chamadas, uso do resultado), não por leitura
  completa de cada uma.
- As 3 palavras globais salvas/restauradas (`0xee0/0xee4/0xee8`) ainda não
  foram confirmadas como RNG vs. estado de animação/física — é a hipótese
  mais provável dado o padrão de save/restore em torno de uma simulação
  cancelável, mas não foi verificada lendo o que realmente as popula.

## 6.5 Com isso mapeado: pontos reais de patch para dificuldade

Agora que a cadeia completa está entendida (seções 6.1–6.4), dá pra listar
alvos concretos de patch, do mais simples/seguro ao mais arriscado:

1. **Bônus de fraqueza elemental (`+0x33`/51, em `0x277c88`)** — trocar a
   constante imediata `#0x33` por um valor maior faria a IA perseguir
   fraquezas elementais com prioridade ainda mais alta. Patch de 1
   instrução (muda o imediato do `add`), baixo risco, efeito bem
   localizado. Precisa ser feito nos dois binários (ARM e x86 — o offset
   x86 ainda não foi localizado).
2. **Limite de timeout da simulação (`0x138`/312 e `0x1b8`/440, em
   `0x277a80` e `0x277760`/`0x27776c`/`0xeff`...)** — não afeta
   "inteligência", só robustez; não é um alvo útil para dificuldade.
3. **Escala HP/fileira (bloco `0x277ccc`–`0x277d30`)** — ajustar o divisor
   usado no `__aeabi_idiv` mudaria o quanto a IA valoriza "finalizar"
   unidades fracas. Médio risco: a constante exata do divisor não foi
   isolada com certeza (vem de uma tabela, não um imediato simples).
4. **Pesos da função de dano base por painel (dentro das 3 estáticas de
   `BattleRoutine` ainda não lidas linha a linha)** — provavelmente o
   maior impacto real em "quão bem a IA avalia dano", mas é o menos
   mapeado dos quatro; exigiria desmontar essas 3 estáticas por completo
   antes de decidir um patch seguro.

**Recomendação prática:** a opção 1 (bônus elemental) é o primeiro patch
real e testável que dá pra fazer com confiança alta a partir do que já
sabemos — pequeno, localizado, fácil de reverter, e o efeito em jogo é
perceptível (IA explora fraquezas elementais com muito mais convicção).
As opções 3 e 4 exigem mais leitura antes de arriscar um patch.

### Patch aplicado (bônus elemental 51 → 102)

Aplicado e verificado nos dois binários — dobra o bônus de fraqueza
elemental (de `0x33`=51 para `0x66`=102). Patch de 1 byte em cada arquivo,
sem mudar tamanho do arquivo nem layout:

| Arquivo | Offset | Antes | Depois | Instrução (antes → depois) |
|---|---|---|---|---|
| `src/lib/armeabi/libgl2jni.so` | `0x277c88` | `0x33` | `0x66` | `addeq r6, r6, #0x33` → `addeq r6, r6, #0x66` |
| `src/lib/x86/libgl2jni.so` | `0x283582` | `0x33` | `0x66` | `lea edi, [edx + 0x33]` → `lea edi, [edx + 0x66]` |

Verificação pós-patch: `readelf -h` válido nos dois, tamanho de arquivo
idêntico ao original (4.463.112 bytes ARM / 4.988.572 bytes x86), e
redesmontagem confirma só a instrução-alvo mudou, nada ao redor foi
afetado. Efeito esperado em jogo: a IA passa a valorizar duas vezes mais
explorar o elemento fraco do alvo ao escolher entre jogadas candidatas —
não muda a estrutura de decisão, só o peso desse critério específico.

**Ainda não feito:** empacotar isso num APK pra testar em jogo (os
scripts `scripts/build.sh`/`install.sh` do projeto cuidam disso, mas não
foram executados aqui) e validar em uma batalha real que o comportamento
mudou perceptivelmente. Reverter é trivial: trocar o byte de volta pra
`0x33` nos dois offsets acima, ou `git checkout` deste commit no worktree.

## 7. Próximos passos sugeridos
- Desmontar os handlers das fases 0 e 1 (`0x279464`, `0x27969c`) — são os
  candidatos mais fortes para conter a lógica real de "qual ação/alvo
  escolher", que é o que precisaria ser ajustado para uma IA "mais
  esperta".
- Continuar usando Capstone diretamente (`/tmp/.../reavenv` +
  `disasm.py`), evitando o Hopper enquanto o problema de inicialização dele
  não for resolvido (possivelmente precisa de reinício do ambiente/MCP, não
  só de mais memória livre).
- Depois de entender a lógica de pontuação, decidir que parâmetro(s)
  ajustar (ex.: reduzir a frequência de desempate aleatório via `ps_rand()`,
  ou ampliar o conjunto de ações candidatas avaliadas) e planejar o patch
  binário (ARM e x86 separadamente).

## 8. Estado desta investigação
Nenhum patch foi aplicado ainda — isto é só levantamento (read-only) rodado
num worktree isolado (`worktree-fft-ai-difficulty`). Nenhum arquivo `.so`
foi modificado. O script de desmontagem manual (`disasm.py`) e o virtualenv
do capstone ficam em `/tmp`/diretório de scratch da sessão, fora do
repositório — não foram commitados por não serem artefatos do projeto.
