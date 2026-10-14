import json

with open("tools/psx_charset.json", encoding="utf-8") as f:
    PSX_CHARS = json.load(f)

assert len(PSX_CHARS) == 2200

def build_psp_chars():
    chars = list(PSX_CHARS)
    chars[0x95] = " "
    chars[0x880] = "á"  # a
    chars[0x881] = "à"  # a
    chars[0x882] = "é"  # e
    chars[0x883] = "è"  # e
    chars[0x884] = "í"  # i
    chars[0x885] = "ú"  # u
    chars[0x886] = "ù"  # u
    chars[0x887] = "-"
    chars[0x888] = "—"  # em dash
    # Font-hack additions: repurposed unused glyph slots (index >= 0x898,
    # beyond the original 2200-entry table) redrawn as PT-BR accented
    # letters missing from the stock font. Byte codes 0xDA78-0xDA7E.
    # See docs/translation-research/font-hack/ for the glyph patch tooling.
    chars.append("ã")   # 0x898 -> 0xDA78
    chars.append("õ")   # 0x899 -> 0xDA79
    chars.append("ç")   # 0x89A -> 0xDA7A
    chars.append("â")   # 0x89B -> 0xDA7B
    chars.append("ê")   # 0x89C -> 0xDA7C
    chars.append("ô")   # 0x89D -> 0xDA7D
    chars.append("ó")   # 0x89E -> 0xDA7E
    return chars

def build_charmap(chars):
    table = {}
    for i in range(0xD0):
        table[i] = chars[i]
        table[i + 0xD000] = chars[i]
    for i in range(0xD0, len(chars)):
        key = (i - 0xD0) % 0xD0 + 0xD100 + 0x100 * ((i - 0xD0) // 0xD0)
        table[key] = chars[i]

    # explicit control codes not covered by the systematic kanji-shift table
    table[0xE0] = "{Ramza}"
    table[0xF8] = "{br}"
    table[0xFB] = "{BeginList}"
    table[0xFC] = "{EndList}"
    table[0xFD] = "{stayopen}"
    table[0xFE] = "{end}"
    table[0xFF] = "{close}"
    table[0xF4] = "{waitpress}"
    table[0xFA] = "{SP2}"  # PSP-specific
    for i in range(256):
        table[0xE200 + i] = "{{delay:{0:02X}}}".format(i)
        table[0xE300 + i] = "{{font:{0:02X}}}".format(i)
        table[0xEE00 + i] = "{{Tab {0:02X}}}".format(i)
    table[0xE1] = "{unitname}"
    table[0xE4] = "{E4}"
    table[0xE5] = "{E5}"
    table[0xE9] = "{E9}"
    table[0xEA] = "{EA}"
    table[0xEB] = "{EB}"
    return table

PSP_CHARS = build_psp_chars()
PSP_TABLE = build_charmap(PSP_CHARS)

TWO_BYTE_LEAD = set(range(0xD0, 0xDB)) | {0xE2, 0xE3, 0xE7, 0xE8, 0xEC, 0xEE, 0xF5, 0xF6}

def decompress(data: bytes) -> bytes:
    """Port of TextUtilities.Decompress. IMPORTANT (verified against the
    original C#): back-references read from the ORIGINAL INPUT stream at
    absolute position (i - jump), NOT from the growing output buffer -
    the C# call site is Decompress(bytes, bytes, 0), i.e. allBytes ==
    sectionBytes == the same raw compressed input. The upper-bound check
    in the source uses >= (not >), so a reference landing exactly on the
    end of the buffer is (quirkily) treated as out-of-range and falls
    back to literal bytes - preserved here for byte-exact behavior."""
    out = bytearray()
    i = 0
    n = len(data)
    while i < n:
        b0 = data[i]
        if 0xF0 <= b0 <= 0xF3 and i + 2 < n:
            b1, b2 = data[i + 1], data[i + 2]
            length = ((b0 & 0x03) << 3) + ((b1 & 0xE0) >> 5) + 4
            j = ((b1 & 0x1F) << 8) + b2
            jump = j - (j // 256) * 2
            src_start = i - jump
            src_end = src_start + length
            if src_start < 0 or src_end >= n:
                out.extend([b0, b1, b2])
            else:
                out.extend(data[src_start:src_end])
            i += 3
        else:
            out.append(b0)
            i += 1
    return bytes(out)

def decode_bytes(data: bytes, table=None) -> str:
    if table is None:
        table = PSP_TABLE
    out = []
    i = 0
    n = len(data)
    while i < n:
        val = data[i]
        key = val
        if val in TWO_BYTE_LEAD and i + 1 < n:
            key = val * 256 + data[i + 1]
            i += 2
        elif 0xF0 <= val <= 0xF3 and i + 2 < n:
            key = val * 256 * 256 + data[i + 1] * 256 + data[i + 2]
            i += 3
        else:
            i += 1
        out.append(table.get(key, "{{0x{0:X}}}".format(key)))
    return "".join(out)

if __name__ == "__main__":
    print("table size:", len(PSP_TABLE))
    print("0x3E ->", PSP_TABLE[0x3E])
    print("0xDA60 ->", PSP_TABLE.get(0xDA60))
    print("0xE0 ->", PSP_TABLE[0xE0])

# ---- Encoding (text -> bytes), for round-trip / repacking ----

def build_reverse_table(table):
    rev = {}
    for key, s in table.items():
        if s not in rev or key < rev[s]:
            rev[s] = key
    return rev

PSP_REVERSE = build_reverse_table(PSP_TABLE)

import re as _re
_TAG_RE = _re.compile(r"\{[^}]*\}")
_HEX_TAG_RE = _re.compile(r"^\{0x([0-9A-Fa-f]+)\}$")

def _key_to_bytes(key: int) -> bytes:
    if key < 256:
        return bytes([key])
    elif key < 65536:
        return bytes([(key >> 8) & 0xFF, key & 0xFF])
    else:
        return bytes([(key >> 16) & 0xFF, (key >> 8) & 0xFF, key & 0xFF])

def encode_string(s: str, terminator: int, reverse=None) -> bytes:
    """Inverse of decode_bytes for a single already-terminated logical string.
    `terminator` is the raw byte (0xFE for {end}, 0xFF for {close}) that
    originally ended this string (decode_bytes strips it into the tag, so
    callers must track which terminator was used when they split)."""
    if reverse is None:
        reverse = PSP_REVERSE
    out = bytearray()
    i = 0
    n = len(s)
    while i < n:
        c = s[i]
        if c == '{':
            j = s.index('}', i)
            tag = s[i:j + 1]
            i = j + 1
            m = _HEX_TAG_RE.match(tag)
            if m:
                out.extend(_key_to_bytes(int(m.group(1), 16)))
            elif tag in reverse:
                out.extend(_key_to_bytes(reverse[tag]))
            else:
                raise ValueError(f"Unknown tag {tag!r} (no reverse mapping)")
        else:
            if c not in reverse:
                raise ValueError(f"Unknown character {c!r} (0x{ord(c):X}) (no reverse mapping)")
            out.extend(_key_to_bytes(reverse[c]))
            i += 1
    out.append(terminator)
    return bytes(out)
