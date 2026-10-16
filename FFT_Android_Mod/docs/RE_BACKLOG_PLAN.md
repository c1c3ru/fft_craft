# Plano de ação — zerar a pendência de engenharia reversa do `libgl2jni.so`

Este documento é o **estado de trabalho** consumido por um loop (`/loop`)
que continua esta investigação de forma incremental, sessão após sessão.
Cada item marcado `[ ]` é um alvo concreto; `[x]` significa lido e
documentado. Os dois documentos de resultado são:

- `AI_DIFFICULTY_RESEARCH.md` — IA de batalha (`BattleRoutine`,
  `FundamentalRoutine`, `EvaluationFunction` etc.)
- `REVERSE_ENGINEERING_NOTES.md` — tudo o resto (licença/OBB, CCRYPT,
  TIM, motor de eventos, `wld_*`, `CEGL2_*`, `CSOUND_*`)

## Como o loop deve operar (metodologia já validada nesta investigação)

1. **Escolher o próximo item não marcado**, nesta ordem de prioridade
   (seções abaixo, de cima para baixo).
2. **Desmontar via Capstone** (`disasm.py`/`disasm_cfg.py`, recriar o
   venv em `/tmp` se necessário — ver "Ferramentas" ao final). Hopper
   **não funciona** neste ambiente (trava na inicialização,
   `provider_timeout` depois de 120s) — nem tentar de novo.
3. **Resolver os alvos de `bl`** contra `.dynsym` antes de ler o corpo
   — isso sozinho já revela o papel de muita coisa. Para `.plt`, usar a
   técnica de somar os dois `add` do stub + o offset do `ldr pc,[...]`
   e cruzar com `.rel.plt` (script descrito na seção "Ferramentas").
4. **Ler o corpo real**, escrever pseudocódigo fiel à aritmética, com
   honestidade de cobertura (nunca afirmar "lido por completo" sem ter
   lido de verdade; nunca afirmar papel de uma função só pelo nome sem
   cruzar com alguma evidência real quando for uma função nova/pouco
   óbvia).
5. **Documentar** no arquivo certo (seção numerada nova, não misturar
   IA de batalha com o resto), **marcar o item como `[x]` neste
   plano**, e no fim da sessão/iteração: **commitar e dar push** no
   branch `worktree-fft-re-loop`.
6. **Parar e escalonar** se um alvo específico resistir (ex.: função
   grande demais pro orçamento da iteração, ou achado ambíguo) — anotar
   o motivo ao lado do item em vez de forçar uma leitura rasa.

## 🔴 Prioridade alta — fecha os ~3 furos que sobraram da IA de batalha

- [x] `BattleRoutine` fase 1 interna (`0x27537c`–`0x27584c`, ~1232 B) —
  lida por completo, ver `AI_DIFFICULTY_RESEARCH.md` seção 18. Achado:
  é a etapa de "censo de unidades + mapa de perigo", termina chamando
  `MakeMapDanger()`. Revelou `ClearMove(MOVE*)` e `MakeMapDanger()`
  (novos), e um salto de controle de volta pro bloco "não pensando" da
  seção 14.2 (`BattleRoutine` não é estritamente uma fase por chamada).
  Pendências sub-item: corpo de `MakeMapDanger()`, e os blocos de
  fallback `0x275d84`/`0x275d30`/`0x275ba8`/`0x275d10`/`0x275dd0`/
  `0x275e18`/`0x275ae8` (fora do range de 1232 B lido).
- [x] `sub_275e3c` (`0x275e3c`, **944 B, não 2992** — corrigido erro de
  aritmética de sessão anterior) — lida por completo, ver
  `AI_DIFFICULTY_RESEARCH.md` seção 19. Achado maior: aplica o
  resultado da habilidade a cada alvo (`setskillresult`) e **ajusta
  diretamente `g->h[0x32]` (o campo de pontuação de `EvaluationFunction`/
  `CompareScore`)** com um peso dependente de uma tabela nova
  (`AbilityCatTable`, stride 8 B) — fecha o ciclo "quem grava a
  pontuação" que a seção 6.4 só tinha pela metade. Também processa
  reações (Counter/Counter Magic) recursivamente via `getreaction_post`
  + chamada recursiva de si mesmo.
- [x] `GetTargetBaseArea(int,int)` (`0x276930`, 644 B) — lida por
  completo, ver `AI_DIFFICULTY_RESEARCH.md` seção 20. **Achado maior
  da sessão:** fecha de vez o item original "tabela de 27 formatos de
  AoE" — não é uma tabela de formatos fixos, é um algoritmo gerador
  usando uma tabela minúscula (`area_data`, 8 entradas de 16 bits,
  valores extraídos e confirmados = padrão "diamante crescente"
  2N+1 bits), expandido em tempo real por altura e recortado pela
  largura real do mapa (`gMapX`/`gMapY`).
