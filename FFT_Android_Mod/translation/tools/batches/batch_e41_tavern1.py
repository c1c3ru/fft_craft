import sys, json
sys.path.insert(0, "tools")
from phrase_translate import apply_phrases

PATH = "/home/c1c3ru/Downloads/finalfantasy/FFT_Android_Mod/translation/ptbr/entry41_join.json"

T = {
"Come on in, then! Make yourself welcome.": "Entre, entao! Fique a vontade.",
"Thanks for dropping in. Do come again.": "Obrigado pela visita. Volte sempre.",
"Here's what all the locals have been going on{br}about.": "Aqui esta o que todo mundo andou comentando{br}por aqui.",
"That, eh? Here's what I've heard.": "Isso, hein? Aqui esta o que eu ouvi.",
"There've been no interesting rumors{br}in recent days.": "Nao tem corrido nenhum rumor interessante{br}nos ultimos dias.",
"I know of a thing or two you might be able to{br}do.": "Eu sei de umas coisinhas que voce talvez possa{br}fazer.",
"That, eh? Here's the bill.": "Isso, hein? Aqui esta a conta.",
"Beg pardons, my lord, I've not heard of any{br}work as of late.": "Perdoe-me, meu senhor, nao ouvi falar de nenhum{br}trabalho ultimamente.",
"You can't take on any more work at present.": "Voce nao pode aceitar mais trabalho agora.",
"You want to take on the job?": "Quer aceitar o trabalho?",
"{EB} and other expenses come{br}to {E4} gil. That all right?": "{EB} e outras despesas somam{br}{E4} gil. Esta bem assim?",
"It seems you're a little short on the gil,{br}my lord.": "Parece que esta faltando gil,{br}meu senhor.",
"Well enough, then. Who's to be sent on the{br}task?": "Muito bem, entao. Quem vai ser enviado para a{br}tarefa?",
"I'd wager the job will take {E4} to {E4} days.{br}How many days will you give 'em?": "Eu diria que o trabalho vai levar de {E4} a {E4} dias.{br}Quantos dias voce vai dar a eles?",
"Those are the terms, then.{br}Have we got a deal?": "Esses sao os termos, entao.{br}Temos um acordo?",
"Finder's fee, supplies,": "Taxa de localizacao, suprimentos,",
"The tavern is closed.": "A taverna esta fechada.",
"You've got some people back from their tasks.": "Algumas pessoas voltaram de suas tarefas.",
"Want to hear the report on that, eh?": "Quer ouvir o relatorio sobre isso, hein?",
"Here's what's underway at the moment.": "Aqui esta o que esta em andamento no momento.",
"I've arranged for their return first thing on{br}the morrow.": "Providenciei o retorno deles a primeira hora{br}de amanha.",
"All their efforts will have been for naught.{br}Are you certain about this?": "Todo o esforco deles tera sido em vao.{br}Tem certeza disso?",
"Right, then. I'll have 'em back on the morrow.": "Certo, entao. Vou traze-los de volta amanha.",
"Days:{Tab 2C}{E4}/{E4}{br}Departing:{Tab 2C}{EB}{br}Units:": "Dias:{Tab 2C}{E4}/{E4}{br}Partida:{Tab 2C}{EB}{br}Unidades:",
"I'm afraid you've no one to send.": "Receio que voce nao tenha ninguem para enviar.",
"Bonus: {Tab 2C}{EB}{br}Reward: {Tab 2C}{E4} gil{br}JP:": "Bonus: {Tab 2C}{EB}{br}Recompensa: {Tab 2C}{E4} gil{br}JP:",
"{EB}{br}Here's the report on that errand.": "{EB}{br}Aqui esta o relatorio sobre aquela tarefa.",
"Kills: {Tab 2A} {0xE804}{E4}{br}Casualties: {0xE804}{E4}": "Mortes: {Tab 2A} {0xE804}{E4}{br}Baixas: {0xE804}{E4}",

"Careful study of these works will no doubt shed{br}light on the secrets behind the War of the Lions.":
    "O estudo cuidadoso dessas obras sem duvida lancara{br}luz sobre os segredos da Guerra dos Leoes.",
"Here is all we know.": "Aqui esta tudo o que sabemos.",
"I will offer my humble assistance whenever it{br}is needed on your quest to discover the truth.":
    "Oferecerei minha humilde ajuda sempre que{br}necessario em sua busca pela verdade.",
"Resume reading from{br}where you left off?{br}{br}{SP2}{SP2}Resume{br}{SP2}{SP2}Restart":
    "Continuar a leitura de{br}onde parou?{br}{br}{SP2}{SP2}Continuar{br}{SP2}{SP2}Recomecar",

"I think I mentioned this once before.": "Acho que ja mencionei isso antes.",
"The winds in that area can be fierce.{br}Watch yourself.": "Os ventos naquela area podem ser ferozes.{br}Tome cuidado.",
"I'd not get my hopes up about finding treasure.": "Eu nao apostaria muito em achar tesouro.",
"Divers need strength and endurance.": "Mergulhadores precisam de forca e resistencia.",
"Beware the strait's rocky shoals.": "Cuidado com os baixios rochosos do estreito.",
"It takes raw strength to be a diver.": "E preciso forca bruta para ser mergulhador.",
"The Bay of Obell is known for strong winds.": "A Baia de Obell e conhecida por ventos fortes.",
"The West Bugross Sea is deep.{br}It'll take muscle to raise that ship.": "O Mar de Bugross Ocidental e profundo.{br}Vai precisar de musculo para erguer aquele navio.",
"I've always loved the legend of King Mesa.{br}But it's naught more than legend, is it?": "Sempre adorei a legenda do Rei Mesa.{br}Mas nao e nada mais que legenda, nao e?",
"Sahagin lurk in those waters. Be careful.": "Sahagins se escondem naquelas aguas. Tenha cuidado.",
"I can never understand the goings-on at the{br}castle.": "Nunca consigo entender o que se passa no{br}castelo.",
"I hear the embassy's treasures are priceless.": "Ouvi dizer que os tesouros da embaixada nao tem preco.",
"I graduated from the Akademy for the{br}Magickal Arts, you know. For true, I did!": "Eu me formei na Academia das Artes{br}Magicas, sabia? E verdade, eu mesmo!",
"The guild's fees are outrageous, but they know{br}their trade.": "As taxas da guilda sao um absurdo, mas eles conhecem{br}o oficio.",
"You'll need intimate knowledge of Mother{br}Nature and the seas to navigate those currents.": "Voce vai precisar de conhecimento profundo da{br}Mae Natureza e dos mares para navegar nessas correntes.",
"Take care that none of those whirlpools claim{br}you as their prize!": "Cuidado para nenhum daqueles redemoinhos{br}te reclamar como presa!",
"I fear any treasure in that mine was long ago{br}discovered. All you'll turn up is dust.": "Temo que qualquer tesouro naquela mina ja tenha sido{br}descoberto ha muito tempo. So vai achar poeira.",
"Real men's work...?": "Trabalho de homem de verdade...?",
"Abandoned mines swarm with monsters.": "Minas abandonadas estao infestadas de monstros.",
"I can't understand why these expeditions are so{br}popular.": "Nao entendo por que essas expedicoes sao tao{br}populares.",
"That mine's famous for its veins of silver.{br}You just might stumble onto one!": "Aquela mina e famosa por seus veios de prata.{br}Voce pode acabar achando um!",
"That was a terrible accident, but it seems{br}they're back in business.": "Aquilo foi um acidente terrivel, mas parece{br}que voltaram ao trabalho.",
"Coal miners need a strong arm. Mining's not{br}easy work.": "Mineiros de carvao precisam de braco forte. Minerar nao{br}e trabalho facil.",
"Keep one eye out for the color, but you'd best{br}keep t'other out for beasts!": "Fique de olho na cor, mas e melhor manter{br}o outro de olho nas bestas!",
"People always tell stories about places like that.": "As pessoas sempre contam historias sobre lugares assim.",
"Like as not, those rumors are true. But there's{br}also talk of a dragon in that mine.": "E bem provavel que esses rumores sejam verdade. Mas tambem{br}se fala de um dragao naquela mina.",
"Coal miners need a strong arm.{br}Mining's not easy work.": "Mineiros de carvao precisam de braco forte.{br}Minerar nao e trabalho facil.",
"{0xEC75}Tavernmaster—{br}I hear there's naught but iron in that mine.{br}Too bad for the miners.": "{0xEC75}Taverneiro—{br}Ouvi dizer que naquela mina nao tem nada alem de ferro.{br}Pena pros mineiros.",
"The real treasure in that mountain is coal. It's{br}not worth much, but there's an awful lot of it.": "O verdadeiro tesouro naquela montanha e o carvao. Nao{br}vale muito, mas tem uma quantidade enorme.",
"You truly think there are lost wonders out{br}there? That Cataclysm talk is naught but myth.": "Voce acha mesmo que ha maravilhas perdidas{br}por ai? Essa historia do Cataclismo e so mito.",
"There's rough terrain around that lake.{br}Best send someone light on their feet.": "Tem terreno dificil ao redor daquele lago.{br}Melhor enviar alguem agil.",
"You won the last one of these, didn't you?": "Voce venceu o ultimo desses, nao foi?",
"There are bats there that'll suck the lifeblood{br}right out of you!": "Tem morcegos ali que vao sugar sua vida{br}ate a ultima gota!",
"At it again, eh? Well, good luck.": "De novo nessa, hein? Bem, boa sorte.",
"They were enormous ruins—no doubt some{br}wonder of the ancients!": "Eram ruinas enormes—sem duvida alguma{br}maravilha dos antigos!",
"It disappeared as soon as she saw them?{br}Sounds like lost ruins!": "Desapareceu assim que ela os viu?{br}Parece ruina perdida!",
"They could be ruins, but I'd wager he saw a{br}mirage.": "Podem ser ruinas, mas eu apostaria que ele viu{br}uma miragem.",
"Ancient ruins have been known to elude the eye.": "Ruinas antigas sao conhecidas por escapar da vista.",
"You're not like to find much more than{br}snakebites on an expedition like this.": "Voce nao deve achar muito mais que{br}picadas de cobra numa expedicao dessas.",
"Master Mog lives in those fens. He's a chatty{br}one—good luck prying yourself away from him.": "Mestre Mog vive naqueles pantanos. Ele e bem{br}falante—boa sorte pra se livrar dele.",
"I hear the marquis has been adding to his estate{br}again. Looks like he has a dungeon now, too.": "Ouvi dizer que o marques anda ampliando sua propriedade{br}de novo. Parece que agora ele tem uma masmorra tambem.",
"An amateur should be fine.{br}The Vaschons have a soft spot for beginners.": "Um amador deve se sair bem.{br}Os Vaschons tem uma simpatia por principiantes.",
"Does that mean an ancient civilization once lived{br}in these hinterlands?": "Isso significa que uma civilizacao antiga ja viveu{br}nessas terras?",
"I've seen them too.{br}They're beautiful. Really!": "Eu tambem os vi.{br}Sao lindos. De verdade!",
"It gets quite slippery there.{br}Send someone who's light on their feet.": "Fica bem resvaladico por ali.{br}Envie alguem agil.",
"Best take a thief to deal with their traps.": "Melhor levar um ladrao pra lidar com as armadilhas deles.",
"Best send a skilled fighter for this one.": "Melhor enviar um lutador habilidoso pra esse.",
"Summon one monster, and most bandits will turn{br}tail and run.": "Invoque um monstro, e a maioria dos bandidos vai{br}dar no pe correndo.",
"The young lord's got a touch of his father's{br}greed—not that you heard that from me.": "O jovem lorde tem um toque da avareza do pai—{br}mas isso voce nao ouviu de mim.",
"You'll might want to bring a healer—just in{br}case.": "Talvez queira levar um curador—so por{br}precaucao.",
"So, the Typhoon is in town, eh?{br}They say he's a formidable swordsman.": "Entao o Tufao esta na cidade, hein?{br}Dizem que ele e um espadachim formidavel.",
"Fighting monsters is right up your alley, eh?": "Lutar contra monstros e a sua praia, hein?",
"Try using magick to finish it off quickly.": "Tente usar magia pra acabar com isso rapido.",
"I've heard tell of Zerro.{br}He's quite skilled with a blade.": "Ja ouvi falar de Zerro.{br}Ele e bem habilidoso com uma lamina.",
"I've heard tell a chimera's flames can melt{br}wrought iron. You'd best take care.": "Ouvi dizer que as chamas de uma quimera derretem{br}ferro forjado. Melhor ter cuidado.",
"I've not heard of pets turning into monsters{br}before.": "Nunca tinha ouvido falar de bichinhos de estimacao virando{br}monstros antes.",
"What are the adults doing that a child must{br}ask for help?": "O que os adultos andam fazendo que uma crianca{br}precisa pedir ajuda?",
"That boy's in trouble, no doubt.": "Esse garoto esta em apuros, sem duvida.",
"What kind of craven blackguard would kidnap a{br}child?": "Que tipo de covarde desprezivel sequestraria uma{br}crianca?",
"What kind of scum would kidnap a little girl?": "Que tipo de escoria sequestraria uma garotinha?",
"A malboro for a pet!? I'll never understand{br}nobility.": "Um malboro de estimacao!? Nunca vou entender{br}a nobreza.",
"Please look into this, for the sake of the{br}townspeople!": "Por favor, investigue isso, pelo bem do{br}povo da cidade!",
"Please solve this as quickly as possible, for the{br}town's sake.": "Por favor, resolva isso o mais rapido possivel, pelo bem{br}da cidade.",
"No doubt it's just children having fun.": "Sem duvida sao so criancas brincando.",
"You'll want someone light on their feet for this{br}task.": "Voce vai querer alguem agil pra essa{br}tarefa.",
"You'll want someone who knows about items for{br}that.": "Voce vai querer alguem que entenda de itens pra{br}isso.",
"I soften up whenever I hear about romance like{br}this. Don't you dare tell a soul.": "Eu me derreto toda vez que ouco sobre um romance{br}assim. Nao va contar pra ninguem.",
"Thieves are usually best at this kind of work.": "Ladroes costumam ser os melhores nesse tipo de trabalho.",
"It's not just monsters. The winds there are{br}quite strong as well. Be careful.": "Nao sao so monstros. Os ventos ali tambem sao{br}bem fortes. Tenha cuidado.",
"Ah, young love. I was young once, too.": "Ah, amor jovem. Eu tambem fui jovem um dia.",
"A linguist would no doubt be appropriate for a{br}task like this.": "Um linguista sem duvida seria apropriado pra{br}uma tarefa dessas.",
"Sounds like a task for someone with smarts.": "Parece uma tarefa pra alguem inteligente.",
"Could the problem be the way he talks?": "Sera que o problema e o jeito que ele fala?",
"This is a job for a chemist, I'd wager!": "Esse e um trabalho pra um quimico, eu diria!",
"We need skilled dancers for Mameco's farewell{br}performance!": "Precisamos de dancarinos habilidosos pra apresentacao{br}de despedida do Mameco!",
"That sort of work takes stamina.": "Esse tipo de trabalho exige resistencia.",
"Play it right, and you could be swimming in gil.": "Jogue certo, e voce pode acabar nadando em gil.",
"Offensive magick should vanquish those{br}monsters in a trice.": "Magia ofensiva deve eliminar esses{br}monstros rapidinho.",
"I love chocobo myself.{br}There's naught better than a good fried wing.": "Eu mesmo adoro chocobo.{br}Nao ha nada melhor que uma boa coxa frita.",
"Best send a learned person to do the tutoring.": "Melhor enviar uma pessoa culta pra fazer as aulas.",
"Best choose someone familiar with the ways of{br}battle.": "Melhor escolher alguem familiarizado com os costumes{br}de batalha.",
"You'll want magick users for this.{br}But you knew that, right?": "Voce vai querer usuarios de magia pra isso.{br}Mas voce ja sabia disso, certo?",
"Best send someone who's skilled at using items.": "Melhor enviar alguem habilidoso em usar itens.",
"{0xEC71}{0xF566}{0xF666}{0xF501}{0xF601}{font:08}Master Darlavon{br}{font:00}Wars are fought with wits and wisdom. Learn{br}all you can here to prepare for what lies ahead.":
    "{0xEC71}{0xF566}{0xF666}{0xF501}{0xF601}{font:08}Mestre Darlavon{br}{font:00}Guerras se ganham com inteligencia e sabedoria. Aprenda{br}tudo que puder aqui para se preparar para o que vem.",
"{0xEC71}{font:08}Master Darlavon{br}{font:00}Arm yourself with knowledge, and it will steel{br}you for whatever you may encounter.":
    "{0xEC71}{font:08}Mestre Darlavon{br}{font:00}Arme-se com conhecimento, e ele vai lhe fortalecer{br}para o que quer que voce encontre.",
"Press ○ to select or unselect units.{br}Press START to accept. You can send up to 3.":
    "Pressione ○ para selecionar ou desselecionar unidades.{br}Pressione START para confirmar. Voce pode enviar ate 3.",
"Terribly sorry, my lord. These jobs are only{br}open to humans without prior engagements.":
    "Sinto muito, meu senhor. Esses trabalhos sao abertos{br}apenas a humanos sem compromissos previos.",
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
