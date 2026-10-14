import struct, sys
sys.path.insert(0, "tools")
from fft_text import decompress, decode_bytes

PACK = "/run/media/c1c3ru/18DB-73EA/base/fftpack.bin"

def load_offsets(path):
    with open(path, "rb") as f:
        count, unk = struct.unpack("<II", f.read(8))
        offsets = list(struct.unpack("<%dI" % (count + 1), f.read(4 * (count + 1))))
    return offsets

def read_entry(path, offsets, idx):
    start, end = offsets[idx], offsets[idx + 1]
    with open(path, "rb") as f:
        f.seek(start)
        return f.read(end - start)

offsets = load_offsets(PACK)

names = {
    17: "event_test_evt.bin",
    18: "event_evtface_bin.bin",
    19: "event_unit_bin.bin",
    20: "event_btlevt_bin.bin",
    36: "text_sys/atchelp.lzw",
    37: "text_sys/spell.mes",
    38: "text_sys/sample.lzw",
    39: "text_sys/world.lzw",
    40: "text_sys/open.lzw",
    41: "text_sys/join.lzw",
    42: "text_sys/help.lzw",
    43: "text_sys/wldhelp.lzw",
}

for idx, name in names.items():
    raw = read_entry(PACK, offsets, idx)
    print(f"=== entry {idx} ({name}) size={len(raw)} ===")
    if len(raw) == 0:
        continue
    decomp = decompress(raw)
    text_raw = decode_bytes(raw[:400])
    text_decomp = decode_bytes(decomp[:400])
    print("RAW decode (first 400 bytes):")
    print(text_raw[:500])
    print("--- DECOMPRESSED decode (first 400 bytes of decompressed) ---")
    print(text_decomp[:500])
    print()
