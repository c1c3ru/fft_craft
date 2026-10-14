import struct
from PIL import Image

PATH = "/home/c1c3ru/Downloads/finalfantasy/FFT_Android_Mod/src/lib/armeabi/libgl2jni.so"
data = bytearray(open(PATH, "rb").read())
BASE = 0x355e54
W, H = 10, 14

def off(i):
    return BASE + i * 35

def unpack(o):
    px = []
    bitpos = 0
    for i in range(W * H):
        byte_idx = o + (bitpos // 8)
        shift = 6 - (bitpos % 8)
        v = (data[byte_idx] >> shift) & 0x3
        px.append(v)
        bitpos += 2
    return px

def pack(px):
    buf = bytearray(35)
    bitpos = 0
    for v in px:
        byte_idx = bitpos // 8
        shift = 6 - (bitpos % 8)
        buf[byte_idx] |= (v & 0x3) << shift
        bitpos += 2
    return bytes(buf)

def row(px, r):
    return px[r*W:(r+1)*W]

def set_row(px, r, vals):
    for c, v in enumerate(vals):
        px[r*W + c] = v

LETTER_A = unpack(off(0x24))
LETTER_C = unpack(off(0x26))
LETTER_E = unpack(off(0x28))
LETTER_O = unpack(off(0x32))

ACUTE_SRC = unpack(off(0x882))  # e-acute, rows 1-3 hold the acute mark

def with_accent_rows(letter_px, accent_rows_src, rows=(1,2,3)):
    px = list(letter_px)
    for r in rows:
        set_row(px, r, row(accent_rows_src, r))
    return px

# Acute: reuse rows 1-3 from e-acute (á/é/í/ú all share the same accent shape)
def glyph_acute(letter_px):
    return with_accent_rows(letter_px, ACUTE_SRC)

# Circumflex ^
CIRC = [0]*(W*H)
set_row(CIRC, 1, [0,0,3,0,0,0,0,0,0,0])
set_row(CIRC, 2, [0,3,0,3,0,0,0,0,0,0])

def glyph_circ(letter_px):
    return with_accent_rows(letter_px, CIRC)

# Tilde ~
TIL = [0]*(W*H)
set_row(TIL, 1, [0,3,3,0,0,0,0,0,0,0])
set_row(TIL, 2, [0,0,2,3,3,0,0,0,0,0])
set_row(TIL, 3, [0,0,0,0,2,0,0,0,0,0])

def glyph_tilde(letter_px):
    return with_accent_rows(letter_px, TIL)

# Cedilla (goes under the letter, rows 11-13)
def glyph_cedilla(letter_px):
    px = list(letter_px)
    set_row(px, 11, [0,0,3,0,0,0,0,0,0,0])
    set_row(px, 12, [0,0,0,3,0,0,0,0,0,0])
    set_row(px, 13, [0,3,3,0,0,0,0,0,0,0])
    return px

GLYPHS = {
    0x898: ("a-tilde", glyph_tilde(LETTER_A)),
    0x899: ("o-tilde", glyph_tilde(LETTER_O)),
    0x89A: ("c-cedilla", glyph_cedilla(LETTER_C)),
    0x89B: ("a-circ", glyph_circ(LETTER_A)),
    0x89C: ("e-circ", glyph_circ(LETTER_E)),
    0x89D: ("o-circ", glyph_circ(LETTER_O)),
    0x89E: ("o-acute", glyph_acute(LETTER_O)),
}

PALETTE = [(255,255,255,255), (20,20,20,255), (140,140,140,255), (80,80,80,255)]

def render_preview(path):
    cols = len(GLYPHS)
    sheet = Image.new("RGBA", (cols*(W+2), H+2), (255,255,255,255))
    for i, (idx, (name, px)) in enumerate(GLYPHS.items()):
        g = Image.new("RGBA", (W,H))
        for p in range(W*H):
            g.putpixel((p%W, p//W), PALETTE[px[p]])
        sheet.paste(g, (i*(W+2), 1), g)
    sheet = sheet.resize((sheet.width*8, sheet.height*8), Image.NEAREST)
    sheet.save(path)
    print("saved", path)
    for idx, (name, px) in GLYPHS.items():
        print(hex(idx), name)

if __name__ == "__main__":
    render_preview("/tmp/fft_work/new_glyphs_preview.png")
