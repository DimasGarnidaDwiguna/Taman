"""
environment/gate.py
-------------------
Gerbang masuk taman kota — dua pilar bata + lengkungan + papan nama.
"""

from core.primitives import color, draw_box, draw_cylinder, draw_sphere, draw_cone


def draw_gate():
    # ── Pilar kiri & kanan ───────────────────────────────────────
    color(0.52, 0.40, 0.28)
    for sx in (-3.2, 3.2):
        draw_box(sx, 0, 16.3, 0.75, 3.8, 0.75)
        # Detail pilar: bata bergaris
        color(0.48, 0.36, 0.24)
        for iy in range(6):
            draw_box(sx, iy * 0.6, 16.3, 0.78, 0.06, 0.78)
        color(0.52, 0.40, 0.28)

    # ── Lengkungan atas ──────────────────────────────────────────
    color(0.45, 0.34, 0.22)
    draw_box(0, 3.6, 16.3, 7.2, 0.5, 0.75)

    # ── Bola dekorasi puncak pilar ───────────────────────────────
    color(0.75, 0.70, 0.55)
    draw_sphere(-3.2, 4.1, 16.3, 0.38)
    draw_sphere( 3.2, 4.1, 16.3, 0.38)

    # ── Papan nama "TAMAN KOTA" ───────────────────────────────────
    color(0.28, 0.55, 0.20)    # hijau tua
    draw_box(0, 3.85, 16.25, 5.0, 0.70, 0.12)
    color(0.90, 0.85, 0.70)    # teks (mock: kotak krem)
    for i, tx in enumerate([-1.5, -0.75, 0, 0.75, 1.5]):
        draw_box(tx, 3.92, 16.19, 0.4, 0.45, 0.04)

    # ── Bollard (pembatas) ────────────────────────────────────────
    color(0.85, 0.75, 0.20)    # kuning keemasan
    for bx in (-2.0, -1.0, 0.0, 1.0, 2.0):
        draw_cylinder(bx, 0, 16.7, 0.09, 0.85, 8)
        draw_sphere(bx, 0.92, 16.7, 0.12)

    # ── Papan informasi (kiri gerbang) ───────────────────────────
    color(0.25, 0.50, 0.18)
    draw_box(-7, 0, 16.6, 2.2, 1.8, 0.14)
    color(0.18, 0.14, 0.08)
    draw_cylinder(-7, 0, 16.6, 0.06, 2.0, 6)
    # bingkai papan
    color(0.45, 0.30, 0.12)
    draw_box(-7, 1.2, 16.63, 2.0, 1.4, 0.04)

    # ── Rambu parkir (kanan gerbang) ─────────────────────────────
    color(0.15, 0.32, 0.68)
    draw_box(9, 0.9, 16.6, 0.9, 0.9, 0.10)
    color(0.18, 0.14, 0.08)
    draw_cylinder(9, 0, 16.6, 0.05, 2.0, 6)
    color(0.95, 0.95, 0.95)    # huruf P
    draw_box(9, 0.9, 16.65, 0.35, 0.55, 0.03)
