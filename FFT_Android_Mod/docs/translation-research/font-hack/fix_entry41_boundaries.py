"""Fix entry41_join.json's string boundaries: the original source/ptbr JSON
was generated with a decompress() that used the wrong back-reference
convention (growing-output-buffer instead of original-input-buffer, the
latter confirmed correct against FFTPatcher's TextUtilities.cs). This
collapsed what should be 6 separate strings (indices 0-5 in the correct
decode: 1 junk-data string + 4 empty strings + 1 more junk string) into a
single garbled string (old index 0). Everything from old index 1 onward
maps EXACTLY (confirmed empirically across indices 1-19 and 100-2000,
zero mismatches) to new index (old_index + 5).

This script rebuilds both source/entry41_join.json and ptbr/entry41_join.json
with the correct 5877-string structure, preserving all existing
translations (just re-indexed).
"""
import json
import re
import struct
import sys

sys.path.insert(0, "/home/c1c3ru/Downloads/finalfantasy/FFT_Android_Mod/translation/tools")
from fft_text import decompress, decode_bytes  # noqa: E402

PACK = "/run/media/c1c3ru/18DB-73EA/base/fftpack.bin"
SRC_JSON = "/home/c1c3ru/Downloads/finalfantasy/FFT_Android_Mod/translation/source/entry41_join.json"
PTBR_JSON = "/home/c1c3ru/Downloads/finalfantasy/FFT_Android_Mod/translation/ptbr/entry41_join.json"

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


def main():
    with open(PACK, "rb") as f:
        count, unk = struct.unpack("<II", f.read(8))
        offsets = struct.unpack("<%dI" % (count + 1), f.read(4 * (count + 1)))
    start, end = offsets[41], offsets[42]
    with open(PACK, "rb") as f:
        f.seek(start)
        raw = f.read(end - start)

    decomp = decompress(raw)
    text = decode_bytes(decomp)
    correct_parts, correct_trailing = split_with_terms(text)
    print(f"correct decode: {len(correct_parts)} strings, trailing_len={len(correct_trailing)}")

    with open(SRC_JSON, encoding="utf-8") as f:
        old_src = json.load(f)
    with open(PTBR_JSON, encoding="utf-8") as f:
        old_ptbr = json.load(f)
    assert len(old_src["strings"]) == len(old_ptbr["strings"]) == 5872
    assert old_src["trailing_len"] == old_ptbr["trailing_len"]

    # Sanity: re-verify the shift=5 correspondence holds for ALL old indices 1..5871
    mismatches = []
    for i in range(1, 5872):
        if list(old_src["strings"][i]) != list(correct_parts[i + 5]):
            mismatches.append(i)
    print(f"shift=5 correspondence check (old_src vs correct): {len(mismatches)} mismatches"
          + (f" e.g. {mismatches[:5]}" if mismatches else ""))
    if mismatches:
        raise SystemExit("Correspondence check failed - aborting, do not proceed blindly.")

    # Build new source: correct_parts[0..5] (6 strings, untranslated/junk) + old_src[1..] shifted
    new_src_strings = [list(p) for p in correct_parts[0:6]] + [list(s) for s in old_src["strings"][1:]]
    new_ptbr_strings = [list(p) for p in correct_parts[0:6]] + [list(s) for s in old_ptbr["strings"][1:]]

    assert len(new_src_strings) == len(correct_parts) == 5877
    assert len(new_ptbr_strings) == 5877

    new_src = {
        "entry_index": 41,
        "source_name": "join",
        "trailing_len": len(correct_trailing),
        "strings": new_src_strings,
    }
    new_ptbr = {
        "entry_index": 41,
        "source_name": "join",
        "trailing_len": len(correct_trailing),
        "strings": new_ptbr_strings,
    }

    with open(SRC_JSON, "w", encoding="utf-8") as f:
        json.dump(new_src, f, ensure_ascii=False, indent=0)
    with open(PTBR_JSON, "w", encoding="utf-8") as f:
        json.dump(new_ptbr, f, ensure_ascii=False, indent=0)
    print(f"wrote corrected {SRC_JSON} and {PTBR_JSON}: {len(new_src_strings)} strings each")


if __name__ == "__main__":
    main()
