# Plano de ação — Fase 2 da engenharia reversa do `libgl2jni.so`

A Fase 1 (`RE_BACKLOG_PLAN.md`) está **zerada**: todos os itens
🔴🟠🟡⚪ têm pelo menos a função-central lida por completo. Mas
"zerado" ali significava algo deliberadamente modesto — cada item 🟡/⚪
só teve **uma** função lida, não a classe inteira, e o binário ARM
tem **6636 símbolos `FUNC`** no total (a imensa maioria nunca tocada).

Este documento é a Fase 2: fecha as **pontas concretas deixadas
abertas** pelas seções já escritas (coisas que uma seção específica já
apontou como "não confirmado" ou "fica pra depois"), e depois abre
sistemas que a Fase 1 nunca tocou. Os dois documentos de resultado
continuam os mesmos:

- `AI_DIFFICULTY_RESEARCH.md` — IA de batalha
- `REVERSE_ENGINEERING_NOTES.md` — tudo o resto

## Como o loop deve operar (mesma metodologia da Fase 1, já validada)

1. **Escolher o próximo item não marcado**, nesta ordem de prioridade
   (seções abaixo, de cima para baixo).
2. **Desmontar via Capstone** (`disasm.py`/`disasm_cfg.py`, recriar o
   venv em `/tmp` se necessário — ver "Ferramentas" ao final). Hopper
   **não funciona** neste ambiente — nem tentar de novo. Para switches
   via tabela de salto computada (`addls pc,pc,rX,lsl#2`), o
   `disasm_cfg.py` não segue sozinho — extrair os words crus da tabela
   e decodificá-los como `b` à mão (técnica usada nas seções 9.8/12.4/21
   do `REVERSE_ENGINEERING_NOTES.md`).
3. **Resolver os alvos de `bl`** contra `.dynsym` antes de ler o corpo.
   Para `.plt`, usar a técnica de somar os dois `add` do stub + o
   offset do `ldr pc,[...]` e cruzar com `.rel.plt`.
4. **Ler o corpo real**, escrever pseudocódigo fiel à aritmética, com
   honestidade de cobertura.
5. **Documentar** no arquivo certo (seção numerada nova, continuando a
   numeração que já existe em cada documento — não reiniciar), **marcar
   o item como `[x]` neste plano**, e no fim da iteração: **commitar e
   dar push** no branch `worktree-fft-re-loop`.
6. **Parar e escalonar** se um alvo específico resistir — anotar o
   motivo ao lado do item em vez de forçar uma leitura rasa.

## 🔴 Prioridade alta — fecha pontas concretas já identificadas nas seções existentes

- [x] `MakeMapDanger()` (`0x27b0b0`, 400 B) — lida por completo, ver
  `AI_DIFFICULTY_RESEARCH.md` seção 23. Fecha o sub-item pendente da
  seção 18. Achado maior: confirma quem escreve o array de "ameaça
  real" `g->b[0xc8d..0xca1]` (fase 1) e o mecanismo do mapa de perigo
  — contribuição de perigo por distância Manhattan, raio 10,
  `10-distância`, somada por painel a partir de cada unidade
  marcada como ameaça (fase 2). Endereçamento 2D exato do acumulador
  (`g+0x174`) ficou ambíguo — escalonado, não forçado (ver seção
  23.3).
- [x] Quem toca `g+0x5e0` — ver `AI_DIFFICULTY_RESEARCH.md` seção 24.
  Achado: um segundo ponto de contato real, dentro de uma função de
  ~1200 B **sem símbolo no `.dynsym`** (`sub_277f78`,
  `0x277f78`–`0x27842c`), que togla bits na mesma tabela durante a
  avaliação de movimento candidato (chama `SetBestMove()` em laço).
  Varredura sistemática por imediato não achou um terceiro ponto —
  escalonado como achado honesto, não forçado. `sub_277f78` virou um
  novo item 🟠 abaixo (grande demais pra ler dentro deste item).
- [x] Cluster `CFFT_STATE` de mapeamento de identidade — todas as 7
  lidas por completo, ver `REVERSE_ENGINEERING_NOTES.md` seção 22.5.
  Achado principal: `AttackTeamFaceIDToFaceID` **chama**
  `WorldFaceIDToFaceID` de verdade pra personagens nomeados
  (retrato compartilhado mapa mundi ↔ tela de time de ataque).
  Achado bônus: `EVTCHRToFID` liga o motor de eventos/diálogo (seções
  9.5–10) a este mesmo sistema de retrato — ponte nunca conectada
  antes. Confirma também que o literal `0x5e0` usado em
  `UnitIDToFID_SP2` é só coincidência numérica, sem relação com o
  `g+0x5e0` da IA (seção 24 do `AI_DIFFICULTY_RESEARCH.md`).
