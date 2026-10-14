import sys
sys.path.insert(0, "tools")
from translate_batch import apply

PATH = "/home/c1c3ru/Downloads/finalfantasy/FFT_Android_Mod/translation/ptbr/entry38_sample.json"

T = {
"This job serves as the foundation for all others, forming{br}the first step on the road to becoming a mighty warrior.{br}This modified version of the squire job does not allow axe{br}use, but does permit robes.":
"Esta classe serve como base para todas as outras, formando{br}o primeiro passo no caminho para se tornar um guerreiro{br}poderoso. Esta versao modificada da classe Soldado nao permite{br}o uso de machados, mas permite vestes.",

"This job serves as the foundation for all others, forming{br}the first step on the road to becoming a mighty warrior.{br}This modified version of the squire job does not allow{br}axe use, but does permit robes, shields, helms, and armor.":
"Esta classe serve como base para todas as outras, formando{br}o primeiro passo no caminho para se tornar um guerreiro{br}poderoso. Esta versao modificada da classe Soldado nao permite{br}o uso de machados, mas permite vestes, escudos, elmos e armaduras.",

"This job serves as the foundation for all others, forming{br}the first step on the road to becoming a mighty warrior.{br}{br}{br}This modified version of the squire job does not allow{br}axe use, but does permit robes, shields, helms, armor,{br}and knight's swords.":
"Esta classe serve como base para todas as outras, formando{br}o primeiro passo no caminho para se tornar um guerreiro{br}poderoso.{br}{br}{br}Esta versao modificada da classe Soldado nao permite{br}o uso de machados, mas permite vestes, escudos, elmos, armaduras{br}e espadas de cavaleiro.",

"Baptized in the divine light of the Church, the holy knight{br}smites foes with powerful Holy Sword techniques.":
"Batizado na luz divina da Igreja, o cavaleiro sagrado{br}abate inimigos com poderosas tecnicas de Espada Sagrada.",

"A warrior sworn to the service of the gods, rending{br}enemies and their items with its Unyielding Blade.":
"Um guerreiro a servico dos deuses, que despedaca{br}inimigos e seus itens com sua Lamina Inflexivel.",

"This job serves as the foundation for all others, forming{br}the first step on the road to becoming a mighty warrior.":
"Esta classe serve como base para todas as outras, formando{br}o primeiro passo no caminho para se tornar um guerreiro poderoso.",

"A warrior sworn to the service of the gods, using{br}its Blade of Ruin to rend both body and soul.":
"Um guerreiro a servico dos deuses, que usa{br}sua Lamina da Ruina para despedacar corpo e alma.",

"An elite knight who wears armor inscribed with{br}magick runes of ancient and mysterious power.":
"Um cavaleiro de elite que veste uma armadura gravada{br}com runas magicas de poder antigo e misterioso.",

"A leader in command of several hundred knights,{br}holding a title high even among the aristocracy.":
"Um lider que comanda centenas de cavaleiros,{br}detentor de um titulo elevado mesmo entre a aristocracia.",

"Daughter to the king and an heir in line for the throne.{br}She is the epitome of elegance and grace.":
"Filha do rei e herdeira do trono.{br}Ela e o epitome da elegancia e da graca.",

"A peerless warrior who commands an entire knightly{br}order. It is said that none can match his swordplay.":
"Um guerreiro sem igual que comanda uma ordem{br}de cavalaria inteira. Dizem que ninguem rivaliza com sua espada.",

"A priest and prophet with ultimate power over the Church.{br}A word from him can sway the fate entire nations.":
"Um sacerdote e profeta com poder absoluto sobre a Igreja.{br}Uma palavra dele pode decidir o destino de nacoes inteiras.",

"Human in appearance, but descended of dragons.{br}The blood of the Holy Dragon flows in her veins.":
"De aparencia humana, mas descendente de dragoes.{br}O sangue do Dragao Sagrado corre em suas veias.",

"A powerful celebrant selected from scores of his peers.{br}He will stop at nothing to hunt down and eliminate heretics.":
"Um poderoso celebrante escolhido entre inumeros pares.{br}Ele nao para por nada ao cacar e eliminar hereges.",

"A fallen knight who has turned his back on the light of the{br}gods. He leeches the souls of enemies with his Fell Sword.":
"Um cavaleiro caido que deu as costas a luz dos{br}deuses. Ele drena as almas dos inimigos com sua Espada Sinistra.",

"An assassin able to corrupt the laws of nature by{br}speaking the words of forbidden Nether Mantra.":
"Um assassino capaz de corromper as leis da natureza{br}ao proferir as palavras do proibido Mantra do Submundo.",

"An elder of the Church who never rests in his mission to{br}spread the teachings of the gods to the common people.":
"Um anciao da Igreja que nunca descansa em sua missao de{br}difundir os ensinamentos dos deuses ao povo comum.",

"A true believer in the divine power of the gods,{br}using Holy Magicks to protect loved ones.":
"Um verdadeiro crente no poder divino dos deuses,{br}que usa Magias Sagradas para proteger quem ama.",

"A learned augur who uses Astrology to manipulate{br}fate and sway the course of battle.":
"Um sabio agoureiro que usa Astrologia para manipular{br}o destino e influenciar o curso da batalha.",

"An engineer working to revive lost technologies, capable{br}of firing guns highly accurately with the Aimed Shot ability.":
"Um engenheiro que trabalha para reviver tecnologias perdidas,{br}capaz de disparar armas com grande precisao usando Tiro Certeiro.",

"The cardinal's power in the Church is second only{br}to that of the High Confessor himself.":
"O poder do cardeal na Igreja so e superado{br}pelo do proprio Alto Confessor.",

"An assassin able to bend the laws of nature by{br}speaking the words of forbidden Sky Mantra.":
"Um assassino capaz de dobrar as leis da natureza{br}ao proferir as palavras do proibido Mantra Celeste.",

"A warrior sworn to the service of the gods, using the{br}Sword Spirit ability to release a wave of spiritual power.":
"Um guerreiro a servico dos deuses, que usa a{br}habilidade Espirito da Espada para liberar uma onda de poder espiritual.",

"Sister to Delita Heiral. She and her brother have relied{br}upon one another since losing their parents long ago.":
"Irma de Delita Heiral. Ela e o irmao contam um com{br}o outro desde que perderam os pais, ha muito tempo.",

"A high-ranking Ivalician leader, the grand duke{br}wields power equivalent to that of lesser kings.":
"Um lider ivalicio de alta hierarquia, o grao-duque{br}detem um poder equivalente ao de reis menores.",

"A devout knight who defends the Church from heretics.{br}Uses Spellblade techniques to strike down the enemy.":
"Um cavaleiro devoto que defende a Igreja dos hereges.{br}Usa tecnicas de Espada Arcana para abater o inimigo.",

"A pious knight clad in pure white armor. His untarnished{br}soul enables him to wield a Holy Sword to smite enemies.":
"Um cavaleiro piedoso vestido com armadura branca pura. Sua alma{br}imaculada lhe permite empunhar uma Espada Sagrada contra inimigos.",

"A witch who has made a pact with the Dark,{br}placing its powers in her thrall.":
"Uma bruxa que fez um pacto com as Trevas,{br}colocando seus poderes sob seu dominio.",

"A title of nobility, ranking fourth in the five ranks{br}of peerage, above baron and below count.":
"Um titulo de nobreza, quarto entre os cinco postos{br}da aristocracia, acima de barao e abaixo de conde.",

"A knight versed in both scripture and sword,{br}sworn to the service of the gods.":
"Um cavaleiro versado tanto nas escrituras quanto na espada,{br}a servico dos deuses.",

"A fearsome warrior steeped in the dark power to which he{br}is bound. He cleaves enemies with a ghastly glowing blade.":
"Um guerreiro temivel imerso no poder sombrio ao qual{br}esta ligado. Ele retalha inimigos com uma lamina sinistra e brilhante.",

"A magick user with countless incantations at his command.{br}His powerful spells make all those who oppose him suffer.":
"Um usuario de magia com inumeras invocacoes a seu comando.{br}Seus poderosos feiticos fazem sofrer todos que o enfrentam.",

"A diabolical killer trained by an order of assassins{br}to quickly dispatch enemies with Subdual Arts.":
"Um assassino diabolico treinado por uma ordem de assassinos{br}para eliminar inimigos rapidamente com Artes de Submissao.",

"A prophet who, misleading the people with falsehoods,{br}has come to attain undeniable power.":
"Um profeta que, enganando o povo com mentiras,{br}alcancou um poder inegavel.",

"A mysterious otherworldly traveler capable of formidable{br}Limit techniques when his rage reaches a breaking point.":
"Um misterioso viajante de outro mundo, capaz de tecnicas{br}formidaveis de Limite quando sua ira atinge o limite.",

"This twisted monster was born of auracite's power.{br}Its attacks wound its enemies in both body and soul.":
"Este monstro retorcido nasceu do poder da auracita.{br}Seus ataques ferem os inimigos no corpo e na alma.",

"A foul knight called forth from the netherworld.":
"Um cavaleiro corrompido invocado do submundo.",

"Servant to a power beyond earthly comprehension.{br}Uses Dread to lull targets into eternal repose.":
"Servo de um poder alem da compreensao terrena.{br}Usa Pavor para levar seus alvos ao repouso eterno.",

"A foul archer called forth from the netherworld.":
"Um arqueiro corrompido invocado do submundo.",

"A being capable of controlling the very laws of nature,{br}and thus ruling all living things far and wide.":
"Um ser capaz de controlar as proprias leis da natureza,{br}governando assim todos os seres vivos por toda parte.",

"A being that has been set free from the laws that govern{br}creation, surpassing pedestrian concepts of morality.":
"Um ser que foi liberto das leis que regem{br}a criacao, superando conceitos triviais de moralidade.",

"A foul black mage called forth from the netherworld.":
"Um mago negro corrompido invocado do submundo.",

"A being that finds ecstasy in all things foul and unclean.{br}Few mortals can maintain their sanity in his presence.":
"Um ser que encontra extase em tudo que e corrompido e impuro.{br}Poucos mortais conseguem manter a sanidade em sua presenca.",

"A foul time mage called forth from the netherworld.":
"Um mago do tempo corrompido invocado do submundo.",

"A ruler from another plane who reigns with an iron fist.{br}He wields boundless magick power with ease.":
"Um governante de outro plano que reina com mao de ferro.{br}Ele empunha um poder magico ilimitado com facilidade.",

"A foul mystic called forth from the netherworld.":
"Um mistico corrompido invocado do submundo.",

"A foul summoner called forth from the netherworld.":
"Um invocador corrompido invocado do submundo.",

"A dragonkin, transformed into this divine dragon that{br}strikes with its colossal body and varied breath attacks.":
"Um draconato, transformado neste dragao divino que{br}ataca com seu corpo colossal e variados ataques de folego.",

"The High Seraph's ultimate form. Creator, destroyer,{br}and master of both tranquility and chaos.":
"A forma suprema do Alto Serafim. Criador, destruidor{br}e senhor tanto da tranquilidade quanto do caos.",

"An expert in the use of items to recover HP or remove{br}vexing status ailments.{br}{font:08}Ability: {font:00}Throw Items":
"Um especialista no uso de itens para recuperar HP ou remover{br}status negativos incomodos.{br}{font:08}Habilidade: {font:00}Arremessar Itens",

"A brave and chivalrous warrior of unmatched skill.{br}Uses a knight's sword to unleash the Arts of War.":
"Um guerreiro bravo e cavalheiresco de habilidade incomparavel.{br}Usa uma espada de cavaleiro para liberar as Artes da Guerra.",

"Equipped with a bow and arrow, this warrior provides{br}valuable long-range attacks. May Aim for higher damage.":
"Equipado com arco e flecha, este guerreiro oferece{br}valiosos ataques a longa distancia. Pode usar Pontaria para mais dano.",

"A warrior, devoted to physical training, whose unarmed{br}attacks are deadly. May use Martial Arts.{br}{font:08}Ability: {font:00}Brawler":
"Um guerreiro dedicado ao treinamento fisico, cujos ataques{br}desarmados sao letais. Pode usar Artes Marciais.{br}{font:08}Habilidade: {font:00}Brigao",

"A warrior who taps into the powers of the divine, using{br}White Magicks to cast spells of recovery and protection.":
"Um guerreiro que acessa os poderes do divino, usando{br}Magias Brancas para lancar feiticos de recuperacao e protecao.",
}

apply(PATH, T, "entry38 batch2")
