import json, re, sys
sys.path.insert(0, "tools")
from phrase_translate import apply_phrases

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
    "{font:08}ATK": "{font:08}ATQ",
    "{font:08}Jump": "{font:08}Salto",
    "{font:08}Move": "{font:08}Movimento",
    "(Phys.)": "(Fis.)",
}

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

ELEMENT_STATUS_WORD = {
    "Fire": "Fogo", "Ice": "Gelo", "Lightning": "Raio", "Water": "Agua", "Wind": "Vento",
    "Earth": "Terra", "Holy": "Sagrado", "Dark": "Trevas",
    "Berserk": "Furia", "Blind": "Cegueira", "Charm": "Encantamento", "Confuse": "Confusao",
    "Disable": "Incapacitar", "Doom": "Perdicao", "Immobilize": "Imobilizar", "KO": "KO",
    "Poison": "Veneno", "Silence": "Silencio", "Sleep": "Sono", "Slow": "Lentidao",
    "Stone": "Petrificacao", "Stop": "Parar", "Toad": "Sapo", "Traitor": "Traidor",
    "Undead": "Morto-Vivo", "Vampire": "Vampiro", "Oil": "Oleo",
    "Float": "Flutuar", "Reflect": "Refletir", "Reraise": "Reerguer", "Regen": "Regeneracao",
    "Protect": "Proteger", "Shell": "Barreira",
}
ELEMENT_LABELS_PT = ["Remove", "Restaura", "Equipar", "Imune", "Fraquezas", "Fraqueza",
                     "Absorve", "Elemento", "Reduz a Metade", "Anula", "Efeito"]
ELEMENT_PATTERN = re.compile(
    r"((?:%s)): \{font:00\}([A-Za-z][A-Za-z, ]*)" % "|".join(re.escape(l) for l in ELEMENT_LABELS_PT)
)

def element_repl(m):
    label, body = m.group(1), m.group(2)
    parts = body.split(", ")
    new_parts, changed_any = [], False
    for p in parts:
        p_s = p.rstrip()
        trailing = p[len(p_s):]
        if p_s in ELEMENT_STATUS_WORD:
            new_parts.append(ELEMENT_STATUS_WORD[p_s] + trailing)
            changed_any = True
        else:
            new_parts.append(p)
    if not changed_any:
        return m.group(0)
    return f"{label}: {{font:00}}" + ", ".join(new_parts)

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
ABILITY_PATTERN = re.compile(r"(Habilidades?): \{font:00\}([A-Za-z][A-Za-z, '\.]*)")

def ability_repl(m):
    label, body = m.group(1), m.group(2)
    parts = body.split(", ")
    new_parts, changed_any = [], False
    for p in parts:
        p_s = p.rstrip()
        trailing = p[len(p_s):]
        if p_s in ABILITY_WORD:
            new_parts.append(ABILITY_WORD[p_s] + trailing)
            changed_any = True
        else:
            new_parts.append(p)
    if not changed_any:
        return m.group(0)
    return f"{label}: " + "{font:00}" + ", ".join(new_parts)

TRIGGER_WORD = {
    "Physical Attack": "Ataque Fisico", "Magick": "Magia", "Critical": "Critico",
    "HP Loss": "Perda de HP", "HP Restored": "HP Restaurado", "Speechcraft": "Oratoria",
    "Throw": "Arremesso", "Bow/Crossbow Attack": "Ataque de Arco/Besta",
    "Some Magicks": "Algumas Magias", "Geomancy": "Geomancia",
}
TRIGGER_PATTERN = re.compile(r"(Gatilho): \{font:00\}([A-Za-z][A-Za-z/, ]*)")

def trigger_repl(m):
    label, body = m.group(1), m.group(2)
    parts = body.split(", ")
    new_parts, changed_any = [], False
    for p in parts:
        p_s = p.rstrip()
        trailing = p[len(p_s):]
        if p_s in TRIGGER_WORD:
            new_parts.append(TRIGGER_WORD[p_s] + trailing)
            changed_any = True
        else:
            new_parts.append(p)
    if not changed_any:
        return m.group(0)
    return f"{label}: {{font:00}}" + ", ".join(new_parts)

HEADER_RE = re.compile(r"^\{font:08\}([A-Za-z][A-Za-z '\.]*?)\{font:00\}\{br\}")

def apply_all(path):
    data = json.load(open(path, encoding="utf-8"))
    strings = data["strings"]
    changed = 0
    for i, (s, t) in enumerate(strings):
        orig = s
        m = HEADER_RE.match(s)
        if m and m.group(1) in ITEM_TYPES:
            s = "{font:08}" + ITEM_TYPES[m.group(1)] + "{font:00}{br}" + s[m.end():]
        if "Squire" in s and "Chemist" in s and "Knight" in s:
            s = apply_phrases(s, JOB_GRID)
        s = apply_phrases(s, LABELS)
        s = ELEMENT_PATTERN.sub(element_repl, s)
        s = ABILITY_PATTERN.sub(ability_repl, s)
        s = TRIGGER_PATTERN.sub(trigger_repl, s)
        s = s.replace("Females Only", "Apenas Mulheres")
        if s != orig:
            strings[i] = [s, t]
            changed += 1
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=0)
    print(f"{path}: {changed} strings touched by glossary pass")

if __name__ == "__main__":
    apply_all(sys.argv[1])
