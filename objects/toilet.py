"""
objects/toilet.py
-----------------
Toilet umum modular: kabin abu-gelap dengan atap pelana, pintu kayu,
panel surya tipis di atap, dan signage warna.
"""

from core.primitives import color, draw_box, draw_cylinder, draw_sphere, draw_disk


_TX, _TZ = 4.0, -15.0   # area belakang-tengah, di belakang air mancur


def draw_toilet():
    tx, tz = _TX, _TZ

    # ── Dinding bangunan (abu-gelap, gaya container) ──────────────
    color(0.32, 0.34, 0.38)
    draw_box(tx, 0, tz, 3.5, 2.6, 2.6)

    # Sekat tengah (pembagi bilik)
    color(0.26, 0.28, 0.32)
    draw_box(tx, 0, tz, 0.10, 2.5, 2.6)

    # ── Atap pelana ───────────────────────────────────────────────
    color(0.20, 0.20, 0.22)
    draw_box(tx, 2.6, tz, 3.7, 0.30, 2.8)

    # Bubungan
    color(0.16, 0.16, 0.18)
    draw_box(tx, 2.92, tz, 3.7, 0.10, 0.20)

    # ── Panel surya tipis di atap ────────────────────────────────
    color(0.10, 0.14, 0.22)
    draw_box(tx, 2.96, tz - 0.5, 3.0, 0.04, 1.6)
    color(0.16, 0.20, 0.30)
    for ix in range(3):
        draw_box(tx - 1.2 + ix * 1.0, 2.99, tz - 0.5, 0.03, 0.04, 1.55)
    for iz in range(3):
        draw_box(tx, 2.99, tz - 1.0 + iz * 0.5, 2.95, 0.04, 0.03)

    # ── Dua pintu (kayu) ─────────────────────────────────────────
    color(0.45, 0.30, 0.14)
    draw_box(tx - 0.95, 0, tz + 1.31, 0.70, 2.10, 0.10)
    draw_box(tx + 0.95, 0, tz + 1.31, 0.70, 2.10, 0.10)

    # Gagang pintu
    color(0.78, 0.74, 0.58)
    draw_sphere(tx - 0.65, 1.0, tz + 1.36, 0.07)
    draw_sphere(tx + 1.25, 1.0, tz + 1.36, 0.07)

    # ── Papan tanda L/P di atas pintu ─────────────────────────────
    color(0.94, 0.94, 0.92)
    draw_box(tx, 2.30, tz + 1.32, 1.50, 0.36, 0.05)

    # Simbol L (biru) dan P (merah)
    color(0.20, 0.40, 0.92)
    draw_box(tx - 0.40, 2.32, tz + 1.36, 0.30, 0.28, 0.03)
    color(0.92, 0.22, 0.22)
    draw_box(tx + 0.40, 2.32, tz + 1.36, 0.30, 0.28, 0.03)
