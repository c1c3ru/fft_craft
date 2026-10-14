import sys
sys.path.insert(0, "tools")
from translate_batch import apply
PATH = "/home/c1c3ru/Downloads/finalfantasy/FFT_Android_Mod/translation/ptbr/entry38_sample.json"

T = {
"Used for self-defense. Although its blade is longer than{br}that of a normal knife, its attack power is rather low.":
"Usada para autodefesa. Embora sua lamina seja mais longa{br}que a de uma faca normal, seu poder de ataque e bem baixo.",
"A sturdy, well-balanced knife forged from the featherlight{br}metal known as mythril.":
"Uma faca resistente e bem equilibrada, forjada do metal{br}leve como pena conhecido como mithril.",
"A knife quenched in an insidious poison that robs its{br}victim of sight.":
"Uma faca temperada num veneno insidioso que rouba{br}a visao da vitima.",
"Created especially for the purpose of fighting mages,{br}this knife has the power to silence its target.":
"Criada especialmente para combater magos,{br}esta faca tem o poder de silenciar seu alvo.",
"A knife with a blade made of a lustrous white alloy{br}of mythril and platinum. ":
"Uma faca com lamina feita de uma liga branca e brilhante{br}de mithril e platina. ",
"This knife gives the wielder a good chance of blocking{br}attacks, making it useful for both offense and defense.":
"Esta faca da ao usuario uma boa chance de bloquear{br}ataques, sendo util tanto para ataque quanto defesa.",
"A knife made of an exceedingly hard metal.{br}Light and sharp.":
"Uma faca feita de um metal extremamente resistente.{br}Leve e afiada.",
"Popular among assassins, this dagger has the power{br}to doom its victims to certain death.":
"Popular entre assassinos, esta adaga tem o poder{br}de condenar suas vitimas a morte certa.",
"This knife's special wave-shaped blade creates a vacuum{br}when swung through the air, increasing its killing power.":
"A lamina ondulada especial desta faca cria um vacuo{br}ao ser brandida no ar, aumentando seu poder letal.",
"A knife manufactured in a region renowned for its{br}blades.":
"Uma faca fabricada numa regiao famosa por suas{br}laminas.",
"A sword specially tailored to the needs of ninjas.{br}Its blade is shorter than that of the average sword.":
"Uma espada feita especialmente para as necessidades dos ninjas.{br}Sua lamina e mais curta que a de uma espada comum.",
"A multipurpose sword for ninjas.":
"Uma espada multiuso para ninjas.",
"This sword's short, lightweight blade makes it very easy{br}to carry.":
"A lamina curta e leve desta espada a torna muito facil{br}de carregar.",
"A sword with a longer blade than that of a normal ninja{br}sword, making it more suitable for use in battle.":
"Uma espada com lamina mais longa que a de uma espada{br}ninja comum, tornando-a mais adequada para batalha.",
"A sword with the power to stop its targets in their{br}tracks, preventing them from taking any actions.{br}":
"Uma espada com o poder de paralisar seus alvos no{br}lugar, impedindo-os de agir.{br}",
"An exquisitely crafted ninja sword that was once used{br}by a secret society.":
"Uma espada ninja de fabricacao refinada, outrora usada{br}por uma sociedade secreta.",
"A powerful ninja sword that was once used by a{br}secret society.":
"Uma poderosa espada ninja outrora usada por uma{br}sociedade secreta.",
"This broad-bladed sword is suited for large slashing{br}strokes. It is inexpensive, but not particularly powerful.":
"Esta espada de lamina larga e indicada para grandes{br}golpes de corte. E barata, mas nao muito poderosa.",
"This straight and sharp double-edged blade can be used for{br}either stabbing or slashing.":
"Esta lamina reta e afiada de dois fios pode ser usada{br}tanto para perfurar quanto para cortar.",
"This sword has a broad and sturdy blade, but its{br}iron construction makes it very heavy.":
"Esta espada tem uma lamina larga e resistente, mas sua{br}construcao em ferro a torna muito pesada.",
"A sword forged from the metal known as mythril.{br}Its brilliantly shining blade is incredibly lightweight.":
"Uma espada forjada do metal conhecido como mithril.{br}Sua lamina brilhante e incrivelmente leve.",
"The blade of this sword is a deep crimson, as if it were{br}drenched in blood. It is cruelly sharp.":
"A lamina desta espada e de um vermelho profundo, como se{br}estivesse encharcada de sangue. E cruelmente afiada.",
"The handle of this single-edged sword has been decorated{br}with intricate coral piecework.{br}":
"O cabo desta espada de um so fio foi decorado{br}com um intricado trabalho em coral.{br}",
"A sword constructed using ancient techniques that{br}have long since perished from the world.{br}":
"Uma espada construida com tecnicas antigas que{br}desapareceram do mundo ha muito tempo.{br}",
"A wide-bladed sword with a midnight blue handle.":
"Uma espada de lamina larga com cabo azul-meia-noite.",
"A shining sword made of a lustrous white alloy of mythril{br}and platinum. Its broad blade is wickedly sharp.":
"Uma espada brilhante feita de uma liga branca e lustrosa de mithril{br}e platina. Sua lamina larga e maliciosamente afiada.",
"The countless tiny diamonds embedded into this sword's{br}blade saw into its victims, causing great damage.":
"Os inumeros diamantes minusculos incrustados na lamina{br}desta espada cortam suas vitimas, causando grande dano.",
"A sword with a transparent blade that resembles ice.":
"Uma espada com lamina transparente que se parece com gelo.",
"A sword inscribed with ancient runes.":
"Uma espada gravada com runas antigas.",
"This dark blade is mentioned in legends about the end{br}of the world.{br}":
"Esta lamina sombria e mencionada em lendas sobre o fim{br}do mundo.{br}",
"A broad-bladed knight's sword made from hardened steel.{br}Jewels have been embedded in its rounded pommel.":
"Uma espada de cavaleiro de lamina larga feita de aco endurecido.{br}Joias foram incrustadas em seu pomo arredondado.",
"It is said that only the true heir to the throne can{br}wield this legendary knight's sword.{br}":
"Diz-se que somente o verdadeiro herdeiro do trono pode{br}empunhar esta lendaria espada de cavaleiro.{br}",
"This knight's sword is mentioned in tales about the end{br}of the world.{br}":
"Esta espada de cavaleiro e mencionada em contos sobre o fim{br}do mundo.{br}",
"This holy knight's sword is said to have been a gift{br}from the gods themselves.{br}":
"Dizem que esta espada sagrada de cavaleiro foi um presente{br}dos proprios deuses.{br}",
"A katana with a brilliant white blade.":
"Uma katana com lamina branca e brilhante.",
"A katana whose blade is adorned with a breathtaking{br}carving of a tiger.":
"Uma katana cuja lamina e adornada com um deslumbrante{br}entalhe de um tigre.",
"A katana with a blade forged of the finest iron sand{br}by master swordsmith Nagamitsu Osafune.":
"Uma katana com lamina forjada da mais fina areia de ferro{br}pelo mestre forjador Nagamitsu Osafune.",
"Referred to as a demon sword, this katana's keen{br}blade showers blood upon the battlefield.":
"Chamada de espada demoniaca, a lamina afiada desta{br}katana derrama sangue pelo campo de batalha.",
"This katana's design was inspired by a legendary blade said{br}to have been plucked from the tail of a marauding dragon.":
"O desenho desta katana foi inspirado numa lamina legendaria{br}que, segundo dizem, foi arrancada da cauda de um dragao saqueador.",
"This exquisitely crafted katana has a beautifully{br}patterned blade and an incredible cutting edge.":
"Esta katana de fabricacao refinada tem uma lamina{br}belamente padronizada e um fio de corte incrivel.",
"Referred to as a demon sword, this katana was said{br}to drink the blood of countless enemies.":
"Chamada de espada demoniaca, dizem que esta katana{br}bebeu o sangue de inumeros inimigos.",
"A katana with a hilt in the shape of a chrysanthemum.":
"Uma katana com punho em forma de crisantemo.",
"This katana's sheath is inlaid with beautiful patterns.{br}It is the life's work of a master swordsmith.":
"A bainha desta katana e incrustada com belos padroes.{br}E a obra de uma vida de um mestre forjador.",
"This katana is decorated with intricate designs.":
"Esta katana e decorada com desenhos intricados.",
"A battle axe with a long handle. Designed for two-handed{br}use, it can easily chop off an enemy's limbs.":
"Um machado de batalha com cabo longo. Feito para uso{br}com as duas maos, pode decepar membros de um inimigo com facilidade.",
"An axe with a large head. Much bigger than the traditional{br}woodman's axe, hence its name.":
"Um machado com uma cabeca grande. Muito maior que o{br}machado tradicional de lenhador, dai o nome.",
"This axe not only has impressive destructive power,{br}but can also slow the actions of its target.":
"Este machado nao so tem um poder destrutivo impressionante,{br}como tambem pode retardar as acoes de seu alvo.",
"A rod fashioned from evergreen wood.":
"Um cajado feito de madeira sempre-verde.",
"A rod imbued with the power of thunder.{br}{br}":
"Um cajado imbuido com o poder do raio.{br}{br}",
"A rod imbued with the power of fire.":
"Um cajado imbuido com o poder do fogo.",
"A rod imbued with the power of ice.":
"Um cajado imbuido com o poder do gelo.",
"A rod with a poisoned tip.":
"Um cajado com a ponta envenenada.",
"A rod that enhances the magickal potency of its wielder.":
"Um cajado que aumenta o poder magico de quem o empunha.",
"A rod wielded by a dragon master. Its tip is made from{br}carved dragon bone.":
"Um cajado empunhado por um mestre dos dragoes. Sua ponta e feita{br}de osso de dragao esculpido.",
"This rod purges doubt from those it touches, turning{br}them into pillars of faith.{br}":
"Este cajado purga a duvida de quem ele toca, transformando-os{br}em pilares de fe.{br}",
"A staff made from sturdy oak.":
"Um cetro feito de carvalho resistente.",
"A staff carried by members of the clergy.":
"Um cetro usado por membros do clero.",
"A staff imbued with the power of spirits.{br}Has the power to restore HP to those it hits.":
"Um cetro imbuido com o poder dos espiritos.{br}Tem o poder de restaurar HP de quem ele atinge.",
"A staff with a giant serpent scale embedded in its tip.":
"Um cetro com uma escama gigante de serpente incrustada na ponta.",
"This cypress staff increases the magick power{br}of its owner.{br}":
"Este cetro de cipreste aumenta o poder magico{br}de seu dono.{br}",
"A shiny staff decorated with gold.":
"Um cetro brilhante decorado com ouro.",
"A staff that increases the strength of its user.":
"Um cetro que aumenta a forca de quem o usa.",
"An ordinary wooden staff that one might find anywhere.":
"Um cetro de madeira comum que pode ser encontrado em qualquer lugar.",
"The head of this large mace is enveloped in flames.":
"A cabeca desta grande maca esta envolta em chamas.",
"A large morning star with a single spike attached to it.":
"Um grande mangual com um unico espigao preso a ele.",
"A firearm brought to Ivalice from the northern{br}country of Romanda.":
"Uma arma de fogo trazida a Ivalice do pais{br}nortenho de Romanda.",
"The barrel of this firearm has been fashioned from{br}mythril.":
"O cano desta arma de fogo foi feito{br}de mithril.",
"A firearm with the power to petrify.":
"Uma arma de fogo com o poder de petrificar.",
"A firearm that shoots freezing bullets.":
"Uma arma de fogo que dispara balas congelantes.",
"A firearm that shoots flaming bullets.":
"Uma arma de fogo que dispara balas flamejantes.",
"A firearm that shoots electrically charged bullets.":
"Uma arma de fogo que dispara balas eletrificadas.",
"A crossbow that can be fired with one hand.{br}Uses shorter bolts than a traditional crossbow.":
"Uma besta que pode ser disparada com uma mao.{br}Usa flechas mais curtas que uma besta tradicional.",
"This crossbow fires specially fashioned bolts that {br}contain a dose of blinding poison.":
"Esta besta dispara flechas feitas especialmente que {br}contem uma dose de veneno cegante.",
"The firing mechanism of this crossbow has been{br}improved upon, increasing its attack power.":
"O mecanismo de disparo desta besta foi{br}aprimorado, aumentando seu poder de ataque.",
"A crossbow that fires bolts dipped in poison.{br}Includes a mechanism for handling the poisoned bolts.":
"Uma besta que dispara flechas mergulhadas em veneno.{br}Inclui um mecanismo para manusear as flechas envenenadas.",
"A crossbow mainly employed for hunting monsters.":
"Uma besta usada principalmente para cacar monstros.",
"The most powerful crossbow ever created.{br}Its unusual size gives it a very strong recoil.":
"A besta mais poderosa ja criada.{br}Seu tamanho incomum lhe da um recuo muito forte.",
"The most common type of bow. It has a long range and is{br}quite durable.":
"O tipo mais comum de arco. Tem longo alcance e e{br}bastante resistente.",
"A bow adorned with silver decorations. Thin metal plates{br}help strengthen its wooden frame.":
"Um arco adornado com decoracoes de prata. Placas finas de metal{br}ajudam a reforcar sua estrutura de madeira.",
"A bow that shoots freezing arrows.":
"Um arco que dispara flechas congelantes.",
"This bow imbues arrows with the power and speed{br}of lightning.{br}":
"Este arco imbui as flechas com o poder e a velocidade{br}do raio.{br}",
"Arrows shot by this bow fly at extremely high speeds. The{br}vacuum created by their flight increases their damage.":
"Flechas disparadas por este arco voam a velocidades extremamente altas. O{br}vacuo criado por seu voo aumenta seu dano.",
"The bow of the goddess of the hunt.":
"O arco da deusa da caca.",
"The bow of a legendary archer. Its unusual size gives it{br}incredible power.":
"O arco de um arqueiro legendario. Seu tamanho incomum lhe da{br}um poder incrivel.",
"The bow of a mythical hero. It is constructed entirely{br}of metal and requires great strength to pull back.":
"O arco de um heroi mitico. E construido inteiramente{br}de metal e exige grande forca para ser puxado.",
"The strains of this harp can affect one's very soul.{br}Causes confusion in the listener.":
"As melodias desta harpa podem afetar a propria alma.{br}Causa confusao em quem a escuta.",
"A harp with a rich timbre and wide tonal range.":
"Uma harpa com timbre rico e amplo alcance tonal.",
"The pure sound of this harp can charm its user's enemies.":
"O som puro desta harpa pode encantar os inimigos de quem a usa.",
"A book made for battle.":
"Um livro feito para a batalha.",
"A light and inexpensive spear. Allows the wielder{br}to attack enemies within a range of two tiles.":
"Uma lanca leve e barata. Permite que quem a empunha{br}ataque inimigos num alcance de dois quadrados.",
"The most commonly used type of spear.{br}Distinguished by its especially long reach.":
"O tipo de lanca mais usado.{br}Destaca-se por seu alcance especialmente longo.",
"The tip of this spear is made from the valuable metal{br}known as mythril.":
"A ponta desta lanca e feita do valioso metal{br}conhecido como mithril.",
"A polearm tipped with a broad, double-edged blade.{br}Its design increases the damage it causes.":
"Uma lanca com uma lamina larga de dois fios na ponta.{br}Seu desenho aumenta o dano que causa.",
"A hefty spear fitted with an obelisk-shaped head.":
"Uma lanca pesada com uma ponta em forma de obelisco.",
"This sacred weapon shines a brilliant blue.":
"Esta arma sagrada brilha num azul resplandecente.",
"A spear made from a mysterious material that is neither{br}wood nor metal. Some say it is a dragon's whisker.":
"Uma lanca feita de um material misterioso que nao e{br}madeira nem metal. Dizem que e um bigode de dragao.",
"This spear has unmatched attack power.":
"Esta lanca tem um poder de ataque incomparavel.",
"A pole carved from the wood of a cypress.":
"Uma vara esculpida na madeira de um cipreste.",
"A thin and supple bamboo pole that bends lithely{br}when swung through the air.":
"Uma vara fina e flexivel de bambu que se dobra com agilidade{br}ao ser brandida no ar.",
"A pole crafted from wood that emits a musky scent.{br}It is in the shape of a large ladle.":
"Uma vara feita de madeira que emite um aroma amadeirado.{br}Tem a forma de uma grande concha.",
"The ribs of this enormous fan are made of iron.{br}When folded up, it may be employed as a pole in battle.":
"As varetas deste enorme leque sao feitas de ferro.{br}Quando dobrado, pode ser usado como uma vara na batalha.",
"One strike from this pole can cause the target to{br}lose his faith.{br}":
"Um golpe desta vara pode fazer o alvo{br}perder sua fe.{br}",
"A pole made from specially treated ivory. It is{br}surprisingly strong, despite its fragile appearance.":
"Uma vara feita de marfim tratado de forma especial. E{br}surpreendentemente resistente, apesar da aparencia fragil.",
"A shaft of boxwood, carved into a hexagonal shape{br}and reinforced with metal plates.{br}":
"Um cabo de buxo, esculpido em forma hexagonal{br}e reforcado com placas de metal.{br}",
"A pole made from a dark material that is neither wood {br}nor metal. Some say it is a dire whale's whisker.":
"Uma vara feita de um material sombrio que nao e madeira{br}nem metal. Dizem que e o bigode de uma temivel baleia.",
"A custom-made handbag designed for battle.":
"Uma bolsa feita sob encomenda para a batalha.",
"The design of this handbag is simple, yet fashionable.":
"O design desta bolsa e simples, porem elegante.",
"A handbag studded with scales from a hydra.":
"Uma bolsa cravejada com escamas de uma hidra.",
"This cloth is thick and brilliantly colored, making it perfect{br}for use in carpets.":
"Este tecido e grosso e com cores vibrantes, sendo perfeito{br}para uso em tapetes.",
"This warm and flexible woolen fabric is exquisitely soft to{br}the touch.":
"Este tecido de la quente e flexivel e requintadamente suave{br}ao toque.",
"A special process has been used to make this thin, smooth{br}silk exceptionally durable.":
"Um processo especial foi usado para tornar esta seda fina{br}e lisa excepcionalmente resistente.",
"The wielder of this sword bears the sins of his{br}previous lives, robbing him or her of all hope.{br}":
"Quem empunha esta espada carrega os pecados de suas{br}vidas passadas, perdendo toda esperanca.{br}",
"This sword brings death to all those who kill in the{br}name of truth and justice.{br}":
"Esta espada traz a morte a todos que matam em{br}nome da verdade e da justica.{br}",
"It is said that a witch bestowed this sword to a{br}knight who died an unnatural death.{br}":
"Dizem que uma bruxa deu esta espada a um{br}cavaleiro que morreu de forma antinatural.{br}",
"A sword said to have been wielded by a hero from{br}the north. A blue jewel is embedded in its broad handle.{br}":
"Uma espada que, segundo dizem, foi empunhada por um heroi{br}do norte. Uma joia azul esta incrustada em seu cabo largo.{br}",
"A tainted blade spoken of in legends about the end of{br}the world, said to feed upon the souls of its victims.{br}":
"Uma lamina corrompida mencionada em lendas sobre o fim{br}do mundo, dizem que se alimenta das almas de suas vitimas.{br}",
"A sword that glitters cruelly like a crescent moon.":
"Uma espada que reluz cruelmente como uma lua crescente.",
"A blade forged for swordsmen who have mastered every{br}technique and achieved knighthood's most exalted rank.":
"Uma lamina forjada para espadachins que dominaram todas{br}as tecnicas e alcancaram o posto mais exaltado da cavalaria.",
"A firearm named for Ras Algethi, the star that forms{br}the Kneeler's head.":
"Uma arma de fogo batizada em homenagem a Ras Algethi, a estrela que forma{br}a cabeca do Ajoelhado.",
"A firearm named for the brightest star in the Whale's{br}Maw.":
"Uma arma de fogo batizada em homenagem a estrela mais brilhante na{br}Boca da Baleia.",
"This axe's small size belies its incredible destructive power.":
"O pequeno tamanho deste machado esconde seu incrivel poder destrutivo.",
"An axe said to have been a gift from spirits inhabiting{br}a spring. Only the righteous may wield it.":
"Um machado que, segundo dizem, foi um presente de espiritos que habitam{br}uma fonte. Somente os justos podem empunha-lo.",
"A katana that strikes like a savage serpent.":
"Uma katana que golpeia como uma serpente selvagem.",
"The creator of this masterpiece learned the art of{br}swordcraft in a faraway land.":
"O criador desta obra-prima aprendeu a arte{br}da forja de espadas numa terra distante.",
"A staff that can only be mastered by the enlightened.":
"Um cetro que so pode ser dominado pelos iluminados.",
"A powerful staff said to give life to its owner's dreams.":
"Um cetro poderoso que, dizem, da vida aos sonhos de seu dono.",
"A rod tipped with a meteorite fragment.":
"Um cajado com a ponta de um fragmento de meteorito.",
"A magicked rod wielded by members of the royal guard.":
"Um cajado magico empunhado por membros da guarda real.",
"A weapon named after the evenstar.":
"Uma arma batizada em homenagem a estrela vespertina.",
"An enormous bow that fires meteor-like arrows.":
"Um arco enorme que dispara flechas como meteoros.",
"A spear said to have been wielded by a child of the{br}gods. Merely lifting it requires great strength.":
"Uma lanca que, segundo dizem, foi empunhada por um filho dos{br}deuses. So para levanta-la e preciso grande forca.",
"A spear with the power to pierce anything.":
"Uma lanca com o poder de perfurar qualquer coisa.",
}
apply(PATH, T, "entry38 items batch1 (132 descriptions)")
