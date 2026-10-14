import sys, re
sys.path.insert(0, "tools")
from extract_strings import load_offsets, read_entry, PACK
from fft_text import decompress, decode_bytes, encode_string

TERM_RE = re.compile(r"\{end\}|\{close\}")

def split_with_terms(text):
    """Split into (string, terminator_byte) pairs. The regex finds each
    {end}/{close} tag; text before it is one logical string."""
    parts = []
    pos = 0
    for m in TERM_RE.finditer(text):
        s = text[pos:m.start()]
        term = 0xFE if m.group(0) == "{end}" else 0xFF
        parts.append((s, term))
        pos = m.end()
    trailing = text[pos:]
    return parts, trailing

offsets = load_offsets(PACK)

for idx in [36, 37, 38, 39, 40, 41, 42, 43]:
    raw = read_entry(PACK, offsets, idx)
    decomp = decompress(raw)
    same_as_raw = (decomp == raw)
    text = decode_bytes(decomp)
    parts, trailing = split_with_terms(text)

    rebuilt = bytearray()
    ok = True
    err = None
    for i, (s, term) in enumerate(parts):
        try:
            rebuilt.extend(encode_string(s, term))
        except ValueError as e:
            ok = False
            err = f"string #{i} {s[:40]!r}: {e}"
            break

    matches = ok and (bytes(rebuilt) == decomp[:len(rebuilt)])
    print(f"entry {idx}: raw==decomp(no compression)={same_as_raw} "
          f"n_strings={len(parts)} trailing_bytes={len(trailing)} "
          f"encode_ok={ok} rebuilt_len={len(rebuilt)} decomp_len={len(decomp)} "
          f"exact_match={matches}" + (f" ERROR={err}" if err else ""))
