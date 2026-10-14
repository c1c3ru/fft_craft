import sys
sys.path.insert(0, "tools")
from translate_batch import apply
from phrase_translate import apply_phrases
import json

PATH = "/home/c1c3ru/Downloads/finalfantasy/FFT_Android_Mod/translation/ptbr/entry38_sample.json"

PHRASES = {
    "Cannot enter water.": "Nao pode entrar na agua.",
}

SENTENCES = {
"A large bird with vestigial wings that are incapable of{br}flight. Its fast running speed makes it an ideal mount.":
"Uma grande ave com asas vestigiais incapazes de{br}voar. Sua velocidade de corrida a torna uma montaria ideal.",
"A large bird whose fast running speed makes it an ideal{br}mount. The only variety of chocobo capable of flight.":
"Uma grande ave cuja velocidade de corrida a torna uma{br}montaria ideal. A unica variedade de chocobo capaz de voar.",
"A large bird with vestigial wings that are incapable of{br}flight. Considered the finest variety of riding chocobo.":
"Uma grande ave com asas vestigiais incapazes de{br}voar. Considerada a melhor variedade de chocobo de montaria.",
"A diminutive species of goblin with large ears and an{br}upturned nose. Surprisingly strong for its small size.":
"Uma especie diminuta de goblin com orelhas grandes e{br}nariz arrebitado. Surpreendentemente forte para seu tamanho.",
"A monster enveloped by raging flames that feed{br}on the highly flammable oil exuded by its body.":
"Um monstro envolto em chamas furiosas que se alimentam{br}do oleo altamente inflamavel exsudado por seu corpo.",
"A nimble quadruped that hunts using its sharp teeth. The{br}fluid covering its fangs and claws causes status effects.":
"Um quadrupede agil que caca usando dentes afiados. O{br}fluido que cobre suas presas e garras causa efeitos de status.",
"A soft-bodied monster covered in slime. Although{br}humanoid in appearance, it has no skeleton.":
"Um monstro de corpo mole cobertor de limo. Embora{br}tenha aparencia humanoide, nao possui esqueleto.",
"A dead warrior resurrected as an undead skeleton.{br}It will often reanimate not long after being KO'd.":
"Um guerreiro morto ressuscitado como um esqueleto morto-vivo.{br}Costuma se reanimar pouco depois de ser derrotado.",
"A restless incorporeal spirit. A mere touch may suck the{br}life from its target, causing debilitating status effects.":
"Um espirito incorporeo inquieto. Um simples toque pode drenar{br}a vida de seu alvo, causando efeitos de status debilitantes.",
"A peculiar monster whose body consists of one gigantic{br}eye. It uses a baleful stare to attack its enemies.":
"Um monstro peculiar cujo corpo e formado por um unico{br}olho gigantesco. Usa um olhar funesto para atacar inimigos.",
"A monstrous bird with a razor-sharp beak and giant wings.{br}Although a skillful flier, it almost always walks on land.":
"Uma ave monstruosa com bico afiadissimo e asas gigantes.{br}Embora voe com destreza, quase sempre caminha em terra.",
"A strangely endearing monster that resembles a domestic{br}pig. Unlike a normal pig, however, it walks on two feet.":
"Um monstro estranhamente adoravel que se parece com um porco{br}domestico. Mas, diferente de um porco normal, anda em duas patas.",
"A tree endowed with consciousness by sprites residing{br}within. Its leaves seem to harbor a mysterious energy.":
"Uma arvore dotada de consciencia por espiritos que{br}habitam em seu interior. Suas folhas parecem abrigar uma energia misteriosa.",
"A monster with the body of a man and the head of a bull.{br}Its gigantic, muscular body makes for devastating attacks.":
"Um monstro com corpo de homem e cabeca de touro.{br}Seu corpo gigantesco e musculoso produz ataques devastadores.",
"This repulsive monster will eat all that comes before{br}its gaping maw. Its body is covered in fetid slime.":
"Este monstro repulsivo devora tudo que surge diante de{br}suas fauces abertas. Seu corpo e cobertor de limo fetido.",
"This fearsome monster has enormous hooves, a great{br}furry mane, gigantic horns, and a thick muscular tail.":
"Este monstro temivel tem cascos enormes, uma grande{br}juba peluda, chifres gigantescos e uma cauda grossa e musculosa.",
"A giant monster covered in scales. Although it has wings,{br}it cannot fly. It is very aggressive and not very intelligent.":
"Um monstro gigante cobertor de escamas. Embora tenha asas,{br}nao pode voar. E muito agressivo e pouco inteligente.",
"This three-headed monster is able to fly, despite its huge{br}size. Each head shares its consciousness with its mates.":
"Este monstro de tres cabecas e capaz de voar, apesar de seu{br}enorme tamanho. Cada cabeca compartilha sua consciencia com as outras.",
"This monster is distinguished by its sharp claws and large{br}horns. It stands on two feet and has a slender tail.":
"Este monstro se distingue por garras afiadas e chifres{br}grandes. Fica em duas patas e tem uma cauda esguia.",
"This taciturn general-purpose robot is a relic of a lost{br}civilization's technology. It exists only to serve its master.":
"Este robo taciturno e multiuso e uma reliquia da tecnologia{br}de uma civilizacao perdida. Existe apenas para servir seu dono.",
"A legendary daemon lord depicted in the constellation of{br}the Serpent Bearer. His fiery wrath cannot be quenched.":
"Um lendario senhor demonio representado na constelacao{br}do Portador da Serpente. Sua ira ardente jamais se apaga.",
"A giant monster covered in scales. This one possesses{br}a strangely intelligent look and deadly breath attacks.":
"Um monstro gigante cobertor de escamas. Este possui{br}um olhar estranhamente inteligente e ataques de folego mortais.",
"A member of a race of daemons that has existed since{br}the age of myth. It employs the destructive Dark Arts.":
"Um membro de uma raca de demonios que existe desde{br}a era dos mitos. Emprega as destrutivas Artes das Trevas.",
"A fell monster named after Ultima, the High Seraph.{br}Attacks with the incredibly destructive Demon Magicks.":
"Um monstro sinistro batizado em homenagem a Ultima, o Alto Serafim.{br}Ataca com as incrivelmente destrutivas Magias Demoniacas.",
"This warrior exchanges life for power, using Darkness{br}to disintegrate all who stand in the way.":
"Este guerreiro troca vida por poder, usando as Trevas{br}para desintegrar todos que ficam em seu caminho.",
"Although able to equip all weapons, this sad warrior excels{br}at none, and is far from being the most powerful.":
"Embora possa equipar todas as armas, este guerreiro pouco{br}talentoso nao se destaca em nenhuma, e esta longe de ser o mais poderoso.",
"A pirate who sails the open sky, free from all laws and{br}obligations. He never lets a mark escape.{br}{font:08}Ability: {font:00}Safeguard":
"Um pirata que navega o ceu aberto, livre de leis e{br}obrigacoes. Ele nunca deixa um alvo escapar.{br}{font:08}Habilidade: {font:00}Protecao",
"A hunter who trails rare monsters, employing{br}Huntcraft skills to overcome them.{br}{font:08}Ability: {font:00}Poach":
"Um cacador que rastreia monstros raros, empregando{br}habilidades de Caca para supera-los.{br}{font:08}Habilidade: {font:00}Capturar",
"A knight who has mastered all techniques and obtained the{br}highest rank. Even stronger when using Onion equipment.":
"Um cavaleiro que dominou todas as tecnicas e alcancou o{br}posto mais alto. Ainda mais forte usando equipamento de Cebola.",
"A dark knight reborn under the protection of daemons.{br}Leeches the souls of enemies with a Fell Sword.":
"Um cavaleiro negro renascido sob a protecao de demonios.{br}Drena as almas dos inimigos com uma Espada Sinistra.",
"A knight devout who defends the Church from heretics.{br}Uses Spellblade techniques to cut down the enemy.":
"Um cavaleiro devoto que defende a Igreja dos hereges.{br}Usa tecnicas de Espada Arcana para abater o inimigo.",
"An evil human being, transformed into this dark dragon{br}with devastating attacks and a variety of breath effects.{br}{font:08}Abilities: {font:00}Counter, Attack Boost, Arcane Strength,{br}Arcane Defense":
"Um ser humano maligno, transformado neste dragao sombrio{br}com ataques devastadores e variados efeitos de folego.{br}{font:08}Habilidades: {font:00}Contra-Ataque, Aumento de Ataque, Forca Arcana,{br}Defesa Arcana",
}

data = json.load(open(PATH, encoding="utf-8"))
strings = data["strings"]
changed = 0
for i, (s, t) in enumerate(strings):
    new_s = apply_phrases(s, PHRASES)
    if new_s in SENTENCES:
        new_s = SENTENCES[new_s]
    elif new_s != s:
        pass
    if new_s != s:
        strings[i] = [new_s, t]
        changed += 1
with open(PATH, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=0)
print("changed:", changed)
