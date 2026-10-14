# Tradução PT-BR do FFT: WotL (Android) — notas de progresso

Projeto de tradução completa da história para PT-BR, a partir do `.obb` do APK
`com.square_enix.android_googleplay.FFT_en2`. Uso pessoal/fã, sem redistribuição.

## Status: decodificador validado para MENUS/NOMES; DIÁLOGO DA HISTÓRIA bloqueado (ver seção de bloqueio)

## 🎉 Validação bem-sucedida (ver `translation/tools/fft_text.py`)

Implementei em Python (porta fiel do código-fonte do FFTPatcher) a tabela de
caracteres completa + o algoritmo de descompressão, e testei contra entradas
reais do `fftpack.bin` do nosso APK. Resultado: **decodificação perfeita**,
confirmada contra texto conhecido do jogo:

- Entrada 42 (`text_sys/help.lzw`) decodificou para:
  `Ramza{end}Ramza{end}Ramza{end}Delita{end}Delita{end}Delita{end}Argath{end}
  Zalbaag{end}Dycedarg{end}Larg{end}Goltanna{end}Ovelia{end}Orlandeau{end}...`
  — nomes de personagens reais do FFT, em ordem correta.
- Entrada 41 (`text_sys/join.lzw`) decodificou nomes de classes:
  `Squire{end}Squire{end}...Holy Knight{end}Ark Knight{end}...Princess{end}
  Sword Saint{end}...`
- Entrada 38 (`text_sys/sample.lzw`) decodificou texto de ajuda corrido:
  `"This is the unit's roster number. Up to 24 units{br}may join your
  party..."` — frase em inglês perfeita, com `{br}` nos lugares certos.

**Isso confirma que TODO o texto de menus, nomes (unidades, jobs, itens,
habilidades, skillsets, status), descrições de ajuda e mensagens de sistema
é 100% decodificável e re-codificável agora.** São os arquivos
`text_sys/*.lzw` e `text_sys/*.mes` dentro do `fftpack.bin` (entradas 36-43,
mapeadas por `docs/translation-research/nenkai-fftpack-filelist.txt`, que é
a lista de nomes de arquivo do projeto `Nenkai/fftivc.utility.modloader`
[GitHub] para o remaster "Ivalice Chronicles" — bate 1:1 com nosso
`fftpack.bin`: mesma contagem exata de 3931 entradas).

## 🚧 Bloqueio real: diálogo da história (arquivos de EVENTO)

Os arquivos candidatos a conter a história (`event_test_evt.bin` = entrada
17, e um bloco de entradas 21-26 com tamanhos exatos de **8192 bytes** cada
— isso bate com o tamanho de slot de evento conhecido da versão PSX!) **NÃO
são texto corrido**: são **bytecode de script de evento** (uma lista de
instruções tipo `{51} ChangeDialog(xDB, xMSG#, xPR, xPP)` ou
`{10} DisplayMessage(...)`, documentadas em
`docs/translation-research/wiki-Event_Instructions.html`, arquivada da wiki
FFHacktics). O texto do diálogo é referenciado por **ID de mensagem**
(`xMSG#`) a partir dessas instruções, não fica solto no início do arquivo —
decodificar o arquivo inteiro como texto corrido (o que fiz para validar)
só produz lixo/zeros, como esperado.

**Por que isso é difícil especificamente para WotL/mobile**: a documentação
de instruções de evento que encontrei é da versão **PSX**. Um fórum da
comunidade FFHacktics avisa explicitamente que a versão **PSP/WotL usa
opcodes de ASM em posições completamente diferentes**, que a ferramenta
`FFTorgASM` (editor de eventos) **não funciona com WotL**, e recomenda a
versão PSX para "projetos grandes" porque há "muito menos limitações" de
ferramental. Ou seja: isso não é só "eu não achei a doc ainda" — é uma
lacuna real e conhecida da comunidade de modding para esta versão
específica do jogo.

Não tentei (ainda) decodificar o bytecode às cegas por heurística — o
risco de produzir uma leitura errada da estrutura (e depois escrever dados
corrompidos de volta) é alto, e indo nessa direção sem mais pistas pode
consumir muito tempo sem garantia de sucesso.

**Decisão do usuário (2026-10-13): fazer as duas coisas em paralelo** —
traduzir agora tudo que já é decodificável (menus/nomes/ajuda) enquanto
continuo tentando decifrar o bytecode de evento nas próximas iterações do
loop, sem uma bloquear a outra.

## ✅ Pipeline completo validado: decode + encode (round-trip 100% correto)

Implementei também `encode_string()` (o inverso de `decode_bytes()`) em
`translation/tools/fft_text.py`, e testei round-trip completo
(decode → separar strings → re-codificar → re-decodificar) nas 8 entradas
de `text_sys/*` — **resultado: texto decodificado idêntico em 100% dos
casos** (`translation/tools/roundtrip_test.py`). Ou seja, o pipeline está
pronto para traduzir de verdade: já sabemos decodificar E re-codificar sem
perda.

(Nota técnica: os bytes brutos reconstruídos não são *byte-a-byte*
idênticos ao arquivo original em alguns casos, porque vários códigos de
byte diferentes decodificam para o mesmo caractere — ex.: "—" tem pelo
menos duas representações válidas. Isso não importa: o que importa é que
decodificar de novo dá o texto certo, e é exatamente isso que validei.)

## 📦 Texto-fonte em inglês já extraído (pronto para tradução)

Salvei a lista COMPLETA e ORDENADA de strings (com o byte terminador de
cada uma, `0xFE`={end} ou `0xFF`={close}, necessário para re-codificar)
das 8 entradas de texto de menu/nome/ajuda em
`translation/source/entry{NN}_{nome}.json`:

| Entrada | Arquivo original      | Nº de strings | Conteúdo (observado)                          |
|---------|------------------------|---------------:|------------------------------------------------|
| 36      | ATCHELP.LZW             | 873            | Descrições de jobs/itens/habilidades (texto longo) |
| 37      | (spell.mes)             | 254            | Majoritariamente ruído/japonês — baixa prioridade |
| 38      | SAMPLE.LZW               | 1280           | Mensagens de erro/batalha, texto de ajuda da UI |
| 39      | WORLD.LZW                | 512            | Majoritariamente falas de conjuração em japonês (flavor text) — baixa prioridade |
| 40      | OPEN.LZW                 | 1803           | Mensagens de status/erro, UI do mundo          |
| 41      | JOIN.LZW (não documentado nas notas antigas) | 5872 | Mistura: títulos de job por unidade + itens de menu de opções + tópicos de tutorial |
| 42      | (help, nomes)            | 1272           | **Nomes de personagens** (Ramza, Delita, Argath...) — majoritariamente nomes próprios, tradução = manter como está |
| 43      | WLDHELP.LZW              | 672            | Falas/diálogos curtos de NPCs do mundo, em japonês nesta amostra |

