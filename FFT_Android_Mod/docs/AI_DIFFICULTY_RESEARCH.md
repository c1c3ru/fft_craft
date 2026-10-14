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

## 9. Continuação (fila de processamento) — 2026-10-14

Sessão seguinte, tratando a investigação como uma fila: Hopper confirmado
de novo como não-utilizável neste ambiente (mesmo erro de sempre —
`provider_timeout` depois de 120s, "não_started", log preso na mesma
linha de GNUstep). Voltei ao Capstone cru (venv isolado, recriado em
`/tmp`, fora do repo) usando `pyelftools` para mapear VA→offset de arquivo
por seção (antes era só "delta zero" hardcoded; agora o script
(`disasm.py`) lê `readelf`-equivalente via pyelftools e funciona para
qualquer seção, inclusive `.data`/`.data.rel.ro*`, o que foi essencial
para o item 2 abaixo). Todo o trabalho desta seção é só sobre o `.so`
ARM (`armeabi`); o x86 não foi tocado ainda.

### 9.1 Item da fila: "os 3 callers de dano base" — achado corrige a hipótese anterior

Os três endereços chamados por `EvaluationFunction` e citados na seção 6.3
(`sem nome próprio`) foram localizados com precisão: ficam no intervalo
*entre o fim do corpo real de `BattleRoutine` e o início de
`GetHightDistance`* — ou seja, são exatamente as "3 funções estáticas
internas de BattleRoutine" que a fila pedia.

| Endereço | Tamanho | Papel real (lido linha a linha) |
|---|---|---|
| `0x2761ec` | 192 B | Cache de afinidade elemental por unidade: se o campo já visto (`sb->e2e`) bate com o "elemento" apontado por `arg0`, retorna o valor cacheado (`sb->b[0x31]`); senão chama `sub_275e3c` (dentro do próprio `BattleRoutine`, ~0x275e3c, não desmontada ainda) e grava o resultado de uma divisão (`__aeabi_idiv`) em `sb->b[0x31]`. |
| `0x2762ac` | 576 B | **Não é cálculo de dano.** É um laço de cópia (`MemCpyB`/`MemCpyW`, nomes confirmados no `.dynsym` nos endereços `0x279c64`/`0x279c34`) que monta, para até **21** "slots" (`cmp r7,#0x15`), um array de atributos de arma/habilidade (campos de 5,16,14,3,8,4,3,3,8 bytes) a partir de uma tabela indexada por um byte de elemento lido em `sb+0x1980+0xb` até o sentinela `0xff`. |
| `0x2764ec` | 520 B | Estrutura quase idêntica à de `0x2762ac` (mesmos tamanhos de campo, mesmo limite de 21, mesma chamada final de 8 bytes para `sb+0xe30+0xc`/`sl+0xe30+0xc`) — é a variante "lado B" do mesmo monta-tabela (provável: arma principal vs. arma secundária/escudo, ou habilidade vs. reação). |

