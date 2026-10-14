import json

PATH = "/home/c1c3ru/Downloads/finalfantasy/FFT_Android_Mod/translation/ptbr/entry41_join.json"

T = {
"Type A": "Tipo A",
"The Enterprise": "O Enterprise",
"The Vaschons": "Os Vaschons",
"The Wyverns": "As Wyverns",
"The Typhoon": "O Tufao",
"The Mudman": "O Homem de Lama",
"The Golem": "O Golem",
"The Informant": "O Informante",
"The Blackjack": "O Blackjack",
"The Yuguewood": "O Yuguewood",
"The Stair": "A Escada",
"The Hollow": "A Cavidade",
"The Crevasse": "A Fenda",
"The Switchback": "A Reviravolta",
"The Crossing": "A Travessia",
"The Catacombs": "As Catacumbas",
"The Oubliette": "A Masmorra Esquecida",
"The Palings": "As Estacadas",
"The Interstice": "O Interstício",
"The Dark": "As Trevas",
"A Stalemate": "Um Impasse",
"The Fete": "A Festa",
"The Highwind": "O Highwind",
"The Hindenburg": "O Hindenburg",
"The Falcon": "O Falcon",
"The Durga": "O Durga",
"The Behemoth": "O Behemoth",
"The Scriptures": "As Escrituras",
"The Machinist": "O Engenheiro",
"The Automaton": "O Automato",
"The Orrery": "O Orrery",
"The Curse": "A Maldicao",
"To Orbonne": "Para Orbonne",
"At Lesalia": "Em Lesalia",
"The Hunter": "O Cacador",
}

data = json.load(open(PATH, encoding="utf-8"))
strings = data["strings"]
changed = 0
for i, (s, t) in enumerate(strings):
    if s in T:
        strings[i] = [T[s], t]
        changed += 1
with open(PATH, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=0)
print("changed:", changed)
