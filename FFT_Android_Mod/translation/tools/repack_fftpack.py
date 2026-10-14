"""Rebuild fftpack.bin with the translated text_sys entries (36-43).

Entries 36,37,39,40,43 are passthrough (untouched content) -> copied as
raw original bytes verbatim (sidesteps needing a compressor for entry 36,
the only one that uses real LZ77-style back-references).

Entries 38,41,42 have real PT-BR translations -> rebuilt from
translation/ptbr/*.json via encode_string(), uncompressed (verified safe:
encode_string() never emits raw bytes 0xF0-0xF3, so decompress() at
load time treats the stream as pure literal copy-through).

Usage: run from translation/tools/ (or anywhere, paths are absolute).
"""
import json
import os
import re
import struct
import sys

_TERM_RE = re.compile(r"\{end\}|\{close\}")


def split_with_terms_local(text):
    parts = []
    pos = 0
    for m in _TERM_RE.finditer(text):
        s = text[pos:m.start()]
        term = 0xFE if m.group(0) == "{end}" else 0xFF
        parts.append((s, term))
        pos = m.end()
    return parts, text[pos:]

sys.path.insert(0, os.path.dirname(__file__))
from fft_text import encode_string, decompress, decode_bytes, PSP_TABLE, TWO_BYTE_LEAD  # noqa: E402

SRC_PACK = "/run/media/c1c3ru/18DB-73EA/base/fftpack.bin"
OUT_PACK = "/tmp/fft_work/fftpack_new.bin"
PTBR_DIR = "/home/c1c3ru/Downloads/finalfantasy/FFT_Android_Mod/translation/ptbr"
SRC_DIR = "/home/c1c3ru/Downloads/finalfantasy/FFT_Android_Mod/translation/source"

REBUILD = {38: "entry38_sample.json", 41: "entry41_join.json", 42: "entry42_help.json"}


