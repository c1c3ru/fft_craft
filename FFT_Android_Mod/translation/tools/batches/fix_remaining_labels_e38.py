import json, sys
sys.path.insert(0, "tools")
from phrase_translate import apply_phrases

PATH = "/home/c1c3ru/Downloads/finalfantasy/FFT_Android_Mod/translation/ptbr/entry38_sample.json"
data = json.load(open(PATH, encoding="utf-8"))
strings = data["strings"]

LABELS = {
    "{font:08}ATK": "{font:08}ATQ",
    "{font:08}Jump": "{font:08}Salto",
    "{font:08}Move": "{font:08}Movimento",
    "(Phys.)": "(Fis.)",
}

changed = 0
for i, (s, t) in enumerate(strings):
    new_s = apply_phrases(s, LABELS)
    if new_s != s:
        strings[i] = [new_s, t]
        changed += 1
with open(PATH, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=0)
print("changed:", changed)
