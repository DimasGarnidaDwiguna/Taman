"""
objects/fountain.py
-------------------
Air mancur bertingkat dengan animasi semburan air realistis.
Semburan mengikuti parabola; posisi dihitung per-frame.
"""

import math
from core.primitives import color, draw_cylinder, draw_disk, draw_sphere


_CX, _CZ = 0.0, 0.0   # pusat air mancur


def draw_fountain(fountain_angle_deg: float):
    cx, cz = _CX, _CZ
    fa_rad = math.radians(fountain_angle_deg)

    # ── Kolam bulat ──────────────────────────────────────────────
    # Dinding luar
    color(0.68, 0.65, 0.62)
    draw_cylinder(cx, 0.0, cz, 3.4, 0.35, 32)

    # Air di dalam kolam
    color(0.28, 0.58, 0.80)
    draw_disk(cx, 0.36, cz, 3.15, 48)

    # Refleksi air (lapisan tipis lebih terang)
    color(0.45, 0.72, 0.92)
    draw_disk(cx, 0.38, cz, 2.4, 32)

    # Tepi bagian atas kolam
    color(0.72, 0.70, 0.68)
    draw_cylinder(cx, 0.30, cz, 3.4, 0.10, 32)

    # ── Pedestal tengah ─────────────────────────────────────────
    color(0.75, 0.72, 0.70)
    draw_cylinder(cx, 0.35, cz, 0.55, 0.85, 16)

    # Piringan tengah
    color(0.70, 0.68, 0.66)
    draw_cylinder(cx, 1.15, cz, 1.0, 0.22, 16)
    draw_cylinder(cx, 1.35, cz, 0.95, 0.08, 16)  # bibir

    # Batang penyangga semburan
    color(0.65, 0.62, 0.60)
    draw_cylinder(cx, 1.43, cz, 0.12, 0.60, 10)
    draw_cylinder(cx, 2.00, cz, 0.25, 0.12, 10)  # kepala nozel

    # ── Semburan air (8 jet parabola berputar) ───────────────────
    color(0.70, 0.88, 1.00)
    jets = 8
    for i in range(jets):
        a = fa_rad + i * 2 * math.pi / jets
        jx0 = cx + 0.25 * math.cos(a)
        jz0 = cz + 0.25 * math.sin(a)
        for j in range(7):
            t = j * 0.14
            wx = jx0 + 1.2 * math.cos(a) * t
            wz = jz0 + 1.2 * math.sin(a) * t
            wy = 2.12 + 1.2 * t - 4.0 * t * t    # parabola
            if wy < 0.36:
                wy = 0.36   # jangan menembus lantai kolam
            r_drop = max(0.02, 0.07 - j * 0.008)
            draw_sphere(wx, wy, wz, r_drop, slices=6, stacks=4)

    # ── Semburan tengah (vertikal) ───────────────────────────────
    color(0.80, 0.92, 1.00)
    for j in range(10):
        t = j * 0.14
        wy = 2.12 + 2.5 * t - 5.5 * t * t
        if wy < 0.36:
            break
        draw_sphere(cx, wy, cz, max(0.03, 0.09 - j * 0.007), slices=6, stacks=4)
