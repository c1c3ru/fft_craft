import struct, sys

path = "/run/media/c1c3ru/18DB-73EA/base/fftpack.bin"
with open(path, "rb") as f:
    data = f.read(4096)

count, = struct.unpack_from("<I", data, 0)
unk, = struct.unpack_from("<I", data, 4)
print("count:", count, "unk:", unk)

offsets = []
pos = 8
for i in range(min(count, 30)):
    val, = struct.unpack_from("<I", data, pos)
    offsets.append(val)
    pos += 4

for i, o in enumerate(offsets):
    print(i, hex(o), o)
