import sys
sys.path.insert(0, "tools")
from translate_batch import apply
PATH = "/home/c1c3ru/Downloads/finalfantasy/FFT_Android_Mod/translation/ptbr/entry38_sample.json"

T = {
"A warrior who uses Black Magicks to channel{br}elemental powers into powerful offensive spells. ":
"Um guerreiro que usa Magias Negras para canalizar{br}poderes elementais em feiticos ofensivos poderosos. ",
"A warrior who uses Time Magicks to control space and{br}time, toying with laws created by the gods themselves.":
"Um guerreiro que usa Magias do Tempo para controlar o espaco{br}e o tempo, brincando com leis criadas pelos proprios deuses.",
"A warrior who may Summon the most powerful of{br}spirits, the beings known as espers.":
"Um guerreiro que pode Invocar os mais poderosos{br}espiritos, seres conhecidos como espers.",
"A warrior whose nimble fingers allow him or her to Steal{br}from nearly anyone.":
"Um guerreiro cujos dedos ageis permitem Roubar{br}de quase qualquer um.",
"A warrior who participates in battle using Speechcraft.{br}Words, rather than swords, are the orator's weapons.{br}{font:08}Ability: {font:00}Beast Tongue":
"Um guerreiro que participa da batalha usando Oratoria.{br}Palavras, e nao espadas, sao as armas do orador.{br}{font:08}Habilidade: {font:00}Lingua Feral",
"A warrior who uses the Mystic Arts to bend the{br}forces of the cosmos to his or her will.":
"Um guerreiro que usa as Artes Misticas para dobrar{br}as forcas do cosmos a sua vontade.",
"A warrior who uses Geomancy to control powers{br}lying dormant in the natural terrain.":
"Um guerreiro que usa Geomancia para controlar poderes{br}adormecidos no terreno natural.",
"A warrior who may make soaring Jump attacks even in{br}full armor, the dragoon is also a master spearman.":
"Um guerreiro capaz de realizar ataques de Salto mesmo{br}com armadura completa, o dragao tambem domina a lanca.",
"Following a warrior ethic from a foreign land, the samurai{br}uses Iaido techniques to attack with his or her katana.":
"Seguindo uma etica guerreira de uma terra estrangeira, o samurai{br}usa tecnicas de Iaido para atacar com sua katana.",
"A warrior who uses stealth to be all but invisible.{br}The ninja may also Throw weapons at faraway enemies.{br}{font:08}Ability: {font:00}Dual Wield":
"Um guerreiro que usa furtividade para ficar quase invisivel.{br}O ninja tambem pode Arremessar armas contra inimigos distantes.{br}{font:08}Habilidade: {font:00}Dupla Empunhadura",
"A learned warrior who uses Arithmeticks to analyze{br}natural phenomena and pinpoint magickal attacks.":
"Um guerreiro erudito que usa Aritmetica para analisar{br}fenomenos naturais e direcionar ataques magicos com precisao.",
"A warrior who uses his voice as a weapon. May use{br}Bardsong to support his allies in battle.":
"Um guerreiro que usa a voz como arma. Pode usar{br}Canto de Bardo para apoiar seus aliados na batalha.",
"A warrior who dances across the battlefield, garbed in{br}colorful raiments. May Dance to hinder the enemy.":
"Um guerreiro que danca pelo campo de batalha, vestido com{br}trajes coloridos. Pode Dancar para atrapalhar o inimigo.",
"A warrior who has abandoned his or her own identity,{br}instead mimicking the actions of allies in battle.":
"Um guerreiro que abandonou a propria identidade,{br}imitando as acoes dos aliados na batalha.",
}
apply(PATH, T, "entry38 batch3 (jobs cont.)")
