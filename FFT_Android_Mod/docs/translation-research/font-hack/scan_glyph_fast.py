import sys
import numpy as np

def decode_2bit_stream(data):
    arr = np.frombuffer(data, dtype=np.uint8)
    # each byte -> 4 values of 2 bits, MSB first
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

def main(path, offsets_in_glyphs, glyph_size=35, w=10, h=14):
    data = open(path, "rb").read()
    n = len(data)
    stream = decode_2bit_stream(data)
    nonzero = (stream != 0).astype(np.int64)
    cum = np.concatenate(([0], np.cumsum(nonzero)))
    n2bit = len(stream)
    pix = w * h  # 140

    # byte-offset candidate range: must leave room for the farthest glyph
    max_delta_bytes = max(offsets_in_glyphs) * glyph_size
    max_base = n - max_delta_bytes - glyph_size
    print(f"file size {n}, scanning {max_base} candidate byte offsets, "
          f"{len(offsets_in_glyphs)} glyph checks each")

    bases = np.arange(0, max_base, dtype=np.int64)
    ok = np.ones(len(bases), dtype=bool)
    for g in offsets_in_glyphs:
        start_bit = (bases + g * glyph_size) * 4
        end_bit = start_bit + pix
        # guard against going past n2bit
        valid = end_bit < len(cum)
        ok &= valid
        cnt = np.zeros(len(bases), dtype=np.int64)
        cnt[valid] = cum[end_bit[valid]] - cum[start_bit[valid]]
        plausible = (cnt >= 15) & (cnt <= 100)
        ok &= plausible

    hit_idx = np.nonzero(ok)[0]
    print(f"{len(hit_idx)} candidate base offsets passed all {len(offsets_in_glyphs)} checks")
    for i in hit_idx[:100]:
        print(hex(int(bases[i])))

if __name__ == "__main__":
    path = sys.argv[1]
    offsets_in_glyphs = [0, 10, 0x880]  # glyph index 0 ('0'), 10 ('A'), 0x880 ('a-acute')
    main(path, offsets_in_glyphs)
