"""
objects/pergola.py
------------------
Pergola kayu dengan tanaman merambat dan bunga.
"""

import math
from core.primitives import color, draw_box, draw_sphere, draw_cylinder


def draw_pergola(x: float, z: float):
    # ── Empat kaki ───────────────────────────────────────────────
    color(0.42, 0.28, 0.14)
    legs = [(-1.6, -1.1), (1.6, -1.1), (-1.6, 1.1), (1.6, 1.1)]
    for lx, lz in legs:
        draw_box(x + lx, 0, z + lz, 0.16, 2.5, 0.16)
        # Umpak beton
        color(0.55, 0.52, 0.50)
        draw_box(x + lx, 0, z + lz, 0.28, 0.18, 0.28)
        color(0.42, 0.28, 0.14)

    # ── Dua balok panjang (membujur) ─────────────────────────────
    color(0.45, 0.30, 0.16)
    draw_box(x, 2.35, z - 1.1, 3.5, 0.14, 0.14)
    draw_box(x, 2.35, z + 1.1, 3.5, 0.14, 0.14)

    # ── Kasau melintang (7 buah) ─────────────────────────────────
    color(0.40, 0.26, 0.13)
    for i in range(7):
        bx = x - 1.5 + i * 0.50
        draw_box(bx, 2.42, z, 0.10, 0.10, 2.40)

    # ── Tanaman merambat ─────────────────────────────────────────
    # Daun di sepanjang kasau
    color(0.18, 0.52, 0.14)
    for i in range(7):
        bx = x - 1.5 + i * 0.50
        for j in range(3):
            oz = z - 0.8 + j * 0.8
            draw_sphere(bx, 2.52, oz, 0.18)

    # Bunga merah kecil
    color(0.88, 0.18, 0.18)
    for i in range(4):
        bx = x - 1.2 + i * 0.80
        draw_sphere(bx, 2.64, z + 0.4, 0.10)

    # Sulur merambat di kaki
    color(0.20, 0.55, 0.16)
    for side_z in (z - 1.1, z + 1.1):
        for lx in (-1.6, 1.6):
            for iy in range(5):
                wy = 0.3 + iy * 0.45
                draw_sphere(x + lx, wy, side_z, 0.12)
