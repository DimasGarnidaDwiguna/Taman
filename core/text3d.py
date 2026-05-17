"""
core/text3d.py
--------------
Helper menggambar teks 3D pakai bitmap font 3x5 pixel.
Setiap pixel jadi box kecil supaya bisa dibaca dari kejauhan.

API:
    draw_text(text, cx, cy, cz, height, depth=0.04, color_rgb=(0,0,0))
    draw_symbol(name, cx, cy, cz, height, depth=0.04, color_rgb=(0,0,0))

`cx, cy, cz` adalah PUSAT teks (bukan baseline). Teks digambar
menghadap +Z (sumbu depan); ketebalan `depth` ke arah +Z.
"""

from core.primitives import color, draw_box


# ────────────────────────────────────────────────────────────────
# Bitmap font 3x5 (kolom × baris). Setiap karakter = list 5 string
# bertinggi 5 baris, lebar 3 kolom. '#' = pixel on, ' ' = off.
# Baris ke-0 = paling atas.
# ────────────────────────────────────────────────────────────────
_FONT = {
    'A': [
        ' # ',
        '# #',
        '###',
        '# #',
        '# #',
    ],
    'B': [
        '## ',
        '# #',
        '## ',
        '# #',
        '## ',
    ],
    'C': [
        ' ##',
        '#  ',
        '#  ',
        '#  ',
        ' ##',
    ],
    'D': [
        '## ',
        '# #',
        '# #',
        '# #',
        '## ',
    ],
    'E': [
        '###',
        '#  ',
        '###',
        '#  ',
        '###',
    ],
    'F': [
        '###',
        '#  ',
        '###',
        '#  ',
        '#  ',
    ],
    'G': [
        ' ##',
        '#  ',
        '# #',
        '# #',
        ' ##',
    ],
    'H': [
        '# #',
        '# #',
        '###',
        '# #',
        '# #',
    ],
    'I': [
        '###',
        ' # ',
        ' # ',
        ' # ',
        '###',
    ],
    'J': [
        '  #',
        '  #',
        '  #',
        '# #',
        ' # ',
    ],
    'K': [
        '# #',
        '## ',
        '#  ',
        '## ',
        '# #',
    ],
    'L': [
        '#  ',
        '#  ',
        '#  ',
        '#  ',
        '###',
    ],
    'M': [
        '# #',
        '###',
        '# #',
        '# #',
        '# #',
    ],
    'N': [
        '# #',
        '## ',
        '###',
        ' ##',
        '# #',
    ],
    'O': [
        ' # ',
        '# #',
        '# #',
        '# #',
        ' # ',
    ],
    'P': [
        '## ',
        '# #',
        '## ',
        '#  ',
        '#  ',
    ],
    'Q': [
        ' # ',
        '# #',
        '# #',
        '###',
        ' ##',
    ],
    'R': [
        '## ',
        '# #',
        '## ',
        '# #',
        '# #',
    ],
    'S': [
        ' ##',
        '#  ',
        ' # ',
        '  #',
        '## ',
    ],
    'T': [
        '###',
        ' # ',
        ' # ',
        ' # ',
        ' # ',
    ],
    'U': [
        '# #',
        '# #',
        '# #',
        '# #',
        '###',
    ],
    'V': [
        '# #',
        '# #',
        '# #',
        '# #',
        ' # ',
    ],
    'W': [
        '# #',
        '# #',
        '###',
        '###',
        '# #',
    ],
    'X': [
        '# #',
        '# #',
        ' # ',
        '# #',
        '# #',
    ],
    'Y': [
        '# #',
        '# #',
        ' # ',
        ' # ',
        ' # ',
    ],
    'Z': [
        '###',
        '  #',
        ' # ',
        '#  ',
        '###',
    ],
    '0': [
        ' # ',
        '# #',
        '# #',
        '# #',
        ' # ',
    ],
    '1': [
        ' # ',
        '## ',
        ' # ',
        ' # ',
        '###',
    ],
    '2': [
        '## ',
        '  #',
        ' # ',
        '#  ',
        '###',
    ],
    '3': [
        '###',
        '  #',
        ' # ',
        '  #',
        '###',
    ],
    '4': [
        '# #',
        '# #',
        '###',
        '  #',
        '  #',
    ],
    '5': [
        '###',
        '#  ',
        '## ',
        '  #',
        '## ',
    ],
    '6': [
        ' ##',
        '#  ',
        '###',
        '# #',
        '###',
    ],
    '7': [
        '###',
        '  #',
        ' # ',
        '#  ',
        '#  ',
    ],
    '8': [
        '###',
        '# #',
        '###',
        '# #',
        '###',
    ],
    '9': [
        '###',
        '# #',
        '###',
        '  #',
        '## ',
    ],
    ' ': [
        '   ',
        '   ',
        '   ',
        '   ',
        '   ',
    ],
    '.': [
        '   ',
        '   ',
        '   ',
        '   ',
        '#  ',
    ],
    '-': [
        '   ',
        '   ',
        '###',
        '   ',
        '   ',
    ],
}

# Lebar karakter (kolom) dan tinggi (baris)
_FW, _FH = 3, 5


# ────────────────────────────────────────────────────────────────
# Public API
# ────────────────────────────────────────────────────────────────
def draw_text(text: str, cx: float, cy: float, cz: float,
              height: float, depth: float = 0.04,
              color_rgb=(0.0, 0.0, 0.0),
              char_spacing: float = 1.0,
              face: str = 'z'):
    """
    Gambar `text` (uppercase) di sekitar pusat (cx, cy, cz).
    `height` = tinggi total karakter.
    `face` = 'z' menghadap +Z, 'x' menghadap +X.
    """
    text = text.upper()
    pixel = height / _FH                      # ukuran 1 pixel kotak
    char_w = _FW * pixel                      # lebar 1 karakter
    gap    = pixel * char_spacing             # jarak antar karakter
    total_w = len(text) * char_w + max(0, len(text) - 1) * gap

    # Sudut kiri-bawah teks
    x0 = cx - total_w * 0.5
    y0 = cy - height * 0.5

    color(*color_rgb)
    for ci, ch in enumerate(text):
        glyph = _FONT.get(ch, _FONT[' '])
        char_x = x0 + ci * (char_w + gap)
        for row in range(_FH):
            for col in range(_FW):
                if glyph[row][col] != '#':
                    continue
                px = char_x + (col + 0.5) * pixel
                py = y0 + (_FH - row - 0.5) * pixel
                if face == 'z':
                    draw_box(px, py - pixel * 0.5, cz,
                             pixel * 0.95, pixel * 0.95, depth)
                else:  # 'x'
                    draw_box(cx, py - pixel * 0.5, px,
                             depth, pixel * 0.95, pixel * 0.95)


def draw_symbol_P(cx: float, cy: float, cz: float,
                  height: float, depth: float = 0.04,
                  color_rgb=(0.0, 0.0, 0.0)):
    """Simbol parkir 'P' besar di tengah panel."""
    draw_text('P', cx, cy, cz, height, depth, color_rgb)
