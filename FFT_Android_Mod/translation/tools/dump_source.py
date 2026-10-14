import sys, json, re
sys.path.insert(0, "tools")
from extract_strings import load_offsets, read_entry, PACK
from fft_text import decompress, decode_bytes

TERM_RE = re.compile(r"\{end\}|\{close\}")

def split_with_terms(text):
    parts = []
    pos = 0
    for m in TERM_RE.finditer(text):
        s = text[pos:m.start()]
        term = 0xFE if m.group(0) == "{end}" else 0xFF
        parts.append([s, term])
        pos = m.end()
    return parts, text[pos:]

NAMES = {36: "atchelp", 37: "spell", 38: "sample", 39: "world",
         40: "open", 41: "join", 42: "help", 43: "wldhelp"}

offsets = load_offsets(PACK)
for idx, name in NAMES.items():
    raw = read_entry(PACK, offsets, idx)
    decomp = decompress(raw)
    text = decode_bytes(decomp)
    parts, trailing = split_with_terms(text)
    out = {
        "entry_index": idx,
        "source_name": name,
        "trailing_len": len(trailing),
        "strings": parts,  # [ [text, terminator_byte], ... ] in original order
    }
    path = f"/home/c1c3ru/Downloads/finalfantasy/FFT_Android_Mod/translation/source/entry{idx:02d}_{name}.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=0)
    print(f"entry {idx} ({name}): {len(parts)} strings -> {path}")
