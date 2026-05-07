"""
objects/flower.py
-----------------
Bedeng bunga warna-warni, semak hijau, dan tanaman pagar.
"""

import math
from core.primitives import color, draw_sphere, draw_cylinder, draw_disk, draw_box


def draw_flower_bed(x, z, radius, cr, cg, cb):
    """
    Bedeng bunga elips: tanah gelap + kelopak melingkar + bunga tengah.
    """
    # Tanah bedeng (sedikit lebih tinggi dari rumput)
    color(0.22, 0.16, 0.10)
    draw_disk(x, 0.04, z, radius + 0.1, slices=16)

    # Daun / rumput pendek
    color(0.25, 0.58, 0.18)
    draw_disk(x, 0.06, z, radius, slices=16)

    # Kelopak — 8 bunga melingkar + 1 tengah
    n = 8
    for i in range(n):
        a = i * 2 * math.pi / n
        fx = x + radius * 0.60 * math.cos(a)
        fz = z + radius * 0.60 * math.sin(a)
        # Tangkai
        color(0.20, 0.50, 0.15)
        draw_cylinder(fx, 0.06, fz, 0.03, 0.22, 4)
        # Mahkota bunga
        color(cr, cg, cb)
        draw_sphere(fx, 0.35, fz, 0.13)
        # Putik (kuning)
        color(0.95, 0.88, 0.10)
        draw_sphere(fx, 0.46, fz, 0.06)

    # Bunga tengah
    color(0.20, 0.50, 0.15)
    draw_cylinder(x, 0.06, z, 0.03, 0.25, 4)
    color(cr * 0.85, cg * 0.85, cb * 0.85)
    draw_sphere(x, 0.40, z, 0.15)
    color(0.95, 0.88, 0.10)
    draw_sphere(x, 0.53, z, 0.07)


def draw_bush(x, z, radius=0.55):
    """Semak hijau dengan 3 bola bertumpuk sedikit."""
    color(0.14, 0.48, 0.10)
    draw_sphere(x, radius * 0.8, z, radius)
    color(0.18, 0.54, 0.14)
    draw_sphere(x + radius * 0.55, radius * 0.65, z + radius * 0.25, radius * 0.72)
    color(0.16, 0.50, 0.12)
    draw_sphere(x - radius * 0.40, radius * 0.55, z - radius * 0.30, radius * 0.65)


def draw_all_flowers():
    # Empat bedeng di sekitar air mancur
    draw_flower_bed(-2.5, -2.5, 0.9, 0.92, 0.20, 0.30)
    draw_flower_bed( 2.5, -2.5, 0.9, 0.92, 0.70, 0.10)
    draw_flower_bed(-2.5,  2.5, 0.8, 0.35, 0.60, 0.92)
    draw_flower_bed( 2.5,  2.5, 0.8, 0.92, 0.88, 0.18)

    # Bedeng tersebar di seluruh taman
    beds = [
        (-14,  4, 0.92, 0.22, 0.32),
        (-10,  8, 0.32, 0.62, 0.92),
        ( 10,  8, 0.92, 0.70, 0.12),
        ( 14,  4, 0.22, 0.80, 0.32),
        ( -6,-12, 0.80, 0.22, 0.62),
        (  6,-12, 0.92, 0.80, 0.12),
        (-16, -8, 0.92, 0.32, 0.52),
        ( 16, -8, 0.32, 0.72, 0.92),
        (  0, 10, 0.92, 0.50, 0.20),
        ( -4, -4, 0.75, 0.20, 0.75),
        (  4, -4, 0.20, 0.75, 0.60),
    ]
    for (bx, bz, cr, cg, cb) in beds:
        draw_flower_bed(bx, bz, 0.75, cr, cg, cb)

    # Semak di berbagai sudut
    bushes = [
        (-4, 14), (-2, 14), (2, 14), (4, 14),
        (-17, -4), (-17, 4), (17, -4), (17, 4),
        (-8, -8),  ( 8, -8),
        (-11, 11), (11, 11),
    ]
    for bx, bz in bushes:
        draw_bush(bx, bz)

    # Tanaman pagar (baris depan taman)
    color(0.18, 0.52, 0.14)
    x = -19.5
    while x <= 19.5:
        draw_sphere(x, 0.35, 15.5, 0.32)
        x += 0.55