- [x] `CINPUT_IF_TOUCH::OnTouchesEnded`/`OnEventDispatched` — lidas
  por completo, ver `REVERSE_ENGINEERING_NOTES.md` seção 26. **Achou e
  corrigiu um erro real na seção 20** (os ramos `if`/`else` do
  `comboState==0` estavam trocados). Quadro de estados completo
  confirmado: `comboState` vai até `4` (não para em `3`); o sinal
  consumível real é `this->+0xd8`, setado nas transições `1→2` e
  `3→4`. `OnEventDispatched` é só um setter simples, não participa
  do combo. Janela de tempo exata ainda não confirmada (escalonado).

## 🟠 Prioridade média — termina as classes já abertas na Fase 1

- [x] `sub_277f78` (`0x277f78`–`0x27842c`, 1204 B) — lida por
  completo, ver `AI_DIFFICULTY_RESEARCH.md` seção 25. **Confirmado**:
  é o laço central "iterar destinos candidatos e avaliar cada um" da
  IA, citado de fora desde a seção 6.1. Achados maiores: (1) fecha
  quem consome `g->b[0xcbb]` (contagem da seção 21); (2) revela um
  **watchdog de tempo real baseado em `VSync`** (aborta a busca após
  440 VSyncs); (3) `SetThisDestination` confirmado como o "commit"
  real do destino escolhido; (4) filtros reais de alcance de
  arco/arma de fogo via `CheckBowReachable`/`CheckGunReachable`.
- [x] `CEGL2_SPRITE::AddPacketPartial` (`0xad324`, 1244 B) — lida por
  completo, ver `REVERSE_ENGINEERING_NOTES.md` seção 13.8. Achado:
  função 100% linear (sem nenhum desvio condicional) que monta um
  quad de 6 vértices via `memcpy` interno duplicando `v1`/`v2` pra
  `v3`/`v4` — confirma o layout "2 triângulos degenerados" na
  origem (onde o lote é montado), não só no desenho. `DrawPartial`/
  `Draw8` continuam não lidas.
- [x] `CEGL2_FBO::RenderToFBO` (`0xaae00`, 868 B) — lida por completo,
  ver `REVERSE_ENGINEERING_NOTES.md` seção 13.9. Fecha o ciclo "criar
  → usar" com a seção 13.5. Achados: usa `GL_TRIANGLE_STRIP` de 4
  vértices (formato diferente do resto do motor, que sempre usa
  `GL_TRIANGLES` com diagonal compartilhada); `glGenerateMipmap` real
  condicional; pula blend quando a cor é opaca. `RenderFromFBO`
  (`0xab164`, 732 B) continua não lida.
- [x] `CEGL2_SHADER::Begin`/`SetTexture` — lidas por completo, ver
  `REVERSE_ENGINEERING_NOTES.md` seção 13.10. Achados: `Begin` nunca
  usa o parâmetro `matrix` (corrige a suposição de 3 argumentos das
  seções 13.1/14); `SetTexture` confirma suporte real a 2 texturas
  simultâneas por shader (bate com `GetMultiTextureHandle` da seção
  13.4).
- [x] `CEGL2_TEX_HYBRID::GL_IsUpdate` (`0xaf120`, 684 B) — lida por
  completo, ver `REVERSE_ENGINEERING_NOTES.md` seção 13.11. Confirma
  o cache/alocador de slots de textura (64 slots, 3 níveis de
  fallback). **4ª ocorrência do padrão "condição impossível = laço
  infinito"** nesta investigação. `GL_Load` (`0xaf818`, 392 B)
  continua não lida.
- [x] `CSOUND_IF_SL::Stream_Load(int)` (`0xbc5a4`, 216 B) — lida por
  completo, ver `REVERSE_ENGINEERING_NOTES.md` seção 17.8. Confirma
  ser a contraparte exata de `CB_for_Stream` (seção 17.4) — o
  primeiro preenchimento de buffer antes do callback assumir.
  Achado bônus: os dois pares de loop-point começam zerados pra
  `-1` (sem loop configurado ao iniciar o streaming).