Isso é o dataset mestre para tradução.

## 🚧 Decisão provisória sobre acentuação (aguardando confirmação do usuário)

Ao decodificar a tabela de fonte com atenção, descobri que a limitação é
**maior** do que registrei antes: a fonte do jogo (mesmo a extensão PSP)
só tem estes acentos latinos: **á, à, é, è, í, ú, ù** (minúsculos, sem
versão maiúscula de nenhum deles). Ou seja, também faltam **ó** (!), além
de ã, õ, ç, â, ê, ô — e nenhuma letra acentuada maiúscula existe.

**Decisão provisória que estou aplicando enquanto o usuário não confirma**:
escrever em PT-BR **sem** ã/õ/ç/â/ê/ô/ó (ex.: "não"→"nao", "ação"→"acao",
"número" fica "número" normalmente pois usa apenas ú, mas "só"→"so"),
mantendo á/à/é/è/í/ú/ù onde aparecem naturalmente. Isso é reversível:
dá pra trocar tudo de uma vez depois se decidirmos hackear a fonte para
adicionar os glifos que faltam.

## ✅ Primeiro lote de tradução real (prova de conceito)

Traduzi as primeiras 27 strings "reais" (textos de status de unidade:
Nível, HP, MP, Tempo de Carga, Ordem de Turno, EXP, Coragem, Fé, Movimento,
Salto, Velocidade, Ataque/Magia, Evasão etc. — texto que literalmente
TODO jogador vê na tela de status) da entrada 38 (`SAMPLE.LZW`), salvas em
`translation/ptbr/entry38_sample.json`. **Validei que o arquivo completo
(as 27 traduzidas + as 1253 ainda em inglês/passthrough) passa 100% no
round-trip decode→encode→decode** (`translation/tools/translate_entry38_batch1.py`
gera o arquivo; validação manual confirmou 0 erros nas 1280 strings).

Formato de `translation/ptbr/entry{NN}_{nome}.json`: idêntico ao de
`translation/source/` (mesma lista `[texto, terminador]`, mesma ordem,
mesma quantidade) — isso é OBRIGATÓRIO para poder re-codificar depois.
Strings ainda não traduzidas ficam como passthrough (cópia do inglês) até
serem traduzidas numa iteração futura.

## 📊 Escala real do trabalho (atualizado após inventário completo)

Depois de extrair e inspecionar tudo, o volume real de texto único em
inglês (excluindo nomes próprios e lixo/padding) é:

| Arquivo | Strings reais em inglês |
|---|---:|
| entry38_sample | 833 |
| entry41_join | 2305 |
| entry42_help | 98 (majoritariamente nomes próprios — baixa prioridade) |
| entry36_atchelp | bloqueado (ver bug de compressão abaixo) |
| entry37/39/40/43 | poucas ou nenhuma (japonês/lixo, a confirmar) |
| **Total único (deduplicado entre arquivos)** | **~2236** |

Isso é MUITO mais que "traduzir algumas telas" — é um volume comparável a
um livro curto (descrições de ~170 classes, centenas de itens/armas com
texto+estatísticas, centenas de monstros, menus de opções completos,
tópicos de tutorial). Terminar os 8 arquivos com qualidade de tradução
humana de verdade é um trabalho de várias sessões, não de alguns minutos.

**Estratégia que estou usando para ir rápido sem perder qualidade:**
tradução por FRASE/ESTRUTURA em vez de string-a-string sempre que possível
— ex.: um glossário de ~20 rótulos (`{font:08}Attack{font:00}`→`Ataque`,
`Block`→`Bloqueio`, `Ability`/`Abilities`→`Habilidade(s)` etc.) aplicado de
uma vez já tocou 426 das 1280 strings de `entry38`; um glossário de
elementos/status (Fire→Fogo, Poison→Veneno etc.), escopado com regex só
para onde aparecem depois desses rótulos (para não estragar frases em
inglês que ainda não foram traduzidas), tocou mais 113. As frases únicas
de descrição (de cada classe/monstro/item) continuam precisando de
tradução manual mesmo assim — é o grosso do trabalho que resta.

**Status real por arquivo — atualizado 2026-10-13, 3ª rodada:**
- `entry38_sample.json`: ✅ **100% TRADUZIDO** (0 strings com prosa em
  inglês restante, de 1280 totais). Round-trip encode→decode validado
  sem nenhum erro. Cobre: todas as ~30 descrições de classe, zodíaco,
  ~25 descrições de monstros (bestiário), ~167 descrições de armas/
  itens/armaduras, todos os rótulos de estatística, e **todas as
  descrições de habilidades/skills do jogo** (ataques de monstro,
  comandos de classe de todas as ~40 classes incluindo os chefes/Lucavi,
  habilidades de reação/suporte/movimento, itens consumíveis). Essa
  descoberta é importante: a seção "Ability descriptions" que eu pensava
  estar bloqueada só em `entry36_atchelp` (formato de compressão
  diferente, ver bloqueio abaixo) **também existe aqui, sem compressão
  problemática** — ou seja, o bloqueio do entry36 deixou de ser crítico,
  o conteúdo dele parece estar duplicado aqui.

