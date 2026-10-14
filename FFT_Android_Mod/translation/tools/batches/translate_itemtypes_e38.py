import json, re, sys
sys.path.insert(0, "tools")
from phrase_translate import apply_phrases

PATH = "/home/c1c3ru/Downloads/finalfantasy/FFT_Android_Mod/translation/ptbr/entry38_sample.json"
data = json.load(open(PATH, encoding="utf-8"))
strings = data["strings"]

ITEM_TYPES = {
"Armguard": "Bracadeira", "Armlet": "Bracelete", "Armor": "Armadura", "Axe": "Machado",
"Bag": "Bolsa", "Book": "Livro", "Bow": "Arco", "Cloak": "Manto", "Cloth": "Tecido",
"Clothing": "Vestimenta", "Crossbow": "Besta", "Fell Sword": "Espada Sinistra",
"Flail": "Mangual", "Gun": "Arma de Fogo", "Hair Adornment": "Adorno de Cabelo",
"Hat": "Chapeu", "Helm": "Elmo", "Instrument": "Instrumento", "Katana": "Katana",
"Knife": "Faca", "Knight's Sword": "Espada de Cavaleiro", "Lip Rouge": "Batom",
"Ninja Blade": "Lamina Ninja", "Perfume": "Perfume", "Pole": "Vara", "Polearm": "Lanca",
"Ring": "Anel", "Robe": "Veste", "Rod": "Cajado", "Shield": "Escudo", "Shoes": "Sapatos",
"Staff": "Cetro", "Sword": "Espada",
}

JOB_GRID = {
"Squire": "Soldado", "Chemist": "Quimico", "Knight": "Cavaleiro", "Archer": "Arqueiro",
"Monk": "Monge", "White": "Branco", "Black": "Negro", "Time": "Tempo",
"Summoner": "Invocador", "Thief": "Ladrao", "Orator": "Orador", "Mystic": "Mistico",
"Geo.": "Geo.", "Dragoon": "Dragao", "Samurai": "Samurai", "Ninja": "Ninja",
"Arith.": "Arit.", "Bard": "Bardo", "Dancer": "Dancarino",
}

changed_headers = 0
changed_grid = 0
header_re = re.compile(r"^\{font:08\}([A-Za-z][A-Za-z '\.]*?)\{font:00\}\{br\}")

for i, (s, t) in enumerate(strings):
    new_s = s
    m = header_re.match(new_s)
    if m and m.group(1) in ITEM_TYPES:
        new_s = ITEM_TYPES[m.group(1)] + new_s[len(m.group(1)):]
        # fix: rebuild properly instead of naive slice
        new_s = "{font:08}" + ITEM_TYPES[m.group(1)] + "{font:00}{br}" + s[m.end():]
        changed_headers += 1

    if "Squire" in new_s and "Chemist" in new_s and "Knight" in new_s:
        before = new_s
        new_s = apply_phrases(new_s, JOB_GRID)
        if new_s != before:
            changed_grid += 1

    if new_s != s:
        strings[i] = [new_s, t]

with open(PATH, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=0)
print("headers changed:", changed_headers, "grid lines changed:", changed_grid)
