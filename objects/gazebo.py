"""
objects/gazebo.py
-----------------
Gazebo / pendopo oktagonal dengan atap kerucut berundak dan bangku dalam.
"""

import math
from core.primitives import color, draw_cylinder, draw_cone, draw_disk, draw_box, draw_sphere


def draw_gazebo(x: float, z: float, radius: float = 2.0):
    posts = 8

    # ── Pondasi / lantai ─────────────────────────────────────────
    color(0.58, 0.40, 0.24)
    draw_disk(x, 0.05, z, radius + 0.5, 8)
    # Step naik
    color(0.62, 0.44, 0.26)
    draw_disk(x, 0.12, z, radius + 0.20, 8)
    color(0.65, 0.46, 0.28)
    draw_disk(x, 0.20, z, radius + 0.05, 8)

    # ── Tiang ────────────────────────────────────────────────────
    color(0.42, 0.26, 0.12)
    for i in range(posts):
        a = i * 2 * math.pi / posts
        px = x + radius * math.cos(a)
        pz = z + radius * math.sin(a)
        draw_cylinder(px, 0.20, pz, 0.10, 2.8, 8)
        # Umpak (basis tiang)
        color(0.50, 0.36, 0.20)
        draw_box(px, 0.20, pz, 0.22, 0.18, 0.22)
        color(0.42, 0.26, 0.12)

    # ── Ring balok keliling ───────────────────────────────────────
    color(0.48, 0.30, 0.15)
    for i in range(posts):
        a1 = i       * 2 * math.pi / posts
        a2 = (i + 1) * 2 * math.pi / posts
        x1 = x + radius * math.cos(a1); z1 = z + radius * math.sin(a1)
        x2 = x + radius * math.cos(a2); z2 = z + radius * math.sin(a2)
        draw_box((x1 + x2) / 2, 2.90, (z1 + z2) / 2,
                 math.hypot(x2 - x1, z2 - z1) + 0.05, 0.14, 0.14)

    # ── Atap bertingkat dua ───────────────────────────────────────
    color(0.62, 0.18, 0.14)
    draw_cone(x, 2.95, z, radius + 0.45, 1.40, 8)
    # Atap atas (lebih kecil)
    color(0.68, 0.20, 0.16)
    draw_cone(x, 4.10, z, 0.80, 0.80, 8)
    # Finial (ujung atap)
    color(0.78, 0.65, 0.30)
    draw_sphere(x, 5.0, z, 0.18)
    draw_cylinder(x, 4.88, z, 0.06, 0.18, 6)

    # ── Bangku dalam gazebo ───────────────────────────────────────
    color(0.45, 0.28, 0.12)
    for i in range(posts):
        a = (i + 0.5) * 2 * math.pi / posts
        bx = x + (radius - 0.45) * math.cos(a)
        bz = z + (radius - 0.45) * math.sin(a)
        draw_box(bx, 0.38, bz, 0.70, 0.07, 0.30)
        # Kaki bangku
        color(0.36, 0.22, 0.10)
        for kx, kz in ((-0.28, -0.10), (0.28, -0.10), (-0.28, 0.10), (0.28, 0.10)):
            draw_cylinder(bx + kx, 0.20, bz + kz, 0.04, 0.19, 4)
        color(0.45, 0.28, 0.12)