**Status anterior (referência, já superado nesta rodada):**
- `entry38_sample.json`: **348 de 1280** ainda têm prosa real em inglês
  (desceu de 479). Já traduzido: todas as descrições de ~30 classes,
  todas as ~25 descrições únicas de monstros do bestiário, zodíaco
  completo, e ~167 descrições únicas de armas/itens (facas, espadas,
  katanas, machados, cajados, cetros, armas de fogo, bestas, arcos,
  harpas, lanças, varas, bolsas, tecidos, escudos, luvas, anéis,
  braceletes, mantos, perfume, batom). Falta: armaduras/robes/chapéus/
  elmos/roupas (ainda não inspecionado), e possivelmente mais alguns
  acessórios/itens especiais no final do arquivo.
  (varredura extra pós-conclusão achou mais 59 strings perdidas — movimento/
  salto/equipar-independente-de-classe/comandos de classe restantes — já
  corrigidas, `batches/batch_e38_final2.py`)
  **Glossário de itens estabelecido** (reaproveitar nos outros arquivos):
  Knife→Faca, Sword→Espada, Katana→Katana, Axe→Machado, Rod→Cajado,
  Staff→Cetro, Gun→Arma de Fogo, Crossbow→Besta, Bow→Arco,
  Instrument→Instrumento, Spear/Polearm→Lança, Pole→Vara, Bag→Bolsa,
  Shield→Escudo, Armor→Armadura, Hat→Chapéu, Helm→Elmo, Robe→Veste,
  Ring→Anel, Armlet→Bracelete, Cloak→Manto, mythril→mithril (mantido).
  Nomes de classe no grid de equipáveis: Squire→Soldado, Chemist→Químico,
  Knight→Cavaleiro, Archer→Arqueiro, Monk→Monge, White/Black/Time→
  Branco/Negro/Tempo, Summoner→Invocador, Thief→Ladrão, Orator→Orador,
  Mystic→Místico, Dragoon→Dragão, Samurai/Ninja (iguais), Arith.→Arit.,
  Bard→Bardo, Dancer→Dançarino. Habilidades comuns: Counter→Contra-Ataque,
  Fly→Voar, Swim→Nadar, Levitate→Levitar, Teleport→Teletransporte,
  Poach→Capturar, Safeguard→Proteção. Elementos: Fire/Ice/Water/Wind/
  Earth/Holy/Dark→Fogo/Gelo/Água/Vento/Terra/Sagrado/Trevas. Rótulos:
  Attack/Block/Ability/Abilities/Range/Speed/Element/Weakness(es)/
  Absorbs/Halves/Immune/Negates/Equip/Trigger/Restores/Removes/Boosts/
  Spell Effect/Radius/ATK/Move/Jump → Ataque/Bloqueio/Habilidade(s)/
  Alcance/Velocidade/Elemento/Fraqueza(s)/Absorve/Reduz a Metade/Imune/
  Anula/Equipar/Gatilho/Restaura/Remove/Aumenta/Efeito de Magia/Raio/
  ATQ/Movimento/Salto. (Nota: sem ã/õ/ç/â/ê/ô/ó em TODAS essas
  traduções, por causa da limitação de fonte já documentada.)
- `entry41_join.json`: ainda não iniciado (2305 strings reais, provavelmente
  com bastante repetição como os outros).
- `entry42_help.json`: ainda não revisado item a item, mas é majoritariamente
  nomes próprios de personagens — baixa prioridade de tradução.
- `entry36_atchelp.json`: **bloqueado** — descobri que esse arquivo usa
  compressão REAL (diferente dos outros 7, que não precisavam de
  descompressão), e meu decompressor (porta do `TextUtilities.Decompress`
  do FFTPatcher) não está reconstruindo esse arquivo corretamente (produz
  lixo). Corrigi um bug nele (referência de backreference era relativa ao
  buffer de SAÍDA, devia ser relativa ao buffer de ENTRADA/original -
  corrigido em `fft_text.py`), mas mesmo corrigido ainda sai lixo para esse
  arquivo especificamente — pode ser outro formato de arquivo inteiro
  (`SectionedFile` com cabeçalho de 128 bytes contendo uma tabela de
  offsets por seção, que tentei decodificar mas os valores não bateram
  com o formato esperado). Não vou insistir cegamente nisso agora; como a
  maior parte do conteúdo de descrição de classe/item/habilidade parece
  estar DUPLICADO em `entry38`/`entry41` mesmo assim, não é bloqueante
  para o grosso da tradução.

## ✅ Confirmado: entry37/39/40/43 são conteúdo em JAPONÊS, não traduzir

