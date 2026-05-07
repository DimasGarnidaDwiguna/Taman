"""
objects/tree.py
---------------
Pohon pinus bertingkat, pohon mahkota bulat, dan pohon palem.
Setiap fungsi menerima posisi dunia + skala opsional.
"""

import math
from core.primitives import color, draw_cylinder, draw_cone, draw_sphere, draw_box


# ────────────────────────────────────────────────────────────────
# Pohon Pinus
# ────────────────────────────────────────────────────────────────
def draw_pine_tree(x, z, scale=1.0):
    tr = 0.14 * scale
    sh = 3.8 * scale     # tinggi batang total

    # Batang — silinder coklat bertekstur
    color(0.38, 0.24, 0.10)
    draw_cylinder(x, 0, z, tr, sh * 0.38, 8)
    color(0.32, 0.20, 0.08)
    draw_cylinder(x, 0, z, tr * 0.6, sh * 0.38, 8)   # garis tekstur

    # Tiga lapisan kerucut (warna makin gelap ke atas)
    layers = [
        (0.08,  0.14, 0.42, 0.50, 0.55),
        (0.30,  0.12, 0.35, 0.44, 0.47),
        (0.52,  0.10, 0.30, 0.38, 0.40),
    ]
    for y_frac, cr, cg, cb_base, cb_tip in layers:
        color(cr, cg, cb_base)
        draw_cone(x, sh * y_frac, z,
                  (0.95 - y_frac * 0.7) * scale,
                  sh * (0.55 - y_frac * 0.20),
                  slices=14)


# ────────────────────────────────────────────────────────────────
# Pohon Mahkota Bulat (mis: beringin, flamboyan)
# ────────────────────────────────────────────────────────────────
def draw_round_tree(x, z, scale=1.0):
    trunk_h = 1.6 * scale
    color(0.38, 0.24, 0.10)
    draw_cylinder(x, 0, z, 0.13 * scale, trunk_h, 8)

    # Mahkota — bola utama + sub-bola untuk siluet tidak bulat sempurna
    ctr_y = trunk_h + 0.9 * scale
    color(0.20, 0.56, 0.16)
    draw_sphere(x, ctr_y, z, 1.0 * scale)
    color(0.24, 0.60, 0.20)
    draw_sphere(x + 0.45 * scale, ctr_y + 0.20 * scale, z - 0.30 * scale, 0.65 * scale)
    draw_sphere(x - 0.40 * scale, ctr_y + 0.10 * scale, z + 0.30 * scale, 0.58 * scale)
    color(0.18, 0.50, 0.14)
    draw_sphere(x + 0.20 * scale, ctr_y - 0.30 * scale, z + 0.50 * scale, 0.55 * scale)


# ────────────────────────────────────────────────────────────────
# Pohon Palem
# ────────────────────────────────────────────────────────────────
def draw_palm_tree(x, z, scale=1.0):
    # Batang sedikit miring ke depan
    h = 4.5 * scale
    color(0.55, 0.40, 0.22)
    draw_cylinder(x, 0, z, 0.16 * scale, h, 10)
    # Cincin batang
    color(0.48, 0.34, 0.18)
    for iy in range(7):
        draw_cylinder(x, iy * h / 7, z, 0.17 * scale, 0.08, 10)

    # Daun (kipas ke 6 arah)
    color(0.20, 0.52, 0.14)
    for i in range(6):
        a = i * math.pi / 3
        lx = x + 1.2 * scale * math.cos(a)
        lz = z + 1.2 * scale * math.sin(a)
        draw_box((x + lx) / 2, h + 0.2 * scale, (z + lz) / 2,
                 1.4 * scale, 0.08 * scale, 0.25 * scale)


# ────────────────────────────────────────────────────────────────
# Kumpulan semua pohon di taman
# ────────────────────────────────────────────────────────────────
def draw_all_trees():
    # Pinus di sepanjang batas taman
    border = [
        (-19, -18), (-15, -19), (-10, -19), (-5, -19),
        (  5, -19), ( 10, -19), ( 15, -19), (19, -18),
        ( 19, -12), ( 19,  -6), ( 19,   0), (19,   6),
        ( 19,  12), (-19, -12), (-19,  -6), (-19,  0),
        (-19,   6), (-19,  12),
    ]
    for px, pz in border:
        draw_pine_tree(px, pz, 1.25)

    # Pohon bulat di area dalam
    inner = [
        (-5, -5), (-3, -10), ( 3, -10), ( 5, -5),
        (-10, -3), (-10, 3), (10,  -3), (10,  3),
        ( -7,  5), (  7,  5), (-3,   8), ( 3,  8),
        (-12, -5), ( 12, -5),
    ]
    for i, (px, pz) in enumerate(inner):
        scale = 0.95 + 0.35 * (i % 3) / 2.0
        draw_round_tree(px, pz, scale)

    # Pinus tersebar ukuran bervariasi
    scatter = [
        (-15, 5), (-16, -2), (-14, 10), (-12, 14),
        ( 14, 10), ( 16,  2), ( 15,  -5), (12, -13),
        ( -5, -14), ( 5, -14), (  0, -16),
        ( -8,  12), (  8, 12),
    ]
    for i, (px, pz) in enumerate(scatter):
        scale = 0.85 + 0.45 * (i % 3) / 2.0
        draw_pine_tree(px, pz, scale)

    # Palem di area depan (dekoratif)
    palm_pos = [(-9, 14), (9, 14), (-16, 14), (16, 14)]
    for px, pz in palm_pos:
        draw_palm_tree(px, pz, 0.85)
