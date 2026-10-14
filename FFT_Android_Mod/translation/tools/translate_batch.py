import json

def apply(path, translations, label=""):
    data = json.load(open(path, encoding="utf-8"))
    strings = data["strings"]
    changed = 0
    for i, (s, t) in enumerate(strings):
        if s in translations:
            strings[i] = [translations[s], t]
            changed += 1
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=0)
    print(f"[{label}] applied {len(translations)} unique translations, "
          f"{changed} occurrences replaced, out of {len(strings)} total strings")
    return changed