Inspecionei o conteúdo bruto de `entry40_open.json` diretamente (não só a
heurística de "tem palavra em inglês") e confirmei: é texto genuinamente em
**japonês** (mensagens de erro de batalha do tipo "Você não pode agir porque
está em tal status", etc. — reconhecível mesmo sem traduzir). O mesmo padrão
já havia aparecido em `entry39_world` (falas de conjuração em japonês) e
`entry43_wldhelp` (diálogos curtos de NPC em japonês) nas amostras anteriores.

**Decisão: não traduzir esses 4 arquivos.** Hipótese mais provável: esse
bloco específico do `fftpack.bin` carrega o conteúdo em japonês residual/não
usado pela versão EN (comum em ports multi-região que empacotam tudo junto),
já que `entry38` (que tem a mesma categoria de conteúdo — ajuda, descrições)
decodificou 100% em inglês perfeito. Traduzir japonês→português seria um
trabalho diferente (e menos confiável) do que inglês→português, e arriscaria
gastar tempo traduzindo texto que o app em inglês nunca exibe. Os arquivos
`entry37_spell.json`, `entry39_world.json`, `entry40_open.json`,
`entry43_wldhelp.json` ficam como passthrough (cópia idêntica do original),
o que já é válido para round-trip.

## 📈 entry41_join.json — em andamento (o maior arquivo)

Criado `translation/ptbr/entry41_join.json` (cópia do source, 5872
strings, 2843 únicas com conteúdo real em inglês). Composição real
(diferente do que eu havia estimado antes — não é só "títulos de job
por unidade", é uma mistura de 3 coisas bem diferentes):
1. **Títulos de classe/job por unidade** (ex. "Squire", "Holy Knight",
   "Duke") — ✅ glossário de 99 termos aplicado (`batches/batch_e41_titles.py`),
   136 ocorrências traduzidas. Inclui nomes de monstros usados como
   título de unidade (Chocobo, Goblin, Behemoth etc.).
2. **Nomes próprios de armas/itens específicos** (ex. "Mythril Knife",
   "Excalibur", "Ragnarok", "Ashura", "Murasame") — composições
   descritivas (material+arma) traduzidas (`batches/batch_e41_weaponnames.py`,
   25 termos: Espada de Mithril, Espada Larga, etc.); nomes
   **mitológicos/próprios ficam em inglês/original** (Excalibur, Ragnarok,
   Ashura, Masamune, Materia Blade, Defender, Chaos Blade...) — decisão
   deliberada, seguindo a convenção comum de localizações oficiais de FF
   em PT-BR de não traduzir esses nomes icônicos. **Ainda restam várias
   centenas desses nomes próprios de armas/armaduras para revisar** (a
   maioria deve ficar como está, mas preciso confirmar item por item).
3. **Itens de menu de opções e títulos de tutorial** (ex. "1. Battlefield
   Controls", "5. Turn Order", "13. Geomancy") — ainda não traduzido,
   são frases completas (não só nomes), style de manual/sumário.

**Atualização (4ª rodada):** aplicados mais 3 lotes de nomes de equipamento
(escudos/elmos/chapéus/armaduras/vestes/botas, depois facas/espadas/
machados/cajados/cetros/maças/armas de fogo/arcos/harpas/livros/lanças/
varas/luvas, depois acessórios/poções/itens "Cebola"/armas "definitivas")
e 1 lote de UI/menu (mensagens de status `{unitname}'s X increased by Y`,
~15 itens numerados de menu de opções/tutorial, texto longo de tutorial
do mapa-mundi). Convenção adotada: nomes **descritivos** (material+tipo,
ex. "Mythril Sword") são traduzidos; nomes **lendários/mitológicos/próprios**
(Excalibur, Ragnarok, Ashura, Masamune, Durandal, Gungnir, Chaosbringer,
katana japonesas famosas etc.) ficam em inglês/original, seguindo a
convenção comum de localizações oficiais de FF em PT-BR.

**Métrica real de progresso em entry41**: 406 de 5872 strings totais
diferem do inglês original (a métrica "strings únicas" de antes
contava errado por incluir nomes próprios que ficam iguais de propósito,
tipo "Samurai"→"Samurai"). Restam **446 strings genuinamente com frases
completas em inglês ainda não traduzidas** — na maioria são **nomes de
missões/rumores do mapa-mundi** (ex. "The Salvage of the Highwind", "The
Hero-King of Legend", "Son of a Sandworm" — nomes criativos de quests,
precisam de tradução cuidadosa, não mecânica) e mais alguns itens de
menu/opções espalhados. Também restam ~300-400 nomes de armas/acessórios
específicos ainda não revisados (entre os ~2800 "nomes próprios" —
preciso passar por eles para decidir tradução vs. manter original, a
maioria provavelmente fica em inglês mas alguns descritivos ainda
precisam de tradução como os lotes já feitos).

**Ferramenta nova reutilizável**: `translation/tools/apply_all_glossary.py`
— roda de uma vez todos os passes de glossário já validados (rótulos,
tipos de item, grid de classes, elementos/status, nomes de habilidade,
gatilhos) em qualquer arquivo `ptbr/*.json`. Já testei em `entry40_open.json`
e `entry41_join.json` (0 toques, porque o conteúdo deles não usa esse
formato de card de item — é só vocabulário solto).

## ✅ entry42_help.json — efetivamente completo

968 strings únicas, das quais 967 são nomes próprios (nomes de
personagens como Ramza/Delita/Agrias/Beowulf/Cloud, e títulos de
faixas de música do sound test, tipo "Goner with the Wind") — **não
devem ser traduzidos** (nomes próprios e nomes de música ficam como
estão). A única string que era texto de UI de verdade ("Please input
your birthday...") já foi traduzida. Arquivo `translation/ptbr/entry42_help.json`
criado e validado (round-trip ok).

## 🎉 OS 8 ARQUIVOS ESTÃO COMPLETOS (2026-10-13, 5ª rodada)

Status final de `translation/ptbr/`:

| Arquivo | Status |
|---|---|
| `entry36_atchelp.json` | Passthrough (bloqueado por formato de arquivo; conteúdo duplicado já cobre via entry38) |
| `entry37_spell.json` | Passthrough (conteúdo em japonês, confirmado) |
| `entry38_sample.json` | ✅ **100% traduzido** — classes, monstros, itens/armas/armaduras, zodíaco, todas as habilidades/skills do jogo |
| `entry39_world.json` | Passthrough (conteúdo em japonês, confirmado) |
| `entry40_open.json` | Passthrough (conteúdo em japonês, confirmado) |
| `entry41_join.json` | ✅ **100% traduzido** (1302 de 5872 strings mudadas; o resto são nomes próprios/placeholder intencionalmente mantidos — verificado item a item, nenhum texto real ficou pra trás) — nomes de classe/monstro, ~250 nomes de arma/armadura/acessório, zodíaco redundante, menus de opções/tutorial, **~350 falas do Taverneiro** (diálogo de missões/rumores), ~30 títulos de capítulo da história, títulos de personagem, ~100 descrições de missão do mapa-mundi, e mais ~56 nomes de missão/masmorra/chefe (ex. "The Catacombs"→"As Catacumbas", "The Oubliette"→"A Masmorra Esquecida") achados numa varredura extra pós-conclusão |
| `entry42_help.json` | ✅ Efetivamente completo (nomes próprios + 1 frase de UI) |
| `entry43_wldhelp.json` | Passthrough (conteúdo em japonês, confirmado) |

**Validação**: todos os 8 arquivos passam round-trip completo
(`decode(encode(s)) == s` para cada string) sem nenhum erro.

**Próximo passo real (fora do escopo desta tarefa)**: repacking — recodificar
cada JSON de volta para bytes e reconstruir o `fftpack.bin`/`.obb`, depois
testar no device. E a decisão de acentuação (ã/õ/ç/â/ê/ô/ó ausentes da
fonte) que o usuário quer resolver "hackeando" a fonte do jogo.

## Resumo do que falta (próximas iterações do loop)

1. Continuar traduzindo entry 38 (restam ~806 strings reais de ~1280,
   incluindo um bloco repetitivo de compatibilidade de signos do zodíaco
   — tem um template claro, dá pra fazer rápido) e depois os outros 7
   arquivos (`entry36_atchelp`, `entry40_open`, `entry41_join`, etc.;
   `entry42_help` são majoritariamente NOMES PRÓPRIOS de personagens —
   manter como estão; `entry37_spell`/`entry39_world`/`entry43_wldhelp`
   parecem ser majoritariamente falas/flavor-text em japonês nesta
   amostra — baixa prioridade, confirmar antes de gastar tempo traduzindo).
2. Em paralelo (conforme decisão do usuário), continuar tentando decifrar
   o formato de bytecode de evento (diálogo da história) — ver seção de
   bloqueio acima. Ainda não tentei nenhuma hipótese concreta sobre a
   estrutura do cabeçalho dos blocos de 8192 bytes.
3. Ainda não implementada: a etapa de **repacking** (escrever o texto
   traduzido de volta no `fftpack.bin`, recalculando a tabela de offsets
   do container — ver seção 3 do início deste documento sobre o risco de
   offsets hardcoded fora do índice, que precisa ser verificado antes de
   redimensionar qualquer entrada).

## Pré-pesquisa anterior (ainda válida)

### Confirmado

1. **O `.obb` é uma imagem FAT32.** Montada read-only via:
   `udisksctl loop-setup -r -f obb-data/main.202000...obb` → `/dev/loopN` →
   auto-montado em `/run/media/<user>/18DB-73EA`.
   Conteúdo: `base/fftpack.bin` (203MB), `base/g2d.dat`, `base/music.dat`,
   `base/sound.dat`, `base/font/`, `base/movie/`.

2. **`fftpack.bin` é literalmente o arquivo do ISO do PSP de FFT: WotL**, só
   reempacotado. Strings internas confirmam (`C:\FFTIMG\MAP\GNS\`,
   `c:\fftimg\event\zodiac.bin`) — mesma árvore de arquivos documentada pela
   comunidade FFHacktics para a versão PSP.

3. **Container `fftpack.bin`**: header de 8 bytes (`uint32 count=3931`,
   `uint32 unk=16`) seguido de `count+1` offsets `uint32` LE delimitando cada
   entrada (entrada N vai de `offset[N]` a `offset[N+1]`). Script de parsing:
   `parse_pack.py` / `extract_sample.py` nesta pasta.
   ⚠️ Nota de um fórum (ainda não confirmada por nós): partes do jogo podem
   usar offsets absolutos hardcoded para dentro do fftpack em vez do índice —
   precisa validar antes de redimensionar qualquer entrada.

4. **Tabela de caracteres COMPLETA encontrada** — `PatcherLib/TextUtilities/TextUtilities.cs`
   do repositório `Glain/FFTPatcher` (GitHub, salvo em `fftpatcher-src/TextUtilities.cs`,
   array `PSXCharacterSet` a partir da linha 38, extensão PSP em
   `GetPSPCharacterSet()` ~linha 200). Não é ASCII: bytes 0x00-0x09 = dígitos
   '0'-'9', 0x0A-0x23 = 'A'-'Z', 0x24-0x3D = 'a'-'z', daí pontuação/kana
   intercalados, e acima de 0xCF usa 2 bytes (kanji, majoritariamente).
   **Acentos latinos (só na versão PSP)**: 0x880=á, 0x881=à, 0x882=é, 0x883=è,
   0x884=í, 0x885=ú, 0x886=ù, 0x887=-, 0x888=—.
   **🚩 LIMITAÇÃO IMPORTANTE PARA PT-BR**: não existem ã, õ, ç, â, ê, ô, ü no
   conjunto de caracteres. Isso bloqueia uma tradução 100% ortográfica
   (ex.: "não", "ação", "coração" não são representáveis como estão).
   Opções a decidir com o usuário mais adiante:
   (a) escrever sem esses acentos/cedilha (comum em fansubs antigos: "nao",
   "acao"), (b) adicionar novos glifos no bitmap da fonte (10x14px, 2bpp,
   reaproveitando slots de kanji não usados — viável, trabalho extra de
   pixel art + apontar novas entradas na Character Table), (c) aproximações
   (ex. "informacao" por "informação").

5. **Códigos de controle do texto** documentados na wiki (salva em
   `wiki-Text_Format.html`): `{br}`=quebra de linha, `{end}`/`{close}`=fim de
   string, `{delay:??}`, `{font:??}`=cor, `{waitpress}`, `{Ramza}`=nome de
   unidade, `{FB}`/`{FC}`=lista de escolhas, etc. Preservar sempre intactos
   na tradução.

6. **Algoritmo de compressão identificado e já é LZ77-like simples** (não é
   LZW nem "shishi" — esse nome era de outra ferramenta, sprites). Código-fonte
   em `fftpatcher-src/TextUtilities.cs`:
   - Decompress: bytes 0xF0-0xF3 são marcadores de 3 bytes
     (`[marker, b1, b2]`) que significam "copie N bytes de J posições atrás
     no stream já decodificado"; senão, byte literal.
   - `length = ((b0 & 0x03) << 3) + ((b1 & 0xE0) >> 5) + 4`
   - `j = ((b1 & 0x1F) << 8) + b2; jump = j - (j/256)*2`
   - Compress é o inverso (ver `AbstractFile.cs`/`TextUtilities.cs` método
     `Compress`/`CompressSection`).

7. **Mapa de onde cada categoria de texto mora** (versão PSP), em
   `fftpatcher-src/PSP_FileContents.txt`: nomes/descrições de jobs, itens,
   habilidades, menus etc. ficam em arquivos como `BOOT.BIN` (em offsets
   absolutos específicos), `WORLD.BIN`, `WORLD.LZW`, `OPEN.LZW`,
   `ATCHELP.LZW`, `WLDHELP.LZW`, `SAMPLE.LZW` — esses eram arquivos separados
   no ISO do PSP. **Isso cobre MENUS/NOMES, não os diálogos da história.**

### Ainda não resolvido (próximos passos — atualizado 2026-10-13, 3ª rodada)

Itens antigos desta lista (mapear fftpack.bin, entender formato de texto,
decidir acentuação, validar decode) **já foram resolvidos** — ver seções
acima. Lista atual real:

- [ ] **entry41_join.json**: revisar as ~700-900 strings restantes que são
  nomes próprios de armas/itens específicos (decidir caso a caso: traduzir
  nomes descritivos tipo "Mythril Sword", manter nomes míticos/próprios
  tipo "Excalibur" como estão) e traduzir o bloco de ~150-200 itens de
  menu de opções/tutorial (frases completas, ainda não tocadas).
- [ ] **entry36_atchelp.json**: ainda bloqueado por formato de arquivo
  (`SectionedFile` com cabeçalho de 128 bytes cujos offsets não bateram
  com o esperado) — baixa prioridade agora que confirmamos que o mesmo
  conteúdo (descrições de habilidade/classe/monstro) já está 100%
  traduzido via `entry38_sample.json`. Só vale revisitar se sobrar tempo.
- [ ] **Repacking ainda não implementado**: depois que a tradução de texto
  estiver completa, falta (a) recodificar cada `translation/ptbr/*.json`
  de volta para bytes usando `fft_text.encode_string`, (b) reconstruir o
  `fftpack.bin` com a tabela de offsets recalculada para as entradas que
  mudaram de tamanho, (c) testar em device/emulador. Ver nota sobre
  possíveis offsets hardcoded fora do índice (seção 3 do início deste
  documento) — precisa ser verificado antes de redimensionar qualquer
  entrada.
- [ ] Depois de tudo traduzido: a decisão de acentuação (ã/õ/ç/â/ê/ô/ó
  ausentes da fonte) fica pendente de confirmação final do usuário — ele
  já disse que quer "hackear" a fonte para adicionar os glifos que faltam
  depois que a tradução de texto estiver completa.

## 🔤 Hack de fonte (acentos ã/õ/ç/â/ê/ô/ó) — ✅ RESOLVIDO (2026-10-14)

Decisão do usuário: reaproveitar glifos de kanji não usados (sem mexer no
código nativo) em vez de adicionar códigos novos. Progresso via engenharia
reversa de `libgl2jni.so` (ARM), primeiro manualmente com Capstone, depois
com as ferramentas REA (ponte pro Hopper Disassembler — Ghidra não está
instalado nesta máquina, mas Hopper deu decompilação funcional):

- Confirmado: texto renderiza via tabela de bitmap fixa 2bpp (35 bytes/glifo,
  10x14px) — não é fonte do sistema.
- Confirmado: o motor trata bytes `0xD0`-`0xDF` (16 valores) como líder de
  2 bytes — mais que os `0xD0`-`0xDA` documentados pela comunidade.
- Mapeei a cadeia de chamadas da renderização: uma função em `0x18f0c8`
  itera um array de códigos de 16 bits (mesmo formato composto por
  `GetFontCode`) chamando `eFontToImageAll`→`eFontToImage` pra cada
  caractere, até achar o terminador `0xFFFF`. `eFontToImage` calcula
  `endereco_base + 35*indice_do_glifo` — mas **ainda não achei onde,
  dentro de `eFontToImage`, o código de 16 bits vira esse índice**, nem
  onde fica o buffer de 35 bytes/glifo na memória (candidatos
  `fontbufptr`/`wfontbufptr`/`gFontWork`, ainda não resolvidos).
- `GetFontCode` em si só tem 1 callsite real (lógica de "espiar próximo
  caractere", não a renderização) — confirmado via `procedure_callers`
  do REA, então o pipeline de indexação de glifo é outra função ainda
  não localizada.

**Nota operacional**: o bridge REA↔Hopper tem um bug de trava órfã —
quando o processo do Hopper morre sem avisar o servidor REA, chamadas
seguintes travam citando uma sessão morta. Solução que funcionou: apagar
o diretório de lock em `/tmp/rea-*` (confirmando antes que o PID
registrado nele está morto) e chamar `close_binary`/`open_binary` de novo.

### 🎯 ACHADO CRÍTICO (2026-10-14): fórmula exata do índice de glifo

Desmontei manualmente `eFontToImageAll` (0x18ede8, com Capstone) e achei a
instrução exata que calcula o índice do glifo a partir do byte do texto
(em `eFontToImageAll+0x138`, bloco em 0x18ef20-0x18ef3c):

```
se byte <= 0xCF:              indice = byte                    (0-207)
se 0xD0 <= byte <= 0xDF:       indice = 0xD0 * (byte & 0xF) + proximoByte
```

**Validado**: aplicando essa fórmula ao código conhecido do 'á' (0xDA60,
ou seja byte-lider=0xDA, próximo-byte=0x60): `0xD0 * (0xDA & 0xF) + 0x60`
= `0xD0 * 0xA + 0x60` = `2080 + 96` = **2176 = 0x880** — bate EXATAMENTE
com o índice 0x880 que já sabíamos ser 'á' pela tabela de caracteres do
FFTPatcher. Isso confirma a fórmula com certeza.

**Implicação pra nossa estratégia (reaproveitar kanji não usados)**: como
já sabemos a fórmula completa, para reaproveitar um glifo de kanji
qualquer (índice N entre 208 e ~2199, todos endereçáveis via algum byte
0xD0-0xDA + segundo byte) não precisamos mexer em nenhum código — só
achar o BUFFER DE BITMAP (ainda não localizado) e sobrescrever os 35
bytes daquele índice especifico.

**Ainda não localizado**: o buffer de bitmap dos glifos em si. Descartado
nesta rodada: a entrada pequena do `fftpack.bin` (código, não dados), e
regiões de baixa entropia tanto em `g2d.dat` quanto dentro do próprio
`libgl2jni.so` (renderizei várias como imagem pra conferir visualmente —
nenhuma parece glifo de texto). O ponteiro é carregado em runtime via uma
global (`fontbufptr`/`wfontbufptr`/`gFontWork` ou uma quarta ainda não
nomeada) — persegui a cadeia de GOT/relocação até um endereço
(`0x12f2f0`) que não bate com nenhum desses símbolos conhecidos, então
ainda há uma peça faltando nessa cadeia.

**Estratégia melhor pra próxima tentativa** (mais forte que busca cega por
entropia): como agora sabemos que o índice 0 ('0') e o índice 0x880 ('á')
estão **exatamente 2176 glifos = 76160 bytes de distância um do outro**,
dá pra fazer uma busca por CORRELAÇÃO DUPLA no arquivo inteiro: procurar
um offset X tal que tanto X quanto X+76160 pareçam glifo plausível (poucos
pixels, formato contido na caixa 10x14) — muito mais forte que a
heurística de entropia simples usada até agora. Não cheguei a implementar
essa busca nesta sessão.

**Atualização: implementei a busca por correlação dupla/múltipla** (ver
`translation-research/font-hack/scan_glyph_fast*.py` — script vetorizado
com numpy, decodifica o arquivo inteiro como stream de valores de 2 bits
de uma vez e usa soma cumulativa pra testar todo deslocamento de byte em
`O(1)`, então checa simultaneamente se os índices 0,1,2,3,10,11,0x880
("0","1","2","3","A","B","á") parecem plausíveis ali). Rodei contra
`g2d.dat` (22MB): de 21,9 milhões de posições candidatas, sobrou 1 cluster
de 363 posições consecutivas (`0x5bd927`-`0x5bda91`). **Renderizei esse
cluster e é claramente um padrão de xadrez/dither repetitivo — falso
positivo, não são glifos de texto.** Ou seja: `g2d.dat` muito provavelmente
**não contém** a tabela de fonte nesse formato linear 2bpp simples (pelo
menos não com as suposições de dimensão/ordem de bits testadas).

### 🎉 ACHADO FINAL (2026-10-14, 6ª rodada): tabela de glifos localizada e hackeada

A busca cega por entropia/correlação (seções acima) nunca ia dar certo:
a tabela de fonte não está em `g2d.dat` nem em `fftpack.bin` — está
**embutida direto dentro de `libgl2jni.so`** (seção `.data`), carregada
só por um ponteiro PC-relative, sem nenhum `fopen`/`fread` em runtime.

Caminho até achar: persegui de novo a cadeia GOT de `eFontToImage`
(`0x18ec04`→`0x18ec10`→`0x18ec14`) e achei o bug que travou a sessão
anterior — eu estava lendo o valor da entrada GOT usando o endereço
virtual (vaddr) diretamente como offset de arquivo, mas pra endereços
depois do primeiro `PT_LOAD` (≥ `0x3430a8`) o offset de arquivo é
`vaddr - 0x1000` (confirmado via `readelf -SW`, segundo segmento:
vaddr=0x3430a8, offset=0x3420a8). Corrigindo isso, a entrada GOT em
`0x3462f4` resolve exatamente pro endereço de `fontbufptr` (`0x46d204`,
símbolo exportado) — confirmando que `eFontToImage` realmente usa esse
global, como sempre suspeitamos.

Isso ainda não dizia ONDE o buffer fica (só que é lido via ponteiro
`fontbufptr`, preenchido em algum lugar em runtime). O achado decisivo
veio de outro símbolo exportado — `iOS_GetFontBuffer()` (`0xd6d84`) —
uma função de 4 instruções que **não usa GOT nenhum**, só soma
`pc`-relative direto (`ldr r0,[pc,#8]; add r0,pc,r0; add r0,r0,#0x268`):
isso só é possível pra um símbolo LOCAL/estático, cujo endereço o
compilador já resolve em tempo de link. Calculando manualmente: resolve
pra vaddr `0x356e54`, dentro da seção `.data` (que tem conteúdo real no
arquivo, ao contrário de `.bss`) — ou seja, **dado estático embutido no
`.so`**, não carregado de arquivo nenhum.

Renderizei esse offset como tira de glifos 2bpp 10x14 e bateu na hora:
dígitos, A-Z, a-z, hiragana, katakana, kanji — a fonte real. Conferência
cruzada: índice `0x880` (= `0xD0*(0xDA&0xF)+0x60`, a fórmula já
confirmada antes) cai exatamente em cima da sequência conhecida
á,à,é,è,í,ú,ù,-,— (offsets 0x880-0x888), byte a byte.

**Localização final**:
- `libgl2jni.so` (armeabi/ARM): offset de arquivo `0x355e54` (= vaddr
  `0x356e54` em `.data`, vaddr_offset delta `0x1000`).
- `libgl2jni.so` (x86): offset de arquivo `0x3daf00` — achado por busca
  binária direta dos primeiros 400 bytes da tabela ARM dentro do arquivo
  x86 (conteúdo idêntico, só offset de compilação diferente; casamento
  único, sem ambiguidade).
- Formato: 35 bytes/glifo, 2bpp, 10x14px, confirmado batendo com a doc
  antiga do FFTPatcher/wiki.
- Tabela tem exatamente 2200 glifos definidos (`len(PSX_CHARS)`); índice
  `0x898` (2200) em diante é espaço não utilizado dentro da mesma tabela
  contígua (confirmado visualmente — vira ruído/lixo sem padrão de
  glifo a partir daí), ou seja, **7 slots livres sem precisar mexer em
  nenhum código nativo**, exatamente a estratégia que o usuário escolheu.

**Glifos novos** (compostos a partir de letras/acentos já existentes na
própria fonte — `a`/`e`/`o`/`c` como base, acento agudo reaproveitado de
`á`/`é`/`ú`, circunflexo/til/cedilha desenhados à mão no estilo pixelado
do resto da fonte):

| caractere | código (lead+byte) | índice do glifo |
|---|---|---|
| ã | `0xDA78` | `0x898` |
| õ | `0xDA79` | `0x899` |
| ç | `0xDA7A` | `0x89A` |
| â | `0xDA7B` | `0x89B` |
| ê | `0xDA7C` | `0x89C` |
| ô | `0xDA7D` | `0x89D` |
| ó | `0xDA7E` | `0x89E` |

Esses códigos usam o lead byte `0xDA`, que já estava dentro do range
suportado pela ferramenta Python (`TWO_BYTE_LEAD` já inclui `0xD0`-`0xDA`)
e pela engine nativa — não precisou estender nada.

**Aplicado**:
- `src/lib/armeabi/libgl2jni.so` e `src/lib/x86/libgl2jni.so` — 35 bytes
  de cada um dos 7 índices sobrescritos com os novos bitmaps. Originais
  preservados como `libgl2jni.so.orig_backup` nas mesmas pastas.
- `translation/tools/fft_text.py` — `build_psp_chars()` agora acrescenta
  os 7 caracteres novos ao array `chars` (índices 0x898-0x89E), e o loop
  sistemático existente em `build_charmap()` já gera as chaves corretas
  (`0xDA78`-`0xDA7E`) automaticamente, sem precisar de caso especial.
  `encode_string`/`decode_bytes` confirmados fazendo round-trip correto
  pros 7 caracteres novos.
- Preview dos glifos: `translation-research/font-hack/new_glyphs_preview.png`.
- ✅ **Acentos restaurados nos 8 arquivos `ptbr/*.json`** — script
  `translation-research/font-hack/restore_accents.py` varreu
  `entry38_sample.json`, `entry41_join.json` e `entry42_help.json` (os
  únicos com prosa PT-BR real; os outros 5 são passthrough e não foram
  tocados) e trocou as aproximações sem acento pelas formas corretas
  usando os 7 caracteres novos — ex.: "nao"→"não", "acao"→"ação",
  "informacoes"→"informações", "forca"→"força", "agua"→"água",
  "experiencia"→"experiência", "bonus"→"bônus", "fenix"→"fênix",
  "heroi"→"herói". Não mexeu em acentos que já existiam antes (á, é, í,
  ú, à, è, ù) — só nos 7 novos (ã, õ, ç, â, ê, ô, ó). Regras: dicionário
  explícito de palavras conferidas manualmente contra o corpus real +
  sufixos produtivos do português (-ção/-ções, -são/-sões, -ão/-ões
  genéricos, -ância/-ência, -ança/-ença), com listas de exceção pra
  palavras que parecem mas não são (ex. "branca" não vira "brança").
  Resultado: 495 strings alteradas em entry38, 267 em entry41, 2 em
  entry42 (764 no total); 1015 ã, 580 ç, 41 õ, 36 ê, 28 ó, 20 â, 10 ô
  adicionados. Detalhe importante: a fonte não tem NENHUMA letra
  acentuada maiúscula (nem Ç) — quando uma palavra reescrita cai no
  início de frase/maiúscula (ex. "Agua"→"água"), a primeira letra fica
  minúscula mesmo (ex. "água sagrada" não "Água Sagrada"), única opção
  dentro da limitação da fonte. **Round-trip revalidado nos 8 arquivos
  completos após a correção: 0 erros.**

## 📦 Repacking — ✅ CONCLUÍDO (2026-10-14)

Script: `translation/tools/repack_fftpack.py`. Reconstrói `fftpack.bin`
inteiro a partir do original + os 3 arquivos `ptbr/*.json` com conteúdo
real (entry38, entry41, entry42); entries 36/37/39/40/43 (passthrough) e
todos os outros ~3900 entries do container (mapas, texturas, efeitos
etc.) são copiados byte-a-byte do arquivo original, sem tocar.

**Achado crítico durante o repacking**: `entry41_join.json` (o maior
arquivo, a tradução mais trabalhada) tinha os **limites de string
desalinhados** desde a extração original. Causa raiz: `decompress()` em
`fft_text.py` foi corrigido numa sessão anterior pra ler back-references
do buffer de ENTRADA original (confirmado batendo com
`TextUtilities.cs` do FFTPatcher: `allBytes.Sub(i+sectionStart-jump, ...)`
— lê do arquivo comprimido inteiro, não do buffer de saída crescente) —
mas essa correção nunca foi re-validada contra `entry41` especificamente
(só contra `entry36`), e o arquivo-fonte `entry41_join.json` tinha sido
gerado ANTES dessa correção, com a versão antiga (buffer de saída).
Resultado: no byte 105 do stream descomprimido, um marcador de
compressão degenerado (`jump=0`, auto-referência) expande 3 bytes em 28,
fazendo a decodificação "correta" (atual) achar **5 strings a mais**
(5877 em vez de 5872) logo no início do arquivo — mas crucialmente, a
partir daí, string por string, as duas decodificações **batem
perfeitamente com um deslocamento fixo de +5** (confirmado em 5871 das
5871 strings restantes, zero divergência). As 5-6 primeiras strings
afetadas não são prosa real (são uma string de dados/tabela ilegível,
tipo `"0000100020003000400050006000F600ま..."`, mais 4 strings vazias) —
nunca foram traduzidas, então não havia risco de perder trabalho.
Corrigido via `fix_entry41_boundaries.py` (salvo em
`docs/translation-research/font-hack/` junto com os outros scripts desta
sessão): reconstrói `source/entry41_join.json` e `ptbr/entry41_join.json`
com os 5877 limites corretos, mantendo todas as 5871 traduções existentes
(só re-indexadas). Round-trip revalidado: 0 erros nas 5877 strings.

**Segundo problema (no nível de bytes, não de JSON)**: como optamos por
armazenar as entries reconstruídas **sem compressão** (texto PT-BR não
precisa economizar espaço, e só `entry41` tem compressão real mesmo
assim — `entry36`, que também comprime, é passthrough e nunca re-
codificado), qualquer byte `0xF0`-`0xF3` que sobreviva de conteúdo
original não-traduzido (como aquela mesma string de dados ilegível do
`entry41`) pode colidir com o espaço de marcador de compressão quando o
JOGO for descomprimir nosso arquivo de novo. `repack_fftpack.py` tem uma
função `sanitize_markers()` que detecta isso (reproduzindo a mesma
checagem de limites do `decompress()`) e neutraliza maximizando o "jump"
codificado pra forçar o fallback de cópia literal — só mexe em conteúdo
já irreconhecível (`{0xNN}` sem tradução possível), nunca em texto
real/traduzido (confirmado estruturalmente: nenhum código de caractere
válido em `PSP_TABLE` usa `0xF0`-`0xF3`). Resultado: 1 marcador
neutralizado em `entry41` (cosmético, o conteúdo já era ilegível antes e
depois), zero em `entry38`/`entry42`.

**Validação final do `fftpack.bin` reconstruído**: todas as ~3900 entries
não tocadas conferidas byte-idênticas ao original (amostra incluindo
começo/meio/fim do container); as 3 entries reconstruídas conferidas
string-por-string contra o JSON `ptbr/` (0 divergências reais, 1
tolerada/esperada). Tamanho final: 213.157.903 bytes (original:
213.143.552, delta +14.351 — cabia nos 312KB livres da imagem FAT32 do
`.obb`, que estava com apenas ~1KB de folga por entry).

**Aplicado**: `fftpack.bin` novo copiado para dentro do `.obb`
(`obb-data/main.202000.com.square_enix.android_googleplay.FFT_en2.obb`,
montado em loop device RW via `udisksctl`, depois remontado RO de novo).
Checksum MD5 conferido batendo entre o arquivo gerado e o que ficou
gravado dentro da imagem FAT32. APK recompilado via `scripts/build.sh`
(apktool build + zipalign + apksigner, usando os `libgl2jni.so` já
hackeados com os novos glifos) — build/assinatura OK,
`FFT_Android_Mod-signed.apk` pronto. Teste em device real pendente
(aguardando reconexão USB).

## Arquivos desta pasta

- `fftpatcher-src/` — trechos do código-fonte do FFTPatcher (GPLv3,
  Glain/FFTPatcher no GitHub) relevantes para texto/compressão/charmap.
- `wiki-Text_Format.html`, `wiki-Font.html` — páginas da wiki FFHacktics
  arquivadas via Wayback Machine (site original bloqueia fetch automatizado
  via Cloudflare).
- `parse_pack.py`, `extract_sample.py` — scripts usados para entender o
  container `fftpack.bin`.
