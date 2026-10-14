import sys, json
sys.path.insert(0, "tools")
from phrase_translate import apply_phrases

PATH = "/home/c1c3ru/Downloads/finalfantasy/FFT_Android_Mod/translation/ptbr/entry38_sample.json"

T = {
"A throwing weapon for ninjas.{br}It spins in the air before hitting its target.":
"Uma arma de arremesso para ninjas.{br}Ela gira no ar antes de atingir o alvo.",
"A pinwheel-shaped throwing star that flies at very{br}high speeds.":
"Uma shuriken em forma de cata-vento que voa a{br}velocidades muito altas.",
"A cross-shaped throwing star used by a famous ninja{br}school. Its blades are serrated for maximum damage.":
"Uma shuriken em forma de cruz usada por uma famosa{br}escola ninja. Suas laminas sao serrilhadas para dano maximo.",
"An explosive sphere that deals fire damage{br}when thrown.":
"Uma esfera explosiva que causa dano de fogo{br}ao ser arremessada.",
"An explosive sphere that deals water damage{br}when thrown.":
"Uma esfera explosiva que causa dano de agua{br}ao ser arremessada.",
"An explosive sphere that deals lightning damage{br}when thrown.":
"Uma esfera explosiva que causa dano de raio{br}ao ser arremessada.",
"The most inexpensive shield available. As expected,{br}its defensive abilities are lacking.":
"O escudo mais barato disponivel. Como esperado,{br}suas capacidades defensivas deixam a desejar.",
"A small shield for close-quarters fighting. Though{br}easy to use, its ability to block attacks is lacking.":
"Um escudo pequeno para combate corpo a corpo. Embora{br}facil de usar, sua capacidade de bloquear ataques e limitada.",
"This bronze shield is rather small, allowing the user{br}to deftly block his opponent's attacks.":
"Este escudo de bronze e bem pequeno, permitindo que o usuario{br}bloqueie com destreza os ataques do oponente.",
"The surface of this small, sturdy shield has been{br}inlaid with a complex ornamental design.":
"A superficie deste escudo pequeno e resistente foi{br}incrustada com um desenho ornamental complexo.",
"A shield constructed of the featherlight metal known{br}as mythril. It is surprisingly light and easy to wield.":
"Um escudo construido do metal leve como pena conhecido{br}como mithril. E surpreendentemente leve e facil de usar.",
"This mythril shield has been decorated with gold accents{br}and provides excellent protection against physical attacks.":
"Este escudo de mithril foi decorado com detalhes dourados{br}e oferece excelente protecao contra ataques fisicos.",
"This mythril shield is inlaid with pale blue gemstones{br}that seem to emit a frigid aura.{br}":
"Este escudo de mithril e incrustado com gemas azul-claras{br}que parecem emitir uma aura gelida.{br}",
"This mythril shield is inlaid with deep crimson gemstones{br}that seem to dance with the power of flame.{br}":
"Este escudo de mithril e incrustado com gemas vermelho-escuras{br}que parecem dancar com o poder das chamas.{br}",
"This shield resembles a breastplate worn by a god.{br}It enhances the user's magickal capabilities.":
"Este escudo se parece com uma armadura usada por um deus.{br}Ele melhora as capacidades magicas do usuario.",
"A shield adorned with brilliant, incredibly hard gems that{br}help protect the user from magicks.":
"Um escudo adornado com gemas brilhantes e incrivelmente duras que{br}ajudam a proteger o usuario contra magias.",
"This brilliant shield has been forged from a lustrous{br}white alloy of mythril and platinum. ":
"Este escudo brilhante foi forjado de uma liga branca{br}e lustrosa de mithril e platina. ",
"This shield has been inlaid with crystalline jewels{br}discovered deep within the earth.":
"Este escudo foi incrustado com joias cristalinas{br}descobertas nas profundezas da terra.",
"A pitch-black shield made by foreign craftsmen.{br}It is made of iron and has a unique shape.":
"Um escudo negro como a noite feito por artesaos estrangeiros.{br}E feito de ferro e tem uma forma unica.",
"A shield bearing the name of an ancient emperor. It boosts{br}the damage dealt by certain elemental magicks.{br}":
"Um escudo que leva o nome de um antigo imperador. Ele aumenta{br}o dano causado por certas magias elementais.{br}",
"A shield that has been brilliantly colored using special dyes{br}and pigments. It halves damage from the primary elements.{br}":
"Um escudo colorido de forma brilhante com corantes{br}e pigmentos especiais. Reduz a metade o dano dos elementos primarios.{br}",
"This shield's blocking capabilities are nearly unrivaled.":
"A capacidade de bloqueio deste escudo e quase incomparavel.",
"Shoes that have been dyed a deep crimson.":
"Sapatos tingidos num vermelho profundo.",
"A sturdy glove that increases weapon attack power.":
"Uma luva resistente que aumenta o poder de ataque da arma.",
"A glove that boosts the wearer's magickal attack power.":
"Uma luva que aumenta o poder de ataque magico de quem a usa.",
"A ring forged from metal inhabited by spirits.":
"Um anel forjado de metal habitado por espiritos.",
"A bracelet embedded with shining magickal jewels.":
"Um bracelete incrustado com joias magicas brilhantes.",
"A short cloak made of thin material that has been{br}imbued with magickal power.":
"Um manto curto feito de material fino que foi{br}imbuido com poder magico.",
"The outside of this cloak is black, while the inside is deep{br}crimson.":
"A parte externa deste manto e preta, enquanto a interna e{br}vermelho profundo.",
"This cloak is as light and soft as a feather.":
"Este manto e leve e suave como uma pena.",
"This cloak makes the wearer invisible—until he or she{br}is discovered.":
"Este manto torna quem o usa invisivel—ate ser{br}descoberto.",
"A perfume with an otherworldly aroma.":
"Um perfume com um aroma de outro mundo.",
"A shield forged for swordsmen who have mastered every{br}technique and achieved knighthood's most exalted rank.":
"Um escudo forjado para espadachins que dominaram todas{br}as tecnicas e alcancaram o posto mais exaltado da cavalaria.",
"A shield imbued with resistance to various attacks.":
"Um escudo imbuido com resistencia a varios ataques.",
"Magickal lip rouge from the popular Feyforge brand.{br}It is a limited-edition product, making it difficult for{br}even the richest noblewomen to obtain.":
"Batom magico da popular marca Feyforge.{br}E um produto de edicao limitada, dificil de obter{br}mesmo para as nobres mais ricas.",
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
