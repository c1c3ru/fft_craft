import sys, json
sys.path.insert(0, "tools")
from phrase_translate import apply_phrases

PATH = "/home/c1c3ru/Downloads/finalfantasy/FFT_Android_Mod/translation/ptbr/entry38_sample.json"

T = {
"Chemist job command. Enables the{br}use of items to assist allies in need.":
    "Comando de classe do Quimico. Permite{br}o uso de itens para socorrer aliados necessitados.",
'Knight job command. Enables the use of "Rend"{br}skills that destroy equipment or reduce attributes.':
    'Comando de classe do Cavaleiro. Permite o uso de habilidades{br}"Rasgar" que destroem equipamento ou reduzem atributos.',
"Monk job command. Turns bare fists{br}into lethal weapons.":
    "Comando de classe do Monge. Transforma os punhos{br}nus em armas letais.",
"White mage job command. Enables the use{br}of healing and support magicks in battle.":
    "Comando de classe do Mago Branco. Permite o uso{br}de magias de cura e suporte em batalha.",
"Black mage job command. Enables{br}the use of attack magicks in battle.":
    "Comando de classe do Mago Negro. Permite{br}o uso de magias de ataque em batalha.",
"Time mage job command. Enables the use of{br}magicks that manipulate time and space.":
    "Comando de classe do Mago do Tempo. Permite o uso de{br}magias que manipulam tempo e espaco.",
"Summoner job command. Calls forth espers{br}from the highest realms of the spirit world.":
    "Comando de classe do Invocador. Convoca espers{br}dos reinos mais elevados do mundo espiritual.",
"Thief job command. Allows a unit to steal gil,{br}items, and even nonmaterial things.":
    "Comando de classe do Ladrao. Permite que uma unidade roube gil,{br}itens e ate coisas nao materiais.",
"Mystic job command. Manipulates the mystic{br}weave of the universe to inflict harm on enemies.":
    "Comando de classe do Mistico. Manipula a trama{br}mistica do universo para causar dano aos inimigos.",
"Geomancer job command. Attacks with mystical{br}powers drawn from the earth itself.":
    "Comando de classe do Geomante. Ataca com poderes{br}misticos extraidos da propria terra.",
"Dragoon job command. Jumps high into the{br}air, then dives downward into the opponent.":
    "Comando de classe do Dragao. Salta bem alto no{br}ar, depois mergulha sobre o oponente.",
"Samurai job command. Unleashes the mystical{br}powers contained within katana.":
    "Comando de classe do Samurai. Libera os poderes{br}misticos contidos na katana.",
"Ninja job command. Attack by throwing {br}weapons from the party inventory.":
    "Comando de classe do Ninja. Ataca arremessando {br}armas do inventario do grupo.",
"Arithmetician job command. Employs arithmetick{br}algorithms to pinpoint targets for magickal attacks.":
    "Comando de classe do Aritmetico. Usa algoritmos{br}aritmeticos para localizar alvos de ataques magicos.",
"Mime job command. Imitate an ally's actions,{br}limited to the abilities employed by normal units.":
    "Comando de classe do Mimico. Imita as acoes de um aliado,{br}limitado as habilidades usadas por unidades normais.",
"Holy knight job command. Smite the foe{br}with holy sword techniques.":
    "Comando de classe do Cavaleiro Sagrado. Abate o inimigo{br}com tecnicas de espada sagrada.",
"Ark knight job command. Slash{br}through the enemy's equipment.":
    "Comando de classe do Cavaleiro da Arca. Corta{br}o equipamento do inimigo.",
"Fell knight job command. Entreat the powers of{br}darkness to release energy through one's sword.":
    "Comando de classe do Cavaleiro Caido. Suplica aos poderes{br}das trevas para liberar energia atraves da espada.",
"White knight job command. Advanced sword{br}skills punish the foe with sacred techniques.":
    "Comando de classe do Cavaleiro Branco. Habilidades avancadas{br}de espada punem o inimigo com tecnicas sagradas.",
"Tietra's job command.{br}Taught by her elder brother, this magick is hers alone.":
    "Comando de classe de Tietra.{br}Ensinada por seu irmao mais velho, esta magia e so dela.",
"Princess job command. Utilizes magick{br}for recovery and protection.":
    "Comando de classe da Princesa. Usa magia{br}de recuperacao e protecao.",
"Machinist job command. Strike specific areas{br}of the target's body to cause status effects.":
    "Comando de classe do Engenheiro. Atinge areas especificas{br}do corpo do alvo para causar efeitos de status.",
"Soldier job command. Unmatched martial{br}skills made possible by fury pushed to its limit.":
    "Comando de classe do Soldado. Habilidades marciais{br}incomparaveis, possiveis gracas a furia levada ao limite.",
"Celebrant job command. Unleashes spirit forces{br}obtained through the darkest of contracts.":
    "Comando de classe do Celebrante. Libera forcas espirituais{br}obtidas atraves do mais sombrio dos pactos.",
"Dragonkin job command. Only usable by{br}those with dragonblood in their veins.":
    "Comando de classe do Draconato. Utilizavel apenas por{br}quem tem sangue de dragao nas veias.",
"Holy Dragon job command. Annihilate{br}foes with tremendous breath attacks.":
    "Comando de classe do Dragao Sagrado. Aniquila{br}inimigos com tremendos ataques de folego.",
"Skyseer job command. Attacks with a power{br}that does not rely upon faith.":
    "Comando de classe do Vidente Celeste. Ataca com um poder{br}que nao depende da fe.",
"Netherseer job command. Attacks with a power{br}that does not rely upon faith.":
    "Comando de classe do Vidente do Submundo. Ataca com um poder{br}que nao depende da fe.",
"Astrologer job command. Halts the{br}movement of the constellations.":
    "Comando de classe do Astrologo. Interrompe{br}o movimento das constelacoes.",
"Assassin job command. Employs{br}the sinister art of execution.":
    "Comando de classe do Assassino. Usa{br}a arte sinistra da execucao.",
"White knight job command. Advanced sword{br}skills smite the foe with sacred techniques.":
    "Comando de classe do Cavaleiro Branco. Habilidades avancadas{br}de espada abatem o inimigo com tecnicas sagradas.",
"Ark knight job command. Releases the{br}spirit contained within one's blade.":
    "Comando de classe do Cavaleiro da Arca. Libera o{br}espirito contido na lamina.",
"Divine knight job command. Pierces{br}through the enemy's equipment.":
    "Comando de classe do Cavaleiro Divino. Perfura{br}o equipamento do inimigo.",
"Sorcerer job command. Magicks scorch{br}foes with the power of light.":
    "Comando de classe do Feiticeiro. Magias queimam{br}inimigos com o poder da luz.",
"Ark knight job command. The demonic{br}act of supping living blood.":
    "Comando de classe do Cavaleiro da Arca. O ato{br}demoniaco de sorver sangue vivo.",
"Templar job command. Brings a magick{br}sword strike down upon the foe.":
    "Comando de classe do Templario. Desfere um golpe{br}de espada magica sobre o inimigo.",
"Nether shaman job command. Manipulates espers{br}to dominate the mortal world.":
    "Comando de classe do Xama do Submundo. Manipula espers{br}para dominar o mundo mortal.",
"Sword saint job command. Employs sword skills{br}with master strokes, striking down enemies.":
    "Comando de classe do Santo da Espada. Usa habilidades de espada{br}com golpes mestres, abatendo inimigos.",
"Cleric job command. Channels light from{br}the heavens into the mortal realm.":
    "Comando de classe do Clerigo. Canaliza a luz{br}dos ceus para o reino mortal.",
"Lucavi job command. This special technique{br}shatters the mind, causing status effects.":
    "Comando de classe do Lucavi. Esta tecnica especial{br}despedaca a mente, causando efeitos de status.",
"Bringer of Order job command. Warps{br}time and space to bring about catastrophe.":
    "Comando de classe do Portador da Ordem. Distorce{br}tempo e espaco para provocar catastrofe.",
"Lucavi job command. This special technique{br}shatters the mind, causing status effects and{br}inflicting psychological damage.":
    "Comando de classe do Lucavi. Esta tecnica especial{br}despedaca a mente, causando efeitos de status e{br}infligindo dano psicologico.",
"Job command of the Impure. Entwines its victim{br}in repellent filth and gnaws away at its flesh.":
    "Comando de classe do Impuro. Envolve sua vitima{br}em imundicie repelente e corroi sua carne.",
"Job command of the Wroth. Mighty magick{br}beyond the comprehension of mere mortals.":
    "Comando de classe do Irado. Magia poderosa{br}alem da compreensao de meros mortais.",
"High Seraph job command. Magick{br}that unleashes absolute power.":
    "Comando de classe do Alto Serafim. Magia{br}que libera poder absoluto.",
"High Seraph job command. A stream of chaos{br}engulfs its victim, causing various status effects.":
    "Comando de classe do Alto Serafim. Um fluxo de caos{br}envolve sua vitima, causando varios efeitos de status.",
"Arch Seraph Job command. Magick that{br}consumes its victim with a wave of absolute{br}power.":
    "Comando de classe do Arquiserafim. Magia que{br}consome sua vitima com uma onda de poder{br}absoluto.",
"Arch Seraph job command. All those embraced{br}by this magick are banished to the netherworld.":
    "Comando de classe do Arquiserafim. Todos os abracados{br}por esta magia sao banidos para o submundo.",
'Knight job command. Enables "Rend" skills{br}that destroy equipment or weaken attributes.':
    'Comando de classe do Cavaleiro. Permite habilidades "Rasgar"{br}que destroem equipamento ou reduzem atributos.',
"Archer job command. Heightens concentration{br}to gather strength and unleash more powerful attacks.":
    "Comando de classe do Arqueiro. Aumenta a concentracao{br}para reunir forca e desferir ataques mais poderosos.",
"Time mage job command. Employs magick{br}to manipulate time and space.":
    "Comando de classe do Mago do Tempo. Usa magia{br}para manipular tempo e espaco.",
"Mystic job command. Employs magick to{br}manipulate the mystic weave of the universe.":
    "Comando de classe do Mistico. Usa magia para{br}manipular a trama mistica do universo.",
"Byblos job command. Magick with the{br}power to control arcane energy.":
    "Comando de classe do Byblos. Magia com o{br}poder de controlar energia arcana.",
"Automaton job command. A series of work{br}commands for performing heavy physical labor.":
    "Comando de classe do Automato. Uma serie de comandos de trabalho{br}para realizar labor fisico pesado.",
"Reaver job command. Enables magick using{br}malicious spirits to attack its victim.":
    "Comando de classe do Devastador. Permite magia usando{br}espiritos maliciosos para atacar sua vitima.",
"Serpentarius job command. Mighty magick{br}beyond the comprehension of mere mortals.":
    "Comando de classe do Serpentario. Magia poderosa{br}alem da compreensao de meros mortais.",
"Archaeodaemon job command. Great magick{br}steeped in the powers of darkness.":
    "Comando de classe do Arquidemonio. Grande magia{br}imersa nos poderes das trevas.",
"Ultima demon job command. Brings forth{br}magickal powers from the dark realm.":
    "Comando de classe do Demonio Ultima. Invoca{br}poderes magicos do reino sombrio.",
"Dark knight job command. Cursed sword{br}techniques cut down the foe.":
    "Comando de classe do Cavaleiro Negro. Tecnicas de espada{br}amaldicoada abatem o inimigo.",
"Sky pirate job command. Unsurpassed in{br}gunplay and thievery. No prey goes uncaught,{br}no target unscathed.":
    "Comando de classe do Pirata do Ceu. Incomparavel com{br}armas de fogo e roubo. Nenhuma presa escapa,{br}nenhum alvo sai ileso.",
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
