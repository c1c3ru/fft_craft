import json, sys
sys.path.insert(0, "tools")
from phrase_translate import apply_phrases

PATH = "/home/c1c3ru/Downloads/finalfantasy/FFT_Android_Mod/translation/ptbr/entry38_sample.json"
data = json.load(open(PATH, encoding="utf-8"))
strings = data["strings"]

SIGNS = {
    "Aries": "Aries", "Taurus": "Touro", "Gemini": "Gemeos", "Cancer": "Cancer",
    "Leo": "Leao", "Virgo": "Virgem", "Libra": "Libra", "Scorpio": "Escorpiao",
    "Sagittarius": "Sagitario", "Capricorn": "Capricornio", "Aquarius": "Aquario",
    "Pisces": "Peixes",
}

phrases = {
    "The guardian constellation of ": "A constelacao protetora de ",
    "Compatibility with other signs:": "Compatibilidade com outros signos:",
    "Good Compatibility: ": "Boa compatibilidade: ",
    "Poor Compatibility: ": "Baixa compatibilidade: ",
    "Best Compatibility: ": "Melhor compatibilidade: ",
    "Worst Compatibility: ": "Pior compatibilidade: ",
    "opposite gender": "sexo oposto",
    "same gender": "mesmo sexo",
}
for en, pt in SIGNS.items():
    phrases[en] = pt

changed = 0
for i in range(38, 50):
    s, term = strings[i]
    new_s = apply_phrases(s, phrases)
    if new_s != s:
        strings[i] = [new_s, term]
        changed += 1

# idx 50: "The 13th sign of the zodiac..."
s, term = strings[50]
strings[50] = ["O 13 signo do zodiaco. Tudo alem{br}do nome permanece envolto em misterio.", term]
changed += 1

print("changed:", changed)
with open(PATH, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=0)

# show results
for i in range(38, 51):
    print(i, repr(strings[i][0])[:160])
