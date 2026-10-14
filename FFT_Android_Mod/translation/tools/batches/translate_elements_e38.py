import json, re, sys

PATH = "/home/c1c3ru/Downloads/finalfantasy/FFT_Android_Mod/translation/ptbr/entry38_sample.json"
data = json.load(open(PATH, encoding="utf-8"))
strings = data["strings"]

WORD = {
"Fire": "Fogo", "Ice": "Gelo", "Lightning": "Raio", "Water": "Agua", "Wind": "Vento",
"Earth": "Terra", "Holy": "Sagrado", "Dark": "Trevas",
"Berserk": "Furia", "Blind": "Cegueira", "Charm": "Encantamento", "Confuse": "Confusao",
"Disable": "Incapacitar", "Doom": "Perdicao", "Immobilize": "Imobilizar", "KO": "KO",
"Poison": "Veneno", "Silence": "Silencio", "Sleep": "Sono", "Slow": "Lentidao",
"Stone": "Petrificacao", "Stop": "Parar", "Toad": "Sapo", "Traitor": "Traidor",
"Undead": "Morto-Vivo", "Vampire": "Vampiro",
}

LABELS_PT = ["Fraquezas", "Fraqueza", "Absorve", "Elemento", "Reduz a Metade", "Imune", "Anula"]
label_alt = "|".join(re.escape(l) for l in LABELS_PT)
# Matches: <Label>: {font:00}<comma list of English words/{tags}> up to next {br}/{end}/{close} or another {font:08}
pattern = re.compile(r"((?:%s)): \{font:00\}([A-Za-z][A-Za-z, ]*)" % label_alt)

def translate_list(m):
    label = m.group(1)
    body = m.group(2)
    parts = body.split(", ")
    new_parts = []
    changed_any = False
    for p in parts:
        p_stripped = p.rstrip()
        trailing = p[len(p_stripped):]
        if p_stripped in WORD:
            new_parts.append(WORD[p_stripped] + trailing)
            changed_any = True
        else:
            new_parts.append(p)
    if not changed_any:
        return m.group(0)
    return f"{label}: {{font:00}}" + ", ".join(new_parts)

changed = 0
for i, (s, t) in enumerate(strings):
    new_s = pattern.sub(translate_list, s)
    if new_s != s:
        strings[i] = [new_s, t]
        changed += 1

with open(PATH, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=0)
print("strings touched by element/status pass:", changed)
