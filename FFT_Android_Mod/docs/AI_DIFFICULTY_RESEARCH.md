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
| `ForAbnormalStatus` | `0x272254` | Decide ação quando a unidade está sob status alterado (passe estrutural completo via `jtable.py`: 100% cobertura, 0 tabelas de salto — ver `REVERSE_ENGINEERING_NOTES.md` seção 387) |
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
  erro de cálculo. Passe estrutural completo (100% cobertura, 0 tabelas de
  salto) refina isto: a função varre unidades próximas (`GetNearestUnit`
  ×3, `IsAlmostNullUnit` como filtro), constrói mapas de custo/alcance
  (`MakeMapCostToDest`, `MakeMapChantedAction`), escolhe um painel seguro
  (`SetSafePanel` ×2, `SetBaseTargetGroup`), monta a ação candidata
  (`SetTmp_UA`), usa `ps_rand()` pra desempate, e comete a decisão final via
  `sub_271628` (helper local sem símbolo — mesma rotina de "validar/
  comprometer-se com a ação" usada por outros handlers de IA: chama
  `GetDestinationsAndMakeMaskTG`, decrementa contador de tentativas em
  `unit[0xcbc]`, chama `SetThisDestination`).
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
globais para `sb->b[0xe3a]`/`sb->b[0xe3b]`. Ambos resolvidos por nome
(o segundo fechado na seção 12): `+0xe3a` ← **`gMapX`**, `+0xe3b` ←
**`gMapY`** (ambos 1 byte, endereços vizinhos `0x5808f5`/`0x5808f4`) — ou
seja, são as duas dimensões do mapa atual, dado de mapa, não de
dificuldade.

### 9.4 Outras funções nominais da fila, desmontadas por completo

| Função | Endereço/tamanho | Pseudocódigo (resumo fiel à leitura linha a linha) |
|---|---|---|
| `GetPanelUnderUnit(int idx, uint8_t out[4])` | `0x278440`, 64 B | `u = &unit_table[idx*0x1e6]; out[0]=u->b[0x4f]; out[2]=u->b[0x50]; out[3]=0; out[1]=u->b[0x51]>>7;` — lê X/Y/flag de altura de uma unidade pelo índice. |
| `GetUnitOnPanel(const uint8_t panel[4])` | `0x276bb4`, 116 B | Faz o inverso: percorre até 21 slots do mesmo array (`stride 0x1e6`), pula slots com `b[1]==0xff` (vazio), compara `b[0x4f]`/`b[0x50]`/`(b[0x51]>>7)` contra `panel[0]/panel[2]/panel[1]`; retorna o índice do primeiro slot que bate, ou `21` ("não encontrado" = limite do laço). |
| `JudgeStatus(int threshold, BWORK* unit, int status_id)` | `0x276cd4`, 164 B | Calcula `byte_idx = floor(status_id/8)` e `bit = 0x80 >> (status_id mod 8)` (idioma clássico de divisão com sinal correta via `asr`/`lsr`); testa o bit em `unit->b[0x61+byte_idx]`. Se o bit não está setado → `false`. Se setado: `status_id==5` → compara `unit->b[0x17d]` contra `threshold` (campo copiado pelas funções da seção 9.1); `status_id>23` → sempre `true`; senão testa um segundo bit em `unit->b[0x57+byte_idx]` (status "permanente") → `true` se setado; senão compara `unit->b[0x4e+status_id]` (contador de duração por status, indexado direto, sem dividir por 8) contra `threshold` → `true` se `duração >= threshold`. |
| `BattleRoutineInit()` | `0x27a974`, 472 B | Ver seção 9.3 — troca de buffers (`BattleWork→spd_back`, `BworkBackup→spad_copy`), zera 3 flags em `sb+0x1980`/`sb+0x1800`, copia `gMapX`/`gMapY` para `sb+0xe3a`/`+0xe3b` (fechado na seção 12), percorre as 21 unidades de `bwork` chamando `SetUnitParameter` e somando `halfword[0x31]`, grava a média saturada em `sb->b[0xe17]`, e por fim zera/seta mais alguns campos de estado (`sb+0x1800+{0x1c,0x20,0x24,0x28}`→`0xff`, `sb+0x1800+0xe10+4`(halfword)→`0x17f`, `sb+0xe16`→`1`). |

### 9.5 O que ainda falta nesta fila (estado real, não estimado)

- **`sub_275e3c`** (chamada por `0x2761ec` — fechada na seção 14.3:
  caracterizada como orquestrador de resultado de habilidade, não lida
  linha a linha).
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

### 10.4 Próximo da fila (concluído a seguir, seção 11)
`SetUnitParameter` (`0x27a3bc`, 1464 B) e `GetDirectionOfAutoUnit`
(`0x279cc0`, 532 B) continuam pendentes (tamanhos/endereços já confirmados
desde a seção 9.5). `GetCountToNextTurn` (`0x27af10`, 204 B, nova nesta
sessão) ainda não foi lida. Nada mudado quanto a CCRYPT/TIM/outros
motores.

## 11. `SetUnitParameter` — desmontada por completo (2026-10-14, continuação)

`SetUnitParameter(int unit_idx)` (`0x27a3bc`, 1464 B / ~366 instruções
reais). É a função que calcula os **parâmetros derivados** de uma
unidade a partir do(s) job(s) e equipamento atuais — não é "dano", é
"preparação de dados" na mesma linha das seções 9.1/10: alimenta a mesma
linha de 16 bytes por unidade (`row`, `g + unit_idx*16 + 0x1800+0x28`) que
`CheckUnitActionEffective` lê depois (seção 10.2 chama essa linha `row`,
offset `+4` relativo bate exatamente com o `+0x182c` usado lá).

### 11.1 Confirmações e tabelas

- **Sentinela de slot vazio confirmado de novo:** `bwork[unit_idx]->b[1]
  == 0xff` → retorno imediato, sem fazer nada. Mesmo sentinela de "slot
  vazio" já visto em `GetUnitOnPanel`/`GetPanelUnderUnit` (seção 9.4) e
  nos laços de 21 (seção 9.1/9.3) — está definitivamente confirmado como
  o padrão universal de "unidade inválida" em toda a base `bwork`.
- **Cap de 15** (`cmp r4,#0xf; bls`, em `g[unit_idx+0x1980+0xc]`): se esse
  byte (papel não identificado — contagem de algo por unidade) passar de
  15, a função não faz nada.
- **Tabela de jobs, stride 34 (`0x22`) confirmado por dois ângulos
  independentes:** o multiplicador `mul r4,#0x22,r4` (linha `0x27a464`)
  *e* o limite de laço `cmp sl,#0x22` (34 iterações, linhas `0x27a5fc`/
  `0x27a628`) apontam para a mesma tabela de 34 bytes por job — não
  resolvi o nome do símbolo desta tabela (fica dentro de `g`/`sl`, não é
  um global GOT separado desta vez), mas o stride 34 é inequívoco.
- `pspItemIsEmpty` (`0x2855b8`, já no `.dynsym` com esse nome exato) é
  chamado para os dois slots de equipamento da unidade
  (`bwork->h[0x20]` e `bwork->h[0x24]`, halfwords — prováveis IDs de arma/
  escudo).
