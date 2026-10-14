import struct, os

path = "/run/media/c1c3ru/18DB-73EA/base/fftpack.bin"
outdir = "/tmp/claude-1000/-home-c1c3ru-Downloads-finalfantasy/c8ce2677-94c6-4cec-9b74-e2cb3804c9bf/scratchpad/entries"
os.makedirs(outdir, exist_ok=True)

with open(path, "rb") as f:
    header = f.read(8)
    count, unk = struct.unpack("<II", header)
    offsets = []
    for i in range(count + 1):
        buf = f.read(4)
        if len(buf) < 4:
            break
        offsets.append(struct.unpack("<I", buf)[0])

    print("num offsets read:", len(offsets), "last offset:", hex(offsets[-1]))
    f.seek(0, os.SEEK_END)
    filesize = f.tell()
    print("file size:", filesize, hex(filesize))

    # sanity: how many entries have nonzero size
    sizes = [offsets[i+1]-offsets[i] for i in range(len(offsets)-1)]
    nonzero = sum(1 for s in sizes if s > 0)
    print("entries:", len(sizes), "nonzero-size:", nonzero, "max size:", max(sizes), "min size:", min(sizes))

    # dump a handful of mid-size entries as samples, plus first 5
    import random
    candidates = list(range(5)) 
    mid_candidates = [i for i,s in enumerate(sizes) if 200 < s < 5000]
    random.seed(1)
    candidates += random.sample(mid_candidates, min(15, len(mid_candidates)))

    for idx in sorted(set(candidates)):
        start, end = offsets[idx], offsets[idx+1]
        f.seek(start)
        blob = f.read(end-start)
        with open(os.path.join(outdir, f"entry_{idx}.bin"), "wb") as out:
            out.write(blob)
    print("dumped", len(set(candidates)), "sample entries to", outdir)
