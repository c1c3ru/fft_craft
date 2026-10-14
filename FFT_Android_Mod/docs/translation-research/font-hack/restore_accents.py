# -*- coding: utf-8 -*-
import json
import re
import sys

sys.path.insert(0, "tools")
from fft_text import encode_string, decode_bytes

EXPLICIT = {
    # a-tilde / c-cedilla / a-circ / e-circ / o-circ / o-acute / o-tilde words
    # not covered by the generic suffix rules below
    "agua": "água",
    "aguas": "águas",
    "forca": "força", "forcas": "forças",
    "cabeca": "cabeça", "cabecas": "cabeças",
    "dancarino": "dançarino", "dancarinos": "dançarinos",
    "dancar": "dançar", "danca": "dança", "dancas": "danças",
    "esforcar": "esforçar", "esforco": "esforço",
    "reforcada": "reforçada", "reforcado": "reforçado", "reforcar": "reforçar",
    "alcancaram": "alcançaram", "alcancou": "alcançou",
    "cacador": "caçador", "cacadores": "caçadores",
    "despedaca": "despedaça", "despedacar": "despedaçar",
    "cancer": "câncer",
    "bonus": "bônus",
    "gemeos": "gêmeos",
    "capricornio": "capricórnio",
    "heroi": "herói",
    "fenomenos": "fenômenos", "fenomeno": "fenômeno",
    "propria": "própria", "proprias": "próprias",
    "proprio": "próprio", "proprios": "próprios",
    "proxima": "próxima", "proximas": "próximas",
    "otima": "ótima",
    "psicologico": "psicológico",
    "maca": "maça",  # weapon ("mace"), confirmed by context (Mangual/Maca de Zeus/Maca de Fogo)
    "entao": "então",
    "maos": "mãos",
    "artesaos": "artesãos",
    "bencao": "bênção",
    "cacar": "caçar", "caca": "caça",
    "braco": "braço", "bracadeira": "braçadeira",
    "diabolico": "diabólico", "diabolica": "diabólica", "diabolicas": "diabólicas",
    "diabolicos": "diabólicos",
    "fenix": "fênix",
    "justica": "justiça",
    "graca": "graça", "gracas": "graças",
    "lancar": "lançar", "lancadas": "lançadas", "lancamento": "lançamento",
    "lancara": "lançara", "avancadas": "avançadas",
}

SUFFIX_RULES = [
    ("ancias", "âncias", 7),
    ("encias", "ências", 7),
    ("ancas", "anças", 6),
    ("encas", "enças", 6),
    ("ancia", "ância", 6),
    ("encia", "ência", 6),
    ("anca", "ança", 5),
    ("enca", "ença", 5),
    ("coes", "ções", 5),
    ("soes", "sões", 5),
    ("cao", "ção", 3),
    ("sao", "são", 3),
    ("oes", "ões", 4),
    ("ao", "ão", 3),
]
EXCLUDE_OES = {"foes", "shoes", "noes"}
EXCLUDE_AO = set()
EXCLUDE_ANCA = {"branca", "brancas"}  # adjective, not a ç-word

WORD_RE = re.compile(r"[A-Za-z]+")

def fix_word(word):
    lw = word.lower()
    repl = None
    if lw in EXPLICIT:
        repl = EXPLICIT[lw]
    else:
        for suf, newsuf, minlen in SUFFIX_RULES:
            if lw.endswith(suf) and len(lw) >= minlen:
                if suf == "oes" and lw in EXCLUDE_OES:
                    continue
                if suf == "ao" and lw in EXCLUDE_AO:
                    continue
                if suf in ("anca", "ancas") and lw in EXCLUDE_ANCA:
                    continue
                repl = lw[: -len(suf)] + newsuf
                break
    if repl is None:
        return word, False
    # The font has no uppercase accented glyphs at all (not even Ç), so a
    # capitalized first letter that would need one stays lowercase instead.
    if word.isupper():
        return "".join(c.upper() if c.isascii() else c for c in repl), True
    if word[0].isupper():
        first = repl[0].upper() if repl[0].isascii() else repl[0]
        return first + repl[1:], True
    return repl, True

def fix_string(s):
    changed = False
    def _sub(m):
        nonlocal changed
        w = m.group(0)
        new, ch = fix_word(w)
        if ch:
            changed = True
        return new
    out = WORD_RE.sub(_sub, s)
    return out, changed

FILES = [
    "ptbr/entry38_sample.json",
    "ptbr/entry41_join.json",
    "ptbr/entry42_help.json",
]

total_changed = {}
char_counts = {c: 0 for c in "ãõçâêôó"}
examples = []

for fn in FILES:
    with open(fn, encoding="utf-8") as f:
        data = json.load(f)
    n_changed = 0
    for entry in data["strings"]:
        s, term = entry
        new_s, changed = fix_string(s)
        if changed:
            n_changed += 1
            if len(examples) < 40:
                examples.append((fn, s, new_s))
            for c in "ãõçâêôó":
                char_counts[c] += new_s.count(c) - s.count(c)
            entry[0] = new_s
    total_changed[fn] = n_changed
    with open(fn, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
        f.write("\n")

print("=== change counts ===")
for fn, n in total_changed.items():
    print(fn, n)
print("=== new char occurrence deltas ===")
for c, n in char_counts.items():
    print(repr(c), n)
print("=== examples ===")
for fn, old, new in examples:
    if old != new:
        print(fn)
        print(" old:", old[:160])
        print(" new:", new[:160])
