import sys
from PIL import Image

PALETTE = [(255,255,255,255), (20,20,20,255), (140,140,140,255), (80,80,80,255)]

def decode_glyph(data, off, w=10, h=14):
    img = Image.new("RGBA", (w, h))
    bitpos = 0
    px = []
    for i in range(w*h):
        byte_idx = off + (bitpos // 8)
        if byte_idx >= len(data):
            px.append(0)
            bitpos += 2
            continue
        shift = 6 - (bitpos % 8)
        val = (data[byte_idx] >> shift) & 0x3
        px.append(val)
        bitpos += 2
    for i, v in enumerate(px):
        x, y = i % w, i // w
        img.putpixel((x, y), PALETTE[v])
    return img

def render_strip(data, base, count=64, w=10, h=14, glyph_size=35, cols=16):
    rows = (count + cols - 1) // cols
    sheet = Image.new("RGBA", (cols*(w+2), rows*(h+2)), (255,255,255,255))
    for i in range(count):
        off = base + i*glyph_size
        g = decode_glyph(data, off, w, h)
        gx = (i % cols) * (w+2)
        gy = (i // cols) * (h+2)
        sheet.paste(g, (gx, gy), g)
    return sheet

if __name__ == "__main__":
    path = sys.argv[1]
    base = int(sys.argv[2], 0)
    out = sys.argv[3]
    count = int(sys.argv[4]) if len(sys.argv) > 4 else 64
    data = open(path, "rb").read()
    sheet = render_strip(data, base, count=count)
    sheet = sheet.resize((sheet.width*3, sheet.height*3), Image.NEAREST)
    sheet.save(out)
    print("saved", out)
