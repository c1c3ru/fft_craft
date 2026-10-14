import json, sys
sys.path.insert(0, "tools")
from phrase_translate import apply_phrases

PATH = "/home/c1c3ru/Downloads/finalfantasy/FFT_Android_Mod/translation/ptbr/entry38_sample.json"
data = json.load(open(PATH, encoding="utf-8"))
strings = data["strings"]

LABELS = {
"{font:08}Abilities": "{font:08}Habilidades",
"{font:08}Ability": "{font:08}Habilidade",
"{font:08}Absorbs": "{font:08}Absorve",
"{font:08}Attack": "{font:08}Ataque",
"{font:08}Block": "{font:08}Bloqueio",
"{font:08}Boosts": "{font:08}Aumenta",
"{font:08}Effect": "{font:08}Efeito",
"{font:08}Element": "{font:08}Elemento",
"{font:08}Equip": "{font:08}Equipar",
"{font:08}Halves": "{font:08}Reduz a Metade",
"{font:08}Immune": "{font:08}Imune",
"{font:08}Negates": "{font:08}Anula",
"{font:08}Radius": "{font:08}Raio",
"{font:08}Range": "{font:08}Alcance",
"{font:08}Removes": "{font:08}Remove",
"{font:08}Restores": "{font:08}Restaura",
"{font:08}Speed": "{font:08}Velocidade",
"{font:08}Spell Effect": "{font:08}Efeito de Magia",
"{font:08}Trigger": "{font:08}Gatilho",
"{font:08}Weaknesses": "{font:08}Fraquezas",
"{font:08}Weakness": "{font:08}Fraqueza",
}

changed = 0
for i, (s, t) in enumerate(strings):
    new_s = apply_phrases(s, LABELS)
    if new_s != s:
        strings[i] = [new_s, t]
        changed += 1

with open(PATH, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=0)
print("strings touched by label pass:", changed)
