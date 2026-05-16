"""
objects/tree.py
---------------
Pohon low-poly bergaya kartun:
  - Pohon pinus: kerucut tinggi tajam (Christmas tree style) — ciri khas referensi
  - Pohon mahkota bulat: cluster bola untuk siluet rimbun
  - Pohon palem: untuk variasi area depan
"""

import math
from core.primitives import color, draw_cylinder, draw_cone, draw_sphere, draw_box
from core.layout    import is_blocked, register_zone


# ────────────────────────────────────────────────────────────────
# Pohon Pinus — kerucut tunggal tinggi (style referensi)
# ────────────────────────────────────────────────────────────────
def draw_pine_tree(x, z, scale=1.0):
    # Batang pendek
    trunk_h = 0.55 * scale
    color(0.42, 0.27, 0.14)
    draw_cylinder(x, 0, z, 0.16 * scale, trunk_h, 8)

    # Mahkota: kerucut tinggi & runcing — warna hijau cyan saturated
    cone_h = 4.6 * scale
    cone_r = 1.05 * scale

    color(0.16, 0.55, 0.42)
    draw_cone(x, trunk_h, z, cone_r, cone_h, slices=14)

    # Highlight kerucut kecil di puncak (lebih terang) untuk dimensi
    color(0.28, 0.66, 0.50)
    draw_cone(x, trunk_h + cone_h * 0.50, z,
              cone_r * 0.55, cone_h * 0.55, slices=12)


# ────────────────────────────────────────────────────────────────
# Pohon Mahkota Bulat
# ────────────────────────────────────────────────────────────────
def draw_round_tree(x, z, scale=1.0):
    trunk_h = 1.4 * scale
    color(0.45, 0.30, 0.15)
    draw_cylinder(x, 0, z, 0.16 * scale, trunk_h, 8)

    # Mahkota — beberapa bola membentuk siluet rimbun
    ctr_y = trunk_h + 0.85 * scale
    color(0.30, 0.72, 0.32)
    draw_sphere(x, ctr_y, z, 1.10 * scale)
    color(0.36, 0.78, 0.36)
    draw_sphere(x + 0.50 * scale, ctr_y + 0.25 * scale, z - 0.30 * scale, 0.70 * scale)
    draw_sphere(x - 0.45 * scale, ctr_y + 0.15 * scale, z + 0.35 * scale, 0.65 * scale)
    color(0.26, 0.65, 0.28)
    draw_sphere(x + 0.20 * scale, ctr_y - 0.30 * scale, z + 0.55 * scale, 0.60 * scale)
    draw_sphere(x - 0.25 * scale, ctr_y - 0.20 * scale, z - 0.50 * scale, 0.55 * scale)


# ────────────────────────────────────────────────────────────────
# Pohon Palem
# ────────────────────────────────────────────────────────────────
def draw_palm_tree(x, z, scale=1.0):
    h = 4.5 * scale
    color(0.58, 0.42, 0.24)
    draw_cylinder(x, 0, z, 0.16 * scale, h, 10)
    color(0.48, 0.34, 0.18)
    for iy in range(7):
        draw_cylinder(x, iy * h / 7, z, 0.17 * scale, 0.08, 10)

    # Daun melengkung ke 6 arah
    color(0.24, 0.62, 0.18)
    for i in range(6):
        a = i * math.pi / 3
        lx = x + 1.4 * scale * math.cos(a)
        lz = z + 1.4 * scale * math.sin(a)
        draw_box((x + lx) / 2, h + 0.2 * scale, (z + lz) / 2,
                 1.6 * scale, 0.10 * scale, 0.30 * scale)


# ────────────────────────────────────────────────────────────────
# Kumpulan semua pohon
# ────────────────────────────────────────────────────────────────
def draw_all_trees():
    """Pohon dipasang di posisi yang TIDAK menabrak struktur besar."""

    # Buffer 1.2m karena mahkota pohon bulat ber-radius ~1m
    BUF = 1.2

    # ── Pohon bulat (round) di sepanjang batas taman ─────────────
    border = []
    bx = -19
    while bx <= 19:
        border.append((bx, -19))
        bx += 2.6
    bz = -16
    while bz <= 12:
        border.append((-19, bz))
        border.append(( 19, bz))
        bz += 2.6

    for i, (px, pz) in enumerate(border):
        if is_blocked(px, pz, BUF):
            continue
        sc = 1.00 + 0.25 * ((i * 3) % 5) / 4.0
        draw_round_tree(px, pz, sc)
        register_zone(px, pz, 0.9 * sc)

    # ── Pohon bulat tersebar di area dalam ───────────────────────
    inner = [
        (-5, -5), (-3, -10), ( 3, -10), ( 5, -5),
        (-10, -3), (-10, 3), (10,  -3), (10,  3),
        ( -7,  5), (  7,  5), (-3,   8), ( 3,  8),
        (-12, -5),
        (-15, 5), (-13, 11), (-12, -8),
        (-8, 12), ( 8, 12),
        (-2, -14), (-7, -14),
    ]
    for i, (px, pz) in enumerate(inner):
        if is_blocked(px, pz, BUF):
            continue
        scale = 0.95 + 0.30 * (i % 3) / 2.0
        draw_round_tree(px, pz, scale)
        register_zone(px, pz, 0.9 * scale)

    # ── Palem di area depan (dekorasi gerbang, di luar pagar) ────
    palm_pos = [(-9, 14), (9, 14)]
    for px, pz in palm_pos:
        if is_blocked(px, pz, 0.8):
            continue
        draw_palm_tree(px, pz, 0.85)