- [x] `CSOUND_LOADER_OGG::Open` (`0xbd56c`, 460 B) — lida, ver
  `REVERSE_ENGINEERING_NOTES.md` seção 17.9. Confirma mais 4 funções
  reais da `libvorbisfile` e revela uma classe nova,
  `COggMemMapFile` (wrapper de arquivo mapeado em memória). **Achado
  possivelmente preocupante**: o caminho "buffer de memória pronto"
  (`buf!=NULL`) só seta uma flag e retorna sucesso, sem nunca chamar
  `ov_open_callbacks` — parece incompleto, não cravado como bug sem
  confirmar se algum chamador usa esse caminho de verdade. Fluxo de
  controle do caminho "arquivo" não 100% decomposto (escalonado).
  `CSOUND_LOADER_PCM::Open` (`0xbced4`, 608 B) continua não lida.
- [x] `CCOMP_Z_ENC::Encode` (`0xb63d0`, 432 B) — lida por completo,
  ver `REVERSE_ENGINEERING_NOTES.md` seção 18.1. Confirma
  `deflateInit_`/`deflate`/`deflateEnd` reais, e fecha a convenção de
  `flags` com `Decode` (`2`=comprimido, `0`=cru). Achado bônus: um
  fallback real — se comprimir não encolher os dados, descarta e
  grava o original sem compressão.
- [x] `CAUTOSAVE::Save(uint)` (`0x28c7ec`, 592 B) — lida, ver
  `REVERSE_ENGINEERING_NOTES.md` seção 19.1. **Achado enorme**: não é
  um save de progresso, é um "suspender pra disco" de verdade — grava
  o conteúdo bruto da heap alocada inteira do jogo (`xpGetHeap`/
  `xpGetHeapSize`/`CFILE::Write`), categoricamente diferente de
  `cSaveFFT::Save` (seção 19). Confirma também `CCOMP_Z_ENC::Encode`
  sendo usado de verdade (nível `-1`) e revela uma API de gerência de
  heap própria do motor (`xpGetHeap`/`xpMoveHeap`). `Load`
  (`0x28ca3c`, 632 B), `pspSaveList`/`pspSaveAuto` continuam não
  lidas.

## 🟡 Prioridade baixa — sistemas que a Fase 1 nunca abriu

- [x] `CINPUT_DATA::GetData(int)` (`0xb3548`, 36 B) — lida por
  completo, ver `REVERSE_ENGINEERING_NOTES.md` seção 27. Confirma um
  array de perfis/slots de input (stride 1436 B), cada um validado
  por um sentinela `-1` na primeira word.
- [x] `CTHREAD::Register`/`CreateAndRegister` — lidas por completo,
  ver `REVERSE_ENGINEERING_NOTES.md` seção 28. Confirma `pthread_create`/
  `sched_yield` reais — diferente do `CCRYPT` morto da seção 9.1, este
  mecanismo é real e funcional. Quem de fato usa `CTHREAD` não
  identificado.
- [x] `CFILE_UTIL::FileCopy` (`0xb79d8`, 424 B) — lida por completo,
  ver `REVERSE_ENGINEERING_NOTES.md` seção 29. Achado: a ordem real
  dos parâmetros é `(destino, fonte)`, confirmada por comportamento,
  não pelo nome. Lê o arquivo inteiro pra memória, escreve em blocos
  de até 4 MiB. `DirCreate` (`0xb78b4`, 204 B) continua não lida.
- [x] `CSTR_UTIL::GetName` (`0xb8d34`, 212 B) — lida por completo, ver
  `REVERSE_ENGINEERING_NOTES.md` seção 30. Achado: trata corretamente
  caracteres multi-byte Shift-JIS (`IsLeadByte`); achado comportamental
  surpreendente — nome sem `.` produz saída VAZIA, não o nome
  original. `Conv`/`Find`/`CLIST::GetData`/`DeleteAll` continuam não
  lidas.
- [x] `wld_anim` (852 B) — lida por completo, ver
  `REVERSE_ENGINEERING_NOTES.md` seção 12.5. **Fecha o último item
  🟡 da Fase 2.** Confirma ser o "tocador" de animação de sprite do
  mapa mundi — tabela de quadros-chave por animação, looping
  automático, múltiplos sub-sprites por quadro, e `GsSortFlipSprite`
  (nova função real da lib PS1, suporte a espelhamento). Reusa o
  mesmo `fadeanb_calc` do HUD (seção 12.4). `wldrute_draw`/
  `wldssd_control` continuam não lidas.

## ⚪ Não iniciado — trabalho de escala grande ou de baixo retorno isolado

- [x] Resolver os literais GOT sem nome das seções 21/25 do doc de IA
  — ver `AI_DIFFICULTY_RESEARCH.md` seção 26. **Achado principal**: 3
  referências antes isoladas (seções 9.3/14.4/21/25) resolvem todas
  pro mesmo endereço, `comtype` — fecha de vez que não eram tabelas
  diferentes. Duas outras tabelas resolvidas por endereço mas sem
  nome real (`0x565db8`, `0x3d21bc`). Os literais do motor de áudio
  (seções 13.6/17.6, `SL_IID_*`) e da seção 13.7 continuam abertos —
  não resolvidos nesta passada.