- [x] `GetDestinationsAndMakeMaskTG()` (`0x278480`, 1932 B) — lida por
  completo, ver `AI_DIFFICULTY_RESEARCH.md` seção 21. **Fecha o
  último item 🔴.** Achado maior: constrói as duas máscaras do "TG"
  (Target Group) citado na seção 6.1 — uma de alcance (`GetTargetBaseArea`
  mode 0/2) e uma de área/AoE (mode 1/3) — cada uma OR-acumulada sobre
  até 21 unidades candidatas, intersectada (AND) com uma tabela
  cacheada por unidade (`g+0xa70`, registro de 0x48 B), com invalidação
  de terreno tipo 4 (caminho simples ou um caminho mais elaborado
  gated por `g->b[0x19b9]` que compara subtipo de tile contra
  `g->h[2]`), e contagem final via `CountMap` em `g->b[0xcbb]`/`[0xcbc]`.
  Também revelou um 2º array paralelo a `bwork[]` (stride 0x1e6
  confirmado de novo) que alterna bits de "ocupação" em `g+0x5e0` como
  efeito colateral sem consumidor identificado. Corrigiu a seção 20:
  `GetTargetBaseArea` tem um `mode==3` não documentado (2º parâmetro
  passa a ser `areaVal` direto nesse caso).

## 🟠 Prioridade média — fecha os parsers/motores já começados

- [x] `TIM_LoadMemory` (`0xa6a9c`, 500 B) — lida por completo, incluindo
  a tabela de salto computada de 21 entradas (extraída lendo os words
  crus), ver `REVERSE_ENGINEERING_NOTES.md` seção 9.8. Achado: o campo
  `field14` que ela lê é o mesmo que `TIM_AnalyzeFileHeader` grava
  (seção 9.2) com os valores `0x18/0x10/8/4` por modo de pixel TIM
  (4bpp CLUT/8bpp CLUT/16bpp direto/24bpp direto) — os 4 casos "reais"
  da tabela de salto (`20/12/4/0`) batem exatamente com esses modos,
  na mesma ordem. Confirmado também, por extração do literal pool
  (`0x55555556`), que o caso 4bpp usa o idioma clássico de compilador
  pra "divisão por 3".
- [x] `CG2D_LOADER_TIM::Load` (**endereço corrigido: `0xa6c90`**, não
  `0xa6cd0` como este plano tinha — `0xa6cd0` cai no meio da função
  real; `.dynsym` confirma `0xa6c90`, mesmo tamanho 204 B) — lida por
  completo, ver `REVERSE_ENGINEERING_NOTES.md` seção 9.10. Confirma o
  mecanismo exato de escolha entre `TIM_LoadFile`/`TIM_LoadMemory`:
  simplesmente `path != NULL`. Achado bônus: `GetImageFormatType`/
  `GetImageFormatExt` retornam `char*` (usadas como origem de
  `strcpy`, não como inteiros).
- [x] Opcodes de áudio/parâmetro do motor de eventos: `snpl_sndreq`,
  `snpl_musicreq`, `snpl_envsndreq`, `snpl_setpara`/`addpara`/
  `subpara`/`chgpara` — lidos linha a linha, ver
  `REVERSE_ENGINEERING_NOTES.md` seção 10.5. Achados: o ponteiro
  global `s` da VM finalmente tem nome real (`snpl_copy`, `0x6b251c`);
  `setpara` escreve direto no parâmetro de 32 bits enquanto
  `addpara`/`subpara` só acumulam um delta pendente de 16 bits
  separado, que só `chgpara` de fato aplica (com clamp `[0,0xffff]`) —
  e `chgpara` **também grava o resultado em `wldinfo_data1`**, uma
  ponte de arquitetura real entre o motor de eventos e o motor
  `wld_*` que não estava documentada.
- [ ] As ~50 funções pequenas restantes de `wld_*` (seção 12.1 lista
  quais das 72 já foram lidas por completo — o resto está só por
  chamada/padrão). Sugestão de ordem: `wldinfo_put` (1040 B),
  `wld_anim` (852 B), `wldrute_draw` (740 B), `wldssd_control` (620 B)
  primeiro (as maiores ainda não lidas).

## 🟡 Prioridade baixa — motores grandes, só a ponte foi confirmada

