"""
environment/ground.py
---------------------
Tanah berumput, jalan aspal, trotoar, dan semua jalur setapak / jogging track.
"""

import math
from OpenGL.GL import *
from core.primitives import (
    color, draw_flat_quad, draw_path_segment, draw_box, draw_disk
)

# Ukuran taman
PARK_HALF = 20.0


def draw_ground():
    # ── Rumput utama ─────────────────────────────────────────────
    color(0.30, 0.58, 0.22)
    draw_flat_quad(-PARK_HALF, -PARK_HALF, PARK_HALF, PARK_HALF, y=0.0)

    # Variasi rumput (lebih terang) di area tengah
    color(0.34, 0.63, 0.25)
    draw_flat_quad(-8, -8, 8, 8, y=0.001)

    # ── Jalan aspal dua lajur ─────────────────────────────────────
    color(0.22, 0.22, 0.22)
    draw_flat_quad(-30.0, 17.0, 30.0, 23.0, y=-0.05)

    # Marka garis putus-putus tengah jalan
    color(0.90, 0.88, 0.80)
    x = -28.0
    while x < 28.0:
        draw_flat_quad(x, 19.85, x + 2.0, 20.15, y=0.00)
        x += 4.0

    # Marka tepi kiri (kuning solid)
    color(0.95, 0.80, 0.05)
    draw_flat_quad(-30.0, 17.05, 30.0, 17.20, y=0.00)
    draw_flat_quad(-30.0, 22.80, 30.0, 22.95, y=0.00)

    # ── Trotoar ───────────────────────────────────────────────────
    color(0.72, 0.70, 0.66)
    draw_flat_quad(-PARK_HALF, 16.0, PARK_HALF, 17.2, y=0.03)

    # Tekstur bata trotoar (grid garis)
    color(0.62, 0.60, 0.57)
    x = -PARK_HALF
    while x <= PARK_HALF:
        draw_flat_quad(x, 16.0, x + 0.02, 17.2, y=0.04)
        x += 1.0

    # ── Area parkir ───────────────────────────────────────────────
    color(0.28, 0.28, 0.28)
    draw_flat_quad(-PARK_HALF, 17.2, PARK_HALF, 23.0, y=-0.04)

    # Garis parkir putih
    color(0.88, 0.88, 0.88)
    px = -PARK_HALF + 1.5
    while px <= PARK_HALF - 2.0:
        draw_flat_quad(px, 17.5, px + 0.08, 20.5, y=0.00)
        px += 2.8


def _ellipse_path(cx, cz, rx, rz, segs, width, y=0.02):
    for i in range(segs):
        a1 = i       / segs * 2 * math.pi
        a2 = (i + 1) / segs * 2 * math.pi
        draw_path_segment(
            cx + rx * math.cos(a1), cx + rz * math.sin(a1),   # ← BUG ASAL, kita perbaiki:
            cx + rx * math.cos(a2), cx + rz * math.sin(a2),
            width, y=y,
        )

# Versi yang benar (pakai cz bukan cx untuk offset Z)
def _ring_path(cx, cz, rx, rz, segs, width, y=0.02):
    for i in range(segs):
        a1 = i       / segs * 2 * math.pi
        a2 = (i + 1) / segs * 2 * math.pi
        draw_path_segment(
            cx + rx * math.cos(a1), cz + rz * math.sin(a1),
            cx + rx * math.cos(a2), cz + rz * math.sin(a2),
            width, y=y,
        )


def draw_all_paths():
    # Polygon offset menggeser depth jalur sedikit ke depan camera tanpa
    # mengubah posisi geometris. Ini menghilangkan z-fighting (kedipan
    # oranye pada jogging track) saat kamera bergerak dengan W/S/A/D/Q/E.
    glEnable(GL_POLYGON_OFFSET_FILL)
    glPolygonOffset(-1.0, -1.0)

    color(0.73, 0.67, 0.58)

    # ── Jalur masuk utama (lebar 3 m) ────────────────────────────
    draw_path_segment(0, 16.0, 0, 5.0, 3.0)

    # ── Jalur melingkar utama (r=7) ───────────────────────────────
    _ring_path(0, 0, 7.0, 7.0, 48, 1.4)

    # ── Jalur radial ke berbagai sudut ───────────────────────────
    radial = [
        ( 0,  5,  -8, -2),
        ( 0,  5,   8, -2),
        ( 0,  5, -12,  8),
        ( 0,  5,  12,  8),
        (-8, -2, -14,-10),
        ( 8, -2,  14,-10),
        ( 0, -7,   0,-16),
    ]
    for x1, z1, x2, z2 in radial:
        draw_path_segment(x1, z1, x2, z2, 1.2)

    glDisable(GL_POLYGON_OFFSET_FILL)
    glPolygonOffset(0.0, 0.0)
