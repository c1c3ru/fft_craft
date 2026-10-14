import sys
import numpy as np

def decode_2bit_stream(data, lsb_first=False):
    arr = np.frombuffer(data, dtype=np.uint8)
    if lsb_first:
        v0 = arr & 0x3
        v1 = (arr >> 2) & 0x3
        v2 = (arr >> 4) & 0x3
        v3 = (arr >> 6) & 0x3
    else:
        v0 = (arr >> 6) & 0x3
        v1 = (arr >> 4) & 0x3
        v2 = (arr >> 2) & 0x3
        v3 = arr & 0x3
    stream = np.empty(len(arr) * 4, dtype=np.uint8)
    stream[0::4] = v0
    stream[1::4] = v1
    stream[2::4] = v2
    stream[3::4] = v3
    return stream

def main(path, offsets_in_glyphs, glyph_size=35, pix=140, lsb_first=False, lo=15, hi=100):
    data = open(path, "rb").read()
    n = len(data)
    stream = decode_2bit_stream(data, lsb_first=lsb_first)
    nonzero = (stream != 0).astype(np.int64)
    cum = np.concatenate(([0], np.cumsum(nonzero)))

    max_delta_bytes = max(offsets_in_glyphs) * glyph_size
    max_base = n - max_delta_bytes - glyph_size

    bases = np.arange(0, max_base, dtype=np.int64)
    ok = np.ones(len(bases), dtype=bool)
    for g in offsets_in_glyphs:
        start_bit = (bases + g * glyph_size) * 4
        end_bit = start_bit + pix
        valid = end_bit < len(cum)
        ok &= valid
        cnt = np.zeros(len(bases), dtype=np.int64)
        cnt[valid] = cum[end_bit[valid]] - cum[start_bit[valid]]
        plausible = (cnt >= lo) & (cnt <= hi)
        ok &= plausible

    hit_idx = np.nonzero(ok)[0]
    print(f"lsb_first={lsb_first} lo={lo} hi={hi}: {len(hit_idx)} hits")
    return [int(bases[i]) for i in hit_idx]

if __name__ == "__main__":
    path = sys.argv[1]
    offsets_in_glyphs = [0,1,2,3,10,11,0x880]
    for lsb in (False, True):
        hits = main(path, offsets_in_glyphs, lsb_first=lsb, lo=10, hi=60)
        for h in hits[:15]:
            print(" ", hex(h))
