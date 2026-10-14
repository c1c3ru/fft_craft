import struct, sys, json, re
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

def split_strings(decoded_text):
    # split on {end} or {close} (string terminators), keep the terminator off
    parts = re.split(r"\{end\}|\{close\}", decoded_text)
    return parts

if __name__ == "__main__":
    offsets = load_offsets(PACK)
    idx = int(sys.argv[1])
    raw = read_entry(PACK, offsets, idx)
    decomp = decompress(raw)
    text = decode_bytes(decomp)
    parts = split_strings(text)
    for i, p in enumerate(parts):
        print(f"{i}\t{p!r}")
