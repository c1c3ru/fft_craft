import sys, json
sys.path.insert(0, "tools")
from phrase_translate import apply_phrases

PATH = "/home/c1c3ru/Downloads/finalfantasy/FFT_Android_Mod/translation/ptbr/entry38_sample.json"

T = {
"Attack by throwing shuriken from inventory.": "Ataque arremessando shuriken do inventario.",
"Attack by throwing knives from inventory.": "Ataque arremessando facas do inventario.",
"Attack by throwing swords from inventory.": "Ataque arremessando espadas do inventario.",
"Attack by throwing flails from inventory.": "Ataque arremessando mangueis do inventario.",
"Attack by throwing katana from inventory.": "Ataque arremessando katanas do inventario.",
"Attack by throwing ninja blades from inventory.": "Ataque arremessando laminas ninja do inventario.",
"Attack by throwing axes from inventory.": "Ataque arremessando machados do inventario.",
"Attack by throwing polearms from inventory.": "Ataque arremessando lancas do inventario.",
"Attack by throwing poles from inventory.": "Ataque arremessando varas do inventario.",
"Attack by throwing knight's swords from inventory.": "Ataque arremessando espadas de cavaleiro do inventario.",
"Attack by throwing books from inventory.": "Ataque arremessando livros do inventario.",
"Attack by throwing bombs from inventory.": "Ataque arremessando bombas do inventario.",

"A perfume with a soothing scent.": "Um perfume com um aroma calmante.",
"A perfume with a refreshing fragrance.": "Um perfume com uma fragrancia refrescante.",
"A perfume with a rich redolence.": "Um perfume com um aroma rico.",

"Absorb HP from the target.": "Absorve HP do alvo.",
"Absorb MP from the target.": "Absorve MP do alvo.",
"Inflict damage with a sinister sword.": "Causa dano com uma espada sinistra.",
"Sacrifice own HP to deal damage to others, with{br}the nearest units suffering the most damage.":
    "Sacrifica o proprio HP para causar dano aos outros, com{br}as unidades mais proximas sofrendo mais dano.",
"Attack by pecking with enormous beak.": "Ataca bicando com um bico enorme.",
"Purge status effects with a cleansing flap of the wings.": "Purga efeitos de status com um bater de alas purificador.",
"Invigorate the life force and restore HP{br}with a flap of the wings.":
    "Revigora a forca vital e restaura HP{br}com um bater de alas.",
"Attack with a rushing body blow.": "Ataca com um golpe de corpo em disparada.",
"Attack with a thorough beating.": "Ataca com uma surra completa.",
"Attack the eyes, robbing the target of sight.": "Ataca os olhos, roubando a visao do alvo.",
"Bite the target to suck their blood and absorb their HP.": "Morde o alvo para sugar seu sangue e absorver seu HP.",
"Attack by biting with an enormous mouth.": "Ataca mordendo com uma boca enorme.",
"Self-destruct, inflicting damage in the surrounding area.": "Autodestroi-se, causando dano na area ao redor.",
"Attack the area with spreading flames.": "Ataca a area com chamas que se espalham.",
"Attack with keen-edged claws.": "Ataca com garras afiadas.",
"Attack with a powerful kick.": "Ataca com um chute poderoso.",
"Poison the target by injecting venom.": "Envenena o alvo injetando veneno.",
"Feast on the target's blood to restore HP.": "Banqueteia-se com o sangue do alvo para restaurar HP.",
"Attack with long, thin, whip-like tentacles.": "Ataca com tentaculos longos, finos, como chicotes.",
"Rob the target of sight by belching black ink.": "Rouba a visao do alvo arrotando tinta negra.",
"Disrupt the psyche, destroying the rational mind.": "Perturba a psique, destruindo a mente racional.",
"Abscond with a fragment of the soul, lowering the{br}target's level by 1.":
    "Rouba um fragmento da alma, reduzindo o{br}nivel do alvo em 1.",
"Strike the target with a bony-handed chop.": "Golpeia o alvo com um corte de mao ossuda.",
"Attack by striking with a mass of arcane power.": "Ataca golpeando com uma massa de poder arcano.",
"Corrupt the target's flesh, turning it undead.": "Corrompe a carne do alvo, tornando-o morto-vivo.",
"Put the target in a deep sleep with a touch.": "Coloca o alvo num sono profundo com um toque.",
"Drain HP from the target with a foul touch.": "Drena HP do alvo com um toque impuro.",
"Coat the target in oil with a greasy touch.": "Cobre o alvo de oleo com um toque gorduroso.",
"Attack with a mighty wing-flap.": "Ataca com um poderoso bater de alas.",
"Inflict status effects with the{br}overwhelming gaze of a massive eye.":
    "Causa efeitos de status com o{br}olhar avassalador de um olho gigantesco.",
"Dishearten the target, reducing Bravery{br}with the overwhelming gaze of a massive eye.":
    "Desanima o alvo, reduzindo a Coragem{br}com o olhar avassalador de um olho gigantesco.",
"Dissolve magick skills, reducing magick attack power{br}with the overwhelming gaze of a massive eye.":
    "Dissolve habilidades magicas, reduzindo o poder de ataque magico{br}com o olhar avassalador de um olho gigantesco.",
"Gaze into the aether to find and cut short{br}the target's silvery thread of life.":
    "Observa o eter para encontrar e cortar{br}o fio de vida prateado do alvo.",
"Attack by tearing with talons while in midair.": "Ataca rasgando com garras enquanto voa.",
"Attack vital spots with a long beak, petrifying the target.": "Ataca pontos vitais com um bico longo, petrificando o alvo.",
"Attack by dropping an explosive feather on the target.": "Ataca soltando uma pena explosiva sobre o alvo.",
"Employ a special skill that reduces physical attack power.": "Usa uma habilidade especial que reduz o poder de ataque fisico.",
"Run at the target at full tilt, crashing into them.": "Corre em direcao ao alvo a toda velocidade, colidindo com ele.",
"Mesmerize the target with a ferocious snort.": "Hipnotiza o alvo com um bufo feroz.",
"Use a fierce cry to summon KO'd units from the{br}brink of death and restore their HP.":
    "Usa um grito feroz para chamar unidades derrotadas{br}de volta da beira da morte e restaurar seu HP.",
"Inflict status effects with an eye-watering miasma.": "Causa efeitos de status com um miasma de lacrimejar os olhos.",
"The ultimate act of porcine altruism.": "O ato supremo de altruismo porcino.",
"Employ the life force of leaves to increase{br}resistance to physical attacks.":
    "Usa a forca vital das folhas para aumentar{br}a resistencia a ataques fisicos.",
"Employ the life force of leaves to increase{br}resistance to magickal attacks.":
    "Usa a forca vital das folhas para aumentar{br}a resistencia a ataques magicos.",
"Employ the life force of leaves to restore HP.": "Usa a forca vital das folhas para restaurar HP.",
"Employ the life force of leaves to restore MP.": "Usa a forca vital das folhas para restaurar MP.",
"Attack with a mighty pickaxe blow.": "Ataca com um poderoso golpe de picareta.",
"Attack with a fearsome spin of the pickaxe.": "Ataca com um giro temivel da picareta.",
"Attack by stamping the earth, dispatching a{br}shockwave throughout the vicinity.":
    "Ataca batendo o pe na terra, disparando uma{br}onda de choque pelas proximidades.",
"Increase physical attack power by stamping{br}the earth and absorbing its life force.":
    "Aumenta o poder de ataque fisico batendo o pe{br}na terra e absorvendo sua forca vital.",
"Expel a combustible liquid produced in the body{br}and set it alight, attacking with flaming breath.":
    "Expele um liquido combustivel produzido no corpo{br}e o incendeia, atacando com folego flamejante.",
"Belch forth sticky secretions from deep within{br}to gum up the target and prevent movement.":
    "Arrota secrecoes pegajosas de dentro{br}para prender o alvo e impedir seu movimento.",
"Coat the target in malboro spores,{br}turning it a malboro.":
    "Cobre o alvo com esporos de malboro,{br}transformando-o num malboro.",
"Attack with piercing horns.": "Ataca com chifres perfurantes.",
"Attack by goring and tossing the target.": "Ataca chifrando e arremessando o alvo.",
"Call forth a tornado to damage the surrounding area.": "Invoca um tornado para causar dano na area ao redor.",
"Inflict damage by bringing about a space-time warp{br}set in place by stars twinkling in the firmament.":
    "Causa dano provocando uma distorcao espaco-temporal{br}criada por estrelas cintilantes no firmamento.",
"Inflict damage with a body blow.": "Causa dano com um golpe de corpo.",
"Attack with breath of ice.": "Ataca com folego de gelo.",
"Attack with breath of flame.": "Ataca com folego de fogo.",
"Attack with breath of lightning.": "Ataca com folego de raio.",
"Each of three heads attacks with insidious breath.": "Cada uma das tres cabecas ataca com folego insidioso.",
"Each of three heads attacks with lightning.": "Cada uma das tres cabecas ataca com raio.",
"Each of three heads attacks with flame.": "Cada uma das tres cabecas ataca com fogo.",
"Each of three heads attacks with darkness.": "Cada uma das tres cabecas ataca com trevas.",
"Attack with a monstrous serpent.": "Ataca com uma serpente monstruosa.",
"Turn the target into a toad with a serpent's gaze.": "Transforma o alvo em sapo com o olhar de uma serpente.",
"Attack with a wave of lost life force.{br}The lower the user's HP, the greater damage inflicted.":
    "Ataca com uma onda de forca vital perdida.{br}Quanto menor o HP de quem usa, maior o dano causado.",
"Cleave the very building blocks of matter apart,{br}attacking with the resulting energy burst.":
    "Separa os proprios blocos fundamentais da materia,{br}atacando com a explosao de energia resultante.",
"Inflict various status effects with the{br}interwoven form of earth in nothingness.":
    "Causa varios efeitos de status com a{br}forma entrelacada da terra no nada.",
"A top-level operation command. Destroy the target.": "Um comando de operacao de alto nivel. Destroi o alvo.",
"A top-level operation command. Compress the target.": "Um comando de operacao de alto nivel. Comprime o alvo.",
"A special operation command. Pulverize the target.": "Um comando de operacao especial. Pulveriza o alvo.",
"Restore twice the amount of the user's HP.": "Restaura o dobro da quantidade de HP de quem usa.",
"Unleash 4 attacks with the emphasis on speed.{br}Each strike inflicts half the usual damage.":
    "Desfere 4 ataques com enfase na velocidade.{br}Cada golpe causa metade do dano usual.",
"Pilfer gil from the target.": "Rouba gil do alvo.",
"Capture the target's heart, enthralling them.": "Captura o coracao do alvo, enfeiticando-o.",
"Purloin the target's equipped helmet.": "Rouba o elmo equipado do alvo.",
"Purloin the target's equipped armor.": "Rouba a armadura equipada do alvo.",
"Purloin the target's equipped shield.": "Rouba o escudo equipado do alvo.",
"Purloin the target's equipped weapon.": "Rouba a arma equipada do alvo.",
"Purloin the target's equipped accessory.": "Rouba o acessorio equipado do alvo.",
"Filch experience points from the target.": "Rouba pontos de experiencia do alvo.",
"Attack either with weapons or without. ": "Ataca com ou sem armas. ",
"Use a potion to restore HP or inflict damage{br}on the undead.":
    "Usa uma pocao para restaurar HP ou causar dano{br}em mortos-vivos.",
"Use an elixir to fully restore HP and MP.": "Usa um elixir para restaurar totalmente HP e MP.",
"Use eye drops when vision has been magickally{br}compromised.":
    "Usa colirio quando a visao foi comprometida{br}por magia.",
"Use a maiden's kiss to change a unit that has been{br}transformed into a toad back to its original form.":
    "Usa um beijo de donzela para devolver a forma original{br}de uma unidade transformada em sapo.",
"Use holy water to lift the curse{br}of undeath from a unit.":
    "Usa agua sagrada para remover a maldicao{br}da morte-vivo de uma unidade.",
"Carefully aim to strike for increased damage.{br}Attack power increases with longer charge time.":
    "Visa com cuidado para golpear com mais dano.{br}O poder de ataque aumenta com mais tempo de carga.",
"Base arithmetick algorithm on the target's CT.": "Baseia o algoritmo aritmetico no CT do alvo.",
"Base arithmetick algorithm on the target's level.": "Baseia o algoritmo aritmetico no nivel do alvo.",
"Base arithmetick algorithm on the target's EXP.": "Baseia o algoritmo aritmetico no EXP do alvo.",
"Base arithmetick algorithm on the height of the {br}target's current tile.":
    "Baseia o algoritmo aritmetico na altura do{br}quadrado atual do alvo.",
"An algorithm for targeting units whose specified{br}attribute is a prime number. A prime number is{br}a number only divisible by 1 and itself. A list ":
    "Um algoritmo para unidades cujo atributo{br}especificado seja um numero primo. Um numero primo e{br}um numero divisivel apenas por 1 e por ele mesmo. Uma lista ",
"An algorithm for targeting units whose{br}specified attribute is a multiple of 5.":
    "Um algoritmo para unidades cujo{br}atributo especificado seja multiplo de 5.",
"An algorithm for targeting units whose{br}specified attribute is a multiple of 4.":
    "Um algoritmo para unidades cujo{br}atributo especificado seja multiplo de 4.",
"An algorithm for targeting units whose{br}specified attribute is a multiple of 3.":
    "Um algoritmo para unidades cujo{br}atributo especificado seja multiplo de 3.",
"Recover from KO status.": "Recupera-se do status KO.",
"Receive the blessing of HP regeneration.": "Recebe a bencao de regeneracao de HP.",
"Recover HP when critically wounded.": "Recupera HP quando gravemente ferido.",
"Recover MP when critically wounded.": "Recupera MP quando gravemente ferido.",
"Receive an immediate turn{br}when critically wounded.": "Recebe um turno imediato{br}quando gravemente ferido.",
"Deal damage equal to own maximum HP{br}when critically wounded.":
    "Causa dano igual ao proprio HP maximo{br}quando gravemente ferido.",
"Counterattack using the same magick with which{br}the user was attacked.":
    "Contra-ataca usando a mesma magia com a qual{br}o usuario foi atacado.",
"Counterattack with a tackle.": "Contra-ataca com um ataque corporal.",
"Counterattack with a geomancy skill.": "Contra-ataca com uma habilidade de geomancia.",
"Recover MP equal to the amount used by the opponent.": "Recupera MP igual a quantidade usada pelo oponente.",
"Receive gil equal to the amount of damage taken.": "Recebe gil igual a quantidade de dano recebido.",
"Counterattack with a physical strike.": "Contra-ataca com um golpe fisico.",
"When HP is restored, distribute any{br}excess among one's allies.":
    "Quando o HP e restaurado, distribui o{br}excesso entre os aliados.",
"Split any damage taken with the{br}opponent who inflicted it.":
    "Divide qualquer dano recebido com{br}o oponente que o causou.",
"Block physical attacks with the equipped weapon.": "Bloqueia ataques fisicos com a arma equipada.",
"Avoid the effects of Speechcraft.": "Evita os efeitos da Oratoria.",
"Block attacks with greater ease.": "Bloqueia ataques com mais facilidade.",
"Catch thrown items and add them to the party inventory.": "Captura itens arremessados e os adiciona ao inventario do grupo.",
"Evade non-ranged physical attacks.": "Evita ataques fisicos que nao sejam a distancia.",
"Dodge arrow and bolt attacks.": "Esquiva de ataques de flecha e besta.",
"Equip helms and armor, regardless of job.": "Equipa elmos e armaduras, independente da classe.",
"Reduce MP consumption by half when using magicks.": "Reduz pela metade o consumo de MP ao usar magias.",
"Increase the amount of JP earned in battle.": "Aumenta a quantidade de JP ganho em batalha.",
"Earn more EXP for the same actions.": "Ganha mais EXP pelas mesmas acoes.",
"Inflict greater damage with physical attacks.": "Causa mais dano com ataques fisicos.",
"Take less damage from physical attacks.": "Recebe menos dano de ataques fisicos.",
"Inflict greater damage with magickal attacks.": "Causa mais dano com ataques magicos.",
"Take less damage from magickal attacks.": "Recebe menos dano de ataques magicos.",
"Make attacks unblockable. If an enemy is{br}in the targeted tile, it will always be hit.":
    "Torna os ataques imbloqueaveis. Se um inimigo estiver{br}no quadrado alvo, sempre sera atingido.",
"Gain the ability to use Speechcraft against{br}monsters, even if not an orator.":
    "Ganha a capacidade de usar Oratoria contra{br}monstros, mesmo sem ser orador.",
"Prevent equipment from being destroyed or stolen.": "Impede que o equipamento seja destruido ou roubado.",
"Wield a weapon with both hands, increasing{br}its destructive power.":
    "Empunha uma arma com as duas maos, aumentando{br}seu poder destrutivo.",
"Add an ability to all monsters in neighboring tiles{br}with an elevation difference of 3h or less.":
    "Adiciona uma habilidade a todos os monstros em quadrados vizinhos{br}com diferenca de elevacao de 3h ou menos.",
"Defend oneself against an attack.{br}Adds the Defend command.":
    "Defende-se de um ataque.{br}Adiciona o comando Defender.",
"Change equipment mid-battle.{br}Adds the Reequip command.":
    "Troca de equipamento no meio da batalha.{br}Adiciona o comando Reequipar.",
"Increase attack power by 50 percent and{br}decrease defensive power by 50 percent.":
    "Aumenta o poder de ataque em 50 por cento e{br}reduz o poder defensivo em 50 por cento.",
"Warp instantly to destination tiles. May fail when{br}attempting to travel to distant locations.":
    "Teletransporta instantaneamente para quadrados de destino. Pode falhar ao{br}tentar viajar para locais distantes.",
}

data = json.load(open(PATH, encoding="utf-8"))
strings = data["strings"]
changed = 0
for i, (s, t) in enumerate(strings):
    new_s = apply_phrases(s, T)
    if new_s != s:
        strings[i] = [new_s, t]
        changed += 1
with open(PATH, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=0)
print("changed:", changed)
