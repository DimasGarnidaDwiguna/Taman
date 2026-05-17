"""
environment/gate.py
-------------------
Gerbang masuk taman — dua pilar bata di sisi pintu, papan nama
"TAMAN KOTA" di ATAS (sebagai arch), papan informasi, dan rambu
parkir di pinggir. Pintu di tengah dibiarkan terbuka.
"""

from core.primitives import color, draw_box, draw_cylinder, draw_sphere
from core.text3d     import draw_text


def draw_gate():
    pillar_h = 3.5

    # ── Pilar kiri & kanan (bata coklat hangat) ──────────────────
    for sx in (-3.4, 3.4):
        # Body utama
        color(0.55, 0.40, 0.26)
        draw_box(sx, 0, 16.3, 0.85, pillar_h, 0.85)
        # Garis bata
        color(0.48, 0.34, 0.20)
        for iy in range(6):
            draw_box(sx, iy * 0.55, 16.3, 0.88, 0.05, 0.88)
        # Topi pilar (lebih lebar)
        color(0.92, 0.88, 0.78)
        draw_box(sx, pillar_h, 16.3, 1.0, 0.20, 1.0)
        # Bola dekorasi puncak
        color(0.95, 0.78, 0.22)
        draw_sphere(sx, pillar_h + 0.35, 16.3, 0.30)

    # ── Arch atas: papan nama "TAMAN KOTA" ──────────────────────
    arch_y = pillar_h + 0.90    # 4.40
    color(0.20, 0.55, 0.22)     # latar hijau
    draw_box(0, arch_y, 16.30, 5.6, 0.80, 0.18)
    color(0.16, 0.45, 0.18)     # bingkai belakang
    draw_box(0, arch_y, 16.22, 5.7, 0.85, 0.05)

    # Bingkai krem di tepi atas & bawah panel
    color(0.95, 0.92, 0.78)
    draw_box(0, arch_y + 0.36, 16.39, 5.5, 0.06, 0.04)
    draw_box(0, arch_y - 0.36, 16.39, 5.5, 0.06, 0.04)

    # Tulisan "TAMAN KOTA"
    draw_text("TAMAN KOTA",
              cx=0.0, cy=arch_y, cz=16.42,
              height=0.50, depth=0.06,
              color_rgb=(0.95, 0.92, 0.78))

    # Lengkungan dekoratif kayu di bawah papan
    color(0.55, 0.40, 0.26)
    draw_box(0, arch_y - 0.50, 16.30, 5.4, 0.12, 0.16)

    # ── Papan informasi (kiri gerbang) ──────────────────────────
    info_x, info_z = -7.5, 16.6
    info_panel_y   = 1.5
    color(0.30, 0.20, 0.10)
    draw_cylinder(info_x, 0, info_z, 0.08, 2.2, 6)
    color(0.20, 0.55, 0.22)
    draw_box(info_x, info_panel_y, info_z + 0.10, 2.0, 1.5, 0.15)
    # Papan tempel kayu di tengah
    color(0.55, 0.40, 0.20)
    draw_box(info_x, info_panel_y, info_z + 0.18, 1.8, 1.3, 0.05)

    # Judul "INFO" di atas
    draw_text("INFO",
              cx=info_x, cy=info_panel_y + 0.42, cz=info_z + 0.22,
              height=0.30, depth=0.04,
              color_rgb=(0.95, 0.92, 0.78))
    # Sub-baris kecil
    draw_text("TAMAN",
              cx=info_x, cy=info_panel_y + 0.05, cz=info_z + 0.22,
              height=0.18, depth=0.03,
              color_rgb=(0.95, 0.92, 0.78))
    draw_text("KOTA",
              cx=info_x, cy=info_panel_y - 0.25, cz=info_z + 0.22,
              height=0.18, depth=0.03,
              color_rgb=(0.95, 0.92, 0.78))

    # ── Rambu parkir (kanan gerbang) ────────────────────────────
    park_x, park_z = 8.5, 16.6
    park_panel_y   = 1.7
    color(0.18, 0.18, 0.20)
    draw_cylinder(park_x, 0, park_z, 0.06, 2.4, 6)
    # Latar biru
    color(0.16, 0.36, 0.78)
    draw_box(park_x, park_panel_y, park_z + 0.08, 0.85, 0.85, 0.10)
    # Bingkai putih
    color(0.96, 0.96, 0.94)
    draw_box(park_x, park_panel_y, park_z + 0.14, 0.78, 0.78, 0.02)
    # Latar biru lebih kecil di dalam bingkai
    color(0.16, 0.36, 0.78)
    draw_box(park_x, park_panel_y, park_z + 0.16, 0.70, 0.70, 0.02)
    # Huruf "P"
    draw_text("P",
              cx=park_x, cy=park_panel_y, cz=park_z + 0.20,
              height=0.55, depth=0.04,
              color_rgb=(0.96, 0.96, 0.94))
