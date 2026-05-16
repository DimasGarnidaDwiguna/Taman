"""
objects/pergola.py
------------------
Pergola kayu dengan tanaman merambat dan bunga.
"""

import math
from core.primitives import color, draw_box, draw_sphere, draw_cylinder


def draw_pergola(x: float, z: float):
    # ── Empat kaki ───────────────────────────────────────────────
    color(0.55, 0.36, 0.18)
    legs = [(-1.6, -1.1), (1.6, -1.1), (-1.6, 1.1), (1.6, 1.1)]
    for lx, lz in legs:
        draw_box(x + lx, 0, z + lz, 0.18, 2.6, 0.18)
        # Umpak beton
        color(0.85, 0.82, 0.76)
        draw_box(x + lx, 0, z + lz, 0.30, 0.18, 0.30)
        color(0.55, 0.36, 0.18)

    # ── Dua balok panjang (membujur) ─────────────────────────────
    color(0.58, 0.38, 0.20)
    draw_box(x, 2.42, z - 1.1, 3.6, 0.16, 0.16)
    draw_box(x, 2.42, z + 1.1, 3.6, 0.16, 0.16)

    # ── Kasau melintang (7 buah) ─────────────────────────────────
    color(0.52, 0.34, 0.16)
    for i in range(7):
        bx = x - 1.5 + i * 0.50
        draw_box(bx, 2.50, z, 0.12, 0.12, 2.40)

    # ── Tanaman merambat ─────────────────────────────────────────
    color(0.22, 0.62, 0.20)
    for i in range(7):
        bx = x - 1.5 + i * 0.50
        for j in range(3):
            oz = z - 0.8 + j * 0.8
            draw_sphere(bx, 2.62, oz, 0.20)

    # Bunga merah & ungu kecil
    color(0.92, 0.20, 0.20)
    for i in range(4):
        bx = x - 1.2 + i * 0.80
        draw_sphere(bx, 2.74, z + 0.4, 0.11)
    color(0.78, 0.30, 0.85)
    for i in range(3):
        bx = x - 1.0 + i * 1.0
        draw_sphere(bx, 2.74, z - 0.5, 0.10)

    # Sulur merambat di kaki
    color(0.24, 0.65, 0.22)
    for side_z in (z - 1.1, z + 1.1):
        for lx in (-1.6, 1.6):
            for iy in range(5):
                wy = 0.3 + iy * 0.45
                draw_sphere(x + lx, wy, side_z, 0.13)
