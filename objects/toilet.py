"""
objects/toilet.py
-----------------
Toilet umum modern: dua bilik (L/P), panel surya di atap,
tanda, dan aksesibilitas difabel.
"""

from core.primitives import color, draw_box, draw_cylinder, draw_sphere, draw_disk


_TX, _TZ = -15.0, -11.0


def draw_toilet():
    tx, tz = _TX, _TZ

    # ── Dinding bangunan ─────────────────────────────────────────
    color(0.70, 0.70, 0.68)
    draw_box(tx, 0, tz, 4.0, 2.8, 3.0)

    # Sekat tengah (pembagi bilik L / P)
    color(0.65, 0.65, 0.63)
    draw_box(tx, 0, tz, 0.14, 2.7, 3.0)

    # ── Atap pelana ───────────────────────────────────────────────
    color(0.28, 0.28, 0.30)
    # Sisi kiri & kanan
    for sx in (-2.1, 2.1):
        draw_box(tx + sx, 2.8, tz, 0.15, 0.55, 3.10)
    # Bubungan
    draw_box(tx, 3.30, tz, 4.20, 0.16, 0.20)

    # ── Panel surya ───────────────────────────────────────────────
    color(0.10, 0.14, 0.22)
    draw_box(tx, 2.86, tz, 3.40, 0.10, 2.60)
    # Garis sel surya
    color(0.14, 0.18, 0.28)
    for ix in range(4):
        draw_box(tx - 1.5 + ix * 1.0, 2.92, tz, 0.04, 0.04, 2.58)
    for iz in range(5):
        draw_box(tx, 2.92, tz - 1.2 + iz * 0.60, 3.38, 0.04, 0.04)

    # ── Dua pintu ────────────────────────────────────────────────
    color(0.32, 0.22, 0.10)
    draw_box(tx - 1.1, 0, tz + 1.52, 0.65, 2.10, 0.08)
    draw_box(tx + 1.1, 0, tz + 1.52, 0.65, 2.10, 0.08)

    # Gagang pintu
    color(0.70, 0.68, 0.58)
    draw_sphere(tx - 0.80, 1.0, tz + 1.57, 0.07)
    draw_sphere(tx + 0.80, 1.0, tz + 1.57, 0.07)

    # ── Papan tanda ───────────────────────────────────────────────
    color(0.92, 0.92, 0.90)
    draw_box(tx, 2.35, tz + 1.52, 1.60, 0.48, 0.06)

    # Simbol L (biru)
    color(0.20, 0.40, 0.88)
    draw_box(tx - 0.50, 2.40, tz + 1.55, 0.32, 0.35, 0.04)
    # Simbol P (merah)
    color(0.88, 0.20, 0.22)
    draw_box(tx + 0.50, 2.40, tz + 1.55, 0.32, 0.35, 0.04)

    # ── Simbol difabel ───────────────────────────────────────────
    color(0.15, 0.35, 0.75)
    draw_box(tx + 2.2, 0, tz + 1.52, 0.70, 2.10, 0.08)
    draw_sphere(tx + 2.2, 1.4, tz + 1.57, 0.25)   # ikon kursi roda

    # ── Wastafel luar ────────────────────────────────────────────
    color(0.78, 0.78, 0.78)
    draw_box(tx + 2.2, 0, tz - 1.52, 0.50, 0.90, 0.40)
    draw_disk(tx + 2.2, 0.92, tz - 1.52, 0.22, 12)
    # Keran
    color(0.72, 0.70, 0.60)
    draw_cylinder(tx + 2.2, 0.92, tz - 1.40, 0.03, 0.22, 6)
    draw_box(tx + 2.2, 1.12, tz - 1.38, 0.14, 0.04, 0.04)
