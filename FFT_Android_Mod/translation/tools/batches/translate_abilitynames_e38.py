import json, re

PATH = "/home/c1c3ru/Downloads/finalfantasy/FFT_Android_Mod/translation/ptbr/entry38_sample.json"
data = json.load(open(PATH, encoding="utf-8"))
strings = data["strings"]

ABILITY_WORD = {
"Counter": "Contra-Ataque", "Fly": "Voar", "Swim": "Nadar", "Levitate": "Levitar",
"Waterbreathing": "Respirar na Agua", "Waterwalking": "Andar na Agua",
"Ignore Elevation": "Ignorar Elevacao", "Ignore Terrain": "Ignorar Terreno",
"Ignore Weather": "Ignorar Clima", "Teleport": "Teletransporte", "Poach": "Capturar",
"Safeguard": "Protecao", "Swiftness": "Agilidade", "Throw Items": "Arremessar Itens",
"Beast Tongue": "Lingua Feral", "Dual Wield": "Dupla Empunhadura", "Brawler": "Brigao",
"Arcane Strength": "Forca Arcana", "Arcane Defense": "Defesa Arcana",
"Attack Boost": "Aumento de Ataque",
}

label_re = re.compile(r"(Habilidades?): \{font:00\}([A-Za-z][A-Za-z, '\.]*)")

def repl(m):
    label, body = m.group(1), m.group(2)
    # split on top-level commas (body has no nested {} here since we stop at {br}/{end} boundary naturally
    # because the regex char class excludes '{')
    parts = body.split(", ")
    changed_any = False
    new_parts = []
    for p in parts:
        p_strip = p.rstrip()
        trailing = p[len(p_strip):]
        if p_strip in ABILITY_WORD:
            new_parts.append(ABILITY_WORD[p_strip] + trailing)
            changed_any = True
        else:
            new_parts.append(p)
    if not changed_any:
        return m.group(0)
    return f"{label}: " + "{font:00}" + ", ".join(new_parts)

changed = 0
for i, (s, t) in enumerate(strings):
    new_s = label_re.sub(repl, s)
    if new_s != s:
        strings[i] = [new_s, t]
        changed += 1

with open(PATH, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=0)
print("changed:", changed)