- [ ] Varredura sistemática das funções `wld_*` restantes (depois das
  3 da seção 🟡 acima) — **lista finita e bem definida** (seção 12.1
  do `REVERSE_ENGINEERING_NOTES.md` já cataloga quais das 72 originais
  faltam, por nome/categoria, seção 11.2). Não é trabalho sem fim —
  é só grande; continuar função por função, maior-primeiro, dentro
  deste mesmo item (sem precisar de uma "Fase 3"):
  - [x] `wldrute_draw` (`0x267f3c`, 740 B) — ver seção 12.6. Desenha a
    linha de rota caminhável do mapa mundi via GTE real (`RotTransSV`)
    + quads semi-transparentes (`SetPolyFT4`/`GsSortPoly`), só pras
    rotas com flag de evento ativa.
  - [x] `wldssd_control` (`0x26b378`, 620 B) — ver seção 12.7.
    **Correção da seção 11.2**: não é widget de UI ("SSD" ficava sem
    identificação), é a máquina de estados de 18 estados que controla
    a música de fundo do mapa mundi, com fila de comandos de troca de
    faixa e fade-in/fade-out reais.
  - [x] `wldfade_proc` (`0x25df88`, 472 B) — ver seção 12.8. Confirma
    `iOSwldssd_wait()` como a ponte real entre o fade visual e a
    máquina de música da seção 12.7 (espera a fila de música esvaziar
    antes de continuar o fade); curva de interpolação assimétrica
    real pros canais de "ambiência" via `changewindowamb`.
  - [x] `wldcenter_chk` (`0x268aec`, 176 B) — ver seção 12.9. Confirma
    o papel sugerido pelo nome: testa se a posição está fora da
    margem de centralização da câmera do mapa mundi.
  - [ ] Demais funções de "Desenho"/"Movimento/câmera"/"Persistência"
    da tabela da seção 11.2 ainda sem leitura linha a linha (a maioria
    pequena, <200 B).
- [x] Binário x86 — primeira comparação feita, ver
  `REVERSE_ENGINEERING_NOTES.md` seção 31. `.dynsym` tem contagem de
  símbolos muito próxima da ARM (6530 vs 6636); `CCOMP_Z_DEC::Decode`
  comparado instrução por instrução — lógica idêntica. Achado real:
  a zlib é embutida/exportada direto no `.dynsym` do x86, em vez de
  importada via `.plt` como no ARM — diferença de linkagem, não de
  lógica. Só 1 função comparada; o resto do x86 continua não lido.
- [x] `BattleRoutine`'s 7 blocos de fallback — lidos por completo
  (e mais ~10 blocos irmãos que apareceram no mesmo intervalo), ver
  `AI_DIFFICULTY_RESEARCH.md` seção 27. **Achado principal**:
  `g->b[0xed4]` é o código de motivo de saída da IA (`0`/`1`/`2`,
  gravado junto com a flag "IA ativa" antes do epílogo real de
  `BattleRoutine`). Achado bônus: mais um escritor da tabela
  `+0xa70`; um bloco de busca grande (256×256) não decomposto por
  completo, candidato a item próprio futuro.

## Ferramentas (idêntico à Fase 1 — recriar se a sessão/worktree for nova)

- Venv do Capstone: `python3 -m venv <tmp>/reavenv && <tmp>/reavenv/bin/pip install capstone pyelftools`
- `disasm.py`/`disasm_cfg.py`/`batch_disasm.py`/`find_bl.py`/
  `find_vtable.py`/`find_pcrel.py` — scripts já escritos na Fase 1,
  ficam no scratch da sessão, não no repositório.
- `.so` alvo principal: `FFT_Android_Mod/src/lib/armeabi/libgl2jni.so`
  (ARM). O item ⚪ do x86 é a primeira vez que o outro binário entra
  em cena.

## Critério de "zerado" desta fase

Mesmo espírito da Fase 1: **nenhum item 🔴/🟠 em aberto**, e cada item
🟡/⚪ com pelo menos a função-central lida. Dado que esta fase já é
"profundidade 2" sobre um binário de 6636 funções, não existe uma meta
de "fim" absoluto — quando os 🔴/🟠 desta fase fecharem, reavaliar se
vale abrir uma Fase 3 ou encerrar o loop de continuação automática.