**Correção importante:** a aritmética de dano de verdade (bônus elemental
`+0x33`, termo escalado por HP, termo por "tier" de poder da habilidade,
inversão aliado/inimigo) está **inline dentro da própria
`EvaluationFunction`** (confirmado por leitura completa, seção 9.3) — as 3
estáticas são *preparação de dados* (cache de elemento + duas cópias de
tabela de equipamento), não a fórmula de dano em si. A suposição da seção
6.4 ("inferimos o papel pelo contexto... provavelmente cálculo de
dano/acerto") estava parcialmente errada para 2 das 3 funções; mantém-se
certa só para a terceira (`0x2761ec`, que de fato alimenta um valor usado
depois no bônus elemental).

Bônus: dois outros helpers sem nome, chamados por `EvaluationFunction` mas
fora do intervalo de `BattleRoutine` (então não contam como "os 3"):
`0x277684` (156 B, no intervalo entre `SetThisDestination` e
`EvaluationFunction`) e `0x276d78` (212 B, entre `JudgeStatus` e
`CheckUnitActionEffective`) — nenhum dos dois foi desmontado ainda.

### 9.2 Item da fila: as 3 variáveis globais da simulação — resolvidas por nome, não é RNG

A hipótese da seção 6.4 ("prováveis candidatas: semente do RNG e/ou estado
de física/animação") estava **errada**. Resolvi os 3 ponteiros via a
cadeia GOT completa (`ldr r,[pc,#imm]` → soma com PC → índice na GOT →
conteúdo da GOT, lido direto do arquivo porque as relocations são
`R_ARM_RELATIVE` com base 0 — ou seja, o valor já gravado no arquivo é o
endereço final) e cruzei o endereço resultante contra o `.dynsym`:

| Campo salvo/restaurado | Variável global real | Tamanho | Seção |
|---|---|---|---|
| `sb+0xee0` | **`_binary_record_bin`** | 156 B | `.data` |
| `sb+0xee4` | **`scritem`** | 256 B | `.bss` |
| `sb+0xee8` | **`pagewinInf`** | 116 B | `.bss` |

Nenhuma é RNG nem física/animação. São estado de **UI/mensagem de
combate**: `pagewinInf` ("page window info") e `scritem` ("script/menu
item") são claramente ligadas ao sistema de janelas/menu de batalha, e
`_binary_record_bin` tem cara de buffer de "registro"/log de mensagem
(nome de símbolo típico de um blob incorporado via `ld -b binary`, mas
aqui usado como variável C comum de 156 bytes). **Isso faz sentido com a
arquitetura já confirmada na seção 6.3/6.4:** como `EvaluationFunction`
chama de verdade `setskilldata`/`setskillresult` (o mesmo código usado
numa ação real), a simulação herda efeitos colaterais desses buffers de
UI/mensagem; salvar/restaurar esses 3 campos evita que uma avaliação
hipotética "vaze" texto de combate ou estado de menu para a tela real caso
a simulação seja abortada (timeout de ~312/440 frames, já documentado).

### 9.3 Achado arquitetural maior: a IA roda sobre buffers trocados, não sobre o array real

Ao desmontar `BattleRoutineInit` (`0x27a974`, 472 B, completa) por outro
item da fila ("Funções Nominais"), apareceu algo que explica *por que* a
simulação pode "fingir" executar uma ação sem tocar o estado real do jogo:

- `BattleRoutineInit` troca o ponteiro global **`BattleWork`** (a variável
  em `0x347bb8`, confirmada por nome — é o `*dword_347bb8`/`sb` usado em
  toda essa investigação) para apontar para **`spd_back`** (buffer de
  6592 B), e troca **`BworkBackup`** (`0x347bc4`) para apontar para
  **`spad_copy`** (2048 B) — ambos resolvidos por nome via a mesma cadeia
  GOT da seção 9.2.
- Ou seja: `sb` (o ponteiro que toda a IA usa — `EvaluationFunction`,
  `SetBMList`, `CompareMove`, as 3 estáticas, etc.) **não aponta para o
  array de batalha real durante essa fase** — aponta para uma cópia de
  trabalho (`spd_back`). Isso é um padrão de *double buffering*: a IA
  simula em cima de uma cópia, e algo em `ClearForBattleRoutine` (ainda
  não lido) deve ser responsável por sincronizar de volta ou alternar os
  buffers no momento certo.

**Correção de outro dado da seção 1:** a tabela global iterada por
`EvaluateAllUnitAction` foi descrita como "até 34 unidades". A
investigação desta sessão confirma, por tamanho de símbolo exato, que o
array real **`bwork`** (resolvido por nome, endereço `0x563560`) tem
**10206 bytes = 21 × 486**, e 486 (`0x1e4+2`) é exatamente o stride de
unidade usado em todo lugar nesta investigação (`GetPanelUnderUnit`,
`GetUnitOnPanel`, o laço de pontuação de `EvaluationFunction`, o laço de
`BattleRoutineInit`). **O limite real é 21 unidades simultâneas, não 34**
— a claim de "34" na seção 1 não foi re-verificada nesta sessão (pode vir
de outro array/contexto, ex. elenco total de personagens possíveis vs.
unidades ativas em campo) e deveria ser revisada quando `EvaluateAllUnitAction`
for relido.

Também dentro de `BattleRoutineInit`: depois da troca de buffers, há um
laço pelas 21 unidades de `bwork` (não de `spd_back`!) que soma o campo
`halfword[0x31]` de cada unidade válida, chama `SetUnitParameter(idx)`
(`0x27a3bc`, ainda não desmontada por completo) por unidade, e no final
calcula a **média** (`soma / contagem`, via `__aeabi_idiv`) dessa soma,
gravando o resultado (saturado em 0xff) em `sb->b[0xe17]`. Esse campo
(`+0xe17`) é exatamente o tipo de "limiar global" que `JudgeStatus` recebe
como parâmetro (seção 9.4) — forte candidato a ser o "nível médio do
grupo" usado como referência de dificuldade de status.

Um terceiro detalhe de `BattleRoutineInit`, possivelmente relevante para o
objetivo final do projeto (seletor de dificuldade): ele copia 2 bytes
globais para `sb->b[0xe3a]`/`sb->b[0xe3b]`. O de `+0xe3a` foi resolvido
por nome: vem de **`gMapX`** (1 byte) — então é dado de mapa, não de
dificuldade; o segundo byte (destino `+0xe3b`) não foi resolvido nesta
sessão (fila aberta).

### 9.4 Outras funções nominais da fila, desmontadas por completo

| Função | Endereço/tamanho | Pseudocódigo (resumo fiel à leitura linha a linha) |
|---|---|---|
| `GetPanelUnderUnit(int idx, uint8_t out[4])` | `0x278440`, 64 B | `u = &unit_table[idx*0x1e6]; out[0]=u->b[0x4f]; out[2]=u->b[0x50]; out[3]=0; out[1]=u->b[0x51]>>7;` — lê X/Y/flag de altura de uma unidade pelo índice. |
| `GetUnitOnPanel(const uint8_t panel[4])` | `0x276bb4`, 116 B | Faz o inverso: percorre até 21 slots do mesmo array (`stride 0x1e6`), pula slots com `b[1]==0xff` (vazio), compara `b[0x4f]`/`b[0x50]`/`(b[0x51]>>7)` contra `panel[0]/panel[2]/panel[1]`; retorna o índice do primeiro slot que bate, ou `21` ("não encontrado" = limite do laço). |
| `JudgeStatus(int threshold, BWORK* unit, int status_id)` | `0x276cd4`, 164 B | Calcula `byte_idx = floor(status_id/8)` e `bit = 0x80 >> (status_id mod 8)` (idioma clássico de divisão com sinal correta via `asr`/`lsr`); testa o bit em `unit->b[0x61+byte_idx]`. Se o bit não está setado → `false`. Se setado: `status_id==5` → compara `unit->b[0x17d]` contra `threshold` (campo copiado pelas funções da seção 9.1); `status_id>23` → sempre `true`; senão testa um segundo bit em `unit->b[0x57+byte_idx]` (status "permanente") → `true` se setado; senão compara `unit->b[0x4e+status_id]` (contador de duração por status, indexado direto, sem dividir por 8) contra `threshold` → `true` se `duração >= threshold`. |
| `BattleRoutineInit()` | `0x27a974`, 472 B | Ver seção 9.3 — troca de buffers (`BattleWork→spd_back`, `BworkBackup→spad_copy`), zera 3 flags em `sb+0x1980`/`sb+0x1800`, copia `gMapX` e um segundo byte não identificado para `sb+0xe3a`/`+0xe3b`, percorre as 21 unidades de `bwork` chamando `SetUnitParameter` e somando `halfword[0x31]`, grava a média saturada em `sb->b[0xe17]`, e por fim zera/seta mais alguns campos de estado (`sb+0x1800+{0x1c,0x20,0x24,0x28}`→`0xff`, `sb+0x1800+0xe10+4`(halfword)→`0x17f`, `sb+0xe16`→`1`). |

### 9.5 O que ainda falta nesta fila (estado real, não estimado)

- **`sub_275e3c`** (chamada por `0x2761ec`, dentro do próprio corpo de
  `BattleRoutine`, perto do fim — `BattleRoutine` vai de `0x274764` até
  `0x275ebc`, 5848 B) — não lida ainda.
- **`CheckUnitActionEffective`** (`0x276e4c`, 1828 B) e **`SetUnitParameter`**
  (`0x27a3bc`, 1464 B) — endereços/tamanhos confirmados nesta sessão, mas
  não desmontadas linha a linha ainda (são as duas maiores da lista
  "Fase 1+" que restam).
- **`GetDirectionOfAutoUnit`** (`0x279cc0`, 532 B) — endereço/tamanho
  confirmados, não lida ainda.
- **Tabela de 27 formatos de AoE** (`0x277bb0`) — não decodificada
  painel-por-painel ainda, mas a arquitetura em volta dela ficou mais
  clara nesta sessão: o jump table de 27 formatos filtra até 40 posições
  candidatas; as posições que sobram são resolvidas para registros de
  unidade reais e colocadas num array de até 21 "alvos atingidos" (mesmo
  stride `0x1e6`/21 da seção 9.3); o laço de pontuação em
  `EvaluationFunction` (`0x277b34`–`0x277d44`) então itera exatamente
  essas 21 entradas. Ainda não mapeei os 27 formatos em si (quais painéis
  cada um inclui).
- **Segundo byte copiado para `sb->b[0xe3b]`** em `BattleRoutineInit`
  (endereço do slot GOT ainda não resolvido para um nome).
- **Handlers isolados / CCRYPT / parser TIM / outros motores** — não
  tocados nesta sessão (prioridade média/baixa na fila); nada mudou em
  relação ao estado anterior.

Nenhum patch novo foi aplicado nesta sessão — tudo acima é só leitura
(read-only), feita no worktree `worktree-fft-re-loop` (branch separada da
`worktree-fft-ai-difficulty` usada nas sessões anteriores). O script de
desmontagem (`disasm.py`, agora usando `pyelftools` para mapear seções) e
o venv do capstone ficam em `/tmp`/scratch da sessão, fora do repositório.

## 10. `CheckUnitActionEffective` — desmontada por completo (2026-10-14, continuação)

Próximo item da fila. `CheckUnitActionEffective(int target_idx, int mode)`
(`0x276e4c`, 1828 B / ~452 instruções reais) é, de longe, a função mais
densa lida até agora — um "gabarito" de ~15 checagens de imunidade/
elemento/status que decidem se aplicar a habilidade atual no alvo
`target_idx` teria algum efeito. Lida por completo via Capstone; a seguir
o glossário de campos resolvidos e depois o pseudocódigo estrutural.

### 10.1 Novos globais/tabelas resolvidos (mesma técnica GOT da seção 9.2)

| Nome resolvido | Endereço | Tamanho | Papel observado no código |
|---|---|---|---|
| `aa` | `0x3cfbbc` | 5152 B | **Tabela mestra de habilidades**, stride de 14 bytes → **368 entradas exatas** (`5152/14=368`). Confirmado duas vezes de forma independente: pelo tamanho/stride do símbolo *e* por um guard explícito no código (`cmp r3,#0x170; bge ...` — `0x170=368`) antes de indexar a tabela. Nome curto ("ability array"?) — não vem de C++ mangling, então é nome C simples preservado no `.dynsym`. |
| `comtype` | `0x3cd9b8` | 256 B | Tabela de 1 byte por entrada (256 entradas), indexada por `g->b[0]` (primeiro byte do struct global de ação/habilidade, `g` = `*BattleWork`, ver seção 9.3). Comparada contra `0xa` (10) para decidir se um bloco extra de checagem elemental é pulado. Papel exato do valor 10 não confirmado. |
| (confirmação) `BattleWork`/`bwork` | — | — | Esta função lê os bytes do "ator/habilidade atual" a partir de `g = *BattleWork` (atualmente = `spd_back`, a cópia de trabalho da seção 9.3), mas lê os **dados do alvo diretamente de `bwork[target_idx]`** (o array real, não a cópia) — ou seja, o "autor da ação" é lido do buffer trocado, mas o "alvo" é lido do estado real. |

Chamadas confirmadas por nome (resolvidas no `.dynsym`): `JudgeStatus`
(`0x276cd4`, já desmontada na seção 9.4 — chamada aqui para os status
**5, 31(0x1f), 33(0x21), 34(0x22), 35(0x23) e 38(0x26)**, sempre com
`g->b[1]` como limiar), `GetCountToNextTurn(BWORK*)` (`0x27af10`, nova —
endereço/papel confirmados agora, corpo ainda não lido), `GetCountToDeath`
(`0x27b240`, já conhecida da seção 1) e `ps_rand()` (`0x28612c`, já
conhecida — usada aqui só uma vez, com um teste de 1 bit, então é um
sorteio efetivamente de 50%).

### 10.2 Pseudocódigo estrutural (fiel à lógica, com rótulos = endereços reais)

Convenção: `g` = `*BattleWork` (struct global do "ator/ação atual"); `t` =
`&bwork[target_idx]` (unidade alvo real); `row` = `g + target_idx*16 +
0x182c` (uma linha de 16 bytes por unidade, dentro do bloco `g+0x1800`);
`res` = o valor que a função devolve (o código usa o registrador ARM
`sb`/r9 como acumulador local de 2 bits — **não é o mesmo `sb` que uso nas
seções 1–9 para o ponteiro global**; troquei o nome aqui por `res` para
não confundir).

```c
int CheckUnitActionEffective(int target_idx, int mode) {
    if ((g->b[0x10] & 0x20) && row->b[8] == 0)      goto FALSE;
    if ((g->b[0x10] & 0x40) && row->b[8] != 0)       goto FALSE;
    if (g->b[0xe2e] == target_idx)                   goto SAME_TARGET;   // 0x277058

    if (mode != 0) goto MODE_NONZERO;                // 0x277030

MODE_ZERO:                                           // 0x276ecc
    if ((g->b[0xe] & 4) && JudgeStatus(g->b[1], t, 33)) goto FALSE;
    res = JudgeStatus(g->b[1], t, 5);
    if (res != 0) goto FALSE;

TURN_DISPATCH:                                       // 0x276f08
    int flagsByte = row->b[7];
    if (g->b[0xd] & 0x20) res = g->b[8];             // reaproveita g->b[8] (não row->b[8]!)
    else                  res = (res >> 5) & 1;
    if (flagsByte & 0x40) goto TURN_CHECK_A;          // 0x277084
    if (flagsByte & 0x20) goto TURN_CHECK_B;          // 0x2770a8

ELEM_GUARD:                                          // 0x276f34
    if ((int8_t)t->b[0x62] < 0) goto ELEM_GUARD_NEG;  // 0x277008
    if (JudgeStatus(g->b[1], t, 31)) goto FALSE;      // (sem exceção aqui, diferente da suposição inicial)

    if (g->b[0xd] & 0x20) {
        if (!(g->b[0xb] & 1)) goto FALSE;
    } else goto FALSE;                                // (replica o 'bne 0x277020' logo após o JudgeStatus(31))

    if (g->b[0x11] != 0) {
        int bits = g->b[0x11] & ~t->b[0x77];
        if (bits == 0) goto FALSE;
        if (g->b[0x11] == 8 && (t->b[0x63] & 0x40)) goto FALSE;
    }

ELEM_MAIN:                                           // 0x276f9c
    if (g->b[0xd] & 2) goto ELEM_BLOCK;               // 0x2770c8
    if (!(g->b[0xe] & 0x20)) goto ELEM_ALT;           // 0x27734c
    if (row->b[8] == 0) {
        if (t->b[0x61] & 0x10) goto TURN_CHECK_RESULT2;  // 0x2770f8 (res=2)
    } else {
        goto ALREADY_AFFECTED;                        // 0x277000: res=1, return
    }

    // (os blocos ELEM_BLOCK/ELEM_ALT/ELEM_GUARD_NEG/TURN_CHECK_RESULT2 se
    // interligam por mais ~12 saltos cruzados — ver tabela 10.3 para os
    // 4+4 ramos elementares/innate que eles cobrem; não reescrevi cada um
    // em C aqui porque o controle de fluxo real tem muito mais arestas
    // compartilhadas do que um `if/else` linear consegue representar sem
    // duplicar blocos)

    // Gabarito elemental principal (0x277148-0x2771c4): 5 iterações
    // (i=0..4) sobre g->b[7+i], cada uma testando
    // (g->b[7+i] & ~t->b[0x61]) e (g->b[7+i] & ~t->b[0x5c]); se alguma das
    // duas vira zero, salta para uma de 4 rotinas via jump table em
    // 0x277184 (índice = categoria-1, 0..3) que ajustam bits individuais
    // de uma máscara de trabalho (`r1`/mode) usando row->b[7]/b[0xc]/b[0xd]
    // e t->b[0x64]/b[0x65] — isto é o sistema clássico de afinidade
    // elemental de 4 estados (Absorve/Anula/Resiste/Fraco) sendo resolvido
    // elemento a elemento; eu não nomearia cada estado com certeza sem
    // cruzar com o layout de `aa[]`.

    // Segundo gabarito (0x2771f8-0x277264): outra iteração de 5 (i=0..4)
    // sobre g->b[7+i] contra t->b[0x61] (bits "ativos") e t->b[0x57]
    // (bits "permanentes" — os MESMOS dois arrays que `JudgeStatus` testa
    // em +0x61/+0x57!), com um dispatch de 3 vias por índice (0,1,>=2)
    // que vai acumulando/invertendo bits de `res`. É, na prática, o mesmo
    // tipo de checagem de status feita por `JudgeStatus`, mas iterando os
    // 5 bytes de categoria da habilidade em vez de um status_id único.

FINAL_DECISION:                                       // 0x277264/0x277294
    if (g->b[0xd] & 8) {
        uint16_t abilityId = g->h[2];                  // signed halfword em g+2
        if ((abilityId & ~4) != 0x76 && (abilityId & ~4) != 0x92) ; // bic/cmp combinados
        else if (!(ps_rand() & 1)) goto FALSE;          // ~50%: só para 2 IDs específicos (0x76=118, 0x92=146)
    }
    res = (g->b[0xd] >> 2) & 1;
    goto RETURN;                                        // 0x277024

TURN_CHECK_A:                                           // 0x277084
    if (g->b[1] < GetCountToNextTurn(t)) goto FALSE;
    if (res != 0) goto FALSE;
    goto TURN_DISPATCH_RETRY;                            // volta por row->b[7], 0x276f2c

TURN_CHECK_B:                                           // 0x2770a8
    if (g->b[1] > GetCountToDeath(t)) goto FALSE;
    if (res != 0) goto FALSE;
    goto ELEM_GUARD;                                     // 0x276f34

MODE_NONZERO:                                           // 0x277030
    if ((g->b[0xe] & 0x40) && JudgeStatus(g->b[1], t, 38)) goto FALSE;
    goto MODE_ZERO;                                      // 0x276ecc (reprocessa com mode "consumido")

SAME_TARGET:                                            // 0x277058
    {
        int16_t abilityId = g->h[2];                     // signed
        if (abilityId < 0x170 && (aa[abilityId].b[4] & 1))
            goto MODE_ZERO_ENTRY;                         // 0x276eb0 (reentra no fluxo normal)
        goto FALSE;                                       // ability fora da tabela aa[] OU bit não setado
    }

ALREADY_AFFECTED:  res = 1; goto RETURN;                 // 0x277000 (reaproveitado por ~15 saltos diferentes)
TURN_CHECK_RESULT2: res = 2; goto RETURN;                // 0x2770f8
FALSE: res = 0;                                          // 0x277020
RETURN: return res;                                      // 0x277024
}
```

**Honestidade sobre a cobertura:** os blocos `ELEM_BLOCK`/`ELEM_ALT`/
`ELEM_GUARD_NEG` (endereços `0x2770c8`, `0x27734c`, `0x277008`,
`0x277398`, `0x2773a4`) e os dois gabaritos de 5 iterações foram lidos
instrução por instrução (nenhum foi pulado), mas o grafo de desvios reais
tem mais arestas compartilhadas do que um `if/else` em C consegue
representar sem duplicar código — por isso optei por descrever esses
trechos em prosa (acima) em vez de forçar uma tradução C ambígua. Qualquer
revisão futura pode ir direto aos endereços citados.

### 10.3 Leitura de conjunto

Reforça o que a seção 9 já vinha mostrando: a "inteligência" da IA de FFT
não é uma fórmula única — é uma sequência de *gates* independentes
(imunidade a status, afinidade elemental de 4 estados, limiar de turnos
até a próxima ação do alvo, limiar de turnos até a morte do alvo, e um
sorteio de 50% só para 2 habilidades específicas) que, juntos, decidem se
vale a pena nem considerar aplicar a habilidade — antes mesmo de chegar à
pontuação real feita em `EvaluationFunction` (seção 6.4/9.1). A tabela
`aa[368]` (habilidades) e `comtype[256]` são os dois achados novos mais
reutilizáveis para trabalho futuro (ex.: qualquer patch que precise
indexar por habilidade usa `aa[]`, stride 14, base `0x3cfbbc`).

### 10.4 Próximo da fila
`SetUnitParameter` (`0x27a3bc`, 1464 B) e `GetDirectionOfAutoUnit`
(`0x279cc0`, 532 B) continuam pendentes (tamanhos/endereços já confirmados
desde a seção 9.5). `GetCountToNextTurn` (`0x27af10`, 204 B, nova nesta
sessão) ainda não foi lida. Nada mudado quanto a CCRYPT/TIM/outros
motores.
