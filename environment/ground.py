"""
environment/ground.py
---------------------
Tanah berumput hijau cerah, jalan aspal di sisi KIRI taman, trotoar,
area parkir, dan jalur setapak.

Layout (mengikuti referensi):
  - Park: kotak hijau dari (-20, -20) ke (20, 20)
  - Trotoar tipis di luar pagar (3 sisi)
  - Jalan aspal di sisi KIRI park (sumbu Z, north-south)
  - Area parkir antara pagar kiri & jalan
  - Trotoar depan park (di sisi gerbang)
"""

import math
from OpenGL.GL import *
from core.primitives import (
    color, draw_flat_quad, draw_path_segment, draw_box, draw_disk
)

# Ukuran taman
PARK_HALF = 20.0


def draw_ground():
    # ── Rumput utama (hijau saturated cerah) ──────────────────────
    color(0.42, 0.78, 0.30)
    draw_flat_quad(-PARK_HALF, -PARK_HALF, PARK_HALF, PARK_HALF, y=0.0)

    # Variasi rumput area tengah (sedikit lebih terang)
    color(0.48, 0.82, 0.34)
    draw_flat_quad(-9, -9, 9, 9, y=0.001)

    # ── Tanah luar park (rumput sedikit lebih gelap) ──────────────
    color(0.36, 0.72, 0.26)
    # Sebelah kanan park
    draw_flat_quad( PARK_HALF, -PARK_HALF, PARK_HALF + 8, PARK_HALF, y=-0.01)
    # Sebelah belakang park
    draw_flat_quad(-PARK_HALF - 8, -PARK_HALF - 8, PARK_HALF + 8, -PARK_HALF, y=-0.01)
    # Sebelah depan (di luar gerbang)
    draw_flat_quad(-PARK_HALF, PARK_HALF, PARK_HALF + 8, PARK_HALF + 6, y=-0.01)
    draw_flat_quad(-PARK_HALF - 8, PARK_HALF - 8, -PARK_HALF, PARK_HALF + 6, y=-0.01)

    # ── Jalan aspal di sisi KIRI taman (running north-south) ──────
    # x: -28 sampai -22  |  z: -28 sampai 26
    color(0.42, 0.42, 0.45)
    draw_flat_quad(-28.0, -28.0, -22.0, 26.0, y=-0.05)

    # Marka tepi jalan kanan (putih solid - dekat parkir)
    color(0.96, 0.96, 0.94)
    draw_flat_quad(-22.10, -28.0, -22.00, 26.0, y=0.005)
    # Marka tepi jalan kiri
    draw_flat_quad(-28.00, -28.0, -27.90, 26.0, y=0.005)

    # Marka garis putus-putus tengah jalan (vertikal, sumbu Z)
    color(0.96, 0.96, 0.94)
    z = -27.0
    while z < 26.0:
        draw_flat_quad(-25.10, z, -24.90, z + 1.6, y=0.005)
        z += 3.6

    # ── Area parkir (di antara pagar kiri & jalan) ────────────────
    # x: -22 sampai -20  |  z: -20 sampai 16  (sejajar pagar kiri taman)
    color(0.36, 0.36, 0.40)
    draw_flat_quad(-22.0, -20.0, -20.0, 16.0, y=-0.04)

    # Garis parkir putih (horizontal, membatasi tiap slot)
    color(0.95, 0.95, 0.93)
    pz = -20.0
    while pz <= 16.0:
        draw_flat_quad(-22.0, pz - 0.05, -20.0, pz + 0.05, y=0.005)
        pz += 3.0

    # Slot difabel (biru terang) — satu slot di tengah area parkir
    color(0.20, 0.40, 0.85)
    draw_flat_quad(-22.0, -3.0, -20.0, 0.0, y=0.006)
    # Garis difabel ulang putih di atasnya
    color(0.95, 0.95, 0.93)
    draw_flat_quad(-22.0, -3.05, -20.0, -2.95, y=0.007)
    draw_flat_quad(-22.0, -0.05, -20.0,  0.05, y=0.007)
    # Simbol kursi roda mock (lingkaran putih)
    draw_disk(-21.0, 0.008, -1.5, 0.45, 16)

    # ── Trotoar depan taman (krem cerah) di sisi gerbang ──────────
    color(0.92, 0.88, 0.78)
    draw_flat_quad(-PARK_HALF, PARK_HALF - 4, PARK_HALF, PARK_HALF - 3, y=0.03)

    # Garis pemisah ubin trotoar
    color(0.82, 0.78, 0.68)
    x = -PARK_HALF
    while x <= PARK_HALF:
        draw_flat_quad(x, PARK_HALF - 4, x + 0.04, PARK_HALF - 3, y=0.04)
        x += 1.6


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
    glEnable(GL_POLYGON_OFFSET_FILL)
    glPolygonOffset(-1.0, -1.0)

    # Jalur krem-pucat (mirip pavers di referensi)
    color(0.93, 0.88, 0.74)

    # ── Jalur masuk utama dari gerbang (z=16 → 5) ────────────────
    draw_path_segment(0, 16.0, 0, 5.0, 3.0)

    # ── Jalur melingkar utama (r=7) ───────────────────────────────
    _ring_path(0, 0, 7.0, 7.0, 48, 1.6)

    # ── Jalur radial ─────────────────────────────────────────────
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
        draw_path_segment(x1, z1, x2, z2, 1.4)

    glDisable(GL_POLYGON_OFFSET_FILL)
    glPolygonOffset(0.0, 0.0)