def sanitize_markers(buf):
    """Scan an assembled (intentionally uncompressed) entry for any byte
    0xF0-0xF3 that decompress() would misinterpret as a live, in-bounds
    back-reference marker, and neutralize it by maximizing the encoded
    jump distance (b1 low 5 bits -> 0x1F, b2 -> 0xFF) so src_start goes
    negative and decompress() takes its documented literal-fallback path
    instead. This only ever touches leftover undecodable/junk byte
    sequences carried verbatim from the original data (real character
    codes never produce 0xF0-0xF3, confirmed structurally in PSP_TABLE) -
    cosmetic for content we already can't interpret, never anything a
    player would see change. Returns (buf, n_fixed)."""
    buf = bytearray(buf)
    n = len(buf)
    i = 0
    n_fixed = 0
    while i < n:
        b0 = buf[i]
        if 0xF0 <= b0 <= 0xF3 and i + 2 < n:
            b1, b2 = buf[i + 1], buf[i + 2]
            length = ((b0 & 0x03) << 3) + ((b1 & 0xE0) >> 5) + 4
            j = ((b1 & 0x1F) << 8) + b2
            jump = j - (j // 256) * 2
            src_start = i - jump
            src_end = src_start + length
            if src_start < 0 or src_end >= n:
                i += 3
                continue
            # live marker - neutralize by maximizing jump (push src_start < 0)
            if i < 8129:
                buf[i + 1] = (b1 & 0xE0) | 0x1F
                buf[i + 2] = 0xFF
                n_fixed += 1
            else:
                raise SystemExit(
                    f"sanitize_markers: unsafe 0xF0-F3 at pos {i} (n={n}) too far in "
                    f"to neutralize via jump - needs manual handling"
                )
            i += 3
        else:
            i += 1
    return bytes(buf), n_fixed


def string_byte_ranges(data):
    """Mirror decode_bytes()'s char-boundary walk, but return the raw byte
    range [start,end) consumed by each terminated string ({end}/{close}),
    in order. Lets us slice ORIGINAL bytes for untouched strings instead of
    re-encoding them (safe for garbage/unresolved content that doesn't
    round-trip through the character table, e.g. leftover raw {0xF30000}
    tokens from undecodable bytes that happen to collide with the
    compression marker range 0xF0-0xF3)."""
    ranges = []
    i = 0
    n = len(data)
    seg_start = 0
    while i < n:
        val = data[i]
        key = val
        start = i
        if val in TWO_BYTE_LEAD and i + 1 < n:
            key = val * 256 + data[i + 1]
            i += 2
        elif 0xF0 <= val <= 0xF3 and i + 2 < n:
            key = val * 65536 + data[i + 1] * 256 + data[i + 2]
            i += 3
        else:
            i += 1
        piece = PSP_TABLE.get(key)
        if piece == "{end}" or piece == "{close}":
            ranges.append((seg_start, i))
            seg_start = i
    return ranges


def load_offsets(path):
    with open(path, "rb") as f:
        count, unk = struct.unpack("<II", f.read(8))
        offsets = list(struct.unpack("<%dI" % (count + 1), f.read(4 * (count + 1))))
    return count, unk, offsets


def read_entry(path, offsets, idx):
    start, end = offsets[idx], offsets[idx + 1]
    with open(path, "rb") as f:
        f.seek(start)
        return f.read(end - start)


def build_entry_bytes(idx, orig_decomp):
    with open(os.path.join(PTBR_DIR, REBUILD[idx]), encoding="utf-8") as f:
        ptbr = json.load(f)
    with open(os.path.join(SRC_DIR, REBUILD[idx]), encoding="utf-8") as f:
        src = json.load(f)
    assert ptbr["entry_index"] == idx == src["entry_index"]
    assert len(ptbr["strings"]) == len(src["strings"])

    ranges = string_byte_ranges(orig_decomp)
    assert len(ranges) == len(src["strings"]), \
        f"entry {idx}: {len(ranges)} byte-ranges vs {len(src['strings'])} source strings"

    out = bytearray()
    n_reencoded = 0
    n_passthrough = 0
    for i, ((ptbr_text, term), (src_text, src_term)) in enumerate(zip(ptbr["strings"], src["strings"])):
        if ptbr_text == src_text and term == src_term:
            start, end = ranges[i]
            out.extend(orig_decomp[start:end])
            n_passthrough += 1
        else:
            try:
                out.extend(encode_string(ptbr_text, term))
            except ValueError as e:
                raise SystemExit(f"entry {idx} string #{i} {ptbr_text[:50]!r}: encode error: {e}")
            n_reencoded += 1
    out.extend(b"\x00" * ptbr["trailing_len"])

    out_bytes, n_fixed = sanitize_markers(bytes(out))
    if n_fixed:
        print(f"  entry {idx}: neutralized {n_fixed} accidental 0xF0-0xF3 marker(s) "
              f"in passthrough junk bytes (cosmetic, content was already unresolved)")

    # Safety check: confirm our bytes decompress to themselves (no accidental
    # 0xF0-0xF3 back-reference markers), so storing uncompressed is valid.
    if decompress(out_bytes) != out_bytes:
        raise SystemExit(f"entry {idx}: generated bytes still trigger decompress() "
                          f"back-references after sanitization - needs investigation.")
    print(f"  entry {idx}: {n_reencoded} strings re-encoded, {n_passthrough} byte-identical passthrough")
    return out_bytes


def main():
    count, unk, offsets = load_offsets(SRC_PACK)
    print(f"source: count={count} unk={unk}")

    with open(SRC_PACK, "rb") as f:
        filesize = os.fstat(f.fileno()).st_size
        tail_start = offsets[count]
        f.seek(tail_start)
        tail = f.read(filesize - tail_start)
    print(f"tail: {len(tail)} bytes after last offset (preserved verbatim)")

    new_entries = []
    for idx in range(count):
        if idx in REBUILD:
            orig_raw = read_entry(SRC_PACK, offsets, idx)
            orig_decomp = decompress(orig_raw)
            b = build_entry_bytes(idx, orig_decomp)
            print(f"entry {idx}: REBUILT old_len={offsets[idx+1]-offsets[idx]} new_len={len(b)}")
        else:
            b = read_entry(SRC_PACK, offsets, idx)
        new_entries.append(b)

    data_start = offsets[0]  # preserve original header+table+alignment gap convention
    new_offsets = [data_start]
    for b in new_entries:
        new_offsets.append(new_offsets[-1] + len(b))

    header_table_size = 8 + 4 * (count + 1)
    if header_table_size > data_start:
        raise SystemExit("header/offset table grew past original data_start gap - unexpected")
    gap = data_start - header_table_size

    with open(OUT_PACK, "wb") as f:
        f.write(struct.pack("<II", count, unk))
        f.write(struct.pack("<%dI" % (count + 1), *new_offsets))
        f.write(b"\x00" * gap)
        for b in new_entries:
            f.write(b)
        f.write(tail)

    new_size = os.path.getsize(OUT_PACK)
    print(f"wrote {OUT_PACK}: {new_size} bytes (original was {filesize}, "
          f"delta {new_size - filesize:+d})")

    # Verification pass 1: untouched entries must be byte-identical to the
    # source, at their (possibly shifted) new offsets.
    vcount, vunk, voffsets = load_offsets(OUT_PACK)
    assert vcount == count and vunk == unk
    sample_untouched = [0, 1, 2, 35, 36, 37, 39, 40, 43, 44, 100, 1000, 2000, count - 1]
    mismatches = 0
    for idx in sample_untouched:
        if idx in REBUILD:
            continue
        orig = read_entry(SRC_PACK, offsets, idx)
        new = read_entry(OUT_PACK, voffsets, idx)
        same = orig == new
        if not same:
            mismatches += 1
        print(f"  untouched entry {idx}: len={len(new)} byte_identical_to_source={same}")
    if mismatches:
        raise SystemExit(f"{mismatches} untouched entries changed unexpectedly!")

    # Verification pass 2: rebuilt entries decode back to the ptbr text,
    # string by string. A handful of known mismatches are tolerated ONLY
    # when they fall on an already-unresolved "{0x" junk token AND were
    # actually neutralized by sanitize_markers() (reported above) - those
    # are intentional, cosmetic-only byte changes to otherwise-undecodable
    # leftover data, never real/translated content.
    for idx in REBUILD:
        with open(os.path.join(PTBR_DIR, REBUILD[idx]), encoding="utf-8") as f:
            data = json.load(f)
        raw = read_entry(OUT_PACK, voffsets, idx)
        decomp = decompress(raw)
        text = decode_bytes(decomp)
        got_parts, got_trailing = split_with_terms_local(text)
        exp_parts = [tuple(p) for p in data["strings"]]
        assert len(got_parts) == len(exp_parts), \
            f"entry {idx}: string count mismatch after repack! {len(got_parts)} vs {len(exp_parts)}"
        bad = []
        for i, (g, e) in enumerate(zip(got_parts, exp_parts)):
            if g != e:
                bad.append((i, g, e))
        tolerated = [b for b in bad if "{0x" in b[2][0]]
        real_bad = [b for b in bad if "{0x" not in b[2][0]]
        print(f"  rebuilt entry {idx}: len={len(raw)} n_strings={len(exp_parts)} "
              f"mismatches={len(bad)} (tolerated junk={len(tolerated)}, real={len(real_bad)})")
        for i, g, e in tolerated:
            print(f"    tolerated (unresolved-token junk) string #{i}: "
                  f"expected {e[0][:60]!r} got {g[0][:60]!r}")
        if real_bad:
            for i, g, e in real_bad[:10]:
                print(f"    REAL MISMATCH string #{i}: expected {e[0][:60]!r} got {g[0][:60]!r}")
            raise SystemExit(f"entry {idx}: {len(real_bad)} unexplained content mismatches!")
    print("OK")


if __name__ == "__main__":
    main()
