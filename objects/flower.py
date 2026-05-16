"""
objects/flower.py
-----------------
Bedeng bunga warna-warni cerah, semak hijau, dan tanaman pagar.
Style: low-poly cluster ketat seperti pada referensi (banyak bola
kecil warna-warni di atas dasar hijau).
"""

import math
from core.primitives import color, draw_sphere, draw_cylinder, draw_disk, draw_box
from core.layout     import is_blocked, register_zone


def draw_flower_bed(x, z, radius, cr, cg, cb):
    """
    Bedeng bunga: cluster bola warna kelopak di atas dasar hijau.
    """
    # Tanah bedeng (sedikit lebih tinggi dari rumput)
    color(0.30, 0.20, 0.12)
    draw_disk(x, 0.04, z, radius + 0.10, slices=14)

    # Daun / dasar hijau cerah
    color(0.30, 0.72, 0.32)
    draw_disk(x, 0.07, z, radius, slices=14)

    # Cluster bunga: 9-13 bunga padat
    n = 11
    for i in range(n):
        a = i * 2 * math.pi / n + (i % 3) * 0.4
        rr = radius * (0.30 + 0.55 * ((i * 5 + 3) % 7) / 6.0)
        fx = x + rr * math.cos(a)
        fz = z + rr * math.sin(a)
        # Variasi warna kecil
        var = 1.0 + 0.10 * ((i % 3) - 1)
        color(min(cr * var, 1.0), min(cg * var, 1.0), min(cb * var, 1.0))
        draw_sphere(fx, 0.22, fz, 0.16)

    # Bunga tengah (lebih besar, ditemani putik kuning)
    color(cr, cg, cb)
    draw_sphere(x, 0.28, z, 0.20)
    color(0.98, 0.88, 0.18)
    draw_sphere(x, 0.42, z, 0.07)


def draw_bush(x, z, radius=0.55):
    """Semak hijau dengan 3 bola bertumpuk."""
    color(0.18, 0.58, 0.18)
    draw_sphere(x, radius * 0.8, z, radius)
    color(0.22, 0.65, 0.22)
    draw_sphere(x + radius * 0.55, radius * 0.65, z + radius * 0.25, radius * 0.72)
    color(0.20, 0.62, 0.20)
    draw_sphere(x - radius * 0.40, radius * 0.55, z - radius * 0.30, radius * 0.65)


def draw_all_flowers():
    # Empat bedeng di sekitar air mancur (di luar basin r=2.8)
    fountain_beds = [
        (-3.5, -3.5, 0.95, 0.20, 0.30),   # merah
        ( 3.5, -3.5, 0.98, 0.72, 0.10),   # oranye
        (-3.5,  3.5, 0.30, 0.55, 0.95),   # biru
        ( 3.5,  3.5, 0.95, 0.92, 0.20),   # kuning
    ]
    for fx, fz, cr, cg, cb in fountain_beds:
        draw_flower_bed(fx, fz, 0.85, cr, cg, cb)
        register_zone(fx, fz, 1.0)

    # Bedeng tersebar
    beds = [
        (-14,  8, 0.95, 0.22, 0.32),    # dipindah dari (-14,4) → menabrak pergola
        (-10,  8, 0.32, 0.62, 0.95),
        ( 10,  8, 0.95, 0.72, 0.12),
        ( 14,  8, 0.22, 0.80, 0.32),    # dipindah dari (14,4) → menabrak gazebo
        ( -6,-12, 0.80, 0.22, 0.62),
        (  6,-12, 0.95, 0.80, 0.15),
        (-16, -8, 0.92, 0.32, 0.52),
        (  0, 10, 0.95, 0.50, 0.20),
        ( -4, -4, 0.78, 0.22, 0.78),
        (  4, -4, 0.22, 0.78, 0.62),
    ]
    for (bx, bz, cr, cg, cb) in beds:
        if is_blocked(bx, bz, 0.9):
            continue
        draw_flower_bed(bx, bz, 0.78, cr, cg, cb)
        register_zone(bx, bz, 0.95)

    # Semak di berbagai sudut
    bushes = [
        (-4, 14), (-2, 14), (2, 14), (4, 14),
        (-17, -4), (-17, 4), (17, -4), (17, 4),
        (-11, 11), (11, 11),
        (-6, -2), (6, -2),
    ]
    for bx, bz in bushes:
        if is_blocked(bx, bz, 0.6):
            continue
        draw_bush(bx, bz)
        register_zone(bx, bz, 0.7)

    # Tanaman pagar (baris depan taman) — sisakan celah ±3.5 untuk
    # pintu masuk gerbang
    color(0.22, 0.62, 0.20)
    x = -19.5
    while x <= 19.5:
        if -3.5 <= x <= 3.5:
            x += 0.55
            continue
        draw_sphere(x, 0.35, 15.4, 0.32)
        x += 0.55