- [x] `CEGL2_SPRITE` — função-central (`DrawScrollBG`, `0xae584`,
  1676 B) lida por completo, ver `REVERSE_ENGINEERING_NOTES.md` seção
  13.4. Achado: formato de vértice **não-intercalado** (3 arrays
  separados, `stride=0`, sem VBO) — diferente do `DrawPacket`
  intercalado da seção 13.1. Desenha até 2 quads (12 vértices,
  `GL_TRIANGLES`) pra scroll contínuo sem costura, com um 2º caminho
  gated por `GetMultiTextureHandle()`. `AddPacketPartial`/`DrawPartial`/
  `Draw8` continuam não lidos por dentro (critério de "zerado" pede só
  a função-central por item 🟡/⚪, não a família inteira).
- [x] `CEGL2_FBO` — função-central (`Create`, `0xaa980`, 472 B) lida
  por completo, ver `REVERSE_ENGINEERING_NOTES.md` seção 13.5. Confirma
  a sequência real de criação de FBO da OpenGL ES 2.0 (13 imports GL
  novos resolvidos). Achado: `field_0x0` tem papel duplo (guarda o FBO
  anterior durante a criação, depois vira sentinela `-1`).
  `RenderToFBO`/`RenderFromFBO` continuam não lidos por dentro.
- [ ] `CEGL2_SHADER` — cache de shader via `std::map` (`Load` 596/384 B,
  `Begin`/`SetTexture`/`SetMatrix4` já usados por outras funções lidas,
  mas não lidos por dentro).
- [ ] `CEGL2_TEX_HYBRID` — decodificação/upload de textura
  (`GL_IsUpdate` 684 B, `DecodeTexture` 468 B, `GL_Load` 392 B) — **
  conecta direto com o parser TIM** (provável ponto de conversão do
  formato TIM decodificado pra textura GL).
- [ ] `CSOUND_IF_SL::Stream_CreatePlayer`/`Stream_Load` (560/216 B) — o
  lado streaming que ficou só inferido por contraste com o estático
  (seção 17.4).
- [ ] `CSOUND_LOADER_OGG`/`CSOUND_LOADER_PCM` por dentro (`Decode` 540 B,
  `Open` 460/608 B) — hoje só sabemos a assinatura e o papel pelo
  contexto de quem chama.

## ⚪ Não iniciado — motores/sistemas inteiros, zero leitura de código

Cada um destes é, pelo tamanho, comparável ao que já foi investigado
nas seções anteriores — não são "pendência pequena":

- [ ] Compressão (`CCOMP_Z_DEC`/`CCOMP_Z_ENC`, 7+7 métodos) — provável
  relação com o formato do `fftpack.bin`/`.obb` (seção 7 do
  `REVERSE_ENGINEERING_NOTES.md` já documentou que o `.obb` é lido sem
  decriptação, mas não investigou compressão).
- [ ] Sistema de save (`pspSaveBase`/`pspSaveList`/`pspSaveAuto`/
  `cSaveFFT`/`CAUTOSAVE`, ~35+6+5+12+8 métodos).
- [ ] Input touch (`CINPUT_IF_TOUCH`/`CINPUT_DATA`, 60+35 métodos).
- [ ] Classes utilitárias (`CRECT`, `CSTR_UTIL`, `CLIST`, `CTHREAD`,
  `CFRAMERATE`, `CFILE_UTIL`) — baixa prioridade, provável trabalho de
  "glue" sem achados arquiteturais novos.
- [ ] `CFFT_STATE` (42 métodos) — candidato a classe orquestradora de
  nível mais alto do jogo inteiro; nunca investigada diretamente (só
  `GetParam` foi referenciado, de fora, várias vezes).

## Ferramentas (recriar se a sessão/worktree for nova)

- Venv do Capstone: `python3 -m venv <tmp>/reavenv && <tmp>/reavenv/bin/pip install capstone pyelftools`
- `disasm.py`/`disasm_cfg.py`/`batch_disasm.py`/`find_bl.py`/
  `find_vtable.py`/`find_pcrel.py` — scripts já escritos durante esta
  investigação (ficam no scratch da sessão, não no repositório — recriar
  conforme necessário; a lógica de cada um está descrita inline nas
  seções correspondentes dos dois documentos de resultado).
- `.so` alvo: `FFT_Android_Mod/src/lib/armeabi/libgl2jni.so` (ARM). O
  binário x86 (`FFT_Android_Mod/src/lib/x86/libgl2jni.so`) **não foi
  tocado nesta investigação** — todo achado é só do binário ARM.

## Critério de "zerado"
Dado o tamanho real (6636 símbolos `FUNC` no `.dynsym` do binário ARM),
"zerar" no sentido literal de ler cada função não é uma meta realista
de curto prazo. O critério prático: **nenhum item de prioridade 🔴/🟠
em aberto**, e cada item 🟡/⚪ com pelo menos a função-ponte/central
lida (mesmo padrão já aplicado a `CEGL2_IF`/`CSOUND_IF`). Quando isso
for atingido, reavaliar se vale continuar para ⚪ por completo ou
encerrar o loop.
