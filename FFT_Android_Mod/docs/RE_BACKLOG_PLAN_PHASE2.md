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
- [ ] `CINPUT_IF_TOUCH::OnTouchesEnded` (`0xb44a4`, 248 B) e
  `OnEventDispatched(int)` (`0xb45c0`, 16 B) — fecha a pergunta aberta
  da seção 20 do `REVERSE_ENGINEERING_NOTES.md`: quem lê
  `comboState==3` (duplo-toque confirmado) e qual é a janela de tempo
  real.

## 🟠 Prioridade média — termina as classes já abertas na Fase 1

- [ ] `sub_277f78` (`0x277f78`–`0x27842c`, ~1204 B, **sem símbolo no
  `.dynsym`** — função local/`static`) — achada durante o item 🔴
  "quem toca `g+0x5e0`" (seção 24 do `AI_DIFFICULTY_RESEARCH.md`),
  mas grande demais pra ler ali. Chama `SetBestMove()` (`0x277f1c`)
  em laço sobre colunas do mapa — forte candidata a ser o verdadeiro
  "laço de escolha de melhor movimento" da IA, nunca documentado até
  agora. Revela também `sub_224d4c`/`sub_224650`/`0x271e1c`
  (chamados por ela, papéis não investigados).
- [ ] `CEGL2_SPRITE::AddPacketPartial` (`0xad324`, 1244 B),
  `DrawPartial` (`0xae090`, 1088 B), `Draw8` (`0xaceec`, 1080 B) — as 3
  maiores da família, ainda não lidas (seção 13.4 só leu
  `DrawScrollBG`).
- [ ] `CEGL2_FBO::RenderToFBO` (`0xaae00`, 868 B) e `RenderFromFBO`
  (`0xab164`, 732 B) — usam o FBO que a seção 13.5 (`Create`) já
  documentou; fecha o ciclo "criar → usar".
- [ ] `CEGL2_SHADER::Begin(int,MATRIX4*)` (`0xab7f4`, 120 B) e
  `SetTexture(int)` (`0xab8e8`, 60 B) — chamadas de verdade por
  `CEGL2_IF::DrawPacket` (seção 13.1), nunca lidas por dentro.
- [ ] `CEGL2_TEX_HYBRID::GL_IsUpdate` (`0xaf120`, 684 B) e `GL_Load`
  (`0xaf818`, 392 B) — fecham a família iniciada por `DecodeTexture`
  (seção 13.7): como a textura decodificada chega até o GL de verdade.
- [ ] `CSOUND_IF_SL::Stream_Load(int)` (`0xbc5a4`, 216 B) — par de
  `Stream_CreatePlayer` (seção 17.6), ainda não lido.
- [ ] `CSOUND_LOADER_OGG::Open` (`0xbd56c`, 460 B) e
  `CSOUND_LOADER_PCM::Open` (`0xbced4`, 608 B) — os pontos de entrada
  reais de parsing de arquivo de ambos os decoders (seção 17.7 só leu
  `Decode`, que já pressupõe o arquivo aberto).
- [ ] `CCOMP_Z_ENC::Encode(uchar*,uchar*,int,int)` (`0xb63d0`, 432 B) —
  contraparte de `CCOMP_Z_DEC::Decode` (seção 18); confirma se usa
  `deflate`/`deflateInit_` reais (mesmo padrão esperado).
- [ ] `CAUTOSAVE::Save(uint)` (`0x28c7ec`, 592 B) e `Load()`
  (`0x28ca3c`, 632 B) — maiores que `cSaveFFT::Save` (seção 19),
  provavelmente o mecanismo real de autosave (diferente do save
  manual). `pspSaveList::paramCreate`/`setUserId`
  (`0x2a3950`/`0x2a38d8`) e `pspSaveAuto::paramCreate` (`0x2a3154`)
  como funções-ponte das outras 2 classes do sistema de save.

## 🟡 Prioridade baixa — sistemas que a Fase 1 nunca abriu

- [ ] `CINPUT_DATA::GetData(int)` (`0xb3548`, 36 B) — a função-central
  da camada de **mapeamento toque→botão** (`CINPUT_DATA` nunca foi
  aberta na Fase 1; só `CINPUT_IF_TOUCH`, a camada de toque bruto).
- [ ] `CTHREAD::Register`/`CreateAndRegister` (`0xb9eb0`/`0xb9f04`,
  84/64 B) — confirma se este engine usa threads reais (pthreads) pra
  algo (áudio? loading assíncrono?) ou se é só um wrapper nunca
  exercitado, igual ao `CCRYPT` morto da seção 9.1.
- [ ] `CFILE_UTIL::FileCopy`/`DirCreate` (`0xb79d8`/`0xb78b4`, 424/204
  B) — as maiores da classe; confirma se são wrappers POSIX
  (`open`/`read`/`mkdir`) ou algo mais específico do PSP-SDK (padrão
  já visto em `GetLocalTime`/`timeGetTime`, seções 19/21).
- [ ] `CSTR_UTIL::GetName`/`Conv`/`Find` (`0xb8d34`/`0xb942c`/`0xb9644`)
  e `CLIST::GetData`/`DeleteAll` (`0xb8a20`/`0xb89b0`) — baixa
  prioridade, provável "glue" puro (mesma ressalva que a Fase 1 já
  tinha pra essas classes), mas nunca confirmado por leitura real.
- [ ] Mais 3 das ~49 funções pequenas de `wld_*` ainda por chamada/
  padrão: `wld_anim` (852 B), `wldrute_draw` (740 B), `wldssd_control`
  (620 B) — já sugeridas pela Fase 1, nunca lidas (só `wldinfo_put`
  foi, seção 12.4).

## ⚪ Não iniciado — trabalho de escala grande ou de baixo retorno isolado

- [ ] Resolver os literais GOT sem nome ainda abertos em várias seções
  (tabelas de terreno da seção 21 do doc de IA; constantes `SL_IID_*`
  e layout de `SLDataFormat_PCM` das seções 13.6/17.6; tabela de
  subtipo de tile da seção 13.7) — mecânico, mas fecha várias notas de
  rodapé de uma vez.
- [ ] Varredura sistemática das ~46 funções `wld_*` restantes (depois
  das 3 da seção 🟡 acima) — escala grande, só vale a pena se for meta
  explícita de "fechar o motor `wld_*` por completo".
- [ ] Binário x86 (`FFT_Android_Mod/src/lib/x86/libgl2jni.so`) — **nunca
  tocado em toda a investigação** (Fase 1 inteira foi só ARM). Nem que
  seja só confirmar que a estrutura é idêntica (mesmos offsets de
  campo, mesma lógica) ou documentar divergências reais.
- [ ] `BattleRoutine`'s 7 blocos de fallback nunca lidos (seção 18 do
  doc de IA): `0x275d84`/`0x275d30`/`0x275ba8`/`0x275d10`/`0x275dd0`/
  `0x275e18`/`0x275ae8`.

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