- `SetTmp_UA(UnitAction*)` (`0x273378`, 1220 B, nome confirmado no
  `.dynsym`) é chamado uma vez por slot de habilidade de job "aprendível"
  dentro do laço de 34 — ou seja, o laço está de fato relacionado a
  habilidades de job (reforça a leitura de "contagem/registro de
  habilidades aprendidas").
- Dois helpers sem nome, ambos chamados por esta função e **grandes o
  suficiente para merecer item próprio na fila**: `0x279f8c` (1072 B,
  logo antes do início de `SetUnitParameter` no binário — chamado quando
  a unidade ainda não tem job secundário definido, `g->b[0x12]==0`) e
  `0x279ac4` (172 B, logo depois do fim de `FundamentalRoutine` — chamado
  depois de cada checagem `pspItemIsEmpty` bem-sucedida, com `r0=row,
  r2=&contador_local`, parece acumular flags de categoria de arma/
  equipamento).

### 11.2 Pseudocódigo estrutural

```c
int SetUnitParameter(int unit_idx) {
    BWORK* u = &bwork[unit_idx];                 // registrador ARM "sb" (r9) — não confundir com o global g
    if (u->b[1] == 0xff) return;                 // slot vazio

    uint8_t cap = g[unit_idx + 0x1980 + 0xc];     // papel exato não identificado
    if (cap > 15) return;

    row = &g[unit_idx*16 + 0x1828];               // mesma linha de 16 B usada em CheckUnitActionEffective (+4)
    uint8_t job2 = u->b[0x12];                    // job secundário (0 = nenhum)

JOB_LOOP_ENTRY:                                   // 0x27a41c
    if (((job2 + 0x50) & 0xff) > 0x2f) goto NO_SUB_JOB;   // 0x27a68c

    if (job2 == 0) {
        r2 = SetUnitParameter_helper_0x279f8c(unit_idx);   // ainda não lido
        goto JOB_LOOP_ENTRY2;                              // 0x27a444, reprocessa com r2 pronto
    }
    // job2 != 0: valida a segunda faixa (sb->b[0x13]) do mesmo jeito;
    // se inválida, chama o MESMO helper 0x279f8c de novo (0x27a8fc)

    // --- laço de 34 (0x22) entradas da tabela de job ---
    for (sl = 0; sl < 0x22; sl++) {
        ability_slot = &g[... + sl*0x22*4 + 0x3bc];  // endereçamento por *4 (word) dentro da tabela de job
        if (ability_slot->b[2] == 0xff) goto NEXT;    // slot de habilidade vazio
        if (<condições de nível/flag em sl,u->b[4],u->b[5]>) {
            SetTmp_UA(ability_slot);                   // 0x273378
            ability_slot->b[3] |= 2;                   // marca habilidade "registrada"
        }
        <contadores r3(sp+8), sb(r9), fp acumulam 1 cada
         conforme bits 0x1/0x2/0x8 de g->b[0xe]/[0xf]>;
        ability_slot->b[3] &= ~7;
        if (g->b[0xf] & 0xc0) continue;    // volta pro topo do laço sem avançar sl de verdade
        if (!(g->b[0xf] & 0x3c)) continue; // idem
        ability_slot->b[3] |= 4;
    }
    // fim do laço: 3 divisões (__aeabi_idiv) escalando os 3 contadores
    // por 4 e dividindo pelo contador `fp` -> percentuais, gravados em
    // row->b[0xc], row->b[0xb] e numa 3ª variável local (0xff-saturada).
    row->b[0xd] = <percentual final>;

    // --- bloco de equipamento (só quando havia job2, i.e. "tem sub-job") ---
    MemCpyB(row+4, g[unit_idx+0x188+1 ...], 5);          // copia 5 bytes de config de volta pra row+4..8
    row->b[1] = g->b[0x189] >> 7;
    row->b[2] = g->b[0x188];
    row->b[3] = 0;
    if (row->b[4] & 8) {
        if (!(row->b[7]>>2 & 1)) {
            if (row->b[4] & 0x40) {
                // varre até 21 unidades de bwork (mesmo stride 0x1e6!)
                // procurando outra unidade com b[0x180]==row->b[5]
                // ("unidade única" já usada por outro slot?) — se achar,
                // vai para o tratamento de duplicata (abaixo); senão,
                // depois de varrer as 21, limpa o bit 3 de row->b[4].
            }
        }
    }

EQUIP_SLOTS:                                       // 0x27a82c
    for (int slot : {0x20, 0x24}) {                 // dois halfwords de item em u
        int item = u->h[slot];
        if (!pspItemIsEmpty(item)) {
            helper_0x279ac4(row, &local_counter);   // acumula flag de categoria de arma
        }
    }
    switch (local_counter) {                        // 5 vias (0..4), jump table em 0x27a884
        case 0: row->b[1] |= 1; row->b[2] |= 0x20; break;        // 0x27a8f0/0x27a8a0
        case 1: row->b[1] |= ... ; goto 0x27a700;                // reentra no fluxo de "unidade única" acima
        case 2: row->b[1] |= 2; row->b[2] |= 0x20; break;        // 0x27a8c4
        case 3: goto 0x27a700;                                   // mesma reentrada do caso 1
        default: row->b[1] |= 1; break;                          // >4 ou não resolvido -> 0x27a95c
    }

DUP_FOUND:                                          // 0x27a90c
    row->b[5] = local_counter & 0xff;
    if (u->b[4] & 0x10) {
        uint8_t a = u->b[0x1de];
        uint8_t b = bwork[other_idx]->b[0x1de];
        u->b[0x1dd] = row->b[5];
        row->tag = ((a ^ b) & 0x30) ? 0xc : 0xe;    // 0x21 do bloco g[idx+0x1980]
    }
    return;
}
```

**Cobertura:** lido instrução por instrução do início ao fim (não há
trecho pulado), mas — como em `CheckUnitActionEffective` — os blocos do
laço de equipamento/duplicata (`0x27a6b4`–`0x27a95c`) têm desvios
cruzados que não cabem num `switch` limpo sem duplicar casos; descrevi
esses trechos em prosa onde a tradução literal ficaria ambígua. Os dois
helpers sem nome (`0x279f8c`, `0x279ac4`) e `GetDirectionOfAutoUnit`
continuam na fila sem leitura própria.

### 11.3 Relevância para o objetivo do projeto (dificuldade)
Nenhum patch óbvio de "dificuldade" apareceu aqui — isto é majoritariamente
contabilidade de habilidades de job e categoria de equipamento, não
poder de combate bruto. O candidato mais interessante continua sendo a
tabela de 34 bytes/job (ainda sem nome de símbolo) se algum dia for
necessário ajustar crescimento de atributo por job; não persegui isso
agora porque sairia do escopo do item da fila.

### 11.4 Próximo da fila (concluído a seguir, seção 12)
`GetDirectionOfAutoUnit` (`0x279cc0`, 532 B) é o único item "Fase 1+"
nomeado que ainda não foi lido. Os dois helpers sem nome descobertos
nesta sessão (`0x279f8c`, 1072 B; `0x279ac4`, 172 B) e `GetCountToNextTurn`
(`0x27af10`, 204 B, da seção 10) ficam como itens novos na fila, ainda
sem leitura. Nada mudado quanto a CCRYPT/TIM/outros motores.

## 12. `GetDirectionOfAutoUnit` — desmontada por completo (2026-10-14, continuação)

Último item nomeado da lista original "Fase 1+". `GetDirectionOfAutoUnit()`
(`0x279cc0`, 532 B, sem parâmetros, confirma o que a seção 1 já indicava)
decide **para qual dos 4 lados cardeais a unidade controlada pela IA deve
ficar de frente**, combinando alcance de movimento, obstáculos de terreno
e para onde o alvo/aliado mais próximo está.

### 12.1 Novos globais resolvidos

| Nome | Endereço | Tamanho | Papel |
|---|---|---|---|
| `gMapY` | `0x5808f4` | 1 B | Fecha o item pendente da seção 9.3/9.5 — é o byte-irmão de `gMapX` (`0x5808f5`), copiado para `sb->b[0xe3b]` por `BattleRoutineInit`. Dimensão Y do mapa atual. |
| `block` | `0x565db8` | 4096 B | Array de dados de terreno por painel, stride de 8 bytes → **512 entradas** (`4096/8`). Indexado como `(Y*gMapX + X)*8` — bate exatamente com o "índice de tile" clássico documentado pela comunidade de RE do FFT original (PSX) para a tabela de blocos do mapa. Campo `+2` = altura do painel; campo `+6` = flags de passabilidade (bit 0 = impassável nesta leitura). |
| (tabela de deltas, sem símbolo próprio) | `0x3e94c0` | 8 B | 4 pares de bytes com sinal: `(0,-1) (-1,0) (0,1) (1,0)` — Norte, Oeste, Sul, Leste nessa ordem. Define os 4 candidatos de direção testados. |

Chamadas confirmadas por nome: `GetPanelUnderUnit` (`0x278440`, seção
9.4), `GetNearestUnit(int tipo)` (`0x27207c`, já citada na seção 1 — aqui
chamada com `tipo=1` e, se o resultado coincidir com o alvo já cacheado,
de novo com `tipo=2` — forte indício de que 1="inimigo mais próximo" e
2="aliado mais próximo", mas o `enum` em si não foi confirmado lendo
`GetNearestUnit`), e `GetDirectionForPanel(int8_t*, int8_t*)` (`0x271504`,
nova — calcula a direção cardeal entre dois painéis, corpo ainda não
lido).

### 12.2 Pseudocódigo

```c
int GetDirectionOfAutoUnit(void) {
    if (g[0x17ff] != 5) return;   // só roda numa fase/estado específico da IA

    int target = g->b[0xe2e];                    // "alvo atualmente cacheado" (mesmo campo da seção 9.1/10/11)
    GetPanelUnderUnit(target, &g->b[0xe30]);      // preenche g+0xe30 = {X, alturaFlag, Y, 0} do painel do alvo

    uint8_t X = g->b[0xe30], dirFlag = g->b[0xe31], Y = g->b[0xe32];
    uint8_t mapX = g->b[0xe3a] /*gMapX*/, mapY = g->b[0xe3b] /*gMapY*/;
    int baseIndex = ((mapX * Y + (dirFlag << 8)) + X) << 3;   // índice (com bit de altura) dentro de `block`

    int fallback = 0;                              // registrador r6: última direção válida encontrada
    bool valid[4];
    for (int i = 0; i < 4; i++) {
        int8_t dx = delta[i][0], dy = delta[i][1];
        uint8_t nx = (X + dx) & 0xff, ny = (Y + dy) & 0xff;
        if (nx >= mapX || ny >= mapY) { valid[i] = false; continue; }   // fora do mapa
        int idx = ny * mapX + nx;
        if (block[idx].b[6] & 1) { valid[i] = false; continue; }         // painel impassável
        if (abs(block[idx].b[2] - block[baseIndex/8].b[2]) > 2) { valid[i] = false; continue; } // diferença de altura > 2
        valid[i] = true;
        fallback = i;                                                    // guarda a última válida encontrada
    }
    // (efeito colateral observado, não totalmente investigado: a função
    // também zera/inicializa ~17 bytes em g+0xca0.. e g+0xc80+0xc.. nesta
    // mesma passada — parece reaproveitar o mesmo trecho de código para
    // resetar algum estado de alcance/alvo auxiliar, não só direção)

RETRY:                                              // 0x279ce4 é o epílogo normal (não um loop!)
    int nearest = GetNearestUnit(1);
    uint8_t panelBuf[4];
    if (nearest == target) {
        nearest = GetNearestUnit(2);
        GetPanelUnderUnit(nearest, panelBuf);
        dir = GetDirectionForPanel(panelBuf, &g->b[0xe30]);
    } else {
        GetPanelUnderUnit(nearest, panelBuf);
        dir = GetDirectionForPanel(panelBuf, &g->b[0xe30]);
    }
    if (!valid[dir]) return;                        // direção calculada bate com um lado bloqueado -> aborta (retorno "indefinido")
    g->b[0xc8d + dir] = 0;                           // zera uma flag por direção (papel exato não confirmado)

    BWORK* u = *(BWORK**)(g + 0x17f8);                // ponteiro interno de g para a unidade controlada
    int curDir = u->b[0x51] & 0xf;                    // nibble baixo do mesmo campo "+0x51" usado em GetPanelUnderUnit/GetUnitOnPanel
    return valid[curDir] ? curDir : fallback;          // mantém a direção atual se ainda for válida; senão usa o fallback do laço de 4
}
```

**Cobertura:** lida instrução por instrução do início ao fim. Os três
saltos `bne/beq 0x279ce4` e o `b 0x279ce4` **não formam um laço** — todos
caem direto no epílogo da função (`add sp,...; pop {...}; bx lr`); a
leitura inicial de que seria um "retry loop" estava errada e foi corrigida
antes de escrever este pseudocódigo. O efeito colateral em `g+0xca0`/
`g+0xc8c` não foi totalmente explicado — fica como observação, não como
fato confirmado.

### 12.3 Estado da fila "Fase 1+" original
Com esta seção, **todas as 7 funções nomeadas originalmente na fila**
(`BattleRoutine`¹, `CheckUnitActionEffective`, `SetUnitParameter`,
`GetUnitOnPanel`, `JudgeStatus`, `GetDirectionOfAutoUnit`,
`BattleRoutineInit`) foram desmontadas pelo menos uma vez nesta e nas
sessões anteriores. ¹`BattleRoutine` em si (o corpo principal, não as 3
estáticas internas da seção 9.1) ainda não foi lida linha a linha — só
suas 3 estáticas internas e o fato de que `sub_275e3c` mora no seu próprio
corpo. Fica como item aberto.

### 12.4 Próximo da fila (todos fechados nas seções 13–14)
Itens que estavam pendentes aqui — `BattleRoutine` (corpo principal),
`sub_275e3c`, `GetCountToNextTurn`, `GetDirectionForPanel`, e os dois
helpers de `SetUnitParameter` — foram todos processados nas seções 13 e
14. Prioridade média/baixa (CCRYPT, parser TIM, outros motores) continua
sem alteração — ver seção 15 para o estado completo da fila original.

## 13. Quatro itens pequenos/médios fechados em sequência (2026-10-14, continuação)

Sessão disparada por "continua até a conclusão total" — varrendo o resto
da fila que ainda tinha endereço conhecido antes de atacar o corpo
principal de `BattleRoutine` (maior peça que falta).

### 13.1 `GetDirectionForPanel(int8_t* a, int8_t* b)` — `0x271504`, 156 B, completa

Calcula a direção cardeal de `b` em relação a `a`, usando os bytes `[0]`
(X) e `[2]`(Y) de cada painel. Com `dx = Xb-Xa`, `dy = Yb-Ya`, calcula
`r2 = dx-dy` e `r3 = -(dx+dy)` (rotação de 45° clássica para achar
quadrante) e devolve:

| Condição | Retorno |
|---|---|
| `r2<=0 && r3<0` | `0` (Norte — bate com a tabela de deltas `(0,-1)` da seção 12.1) |
| `r2<=0`, senão | `1` (Oeste, `(-1,0)`) |
| `r2>0 && r3<=0`, fora de um caso-limite | `2` (Sul, `(0,1)`) |
| caso-limite (`r2>0 && r3>0`, ambos "zero-ish") | `3` ou `4`, dependendo do sinal residual de `r2`/`r3` |

**Achado curioso, não totalmente explicado:** existe um 5º valor de
retorno (`4`) para o caso-limite. Em `GetDirectionOfAutoUnit` (seção
12.2) esse valor acaba indexando `sp+0x14+4 = sp+0x18`, que é exatamente
o byte seguinte ao array de 4 validades (`valid[0..3]`) — ou seja, lê
"lixo" de pilha (na prática, o primeiro byte do buffer de painel reusado)
em vez de um 5º slot de validade real. Não sei se isso é intencional no
código original (ex.: o código-fonte original também só previa 4
direções e o `case 4` nunca ocorre na prática por construção dos dois
pontos de entrada) ou um artefato de como o compilador layoutou a pilha.
Fica como observação, não como bug confirmado.

### 13.2 `GetCountToNextTurn(BWORK* u)` — `0x27af10`, 204 B, completa

Implementa a fórmula clássica de **tempo até a próxima ação** (CT/Charge
Time) do FFT original: `ceil((100 - u->b[0x41]) / u->b[0x40])`, com vários
*gates* de status que a tornam "infinita" (retorna `INT_MAX`):

```c
int GetCountToNextTurn(BWORK* u) {
    if (u->b[0x40] == 0) return INT_MAX;                 // velocidade zero -> nunca age
    if (u->h[0x61] & 0x8140) return INT_MAX;              // status que impedem agir (bits 0x40/0x8000 combinados)
    row = &g[u->b[1]*16 + 0x1828];                         // u->b[1] = índice da própria unidade (auto-referência!)
    if (row->b[0xb] & 0x20) return INT_MAX;                // flag calculada por SetUnitParameter (seção 11)

    r6 = (u->b[0x64] & 2) ? u->b[0x6c] : u->b[0x64];        // "velocidade efetiva" alternativa quando uma flag está setada
    if (u->b[0x41] <= 0x63) {
        int rem = 0x64 - u->b[0x41];                        // 100 - CT_atual
        r6 += rem / u->b[0x40];                              // __aeabi_idiv
        if (rem % u->b[0x40] != 0) r6 += 1;                  // __aeabi_idivmod -> arredonda para cima
    }
    if (u->b[0x61] & 0x20) return r6;
    if (u->b[0x65] & 0x10) return max(u->b[0x71], r6);       // status impõe um mínimo de turnos de espera
    return r6;
}
```

Confirma — com fórmula explícita, não só por nome — que `JudgeStatus`/
`CheckUnitActionEffective` (seções 9.4/10) e esta função compartilham os
mesmos dois arrays de flags de status (`+0x61`/`+0x65` nesta função, que
correspondem a `t->b[0x61]`/`t->b[0x65]` lá). `__aeabi_idivmod`
(`0x2ca878`, nome confirmado no `.dynsym`) é a mesma rotina de divisão
usada em quase toda a aritmética de dano/pontuação já vista — aqui, pela
primeira vez, usada explicitamente para obter o **resto** (arredondamento
para cima).

### 13.3 Os dois helpers de `SetUnitParameter`

**`0x279ac4` (172 B) — completa, achado forte:** `ClassifyWeaponCategory
(row, itemId, int* counterFlags)`. Chama `pspItemGetWeaponData` (nome
exato confirmado no `.dynsym` — fecha de vez a suspeita da seção 11.2
sobre "categoria de arma"). Se o item não é arma (bits `0x10`/`0x20` do
byte `+1` dos dados da arma ambos zero) — não faz nada. Senão marca
`row->b[3]` (bit `0x80` ou `0x40`, dependendo de qual dos dois bits) e
acumula em `*counterFlags` um de `{1,2,4}` conforme o campo `+2` dos dados
da arma vale `{outro,6,7}` — e grava `row->h[4]=itemId`, `row->b[0]=
arma->b[0]`, `row->b[6] |= arma->b[6]`. É exatamente a tabela que
`SetUnitParameter` consome no `switch` de 5 vias da seção 11.2.

**`0x279f8c` (1072 B) — lida, estrutura confirmada, 3 ramos de categoria
não desmontados linha a linha:** `ResolveDefaultJobAbilities(int
unit_idx, int job_or_group_id, int* out)`, chamada por `SetUnitParameter`
só quando a unidade **não tem job secundário** (`g->b[0x12]==0`, seção
11.2). Fluxo confirmado:
1. `get_ability(job_or_group_id, 1)` (`0x1d82a8`, nome confirmado)
   devolve um ponteiro para uma lista de até **16** IDs de habilidade
   (halfwords, terminada por `0`).
2. Lê um byte de categoria indexado por `job_or_group_id` numa tabela
   ainda não nomeada e despacha para um de 3 ramos
   (`categoria==2→0x27a240`, `==3→0x27a348`, `==10→0x27a384`) ou segue no
   fluxo principal para qualquer outro valor.
3. No fluxo principal: para cada uma das 16 entradas da lista, testa o
   bit 7 do campo `+7` de `aa[ability_id]` (tabela mestra de habilidades,
   seção 10.1); se setado e `ability_id<=367` (limite de `aa[]`, igual ao
   visto na seção 10), compara `aa[ability_id].b[0xd]` (às vezes
   dividido por 2) contra um campo da própria unidade (`u->h[0x36]`) e
   contra duas flags adicionais (`g->b[0xe]&4`, `u->b[0x5b]&0x40` /
   `aa[ability_id].b[6]&8`+`u->b[0x1a6]&8`) — quando tudo bate, chama
   `CheckAbilityGet(unit_idx, ability_slot, loop_index)` (`0x279b70`,
   nome confirmado, corpo ainda não lido).
4. Devolve `*out` inalterado nos casos simples, ou um valor derivado de
   `loop_index`/da condição `categoria==9` num dos desvios finais —
   **esse detalhe final não foi confirmado com certeza**.

Os 3 ramos de categoria (`0x27a240`/`0x27a348`/`0x27a384`) **não foram
lidos** — cada um é uma variação do mesmo padrão de "percorrer a lista de
16 e chamar `CheckAbilityGet`", mas com condições de entrada diferentes;
dado que esta função já é claramente contabilidade de habilidades padrão
(não combate), não persegui os 3 ramos até o fim nesta passada — ficam
na fila caso seja necessário no futuro.

### 13.4 Próximo da fila
O item grande que resta da lista original é o **corpo principal de
`BattleRoutine`** (`0x274764`–`0x275e3c`, 5848 B — corrige um erro de
aritmética hexadecimal das seções 9.5/11.2/12.3, que diziam `0x275ebc`)
— ver seção 14.

## 14. `BattleRoutine` — corpo principal mapeado por completo (2026-10-14, continuação "até conclusão total")

**Correção de endereço:** `0x274764 + 5848 = 0x275e3c`, não `0x275ebc`
como as seções anteriores diziam (erro de soma hexadecimal manual). Isso
na verdade resolve uma dúvida em aberto: `0x275e3c` é exatamente o
endereço de `sub_275e3c` (seção 9.1) — ou seja, o tamanho de símbolo
"errado" de `BattleRoutine` não inclui as 3 estáticas de dano (seção 9.1),
só o próprio `sub_275e3c` (ver 14.3).

**Problema técnico resolvido:** a desmontagem linear ingênua (mesma
técnica usada em todas as funções anteriores) parava em `0x274c20`, bem
antes do fim — não porque o resto fosse dado, mas porque `BattleRoutine`
tem blocos de código alcançáveis **só por salto** (não por sequência),
com pequenos "poços" de literal pool intercalados que o Capstone não
decodifica como ARM válido e por isso aborta o laço linear. Escrevi uma
segunda versão do desmontador (`disasm_cfg.py`) que segue os alvos de
`b`/`bl` recursivamente (descida recursiva simplificada) — com isso, 1453
das ~1462 instruções do intervalo relatado foram decodificadas (quase
tudo é código real, não dado).

### 14.1 Estrutura de despacho confirmada (lida por completo)

`BattleRoutine(int unit_idx, ActionRequest* out)` é, no topo, **um
dispatcher de fase** com duas variáveis de estado diferentes das de
`FundamentalRoutine` (que usa `unit[0xc70]`, seção 6):

```c
int BattleRoutine(int unit_idx, ActionRequest* out) {
    if (VSync(1) > 0x1b8) return -1;                 // mesmo timeout de 440 "ticks" visto em EvaluationFunction

    if (!(g->b[0x19b7])) {                            // g->b[0x1980+0x37] — "modo IA ativo"?
        goto NOT_THINKING;                             // 0x274938 — ver 14.2
    }

    switch (g->b[0xed4]) {                            // fase própria de BattleRoutine
    case 0:  goto PHASE0;                              // 0x274c5c — chama EvaluationFunction! (14.2)
    case 1:  goto PHASE1;                              // 0x27537c — maior bloco não lido em detalhe (~1232 B)
    case 2:
        switch (g->b[0xc6d]) {                         // sub-fase dentro da fase 2
        case 0: return ForAbnormalStatus();            // 0x272254 — já conhecida (seção 1)
        case 2: return DattoNoGotokuNigeyoRoutine();    // 0x27286c — NOVA: rotina de "fuga" (nome japonês preservado)
        case 3: return ForAutoCommand();                // 0x272aac — NOVA: comando automático genérico
        default:
            int r = MainBattleRoutine();                 // 0x27426c — a mesma MainBattleRoutine que (supostamente) chama BattleRoutine!
            if (r == -1) { g->b[0xc6d] = 7; goto TURN_DONE; }  // 0x275ddc
            goto FINALIZE;                               // monta o ActionRequest de destino e retorna 0 (14.4)
        }
    default: goto NOT_THINKING;
    }
}
```

**Achado notável, ainda sem explicação completa:** o ramo "senão" da
fase 2 chama `MainBattleRoutine` — a mesma função que a seção 1 (há
sessões) descreveu como "laço principal de IA por turno" que, por nome,
se esperaria que fosse a *chamadora* de `BattleRoutine`, não o contrário.
Pode ser uma re-entrada legítima (ex.: `BattleRoutine` devolve controle
ao laço principal para processar a próxima sub-ação dentro do mesmo
turno) ou minha suposição antiga sobre a direção de chamada de
`MainBattleRoutine` estar incompleta. **Não resolvido nesta sessão** —
precisaria ler `MainBattleRoutine` (`0x27426c`) para confirmar.

### 14.2 Bloco "não pensando" (`0x274938`–`0x274c5c`, ~772 B, lido por completo) — chama `EvaluationFunction` diretamente

Confirma, pela primeira vez com endereço exato, **que `BattleRoutine`
chama `EvaluationFunction` diretamente** (`bl 0x277720`, em `0x274c5c`) —
até agora só sabíamos que `SetBestMove`/`SetBMList` a chamavam (seção
6.3). Ou seja, `BattleRoutine` tem pelo menos dois caminhos até a
avaliação de jogada: via a cadeia `FundamentalRoutine→SetBestMove→
EvaluationFunction` (seção 6) e via este atalho direto quando
`g->b[0xed4]==0`.

### 14.3 `sub_275e3c` (`0x275e3c`–`0x2761ec`, 944 B — corrigido na seção 19, era dito 2992 B por engano) — caracterizada, não lida linha a linha

Chamada por `0x2761ec` (a "estática de cache elemental", seção 9.1) e
**recursiva** (chama a si mesma uma vez). Lista de chamadas confirmadas
no `.dynsym` deixa o papel bem claro — é o **orquestrador de resolução de
resultado de habilidade**:

| Chamada | Papel (pelo nome) |
|---|---|
| `getskillresult_main(int, SKILL_RESULT*)` | Calcula o resultado principal de uma habilidade |
| `getskillresult_first(int)` | Primeira fase do cálculo de resultado |
| `setskillresult(int)` | Aplica o resultado (já citada na seção 6.3) |
| `setskillresult_caster(int)` | Aplica efeitos no próprio conjurador |
| `afterskillhandle(BWORK*)` | Pós-processamento após a habilidade |
| `getreaction_post(uint16_t*)` | Resolução de habilidade de Reação |
| (PLT, `0x715cc`) | Import não identificado (índice do `.rel.plt` não resolvido) |

Isso explica exatamente por que o cache elemental de `0x2761ec` depende
dele: para saber o elemento/afinidade relevante, primeiro é preciso saber
**qual resultado de habilidade está sendo resolvido agora**. Não desmontei
linha a linha (748 instruções estimadas) — ficaria como item de fila
separado se algum dia for necessário.

### 14.4 Cauda "finalizar destino" (vários pontos de entrada convergem em `0x2748d8`)

Pelo menos 4 pontos diferentes do dispatcher (`0x275acc`, `0x275b10`,
além do fluxo principal) convergem no mesmo bloco de finalização, que:
grava um código em `*out` (valores `0` ou `2` observados), empacota os
campos de `g+0x1800..1802` e `unitPtr->b[0x1a9]/[0x1aa]` num pacote de 24
bytes via duas chamadas a `MemCpyW` (`0x279c34`, já conhecida), chama
`SetThisDestination(&g->b[0xe30])` (já conhecida, seção 1), e retorna.
Ou seja: **todo mundo que "termina de decidir o que fazer" passa por
aqui** para empacotar a decisão no `ActionRequest` de saída.

### 14.5 O que NÃO foi lido (honestidade de cobertura)
`BattleRoutine` tem ~1453 instruções reais. As partes com pseudocódigo
confirmado nesta seção cobrem o dispatcher de topo e os dois blocos de
borda (14.2, 14.4) — uma fração minoritária do total. **Os blocos
internos de cada fase** (principalmente a "Fase 1", `0x27537c`–
`0x27584c`, ~1232 B, o maior bloco não lido da função) e um bom número de
sub-blocos menores (`0x275d58`, `0x2756ec`, `0x275254`, `0x2755f0`,
`0x275890`, entre outros, vistos de passagem nos saltos mas não
desmontados) **não foram traduzidos para pseudocódigo** nesta sessão.
Dado que os 3 comportamentos de fase-2 mais interessantes
(`ForAbnormalStatus`, a rotina de fuga, `ForAutoCommand`) já são funções
*próprias e nomeadas* (não inline aqui), o valor marginal de desmontar o
resto do dispatcher de `BattleRoutine` linha a linha é mais baixo do que
foi para `CheckUnitActionEffective`/`SetUnitParameter` — mas fica
registrado como trabalho pendente, não como "concluído".

## 15. Item "tabela de AoE de 27 formatos" — revisitado, premissa corrigida

Voltando ao item 3 da fila original ("Tabela de AoE: decodificar o
array/matriz dos 27 formatos... mapear os bytes de filtro de posição
painel por painel"). A tabela de salto de 27 casos em `0x277bb0`
(mencionada desde a seção 6.4/9.5) existe mesmo nesse endereço exato —
mas uma leitura mais cuidadosa nesta sessão mostra que **a premissa do
item estava errada**: não é uma tabela de 27 *formatos espaciais* de
área de efeito. É outra coisa.

### 15.1 O que o laço de `0x277b34`–`0x277c44` realmente é

Este é o **mesmo laço de pontuação por alvo** já documentado em detalhe
nas seções 6.4/9.3 (o laço externo de até 21 candidatos, variável `fp`).
Dentro dele, o laço interno de `r3=0..39` (`cmp r3,#0x28`, 40 iterações —
isto sim bate com "40 posições" das notas antigas) **não itera painéis
do tabuleiro**: itera os **40 bits de status possíveis** do alvo atual,
lendo-os do mesmo bitmap de 5 bytes (`target->b[0x61..0x65]`) que
`JudgeStatus`/`CheckUnitActionEffective`/`GetCountToNextTurn` já usam
(`byte = r3>>3`, `bit = r3&7` — o idioma exato de bit-index visto nessas
três funções). A tabela de salto em `0x277bb0` (`ip = r3-10`, 28 casos,
`0..0x1b`) só existe para dar tratamento especial a 28 dos 40 bits de
status (índices 10–37) — a maioria desses 28 casos (19 deles) salta
direto para o mesmo acumulador genérico (`0x277c3c`), e só uns poucos
(índices relativos 1,2,3,4 → bits de status 11-14; e 24,25 → bits 36,37)
vão para blocos próprios (`0x277db0`/`0x277dd4`/`0x277df0`/`0x277c28`,
nenhum lido em detalhe nesta sessão).

### 15.2 `SV` — a tabela real que estava sendo procurada (mas não é espacial)

Resolvida por nome via a mesma técnica GOT das seções anteriores:
**`SV`** (`0x3e94c8`, 80 bytes = **40 halfwords**, um por bit de status)
— quase certamente "Status Value": o peso que a IA dá a infligir (ou
curar) cada um dos 40 status possíveis. É isso que o acumulador genérico
soma (`r6 += SV[statusBit]`) para cada bit de status que a habilidade
afeta no alvo — **não** um peso por painel.

### 15.3 Conclusão sobre o item da fila
**Não existe, neste ponto do código, uma tabela de 27 formatos espaciais
de área de efeito indexados painel-por-painel.** O que existe é uma
tabela de pontuação por *status* (`SV[40]`) com 28 casos especiais
tratados por salto. A geometria real de "quais painéis uma habilidade
afeta" (a parte que o item 3 originalmente queria mapear) deve estar em
`GetTargetBaseArea(int,int)` (`0x276930`, 644 B) ou
`GetDestinationsAndMakeMaskTG` (`0x278480`, 1932 B) — ambas já nomeadas
desde a seção 1/6.1 mas **nenhuma das duas foi lida nesta sessão**. Ficam
como o alvo correto para qualquer trabalho futuro de "decodificar a
área de efeito painel a painel" — o endereço `0x277bb0` citado nas notas
anteriores não é mais o lugar certo para procurar isso.

## 16. Estado completo da fila original (backlog do pedido inicial) — 2026-10-14

Varredura final dos 8 itens originais da tarefa, para dar uma resposta
honesta a "continue até a conclusão total".

### Prioridade Alta

1. **Os 3 Callers de Dano Base** — ✅ Concluído (seção 9.1). Achado:
   não são fórmula de dano; são preparação de dados (cache elemental +
   2 montadores de tabela via `MemCpyB`/`MemCpyW`). A aritmética de dano
   real está inline em `EvaluationFunction` (seções 6.4/9.3).
2. **Variáveis Globais da Simulação (3 campos salvos/restaurados)** — ✅
   Concluído (seção 9.2). Resolvidas por nome: `_binary_record_bin`,
   `scritem`, `pagewinInf` — estado de UI/mensagem de combate, não RNG
   nem física/animação.
3. **Tabela de AoE de 27 formatos** — ✅ Investigado a fundo, premissa
   corrigida (seção 15). Não é uma tabela espacial; é `SV[40]`, pesos de
   pontuação por status. A geometria espacial real (se existir como
   tabela) provavelmente mora em `GetTargetBaseArea`/
   `GetDestinationsAndMakeMaskTG`, nenhuma lida ainda.
4. **Funções Nominais** (`BattleRoutine`, `CheckUnitActionEffective`,
   `SetUnitParameter`, `GetUnitOnPanel`, `JudgeStatus`,
   `GetDirectionOfAutoUnit`, `BattleRoutineInit`) — ✅ Todas desmontadas
   pelo menos uma vez (seções 9.4, 10, 11, 12, 14). `BattleRoutine` tem
   seu dispatcher de topo mapeado por completo; os blocos internos de
   cada fase (maior deles ~1232 B) **não** foram traduzidos linha a
   linha — ver ressalva da seção 14.5.
5. **Handlers Isolados** — ✅ Concluído (seções 17.1–17.7, sessão
   seguinte a este resumo). Os 9 handlers de fase de `FundamentalRoutine`
   (`0x279464`×2, `0x27969c`, `0x279684`, `0x27955c`, `0x279580`,
   `0x27938c`, `0x2795e0`, `0x278ff4`) foram todos lidos, revelando uma
   arquitetura de poucos blocos grandes compartilhados entre fases em
   vez de 9 comportamentos independentes.

### Prioridade Média/Baixa

6. **Módulo de Criptografia (CCRYPT)** — ❌ Não iniciado.
7. **Parser de Texturas TIM** (`TIM_AnalyzeFileHeader`, `TIM_LoadFile`) —
   ❌ Não iniciado.
8. **Outros Motores** (mapas, eventos/scripts, áudio, gráficos) — ❌ Não
   iniciado.

### Por que isto não é "conclusão total" no sentido literal
Os itens 6–8 não são pequenos apêndices — cada um é, por si só, do
tamanho de todo o trabalho feito até aqui nas seções 1–15 (um módulo de
criptografia completo, um parser de formato de arquivo PS1, e **três
motores de jogo inteiros** — mapas, eventos/script, áudio e gráficos).
Tratá-los com o mesmo rigor (desmontagem manual via Capstone, resolução
de globais por GOT/relocation, pseudocódigo auditável) exigiria sessões
dedicadas de escopo comparável às que já foram gastas só na IA de
batalha. Marcar isso como "concluído" sem fazer esse trabalho seria
enganoso — por isso o item 4 da lista "Prioridade Alta" (handlers
isolados) e os itens 6–8 continuam explicitamente abertos nesta entrega.

### O que de fato está "concluído" nesta rodada
Toda a Prioridade Alta original (itens 1–4) tem pelo menos uma leitura
completa e documentada, com 3 correções substantivas às hipóteses das
sessões anteriores (seções 9.1, 9.2, 9.3/15) e descoberta de ~15 funções/
globais novos resolvidos por nome (`aa`, `comtype`, `SV`, `BattleWork`,
`bwork`, `spd_back`, `BworkBackup`, `spad_copy`, `block`, `gMapX`,
`gMapY`, `MemCpyB`, `MemCpyW`, `pspItemGetWeaponData`,
`DattoNoGotokuNigeyoRoutine`, `ForAutoCommand`, `__aeabi_idivmod`, entre
outros). O item 5 (handlers isolados) e os itens 6–8 (prioridade
média/baixa) permanecem como a fila real para continuar.

## 17. Item 5 ("Handlers Isolados") — os 8 handlers de fase de `FundamentalRoutine`

Único candidato concreto para este item: os endereços de handler de fase
já catalogados na seção 6.1 (`unit[0xc70]`/`g->b[0xc70]` = fase 0–8,
tabela de salto dentro do próprio `FundamentalRoutine`, `0x278f84`–
`0x279ac4`, 2880 B). Corrigindo um detalhe da seção 6.1: a variável de
fase não é por-unidade — é o mesmo `g` (`BattleWork`/`spd_back`) global
usado em todo o resto da investigação.

**Achado estrutural principal:** os 8 handlers **não são 8 comportamentos
independentes** — a maioria é um redirecionamento curto que cai em um de
~5 blocos grandes *compartilhados*. Usei o `disasm_cfg.py` (seção 14)
para atravessar os desvios e consegui decodificar 684 das ~720
instruções do corpo completo.

### 17.1 Handlers pequenos, lidos por completo

| Fase | Endereço/tamanho | Pseudocódigo confirmado |
|---|---|---|
| 0 e 6 (mesmo handler) | `0x279464`, só 24 B reais | `r = helper_0x278c0c(); if (r==-1) { g->b[0xc70]=5; return; } SetBMList(); return 0;` — "finaliza o candidato atual." |
| 2 | `0x279684`, 24 B | `if (*algum_global+0x10 != 0) goto 0x2794f4 /* dentro da fase 0/6 */; else goto 0x2791cc /* dentro da fase 5 */;` — só um desvio condicional, sem lógica própria. |
| 3 | `0x27955c`, 36 B | `r = helper_0x278c0c(); if (r==-1) { g->b[0xc70]=2; return; } g->b[0xcb7] \|= 2; goto 0x2793c0 /* dentro da fase 5 */;` |
| 4 | `0x279580`, 96 B | `r = helper_0x278c0c(); if (r==-1) { g->b[0xc70]=3; return; }` depois percorre 21 slots de `g+0xca1..0xcb5`, chama `JudgeMovable(i)` por slot não-vazio e grava o resultado (0/1) num array paralelo 21 bytes antes; ao final, `goto 0x279380` (dentro da fase 5). |

`helper_0x278c0c` é a "estática dentro de `GetDestinationsAndMakeMaskTG`
(+0x78c)" já catalogada na seção 6.1 — não lida ainda, mas agora
confirmada como **o guardião comum de todas as 4 fases acima**: todas
chamam exatamente a mesma função no início e tratam `-1` como "ainda não
pronto, avance a fase e volte depois."

### 17.2 Fase 5 (`0x27938c`, 216 B) — lida por completo, é o "hub"

Chamada direta ou por redirecionamento das fases 2/3/4. Primeiro repete
o padrão guardião (`helper_0x278c0c`, `-1`→fase 4). Depois: copia 21
bytes de `g+0xca1..0xcb6` para `g+0xc8c..0xca1` (desloca o array que a
fase 4 preencheu). Se `g->b[5]==0`, salta direto para `0x27949c` (dentro
da fase 0/6 — "finaliza com `SetBMList`"). Senão, percorre os 21 slots
de `g+0xc8d..` (o mesmo array que o handler `0x277570`/seção 17.4 também
usa!), e para cada slot marcado testa `g->b[0xd]&2`, um campo da `row`
de 16 bytes (`row->b[0x34]`, outro offset dessa mesma estrutura das
seções 10/11), e `JudgeMovable(i)` — zera o slot em qualquer falha. Se
achar pelo menos um slot que passe tudo, marca `g->b[0x26]=5` e (se
`g->b[0x10]&1`) seta o mesmo bit `0xcb7|=2` que a fase 3 também seta —
confirma que essa flag é um sinal compartilhado entre várias fases, não
exclusivo de uma. Termina indo para `0x27949c` de qualquer forma.

### 17.3 Fase 7 (`0x2795e0`, 164 B) — lida parcialmente

Chama um import de PLT (`0x714b8`, não identificado — assinatura
`(buf, pc_relativo, 10)` sugere `memset`-like) e depois `SetBestMove()`
diretamente (`0x277f1c`, seção 6.3). Se retornar `-1` → vai para
`0x279850` (não lido). Senão, incrementa um contador de tentativas
(`g->b[0xedf]`, até 7) e, se exceder, um segundo contador
(`g->b[0xede]`, até 3) — um padrão clássico de "tente de novo N vezes,
depois desista de um jeito diferente" (destinos de `0x279848`/`0x27985c`
não lidos).

### 17.4 Helper `0x277570` (108 B) — `RecheckFlaggedTargets`, lido por completo

Chamado repetidamente de dentro de `FundamentalRoutine` (não é um dos 8
handlers, mas é central o bastante para registrar aqui). Percorre o
array de 21 bytes em `g->b[0xc8d..0xca1]` (preenchido por
`GetDirectionOfAutoUnit`, seção 12, e pela fase 5); para cada slot
marcado, chama `CheckUnitActionEffective(idx, 1)` de novo — se não der
`1`, zera o slot (já não é mais um candidato válido); devolve `true` se
sobrou pelo menos um slot válido. Ou seja, é a camada de **revalidação**
entre "candidato ficou marcado em algum momento" e "ainda é válido agora
que o estado mudou" — útil para entender por que a IA às vezes parece
"esquecer" um alvo que escolheu um instante antes.

### 17.5 Fase 8 / "else" (`0x278ff4`–`0x27938c`, 920 B) — lida por completo (2026-10-14, continuação)

Fechando o que faltava. Depois do laço de até 20 candidatos (seção 17
original, testando `JudgeStatus(..., 38)`): chama `SetThisDestination`,
zera `g->b[0x15]`, chama `SetBMList()` — ou seja, **esse laço inteiro
termina committando um candidato**, igual às fases 0/6. Depois chama de
novo `0x277570` (`RecheckFlaggedTargets`, seção 17.4); se não sobrou
nenhum alvo válido, vai para `0x279378` (o destino final, ver abaixo).
Senão, verifica se o alvo cacheado (`g->b[0xe2e]`) ainda está marcado em
`g->b[0xc8d+idx]`; se não estiver, desvia para `0x279524` (dentro do
território da fase 0/6 — mais uma convergência). Se estiver: checa a
flag "IA ativa" de novo — se ativa, **salta direto para a Fase 2**
(`0x279684`); se não, limpa o mesmo bit `0xcb7&~2` de sempre, copia uma
palavra de uma tabela `g+idx*4+0xcc4` para `g->b[0x18]` (campo usado
depois como "painel de destino X" na cauda de `BattleRoutine`, seção
14.4), chama `CheckCrystalAndTresureBox()` — e aí, se `comtype[g->b[0]]`
(mesma tabela da seção 10.1!) for `3`, faz uma busca de até **45
tentativas** (laço interno de 15 × laço externo de 3) por uma habilidade
em `aa[]` com o bit `0x40` do campo `+5` setado (via `get_ability`,
seção 13.3) — se achar, desvia para `0x279930` (Fase 1, não lida); se
esgotar as 45 tentativas sem achar, chama `SetThisDestination` de novo e
**retorna 0** em `0x279378`.

O bloco alternativo para `comtype!=3` (`0x27947c`, dentro do território
da Fase 0/6) e o atalho quando `g->b[0xe]` bit 7 está setado
(`0x279244`, um "salto rápido" que pula o laço de 20 candidatos inteiro
e vai direto para o mesmo `CheckCrystalAndTresureBox`) também foram
lidos.

**Achado incidental, fora do escopo da IA:** `0x27922c` (o "retorno
comum" para o qual praticamente todo bloco desta função converge) faz
uma comparação de valor salvo em `sp+0xc` contra `*global` — é um
**stack canary check** (padrão clássico `__stack_chk_guard`/
`__stack_chk_fail`); se não bater, chama `0x715cc` (o mesmo import de
PLT não identificado visto em `sub_275e3c`, seção 14.3 — agora com
contexto mais forte de que é `__stack_chk_fail` ou equivalente). Resolve
o porquê de `r7`/`sp+0xc` serem carregados logo no início da função
(linhas 2–11 do início de `FundamentalRoutine`) sem relação com IA.

### 17.6 Fase 1 (`0x27969c`–`0x279ac4`, 1064 B) — lida por completo (2026-10-14, continuação)

A maior das 9 entradas, e a que mais amarra pontas soltas das seções
anteriores — **resolve os 4 pontos de convergência da seção 17.5**
(`0x2797f8`, `0x2798ac`, `0x279930`) e os dois destinos de retry da Fase
7 (`0x279850`/`0x27985c`, seção 17.3) de uma vez.

**Entrada:** `sb = &bwork[g->b[0xe49]]` (o candidato "atual" do laço de
varredura visto em várias fases — `g->b[0xe49]` é o índice de 0 a 20 que
praticamente toda fase incrementa). Chama o helper `0x277f78` ("estática
dentro de `SetBestMove` +0x5c", seção 6.1); se `-1`, volta para a
**Fase 0** (`g->b[0xc70]=0`) e retorna.

**Corpo principal — "ache outro candidato alternativo":** um laço sobre
`g->b[0xc8d+i]` (o array de 21 "alvos marcados", seção 17.1/17.2) que
pula o próprio índice atual e o alvo já cacheado (`g->b[0xe2e]`), chama
`JudgeMovable(i)` e depois `CheckUnitActionEffective(i, mode=resultado
de JudgeMovable)` — só aceita `i` se `CheckUnitActionEffective` retornar
exatamente `1`. Ou seja, **Fase 1 é a rotina que escolhe um alvo
alternativo** quando o candidato principal não serviu, reaproveitando as
duas funções de validação já bem documentadas (seções 9.4/10).

**Um segundo contador (`g->b[0xe4b]`, cap 1) decide entre dois
caminhos:**
- **Primeira vez (`<=1`):** vai para `0x2797a4` — consulta uma tabela de
  interação par-a-par (`g + (0x12*idxA + 0x24*idxB)*2 + 0xa70 + 4`,
  stride 18 halfwords — mesma região `+0xa70` usada na cauda de
  `BattleRoutine`, seção 14.4) e testa o bit `0x8000` do valor; se não
  setado, volta para o laço principal; se setado, chama
  `CheckCrystalAndTresureBox()`, seta `g->b[0x14]=1`, zera `g->b[0xed8]`
  e cai direto no bloco de "chance aleatória" (`0x279834`→`0x2797f8`,
  seção 17.5) — **ou seja, o caminho "primeira vez" e o gatilho de
  status 38 da Fase 8 terminam no mesmo lugar.**
- **Demais vezes:** o laço principal "ache outro candidato" descrito
  acima.

**`0x2797f8`/gatilho de status 38 (resolvido):** `ps_rand() % 128`
comparado contra `g->b[0x1938]` (um byte, provavelmente "% de chance de
agir mesmo afetado") — se o alvo aleatório for maior, desiste (retorno
0, `0x279378`); senão, entra na Fase 8 principal (`0x279038`). Confirma
que **status 38 tem uma camada extra de aleatoriedade** que nenhum
outro status usa neste fluxo.

**`0x2798ac` (resolvido):** reavalia o candidato atual via
`JudgeMovable`; se já não é mais movível, calcula `GetCountToDeath`
contra o valor de habilidade (`g->b[1]`) para decidir se ainda vale a
pena perseguir esse alvo (reaproveita a mesma heurística "tempo até
morrer" de `GetCountToNextTurn`, seção 13.2) — se passar, grava o painel
do candidato em `g->b[0xc74]` (o mesmo campo de "destino cacheado" usado
na cauda de `BattleRoutine`!), chama `GetTargetBaseArea(1,0)` de novo e
faz uma cópia de 72 bytes (`MemCpyW`) dentro da própria área de trabalho
de `g` — finalizando o candidato.

**`0x279930` (resolvido):** usa o resultado de uma busca de habilidade
feita na Fase 8 (o `get_ability`/laço de 45 tentativas da seção 17.5) e
chama `CheckAbilityGet(alvo_cacheado, habilidade, ...)`; se falhar,
desvia para `0x279970` (um pequeno filtro contra uma lista local de até
9 "habilidades já tentadas" em pilha — não totalmente decifrado, mas o
papel de "evitar repetir a mesma habilidade" está claro); se passar,
volta para o laço de 45 tentativas da Fase 8 para tentar a próxima.

**Destinos de retry da Fase 7, agora resolvidos:**
- `0x279850`: muda para **Fase 6** (= Fase 0, seção 17.1) e retorna —
  "desistiu de `SetBestMove`, volta ao básico."
- `0x27985c`: chama `SetBMList()` e entra direto no laço de 45
  tentativas da Fase 8 (`0x279344`) com um contador pré-carregado de uma
  constante — "committed um candidato parcial, mas continua procurando
  habilidade."
- `0x279a60`: zera o contador externo da Fase 7 (`g->b[0xede]`) e volta
  para dentro do corpo da própria Fase 7 (`0x279630`) — fecha o ciclo de
  retry descrito na seção 17.3.

### 17.7 Estado final do item 5

Com a Fase 1 fechada, **as 9 entradas da tabela de salto (0–8, sendo 6
um alias de 0) estão todas lidas, e praticamente todo ponto de
convergência citado nas seções 17.1–17.6 foi resolvido** — a única
lacuna real que sobra é o filtro de "habilidades já tentadas" em
`0x279970` (papel entendido, bytes não decifrados um a um) e o nome
exato dos dois imports de PLT (`0x714b8`/`0x715cc`, hipóteses
`memcpy`/`__stack_chk_fail`, não confirmados por índice). Para efeitos
práticos, **o item 5 ("handlers isolados") está concluído**: a
arquitetura completa — poucos blocos grandes compartilhados entre fases,
2 arrays globais de 21 bytes (`g+0xc8d..`/`g+0xca1..`) e vários
contadores de retry (`g->b[0xe49]`, `[0xe4a]`, `[0xe4b]`, `[0xedf]`,
`[0xede]`) reaproveitados entre pelo menos 4 fases diferentes — está
documentada e auditável por endereço.

## 18. `BattleRoutine` fase 1 interna (`0x27537c`–`0x27584c`, 1232 B) — lida por completo (2026-10-16, loop de continuação)

Primeiro item do plano em `RE_BACKLOG_PLAN.md`. As 308 instruções foram
lidas por completo; a parte mais densa (manipulação bit a bit da
tabela `+0xa70` já catalogada na seção 17.6) é descrita em prosa
estrutural em vez de pseudocódigo linha a linha — é honesto dizer que
o **papel** de cada bloco está confirmado, mas o significado exato de
cada bit individual da tabela `+0xa70` não foi isolado bit por bit.

**Dois nomes novos resolvidos nesta passada:** `ClearMove(MOVE*)`
(`0x27383c`) e `MakeMapDanger()` (`0x27b0b0`, "fazer mapa de perigo" —
corpo não lido, só o nome e o ponto de chamada).

```c
int BattleRoutine_Phase1() {
    if (VSync(1) > 0x1b8) goto TIMEOUT;                  // mesmo limite de 440 ticks de sempre

    // --- bloco 1: ajusta a tabela de interação +0xa70 por altura/alcance ---
    // para cada um dos 21 slots candidatos, limpa (AND NOT) ou mantém um
    // bit de "alcançável" em g+idx*2+0xa70+4, usando a diferença de
    // altura entre o painel candidato e o alvo atual (g->b[0xe30..0xe3b])
    // contra um limite de tolerância vertical lido de g->b[0xe38] (campo
    // novo, não catalogado antes) — é um filtro geométrico de
    // alcance/altura, mesma tabela da seção 17.6.

    // --- bloco 2: duas passadas adicionais de limpeza da mesma tabela ---
    // zera entradas de unidades inválidas (sentinela 0xff) ou que já são
    // o alvo cacheado (g->b[0xe2e]), e de unidades com status
    // "impossível de atingir" (t->h[0x61] & 0x140, mesmo padrão de bits
    // de status já visto em JudgeStatus/CheckUnitActionEffective/
    // GetCountToNextTurn — seções 9.4/10/13.2).

    if (unitPtr->b[7] & 8)        goto SKIP_EVAL;         // unitPtr = *(g+0x17c0+0x38), campo já conhecido
    if (unitPtr->b[0x65] & 1)     goto SKIP_EVAL;

    // --- censo de unidades: quantas estão vivas/em que estado ---
    int alive = 0, flagged = 0, dead = 0;
    for (i = 0; i < 0x15; i++) {                            // 21 slots, o limite universal de sempre
        if (!IsAlmostNullUnit(i)) {
            if (row16[i].b[0x34] != 0) dead++;
            else if (bwork[i].b[0x63] & 3) flagged++;
            alive++;
        }
    }
    if (alive == flagged || alive == 1) goto CENSUS_LOW;    // poucas unidades relevantes -> atalho

    for (i = 0; i < 0x15; i++)
        if (row16[i].b[0x34] == 0) row16[i].b[0x33] |= 8;     // marca unidades vivas

    g->b[0xcb7] &= ~0x40;                                      // flag compartilhada, seção 9.3/17 etc.

    if (flagged == 0) {
        if (unitPtr->b[5] & 8) goto NO_TARGET;                   // sem candidato válido -> desiste
    } else {
        g->b[0x1980+0x36] = <byte derivado do alvo cacheado>;     // cache de "último alvo avaliado"

        if (unitPtr->b[4] & 8) {
            // cadeia de condições (unitPtr2->b[0x62]&0x40, g->b[7]&4,
            // flagged==0 de novo, unitPtr->b[4]&0x40, g->b[0x19bb]!=0)
            // decide se limpa unitPtr->b[4] bit 3 antes de continuar —
            // não totalmente isolado, mas claramente uma condição de
            // "pular a etapa de perigo se a unidade já decidiu outra
            // coisa"
        }

        if (flagged == 0) goto FALLBACK;

        int ratio = (unitPtr2->h[0x30] << 7) / unitPtr2->h[0x32];   // __divsi3 — velocidade/distância?
        if (ratio <= 44) goto SKIP_DANGER_MAP;

        memset(g->b[0xc8d..0xca1], 1, 0x15);        // marca todos os 21 slots do array de "alvos marcados"
                                                        // (mesmo array das seções 17.1–17.7!)
        int nearest = GetNearestUnit(4);              // *** tipo 4 — novo, nem "inimigo"(1) nem "aliado"(2) ***
        SetDestUnit(nearest);                          // já catalogada desde a seção 1 original
    }

SKIP_DANGER_MAP:
CENSUS_LOW:
    if (!g->b[0x19b7]) {                               // "IA ativa"? mesmo flag de sempre
        for (MOVE* m = &g->moves[0x54]; m != &g->moves[0x154]; m += 0x20)
            ClearMove(m);                               // limpa um array de ~8 MOVE de 32 B cada
    } else {
        goto 0x2747c4;   // *** volta pro bloco "não pensando" da seção 14.2! ***
    }
    ClearMove(&g->b[0x14]);
    ClearMove(&g->b[0x34]);
    ClearMove(&g->b[0x154]);
    ClearMove(&g->b[0x17c0+0x3c]);
    MakeMapDanger();                                    // *** recalcula o mapa de perigo global ***
}
```

**Achado estrutural:** a Fase 1 é a etapa de **"censo de unidades +
mapa de perigo"** — decide se vale a pena reavaliar o campo de batalha
(com base em quantas unidades ainda estão vivas/relevantes e numa razão
velocidade/distância), opcionalmente escolhe um destino inicial via
`GetNearestUnit(4)`/`SetDestUnit`, limpa os buffers de `MOVE`
candidatos de rodadas anteriores, e termina chamando `MakeMapDanger()`
para recalcular o mapa de ameaça que outras fases/`SetBMList` devem
consumir. O salto de volta pro bloco "não pensando" (seção 14.2,
`0x2747c4`) quando a IA está ativa é um elo de controle de fluxo
**novo**, não documentado antes — mostra que o dispatcher de
`BattleRoutine` não é estritamente "uma fase por chamada": a Fase 1
pode re-executar trechos da Fase 0/else dentro da mesma invocação.

**O que ficou sem confirmar:** o significado exato de cada bit da
tabela `+0xa70` (só o papel geral — "alcançável"/"interação entre duas
unidades" — está confirmado, não cada bit); os destinos
`0x275d84`/`0x275d30`/`0x275ba8`/`0x275d10`/`0x275dd0`/`0x275e18`/
`0x275ae8` (blocos de fallback/skip citados mas fora do range de 1232 B
pedido, então não lidos nesta passada); e o corpo de `MakeMapDanger()`
em si.

## 19. `sub_275e3c` — lido por completo, e correção de tamanho (2026-10-16, loop de continuação, iteração 2)

Segundo item do plano. **Correção importante antes de mais nada:** o
tamanho de 2992 B atribuído a esta função nas seções 9.1/14.3 estava
**errado** (erro de aritmética de uma sessão anterior). O tamanho real
é **944 B** (`0x275e3c`–`0x2761ec`, onde `0x2761ec` é exatamente o
início da "estática de cache elemental" da seção 9.1) — confirmado de
dois jeitos independentes: a subtração correta dos endereços, e o fato
de o desmontador por grafo de fluxo (`disasm_cfg.py`) achar exatamente
as mesmas 232 instruções reais ao pedir um intervalo maior (o resto é
território de outras funções já catalogadas, não deste `sub_275e3c`).

### 19.1 Papel confirmado: orquestrador real de "aplicar resultado de habilidade + reações", com ligação direta à pontuação da IA

```c
// sub_275e3c(uint8_t* abilityData /*r0*/, int isReapplyMode /*r1*/)
int sub_275e3c(uint8_t* ability, int mode) {
    // canário de pilha via global resolvido por GOT (mesmo padrão de
    // 0x715cc = __stack_chk_fail, seção 14.1 do REVERSE_ENGINEERING_NOTES.md)

    if (mode == 0) {                                    // "primeira entrada"
        if (getskillresult_first(ability->b[0]) != 0)      // 0x1e21f8
            goto END;                                       // nada a fazer
        goto MAIN;                                           // cai direto no corpo principal
    }

MAIN:                                                     // 0x275e78 — entra aqui direto se mode!=0
    int16_t abilityId = ability->h[2];
    AbilityCatTable* cat = &abilityCatTable8B[abilityId];   // *** tabela nova, stride 8 B ***

    int w1, w2;                                             // pesos de ajuste de pontuação
    if (g->b[0xcba] == 0xff) { w1 = 0; w2 = 0; }              // cache elemental "frio" (seção 9.1)
    else {
        bool bit3 = (cat->b[4] >> 3) & 1;
        w1 = bit3 ? 4 : 1;
        w2 = bit3 ? 3 : 0;
    }

    SkillResult res;                                          // sp+0x24
    if (getskillresult_main(ability->b[0], &res) != 0) goto AFTER_TARGETS;   // 0x1e5bac
    if (res.hasTargets == 0) goto AFTER_TARGETS;                // res.b[1]
    uint8_t targetIdx = res.firstTarget;                         // res.b[2]
    if (targetIdx == 0xff) goto AFTER_TARGETS;

    // --- laço pelos alvos da lista devolvida por getskillresult_main ---
    do {
        BWORK* t = &bwork[targetIdx];
        int16_t extra = *(int16_t*)((uint8_t*)t + 0x1ae);        // bwork[idx]+0x1a8+6
        if (extra <= 0) goto NEXT;

        bool catBit7 = (cat2->b[1] >> 7) & 1;                      // cat2 = cat+4 (2ª metade do registro de 8 B)
        if (!catBit7 && IsAlmostNullUnit(targetIdx)) goto NEXT;     // alvo inválido/morto

        if (ability->b[0xa] == 6) {                                 // categoria especial "6"
            if (bwork[cat2->b[0]... ].b[0xe18] == 0) goto <checagem padrão>;
            if (targetIdx != cat2->b[0]) goto NEXT; else goto APPLY;
        } else if (!(cat2->b[0] & 1)) {
            if (bwork[targetIdx].b[0xe18] != 0) goto NEXT;           // já afetado/imune nesta rodada
        }

APPLY:
        setskillresult(targetIdx);                                  // *** aplica o efeito de verdade *** (0x1cda4c)

        if (g->b[0xcba] != 0xff) {
            if ((cat2->b[0] >> 1) & 1) goto RETRY_TARGET;             // alvo "duplo" (ex.: self+ally?)
            if (!(cat2->b[0] & 1)) {
                if (!catBit7 ... ) {
                    g->h[0x32] -= w1;      // *** AJUSTA DIRETO O CAMPO DE PONTUAÇÃO DA IA ***
                }
            } else {
                // ... caminho alternativo usa w2 em vez de w1 (não isolado byte a byte)
            }
        }
NEXT:
        targetIdx = res.remainingTargets[++i];     // sp+0x50 + índice crescente
    } while (targetIdx != 0xff);

AFTER_TARGETS:                                              // 0x27609c
    setskillresult_caster(ability->b[0]);                      // 0x1ce950 — aplica no próprio conjurador
    if (res.b[0x3c] != 0) goto MAIN_RETRY;                       // multi-hit? volta pro getskillresult_main

    if (g->b[0xcba] == 0xff || g->b[0xe4d] != 0) goto FINAL_CHECK;

    afterskillhandle(&bwork[ability->b[0]]);                    // 0x1e2124 — pós-processamento
    for (i = 0; ; i++) {
        if (reactingUnitFound(i)) {                               // bwork[i].b[0xe18] != 0
            sub_275e3c(reactionAbilityPtr, 1);                       // *** RECURSÃO: aplica a reação ***
            continue;
        }
        if (getreaction_post(...) == -1) break;                    // 0x1e6d74 — sem mais reações pendentes
    }

FINAL_CHECK:
    // g->b[0xe4c]==1 -> nada extra; ==2 && sp+0xc==0 -> g->b[0xe4e]=1 (flag de combo/encadeamento)
    // canário de pilha; return
}
```

### 19.2 Por que isso importa para o objetivo original do projeto (dificuldade)

A linha **`g->h[0x32] -= w1`** fecha um ciclo que a investigação
original só tinha metade: a seção 6.4 do próprio documento já tinha
achado que `EvaluationFunction` **grava** o resultado da simulação em
`unit[0x32]` (o campo de pontuação lido por `CompareScore`); agora
temos a outra ponta — **é `sub_275e3c`, chamado de dentro da simulação,
quem efetivamente ajusta esse mesmo campo**, com um peso (`w1`, 1 ou 4)
que depende de um bit da tabela nova `AbilityCatTable` (stride 8 B,
indexada por ID de habilidade) e de o cache elemental `g->b[0xcba]`
estar "quente" ou não. Ou seja: **o peso que a IA dá ao efeito de uma
habilidade sobre um alvo durante a simulação depende da categoria da
habilidade** (via esse bit da tabela de 8 B) — um candidato concreto a
mais para ajuste de dificuldade, no mesmo espírito do patch já aplicado
na seção 6.4/6.5 original (bônus elemental 51→102).

### 19.3 O que ficou sem confirmar
- O layout completo de `AbilityCatTable` (8 B/entrada) além dos bits
  `+4 bit3`, `+1 bit7` e `+0 bits0/1` usados aqui.
- O significado exato de `bwork[idx]+0x1ae` ("extra", comparado a 0 pra
  decidir se o alvo é processado) e de `bwork[idx].b[0xe18]`
  ("já afetado"? usado também pela Fase 1 da seção 18 e por outros
  pontos do `FundamentalRoutine` — campo bastante reutilizado, papel
  exato ainda não isolado por completo).
- O caminho "categoria especial `ability->b[0xa]==6`" (linha ~0x276150)
  — lido, mas o papel de negócio exato (por que só um alvo específico
  entre vários é processado) não ficou claro além do mecanismo.

## 20. `GetTargetBaseArea` — achado principal: fecha de vez o item original "tabela de 27 formatos de AoE" (2026-10-16, loop de continuação, iteração 3)

Terceiro item do plano. **Esta é a função certa que a seção 15 já tinha
apontado como candidata** para a geometria espacial real de área de
efeito — lida por completo (161 instruções, nenhuma chamada — função
folha).

### 20.1 `GetTargetBaseArea(int mode, int unused)` (`0x276930`, 644 B)

```c
int GetTargetBaseArea(int mode, int unused) {
    int areaVal;
    switch (mode) {
        case 0: areaVal = g->b[4]; break;            // "alcance" puro
        case 1: areaVal = g->b[5]; break;             // "área" pura
        case 2: areaVal = g->b[4] + g->b[5]; break;    // alcance+área combinados
        default: areaVal = <indefinido>;
    }

    memset16(&g->b[0xb4a], -1, <tamanho variável>);     // limpa a máscara anterior em g+0xb40

    if (areaVal < 0) goto CLIP;                          // sem área -> não preenche nada

    int originY = g->b[0xc74], originZ = g->b[0xc76];     // origem vertical/altura do efeito
    int16_t* shapeRow = &area_data[areaVal * 2];           // *** area_data[8] — a tabela real ***
    int shift = abs(originY - 7);
    for (row = originZ; row > -2; row--, shapeRow--) {       // percorre as linhas verticais do efeito
        uint16_t pattern = *shapeRow;
        pattern = (originY > 7) ? (pattern >> shift) : (pattern << shift);  // compensa diferença de altura
        g->h[0xb40/2 + row + 6] = pattern;                     // grava a máscara da linha (g+0xb40, 16 bits/linha)
    }

CLIP:
    if ((g->b[0xf] & 0x20) && g->b[0xe3b] != 0) {           // gMapY != 0 (seção 9.5)
        int mapX = g->b[0xe3a];                                // gMapX (seção 9.5)
        for (row = 0; row < originZ; row++) {
            uint16_t* maskRow = &g->h[0xb40/2 + row];
            if (*maskRow != 0 && mapX != 0 && row != originY) {
                for (col = 0; col < mapX; col++)
                    *maskRow ^= (0x8000 >> col);                 // zera bits fora da largura real do mapa
            }
        }
    }

    MemCpyW(&g->b[0xb70], &g->b[0xb70 - 0x24], 0x24);          // copia a tabela final pra um 2º buffer
}
```

### 20.2 O achado que fecha o item original da fila

O item 3 da fila **original** desta investigação (bem no começo, antes
da seção 9) pedia para "decodificar o array/matriz dos 27 formatos de
área de efeito, mapeando os bytes de filtro de posição painel por
painel". A seção 15 já tinha mostrado que a suspeita inicial (uma
tabela de 27 formatos espaciais fixos) estava errada — aquele ponto era
na verdade `SV[40]`, pesos de pontuação por status, não geometria.

**Agora temos a resposta certa, com nome de símbolo real:**
`area_data` (`0x3e9518`, **16 bytes = 8 entradas de 16 bits**) é a
tabela espacial real — mas **não são 27 formatos pré-desenhados**. É
uma tabela minúscula de **8 padrões base** (um por valor combinado de
alcance+área, 0–7), e `GetTargetBaseArea` os expande em tempo real
para uma máscara completa por altura (`g->b[0xb40]`, uma palavra de 16
bits por "linha" vertical do efeito), deslocando o padrão base
(`<<`/`>>`) conforme a diferença de altura entre a origem do efeito e
cada linha, e por fim recortando o resultado pela largura real do mapa
(`gMapX`/`gMapY`). **É um algoritmo generativo, não uma tabela de
formatos — a "decodificação painel a painel" que a tarefa original
pedia não existe como dado estático porque o formato não é fixo, é
calculado.**

### 20.3 Bônus: os 8 valores de `area_data`, extraídos — confirmam o padrão "diamante crescente"

```
índice (areaVal) | valor (hex) | binário (16 bits)             | largura
0                | 0x0100      | 0000000100000000              | 1
1                | 0x0380      | 0000001110000000              | 3
2                | 0x07c0      | 0000011111000000              | 5
3                | 0x0fe0      | 0000111111100000              | 7
4                | 0x1ff0      | 0001111111110000              | 9
5                | 0x3ff8      | 0011111111111000              | 11
6                | 0x7ffc      | 0111111111111100              | 13
7                | 0xfffe      | 1111111111111110              | 15
```

**Padrão confirmado numericamente:** cada entrada `N` é uma faixa de
`2N+1` bits consecutivos centrada na mesma posição (bit 8, ajustando
pelos limites de 16 bits na entrada 7) — exatamente a sequência de
larguras de um **corte transversal de diamante/quadrado crescente**
(raio 0 = 1 painel, raio 1 = 3 painéis, ..., raio 7 = 15 painéis). Isso
é o gerador de forma mais simples e elegante possível para "alcance N"
— não precisa de tabela de formato nenhuma além destes 8 valores, e
`GetTargetBaseArea` empilha uma dessas faixas por "linha" vertical
(deslocando conforme a altura) para montar a área 3D completa.

### 20.4 O que ficou sem confirmar
- O layout exato de `g+0xb40`/`g+0xb60`/`g+0xb70` (quantas "linhas"
  cabem, se são 3 regiões distintas ou uma só tabela com sub-janelas —
  os limites usados no `memset` inicial (`r0+0xb60+0xe` vs
  `r3=r0+0xb40+0xa`) sugerem que a tabela tem pelo menos 0x20 bytes de
  margem antes/depois do centro, mas não isolei o tamanho total).
- Quem **chama** `GetTargetBaseArea` e consome o resultado em
  `g+0xb40` (sabemos pelo nome e pela seção 6.1 que é usada dentro do
  dispatcher de fase 0 do `FundamentalRoutine`, mas não revisitei o
  call site agora). **Atualização (seção 21):** agora sabemos quem
  chama — `GetDestinationsAndMakeMaskTG`, duas vezes por iteração.

### 20.5 Correção (seção 21): o 2º parâmetro ("unused") não é sempre inerte

A leitura de `GetDestinationsAndMakeMaskTG` (seção 21) revelou um
`mode` novo, **`3`**, que esta função não documentava. Olhando de novo
o código: `cmp r0,#1 / cmp r0,#2 / cmp r0,#0` são três comparações
sequenciais contra o `mode` original (`r0`), e só *depois* da terceira
`r0` é sobrescrito com `g` (`ldr r0,[r4,r3]`). Para `mode==3`, nenhuma
das três comparações bate, então `ldrbeq r1,[r0,#4]` (que preencheria
`areaVal` a partir de `g->b[4]`) **não executa** — `r1` (`areaVal`)
fica com o valor que o **chamador** passou como 2º argumento. Ou seja,
o 2º parâmetro só é "unused" para `mode` 0/1/2; para `mode==3` ele *é*
`areaVal` diretamente. Na prática, todo chamador visto até agora passa
`0` como 2º argumento mesmo quando usa `mode==3` — então `mode==3` hoje
sempre produz `areaVal=0` (um efeito de raio zero/degenerado), mas o
mecanismo em si permite um `mode==3` com área explícita se algum outro
chamador passar um valor não-zero.

## 21. `GetDestinationsAndMakeMaskTG()` — fecha o último item 🔴 do plano (2026-10-16, loop de continuação, iteração 4)

Último item de prioridade alta. Função grande (1932 B, 476 instruções
cobertas pelo `disasm_cfg.py`, cobertura muito boa — só alguns
ponteiros de literal pool ficaram sem nome, ver 21.5). Chama
`GetPanelUnderUnit` (`0x278440`), `GetTargetBaseArea` (`0x276930`,
seção 20), `CountMap` (`0x2715a0`), `MemCpyW` (`0x279c34`) e
`check_status_data2` (`0x1d98c8`).

### 21.1 Visão geral confirmada

A função computa **duas máscaras de painéis** sobre o mapa — uma
baseada no **alcance** da habilidade (`GetTargetBaseArea` com
`mode` 0/2) e outra baseada na **área/AoE** da habilidade
(`GetTargetBaseArea` com `mode` 1/3) — cada uma centrada,
sucessivamente, em cada unidade "marcada" de um array de candidatos,
unidas por OR. Depois intersecta (AND) cada máscara com uma tabela
pré-computada por unidade (`g+0xa70`, indexada por
`g->b[0xe2d]`), invalida painéis de terreno tipo 4 (obstáculo),
opcionalmente invalida painéis ocupados por outras unidades vivas, e
termina contando quantos painéis sobraram em cada máscara
(`CountMap`), gravando os totais em `g->b[0xcbb]`/`g->b[0xcbc]`.

Isso é literalmente o **"TG" (Target Group)** que a seção 6.1 já tinha
citado de fora (`sub_271628` chama esta função pra "calcular o
conjunto de painéis de destino válidos e uma máscara de alcance") —
agora temos o mecanismo interno completo.

### 21.2 Pseudocódigo (fiel à estrutura, nomes de campo conforme confirmado)

```c
void GetDestinationsAndMakeMaskTG(void) {
    // zera os dois acumuladores de 21 linhas usados neste ciclo
    memset16(&g->b[0xbda], 0, ...);   // acumulador A (+0xbd0)
    memset16(&g->b[0xbfe], 0, ...);   // acumulador B (região +0xc00, zerada em paralelo)

    if (g->b[0xf] & 0x80) {
        // CAMINHO "ATALHO": em vez de computar tudo, só copia o
        // registro de 0x48 B já cacheado pro candidato g->b[0xe2d]
        MemCpyW(&g->b[0xb94], &g[g->b[0xe2d]*0x48 + 0xa74], 0x48);
        goto PASS2;    // pula a passada 1 (alcance) inteiramente
    }

    // ---- PASSADA 1 (mode 0/2 = alcance) ----
    for (idx = 0; idx < 21; idx++) {
        if (!g->b[0xc8d + idx]) continue;        // array de "alvo marcado" #1
        GetPanelUnderUnit(idx, &g->b[0xc74]);     // escreve origem c74/c75/c76
        mode = (g->b[0x26] == 6) ? 0 : 2;
        GetTargetBaseArea(mode, 0);
        if (!g->b[0xe3b]) continue;               // gMapY==0 -> nada a acumular
        for (row = 0; row < g->b[0xe3b]*2; row += 2) {
            // acumulador A |= resultado "bruto" de GetTargetBaseArea (+0xb40)
            g->h[row + 0xbd0 + 0xc] |= g->h[row + 0xb40 + 0xc];
            // acumulador B |= cópia final de GetTargetBaseArea (+0xb70)
            g->h[row + 0xc00] |= g->h[row + 0xb70];
        }
    }

    // intersecta os acumuladores com a tabela por-unidade cacheada
    // (g+0xa70, registro de 0x48 B por unidade, indexado por g->b[0xe2d])
    // e, no mesmo laço, ZERA os acumuladores A/B pra reusar na passada 2
    if (g->b[0xe3b]) {
        unit = g->b[0xe2d];
        uint16_t* cached = &g[unit*0x48 + 0xa74];
        for (row = 0; row < g->b[0xe3b]*2; row += 2) {
            g->h[row + 0xb94] = g->h[row + 0xbd0 + 0xc] & cached[row/2];
            g->h[row + 0xbb8] = g->h[row + 0xc00]       & cached[row/2 + 0x12 /*=+0x24 B*/];
            g->h[row + 0xbd0 + 0xc] = 0;   // limpa acumulador A
            g->h[row + 0xc00]       = 0;   // limpa acumulador B
        }
    }

PASS2:
    // registra c74/c75/c76 anteriores, prepara contexto de linha
    // (gMapX, gMapY, g->b[0], g->h[2] com sinal, g->b[0x19b9]) em slots
    // de pilha reaproveitados no laço de bits abaixo.
    // Em seguida: 2 iterações externas consumindo, respectivamente,
    // a tabela +0xb94 (resultado da passada 1, mode 0/2 ∩ cache) e a
    // tabela +0xbb8 (idem, offset +0x24) — para cada bit setado em
    // cada linha:
    //   - se g->b[0x19b9] == 0: checa terreno da tile (tabela GOT A
    //     indexada por g->b[0], byte lido, comparado a 4) -> se ==4,
    //     limpa o bit (ver 21.3).
    //   - se g->b[0x19b9] != 0: faz o mesmo + uma checagem extra
    //     contra um "subtipo de tile" e g->h[2] (ver 21.3, caminho
    //     mais elaborado).

    if (g->b[0x10] & 8) goto SKIP_SECOND_PASS;  // (ver 21.4, bit não
                                                  // totalmente isolado)

    // ---- PASSADA 2 (mode 1/3 = área/AoE) ----
    for (idx = 0; idx < 21; idx++) {
        if (!g->b[0xc8d + idx]) continue;   // MESMO array "marcado" #1
        GetPanelUnderUnit(idx, &g->b[0xc74]);
        mode = (g->b[0x26] == 6) ? 3 : 1;
        GetTargetBaseArea(mode, 0);
        if (!g->b[0xe3b]) continue;
        for (row = 0; row < g->b[0xe3b]*2; row += 2) {
            g->h[row + 0xbd0 + 0xc] |= g->h[row + 0xb40 + 0xc];
            g->h[row + 0xc00]       |= g->h[row + 0xb70];
        }
    }

    // se g->b[0xe] & 0x10: percorre o array "marcado" #2 (g->b[0xca1+k])
    // em paralelo com bwork[] (stride 0x1e6 confirmado!), e para cada
    // unidade viva relevante alterna (XOR) um bit em g+0x5e0 baseado
    // na posição daquela unidade -- ver 21.4; efeito nunca é lido de
    // volta DENTRO desta função (fica pra outro consumidor).

    if (g->b[0xe3b]) {
        // funde (AND) as duas regiões +0xc20/+0xbd0/+0xc00 entre si
        // com deslocamentos fixos de 0x46/0x48 B -- ver 21.4, não
        // totalmente isolado qual "linha" corresponde a qual.
    }

SKIP_SECOND_PASS:
    g->b[0xcbb] = CountMap(&g->b[0xbdc]);          // conta máscara final (passada 2)
    g->b[0xcbc] = CountMap(&g->b[0xbdc] - 0x48);   // conta máscara da passada 1 (+0xb94)
}
```

### 21.3 Achado forte: `mode` 0/2 = alcance, `mode` 1/3 = área — confirma a semântica de "TG"

As duas passadas usam exatamente os pares de `mode` que
`GetTargetBaseArea` (seção 20.1) já definia como **alcance puro**
(`mode 0`, ou `2` quando combinado com área) e **área pura** (`mode 1`,
ou `3` — que, pela correção da seção 20.5, hoje sempre degenera pra
`areaVal=0` porque o chamador aqui passa `0` como 2º argumento em
ambas as chamadas). Isso fecha com muita confiança a leitura de que
esta função produz **dois conjuntos de painéis**: um de "onde a
habilidade alcança" (passada 1) e outro de "qual a pegada de área da
habilidade a partir de cada painel candidato" (passada 2) — literalmente
o "Target Group" (conjunto de alvos válidos) + "máscara de alcance"
que a seção 6.1 já tinha inferido de fora, agora com o mecanismo
completo por dentro.

**Achado extra importante:** as duas passadas usam o **mesmo par de
acumuladores de scratch** (`g+0xbd0`/`g+0xc00`) — não são regiões
paralelas independentes. A passada 1 roda, salva seu resultado
(intersectado com a tabela por-unidade `g+0xa70`) em `g+0xb94`/`g+0xbb8`,
**zera os acumuladores**, e só então a passada 2 roda reusando o
mesmo espaço.

### 21.4 O caminho condicional por `g->b[0x19b9]` (invalidação de terreno tipo 4)

O laço de bits por linha (que roda duas vezes, uma por tabela de
passada 1) testa cada bit setado; se o terreno da tile (lookup
GOT-resolvido, indexado por `g->b[0]` = id do invocador) é `4`
(obstáculo, mesmo valor já visto em outras rotinas), o comportamento
depende de `g->b[0x19b9]` (byte vizinho ao flag "IA ativa" conhecido,
`+0x1980+0x37`, mas não o mesmo byte):

- **`g->b[0x19b9] == 0`** (caminho simples, `0x2786ac`–`0x2786d4`):
  terreno `4` → **limpa o bit incondicionalmente** (tile obstáculo não
  é destino válido).
- **`g->b[0x19b9] != 0`** (caminho elaborado, `0x278908`–`0x2789c4`):
  além do terreno, consulta um registro de 8 bytes por tile (tabela
  GOT A, indexada por `coluna*8`, byte `+3` = "subtipo da tile"). Se
  esse subtipo for **> 63**, limpa o bit sempre. Se for **≤ 63** e o
  terreno for `4`, faz **mais um lookup** (tabela GOT C, indexada por
  `subtipo & 0x3f`) e compara o resultado contra `g->h[2]` (campo de
  16 bits com sinal, carregado uma vez no início da função) — só limpa
  o bit se **não bater**. Isso tem toda a aparência de "terreno tipo 4
  cobre vários subtipos (lava, água, etc.), e a habilidade só pode
  alcançar aquele subtipo específico se `g->h[2]` (provavelmente a
  afinidade elemental/terreno exigida pela habilidade) combinar" —
  mecanismo plausível, mas o papel exato de `g->h[2]` e das 3 tabelas
  GOT não foi cruzado com nome de símbolo (ver 21.5).

Bloco adicional, gated por `g->b[0xe] & 0x10` (`0x2787e8`–`0x278878`,
só roda depois da passada 2): percorre o array "marcado" #2
(`g->b[0xca1+k]`, 21 bytes) em paralelo com um ponteiro que **avança
exatamente `0x1e6` (486) bytes por iteração** — confirmando de novo o
stride real de `bwork[]`. Para cada unidade onde
`(g->b[0x26]==5) || (bwork[idx].b[0x61] & 4)` é verdade, calcula o
painel da própria posição da unidade (`b[0x4f]/b[0x50]/b[0x51]`, igual
a `GetPanelUnderUnit`) e **alterna (XOR)**, não limpa, um bit em
`g+0x5e0` (tabela de 18 halfwords por linha — resolve a aparente
discrepância de stride da seção anterior: `g+0x5e0` usa stride 18
halfwords, `g+0xa70` usa stride 0x48 B por unidade — **são duas
tabelas diferentes**, não a mesma tabela lida com strides
conflitantes). O resultado em `g+0x5e0` **nunca é lido de volta dentro
desta função** — é efeito colateral para outro consumidor (candidato
mais provável: o código que decide se um painel de movimento está
"ocupado por outra unidade", mas o call site que lê `g+0x5e0` não foi
localizado nesta iteração).

Bloco final condicional em `g->b[0xe3b]` (gMapY, `0x278878`–`0x2788dc`):
faz duas passadas de AND entre as regiões `+0xc20`/`+0xbd0`/`+0xc00`
com deslocamentos fixos de `0x46`/`0x48` bytes, produzindo o conteúdo
final que é contado em `g->b[0xcbb]`. A relação exata de alinhamento
entre as três regiões sobrepostas (`+0xbd0`, `+0xc00`, `+0xc20`) **não
foi totalmente isolada** — ficou claro que é uma fusão/interseção das
duas tabelas da passada 2, mas não o motivo do deslocamento de
0x46/0x48 especificamente.

### 21.5 O que ficou sem confirmar

- **Ponteiros GOT sem nome usados no laço de validação de
  terreno/subtipo — resolvidos na seção 26**: a tabela
  "terreno-por-caster" é `comtype` (já catalogada); a tabela de 8 B
  por painel resolve pro endereço `0x565db8` (sem símbolo); a tabela
  de lookup-por-subtipo resolve pro endereço `0x3d21bc` (sem
  símbolo) — essas duas últimas continuam sem nome real, só com
  endereço confirmado.
- O significado exato de `g->h[2]` (campo de 16 bits com sinal, lido
  uma vez no início da passada de bits) — hipótese forte é "afinidade
  de terreno/elemento exigida pela habilidade atual", mas não
  confirmado contra nenhum outro call site.
- Quem **lê** `g+0x5e0` depois que este bloco o escreve (XOR) — efeito
  colateral sem consumidor identificado nesta função.
- O alinhamento exato de linha entre `+0xbd0`/`+0xc00`/`+0xc20` no
  bloco de fusão final (21.4, último parágrafo).
- O bit `g->b[0x10] & 8` que pula a passada 2 inteira (`0x278730`) —
  mecanismo claro (skip condicional), mas o significado do bit (que
  categoria de habilidade dispensa o cálculo de área?) não foi
  cruzado com outra função.

### 21.6 Fecha o plano de prioridade 🔴

Com esta função, **todos os 4 itens de prioridade alta do
`RE_BACKLOG_PLAN.md` estão lidos e documentados** (seções 18–21). O
loop passa agora para a prioridade 🟠 (parsers/motores já começados:
`TIM_LoadMemory`, `CG2D_LOADER_TIM::Load`, opcodes de áudio do motor
de eventos, e as ~50 funções pequenas restantes de `wld_*`).

## 23. `MakeMapDanger()` lida por completo — fecha o item pendente da seção 18, primeiro item da Fase 2 (2026-10-16, Fase 2, iteração 1)

A seção 18 tinha deixado pendente o corpo de `MakeMapDanger()`
(chamada pela fase 1 interna de `BattleRoutine`). Lida agora por
completo: `MakeMapDanger()` (`0x27b0b0`, 400 B, cobertura total: 98
instruções reais pra 98 esperadas).

### 23.1 Fase 1 da função: fecha "quem escreve" o array de alvos marcados #1

```c
void MakeMapDanger_Phase1() {
    for (int idx = 0; idx < 21; idx++) {
        g->b[0xc8d + idx] = 0;                       // zera o slot
        if (IsAlmostNullUnit(idx)) continue;           // 0x273cc8 — unidade quase morta, ignora
        if (!IsNeedlessToFear(idx))                      // 0x27afdc — "não há nada a temer"?
            g->b[0xc8d + idx] = 1;                         // marca como "ameaça real"
    }
}
```

**Achado que fecha um buraco antigo**: o array `g->b[0xc8d..0xca1]`
(21 bytes) — já usado como "array de alvo marcado #1" por
`GetDestinationsAndMakeMaskTG`/seção 21 e por outras funções, mas
nunca com a escrita confirmada — **é escrito exatamente aqui**: marca
como "1" cada unidade que não está quase morta E que não é
"dispensável de temer" (ou seja, uma ameaça real). `IsAlmostNullUnit`/
`IsNeedlessToFear` não foram lidas por dentro, mas os nomes já
confirmam o papel com alta confiança.

### 23.2 Fase 2 da função: o "mapa de perigo" real — distância Manhattan com raio 10

```c
void MakeMapDanger_Phase2() {
    int16_t gMapY = g->b[0xe3b], gMapX = g->b[0xe3a];     // seção 9.5
    for (int pass = 0; pass < 2; pass++) {                  // sp8 = 0, depois 0x24 — 2 passadas
        uint8_t* dangerBase = (uint8_t*)g + pass*8;            // ver 23.3, endereçamento não 100% resolvido
        uint16_t* rowMaskPtr = (uint16_t*)((uint8_t*)g + 0xa72 + pass);
        for (int row = 0; row < gMapY; row++) {
            uint16_t rowMask = *++rowMaskPtr;                   // tabela em g+0xa70, mesma região da seção 21
            if (rowMask == 0 || gMapX == 0) continue;
            for (int col = 0; col < gMapX; col++) {
                if (!(rowMask << col & 0x8000)) continue;          // só colunas com bit setado na máscara da linha
                dangerBase[col + 0x174] = 0;                        // zera antes de acumular
                for (int k = 0; k < 21; k++) {                       // mesmo array de "ameaça real" da fase 1!
                    if (!g->b[0xc8d + k]) continue;
                    int dx = abs(bwork[k].b[0x4f] - col);              // posição real da unidade (campos
                    int dz = abs(bwork[k].b[0x50] - row);               // já confirmados em todo o resto do doc)
                    int dist = dx + dz;                                  // distância Manhattan
                    if (dist <= 10)
                        dangerBase[col + 0x174] += (10 - dist);            // *** contribuição de perigo ***
                }
            }
        }
    }
}
```

**Confirma o mecanismo real do "mapa de perigo" da IA**: cada unidade
marcada como ameaça real (fase 1) contribui com perigo pra cada
painel dentro de um raio de **10 (distância Manhattan)**, com a
contribuição caindo linearmente (`10 - distância`) conforme a
distância aumenta — exatamente o "mapa de calor de ameaça" clássico
que uma IA de tática usa pra decidir painéis seguros de recuo/avanço.
Confirma de novo o stride real de `bwork[]` (`0x1e6`) e os campos de
posição `b[0x4f]`/`b[0x50]` (já usados em toda a investigação).

### 23.3 O que ficou sem confirmar

- **O endereçamento 2D exato do acumulador de perigo (`+0x174`)**: a
  posição de escrita (`dangerBase + col`) depende da coluna e da
  passada (`pass`, só 2 valores: `0`/`0x24`), mas **não da linha
  (`row`)** dentro do loop — ou seja, cada coluna acumula
  contribuições de TODAS as linhas onde o bit da máscara daquela
  linha está setado, não um grid 2D completo linha×coluna. Não ficou
  claro se isso é intencional (o "perigo" é por coluna, não por
  painel completo) ou se há uma indireção que não enxerguei. Marcado
  como ambíguo em vez de forçar uma leitura — exatamente o caso que a
  metodologia do plano pede pra escalonar, não inventar.
- `IsAlmostNullUnit`/`IsNeedlessToFear` não lidas por dentro — nomes
  dão confiança alta no papel, mas não confirmado por instrução real.
- Quem **consome** o mapa de perigo em `g+0x174` depois de calculado
  (provavelmente a função de decisão de movimento da IA, não
  localizada nesta passada).

## 24. Quem toca `g+0x5e0` — achado: uma função de ~1200 B sem símbolo, nunca documentada antes (2026-10-16, Fase 2, iteração 2)

Segundo item da Fase 2: "quem lê `g+0x5e0`" (tabela de ocupação de
painel escrita por `GetDestinationsAndMakeMaskTG`, seção 21, mas nunca
lida de volta na própria função). Escrevi um script novo
(`find_imm.py`, mesma técnica de varredura linear do `find_bl.py`,
mas procurando um **imediato** em vez de um alvo de `bl`) pra varrer
`.text` inteiro por instruções usando o literal `0x5e0`. Filtrando os
falsos positivos (a grande maioria é `ldr rX,[pc,#0x5e0]` — carga de
literal pool, deslocamento coincidente, nada a ver com `g`) e
restringindo à região de código da IA (`0x270000`–`0x280000`), sobrou
**um único candidato real**: `0x278014`.

Esse endereço cai dentro de uma função **sem símbolo no `.dynsym`**
(local/`static`, como outras já vistas nesta investigação) — o `.so`
não tem NENHUM nome pra ela. Chamo de `sub_277f78` (`0x277f78`,
~1204 B, `0x277f78`–`0x27842c`). **Não lida por completo** — é grande
demais pro escopo deste item específico — mas o suficiente pra
confirmar o que importa pra esta pergunta:

```c
// sub_277f78() — parte do laço de avaliação/escolha de movimento da IA
void sub_277f78() {
    if (!(g->b[0x19b7] && g->b[0xc72])) { /* ...caminho alternativo, não lido... */ return; }

    // lê g->h[0x28]/h[0x2a]/h[0x2c] (coordenadas candidatas X/Y/Z) e
    // toggla um bit em g+0x5e0 (stride 18 halfwords, mesma tabela da
    // seção 21!) usando essas coordenadas:
    uint16_t* row = &g->h[(g->h[0x2a] * 18 + g->h[0x2c]) + (0x5e0/2) + 6];
    *row ^= (0x8000 >> g->h[0x28]);     // *** idêntico ao idioma da seção 21 ***

    SetBestMove();          // 0x277f1c — chamado ANTES deste trecho, no topo do laço
    // ... segue um laço sobre as colunas do mapa (0..gMapX), testando
    // bits de uma máscara de destino (r6) e, para cada bit setado,
    // repetindo o ciclo "atualiza g->h[0x28/0x2a/0x2c] -> chama
    // SetBestMove() de novo" -- claramente a ITERAÇÃO sobre painéis
    // candidatos de destino que todo o resto do documento já citava
    // de fora, mas nunca tinha sido localizada concretamente.
}
```

**Achado principal**: `g+0x5e0` tem **dois pontos de contato
confirmados**, não um: `GetDestinationsAndMakeMaskTG` (seção 21,
constrói a ocupação a partir da posição real das unidades vivas) e
este `sub_277f78` (togla bits durante a própria avaliação/iteração de
movimento candidato, chamando `SetBestMove()` em laço). A varredura
sistemática por imediato `0x5e0` em toda a região de código da IA
**não achou nenhum terceiro ponto** — ou seja, não existe (ou não é
visível por essa técnica) um "consumidor puro" que só lê a tabela pra
filtrar destinos; os dois pontos encontrados são ambos
leitura-modificação-escrita (XOR), não leitura simples.

**Escalonado, não forçado**: `sub_277f78` é claramente uma função
importante (provavelmente o verdadeiro "laço de escolha de melhor
movimento" da IA, nunca documentado até agora) — grande demais pra
ler por completo dentro do escopo deste item. Adicionada como novo
item 🟠 no `RE_BACKLOG_PLAN_PHASE2.md` pra uma leitura dedicada futura.

### 24.1 O que ficou sem confirmar
- `sub_277f78` por completo (só a parte relevante pra `g+0x5e0` foi
  lida com confiança).
- `sub_224d4c`/`sub_224650`/`0x271e1c` (chamados por `sub_277f78`,
  nomes/papéis não investigados).
- Se existe um consumidor "read-only" de `g+0x5e0` que a técnica de
  varredura por imediato não conseguiria achar (ex.: acessado via um
  ponteiro computado em OUTRO lugar e só passado como parâmetro, sem
  reconstruir o literal `0x5e0` de novo).

## 25. `sub_277f78` lida por completo — o verdadeiro laço "iterar destinos candidatos e avaliar cada um" da IA (2026-10-16, Fase 2, iteração 5)

A função sem símbolo achada na seção 24 (`0x277f78`–`0x27842c`,
1204 B) foi lida por completo (301 instruções, cobertura total). É,
com alta confiança, **o laço central que a seção 6.1 já citava de
fora como "quem decide o melhor movimento"** — fecha esse buraco de
vez, e amarra sozinha achados de 5 seções diferentes (18, 20, 21, 23,
24) num único mecanismo coerente.

### 25.1 Visão geral confirmada

```c
void sub_277f78() {   // nome de referência — sem símbolo no .dynsym
    if (!(g->b[0x19b7] && g->b[0xc72])) goto COOLDOWN_OR_COMMIT;  // ver 25.4

    // lê uma máscara de linha da tabela em g+0x5a0 (mesmo formato
    // mla(row,0x12,z)+0x5a0 — tabela PARALELA à +0xa70, papel exato
    // não isolado) usando a posição candidata atual
    // (g->h[0x28]=coluna, g->h[0x2a]=linha, g->h[0x2c]=z)
    int result = SetBestMove();          // 0x277f1c — AVALIA a posição candidata atual
    if (result == -1) { g->b[0xc72] = 1; return; }   // sinaliza "tentar de novo"

    if (!g->b[0x19bc]) return;             // flag irmã da "IA ativa" (+0x1980+0x3c) — sem ela, sai

    if (g->b[0xe4e] != 0) {
        // *** togla o bit em g+0x5e0 pra este candidato (seção 24) ***
        g->h5e0row ^= (0x8000 >> col);
        // *** decrementa o contador de painéis restantes! ***
        if (--g->b[0xcbb] != 0) goto NEXT_CANDIDATE;    // 0xcbb = contagem da seção 21 (CountMap)!
        // contagem zerou -> avança pra próxima "linha" de busca
        g->b[0xcbb-ish state]; iteration_row++;
    }
    goto MAIN_SCAN_LOOP;   // ver 25.3
}
```

**Confirma, com leitura real, quem consome `g->b[0xcbb]`** — o
contador de painéis de destino que `GetDestinationsAndMakeMaskTG`
calculava via `CountMap` (seção 21) e que ficava sem consumidor
identificado: **é decrementado aqui, um por candidato avaliado**, até
chegar a zero.

### 25.2 `COOLDOWN_OR_COMMIT` — o watchdog de tempo real da IA, e o "commit" do destino escolhido

Quando a IA não está "ativa" (ou não há mais candidatos pendentes,
`g->b[0xc72]==0`), a função faz duas coisas bem diferentes:

```c
int vcount = VSync(1);                 // *** chamada real da lib gráfica do PS1! ***
if (vcount > 0x1b8 /* 440 */) {         // *** watchdog de tempo: aborta se "pensar" demais ***
    g->b[0xc72] = 0;
    return -1;
}

g->b[0x19b7] = 0;                        // desliga a flag "IA ativa"
void* dest = g->b[0x14] ? &g->b[0xe30] : &g->b[0x18];  // escolhe a origem do destino final
SetThisDestination(dest);                 // *** COMMIT: grava o destino escolhido de verdade ***

if (g->b[4] != 0) {                        // contexto de habilidade específica
    if (getskillrange(&g->b[0x1c]) == 3) return 0;   // 0x1e03c8 — recalcula alcance, aborta se código 3
}
// (senão) zera o bit 0x40 de um registro de 8 B por painel num array
// de 512 entradas (provável "tabela de ocupação/visitado de todo o
// mapa", stride 8 B — tamanho MUITO maior que `bwork` — ver 25.5),
// depois marca esse mesmo bit SÓ pro painel que acabou de ser
// escolhido (`dest`) -- "desmarca tudo, marca só o escolhido".
```

**Achado maior: a IA tem um orçamento de tempo real, medido em
contagens de `VSync` (biblioteca gráfica do PS1 de verdade), não em
número de candidatos** — se passar de **440 VSyncs** avaliando
candidatos, a busca é abortada (`g->b[0xc72]=0`, retorna `-1`). Isso é
literalmente um watchdog de "não deixa a IA travar o jogo pensando
demais", medido pelo mesmo relógio que o jogo usa pra desenhar
quadros. E **`SetThisDestination` é a função real de "commit"** —
grava o destino que `SetBestMove()` escolheu ao longo de todas as
iterações anteriores.

### 25.3 O laço principal de varredura — filtro de alcance de arma (arco/arma de fogo)

O corpo central (`0x278104`–`0x278318`) é um laço duplo
linha-por-linha/coluna-por-coluna sobre uma máscara construída a
partir da região de `GetTargetBaseArea` (`g+0xb40`) **intersectada**
com a tabela de 512 entradas mencionada em 25.2 (só considera painéis
que foram marcados como "escolhidos" em alguma iteração anterior —
mecanismo de deduplicação entre passadas, não isolado por completo).
Pra cada bit setado (um painel candidato):

```c
g->h[0x2a] = row; g->h[0x28] = col; g->h[0x2c] = z;   // define a NOVA posição candidata

if (g->b[0x26] == 6 || (g->b[0xf] & 0xc0)) {
    // acha qual unidade de bwork[] (se alguma) ocupa este painel
    // exatamente (bwork[k].b[0x4f]/b[0x50]/b[0x51]) e grava o índice
    // em g->b[0x27]; se nenhuma, recomeça o fluxo de "próximo candidato"
} else if (g->b[0xf] & 0x80) {                              // *** flag "arco" ***
    if (!CheckBowReachable(g->b[0xe2e], g->b[0x27])) {        // 0x224650
        continue;   // painel fora de alcance de arco -> descarta, próxima coluna
    }
} else if (g->b[0xf] & 0x40) {                              // *** flag "outra arma à distância" (arma de fogo?) ***
    if (comtype[g->b[0]] == 1) {    // *** confirmado na seção 26: é `comtype`, não uma tabela nova ***
        // caso especial: se a distância real (GetDistance, 0x271e1c)
        // entre o invocador e o alvo for <= 1 (adjacente), PULA o
        // teste de arma — só testa CheckGunReachable se for > 1
        if (GetDistance(...) > 1 && !CheckGunReachable(g->b[0xe2e], g->b[0x27]))  // 0x224d4c
            continue;
    } else if (!CheckGunReachable(g->b[0xe2e], g->b[0x27])) {
        continue;
    }
}
// painel passou os filtros -> decide g->b[0xe4e] a partir de um bit
// de g->b[0xcb7], e VOLTA PRO TOPO (chama SetBestMove() de novo pra
// esta nova posição candidata)
goto TOP;
```

**Confirma, com chamadas reais, os dois filtros de alcance de arma à
distância da IA**: `CheckBowReachable`/`CheckGunReachable` (nomes
reais do `.dynsym`) — a IA não considera um painel de destino válido
pra uma habilidade de arco/arma de fogo sem antes confirmar
alcançabilidade real, com um atalho de "se já está adjacente, nem
precisa checar arma de fogo" via `GetDistance`.

### 25.4/25.5 O que ficou sem confirmar
- O papel exato da tabela em `g+0x5a0` (mesma fórmula de indexação da
  `+0xa70`, mas base diferente — provavelmente um dado paralelo por
  linha, não isolado).
- A tabela de 512 entradas × 8 B (`bit 0x40` = "painel escolhido
  nalguma iteração") — maior que `bwork` (21×486 B), provavelmente
  cobre painéis de mapa, não unidades; papel exato de dedução
  cruzada com a máscara de `GetTargetBaseArea` não fechado 100%.
- `g->b[0x14]`, `g->b[4]`, `g->b[0x26]==6`, `g->b[0xcb7]` bit 1 — todos
  usados como seletores de caminho, papel de negócio exato (que
  categoria de ação/habilidade cada valor representa) não cravado.
- `weaponCategoryTable` (lookup GOT por `g->b[0]`, caster) — **resolvido
  na seção 26: é `comtype`**, não uma tabela nova.

## 26. Resolução de literais GOT sem nome — primeiro item ⚪ da Fase 2 (2026-10-16, Fase 2, iteração 19)

Primeiro item ⚪: fechar os literais GOT sem nome deixados abertos nas
seções 21/25. Técnica: ler o valor bruto do pool de literais (o
deslocamento somado ao `sl`/`r8`, a âncora GOT confirmada
`0x347d58`), calcular o endereço final, e cruzar com os globais já
nomeados na investigação.

### 26.1 Achado principal: 3 referências antes isoladas eram todas `comtype`

As 3 tabelas da seção 21 marcadas como "terrain-table A" (usada em
`GetDestinationsAndMakeMaskTG`, comparada contra `4`) e a
`weaponCategoryTable` da seção 25 (usada em `sub_277f78`, comparada
contra `1`) resolvem **para o mesmo endereço**: `0x3cd9b8` = `comtype`
(já catalogada, seção 9.3/tabela de globais, 256 B, indexada por
`g->b[0]`). Confirmado comparando o deslocamento exato do literal
(`-0x1910` relativo à âncora GOT, idêntico nos dois pontos de
chamada).

**Isso fecha 3 usos isolados de `comtype` em uma única tabela
coerente**, usada com constantes de comparação diferentes conforme o
contexto: `==10` (seção 9.3, achado original), `==3` (seção 14.4,
`CheckCrystalAndTresureBox`), `==4` (seção 21, validação de
terreno), `==1` (seção 25, decisão de pular checagem de arma de
fogo). Isso é consistente com `comtype` ser uma pequena enumeração de
categoria (provavelmente "tipo de movimento/interação com terreno"
por unidade), onde cada chamador testa pelo valor específico que lhe
interessa — mas o significado exato de cada valor numérico (0-255,
quais correspondem a quê) continua sem ser cravado.

### 26.2 Duas tabelas novas, endereço confirmado mas sem nome

- **Tabela "8 B por painel"** (seção 21, usada em
  `GetDestinationsAndMakeMaskTG` pra validar subtipo de tile) resolve
  pro endereço **`0x565db8`** — fica logo depois do fim real de
  `bwork[]` (`0x563560` + `0x27de` = `0x565d3e`, só 122 B de
  distância) — provavelmente um array de registros por painel do
  mapa (não confirmado o tamanho total nem o propósito de cada um dos
  8 bytes por entrada, só que o byte `+3` é comparado contra `0x3f`).
- **Tabela "lookup por subtipo"** (seção 21, usada tanto no caminho
  simples quanto no caminho complexo da validação de terreno) resolve
  pro endereço **`0x3d21bc`** — não adjacente a nenhum global já
  nomeado nesta investigação (`aa`/`comtype`/`SV`/`area_data`).

**O que ficou sem confirmar:** os literais GOT das seções 13.6/17.6
(constantes `SL_IID_*` e layout de `SLDataFormat_PCM`, motor de
áudio) e da seção 13.7 (tabela de subtipo de tile do `DecodeTexture`)
não foram resolvidos nesta passada — ficou só a parte do lado da IA
de batalha, que tinha os endereços de chamada mais concretos já
documentados.

## 27. Os 7 blocos de fallback do `BattleRoutine` — segundo item ⚪ da Fase 2, fecha a pendência da seção 18 (2026-10-16, Fase 2, iteração 20)

A seção 18 tinha deixado pendentes 7 endereços de blocos de fallback
nunca lidos (`0x275d84`/`0x275d30`/`0x275ba8`/`0x275d10`/`0x275dd0`/
`0x275e18`/`0x275ae8`), fora do range de 1232 B lido na época. Lidos
agora todos — e, como estão intercalados num intervalo contíguo de
~816 B, a leitura revelou **mais ~10 blocos irmãos** que não tinham
sido explicitamente pedidos, mas fazem parte do mesmo tecido de
"saltos de volta pro meio do `BattleRoutine`".

### 27.1 Achado principal: `g->b[0xed4]` é o código de motivo de saída da IA

Confirmado por 3 blocos diferentes que convergem no mesmo padrão:
antes de `BattleRoutine` retornar `-1` pelo seu epílogo real
(`0x274c18`, bate com o range `0x274764`–`0x274c1c` já confirmado),
sempre se grava `g->b[0x19b7]=1` (flag "IA ativa", já conhecida) **e**
um valor diferente em `g->b[0xed4]`:

| Bloco | `g->b[0xed4]` | Contexto |
|---|---|---|
| `0x275d84` | `1` | fallback direto (condição não decomposta) |
| `0x275ddc` | `2` | depois de `sub_272aac()` retornar `-1` |
| `0x275dfc` | `0` | fallback direto (condição não decomposta) |

**Isso confirma que `g->b[0xed4]` é um código de "motivo pelo qual a
IA parou de pensar"**, nunca identificado antes — um dado novo e
concreto pra uma investigação futura que queira mapear os valores
0/1/2 a motivos específicos.

### 27.2 Outros achados confirmados

- **Confirma mais um escritor da tabela `+0xa70`** (18 halfwords de
  stride, mesma região das seções 21/23): o bloco `0x275b34` grava
  direto a partir de `g->b[0xe30]/[0xe31]/[0xe32]` (campos de
  posição-alvo já estabelecidos) via `(0x8000 >> col)`, mesmo idioma
  de bit confirmado em várias outras seções.
- **Confirma mais dois flags vizinhos da já conhecida "IA ativa"**
  (`g->b[0x1980+0x37]`): `g->b[0x1980+0x36]` e `g->b[0x1980+0x39]` —
  ambos usados nesses blocos de fallback, papel exato não cravado.
- **Um bloco (`0x275ba8`) zera `g->b[0x1836]`(`+0x36`) e preenche o
  array `g->b[0xc8d..0xca1]` (21 slots) com `1` incondicionalmente**
  — diferente de `MakeMapDanger` (seção 23), que só marcava unidades
  específicas; aqui é "marca todo mundo como ameaça", um caminho de
  fallback mais agressivo/pessimista.
- **Um bloco grande (`0x275bf4`–`0x275d0c`, ~280 B) implementa um
  laço de busca duplo (até 256×256 iterações)**, chamando duas
  funções nunca vistas (`sub_279b70`, `sub_28551c`), comparando bytes
  de registro (`+5`/`+2`) e um campo de outro struct (`+0x1de`,
  bits `0x30`) contra uma tabela GOT indexada por tipo — provável
  busca de "melhor item/equipamento compatível" entre até 256
  candidatos, mas **não decomposto por completo** (escala grande
  demais pro escopo deste item; candidato a item próprio numa
  iteração futura).
- `0x275e18` confirma `GetPanelUnderUnit`/`IsAlmostNullUnit` (ambas já
  nomeadas, seções AI anteriores) sendo chamadas em sequência pra
  validar a posição de uma unidade específica antes de decidir o
  próximo salto.
- Revela 2 funções novas, não investigadas: `sub_272aac()` (chamada
  em `0x275b7c`, resultado comparado contra `-1`/`0` pra escolher
  entre 3 caminhos diferentes) e `sub_27207c(5)` (chamada em
  `0x275dd4`).

### 27.3 O que ficou sem confirmar
- O laço de busca de `0x275bf4` por completo (ver 27.2).
- `sub_272aac`/`sub_27207c` — só os pontos de chamada, não o corpo.
- O significado exato dos valores `0`/`1`/`2` de `g->b[0xed4]` em
  termos de jogo (que condição real cada um representa).

## 28. `FundamentalRoutine()` — passe estrutural — o dispatcher central que amarra várias sub-rotinas de IA já lidas separadamente (2026-10-17, Fase 3, lote paralelo)

`FundamentalRoutine()` (`0x278f84`, 2.880 B) — descida recursiva via
`jtable.py` (ferramenta nova da Fase 3, validada contra o switch de
`battle()`): **688 de ~720 instruções possíveis (96%)**, uma tabela
de salto resolvida (9 casos, 9 endereços distintos); **100
branches, 56 de retrocesso**.

### Confirma ser o dispatcher central de fase da IA, amarrando sub-rotinas já lidas em seções anteriores

```
SetBestMoveAnywhereOK() / SetBMList()           — já citadas desde a seção 6.1
CheckUnitActionOK(unsigned char*) / CheckUnitActionEffective(int,int)
GetTargetBaseArea(int,int) / JudgeMovable(int) / SetThisDestination(unsigned char*)
SetBestMove() / sub_277f78 (RecheckFlaggedTargets, §17.4) / sub_277f78 (§25)
JudgeStatus(int, BWORK*, int) / GetPanelUnderUnit(int, unsigned char*)
CheckCrystalAndTresureBox() / GetCountToDeath(BWORK*) / CheckAbilityGet(int,int,int)
get_ability(int,int) / pspItemGetOptionData / pspRoutineCheckArithmeticPermission()
```
O switch de 9 casos (um "estado/fase" de decisão por caso) confirma
que `FundamentalRoutine` é o **ponto de dispatch que várias
sub-rotinas de IA já lidas nesta investigação (§6.1, §17.4, §25)
tinham como contexto implícito, mas nunca com o chamador real
identificado**. Dois achados novos concretos: **`CheckCrystalAndTresureBox()`**
confirma que a IA considera explicitamente painéis de cristal/baú de
tesouro (mecânica real do FFT quando uma unidade morre) na tomada de
decisão; **`GetCountToDeath(BWORK*)`** confirma que a IA calcula
quantos turnos faltam até uma unidade morrer (ex.: por veneno/
contagem regressiva), informação usada pra priorizar alvos.
`pspRoutineCheckArithmeticPermission()` é um nome estranho, não
decifrado — tratado como está.

**O que ficou sem confirmar**: os corpos dos 9 handlers da tabela
(qual fase de decisão corresponde a qual caso); a ordem exata de
chamada das sub-rotinas dentro de cada caso. Marcada
`read_structural`.
