"""
environment/gate.py
-------------------
Gerbang masuk taman — dua pilar bata di sisi pintu, papan nama
"TAMAN KOTA" di ATAS (sebagai arch), dan papan informasi di
pinggir kiri. Pintu di tengah dibiarkan terbuka.

Catatan: rambu parkir "P" tidak di sini, melainkan di area parkir
mobil (lihat objects/parking.py).
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
    # Panel: y_bottom = 4.10, tinggi 0.80 → spans 4.10..4.90, pusat 4.50
    arch_panel_bot = pillar_h + 0.60     # 4.10
    arch_panel_h   = 0.80
    arch_center_y  = arch_panel_bot + arch_panel_h * 0.5   # 4.50

    color(0.20, 0.55, 0.22)              # latar hijau
    draw_box(0, arch_panel_bot, 16.30, 5.6, arch_panel_h, 0.18)
    color(0.16, 0.45, 0.18)              # bingkai belakang
    draw_box(0, arch_panel_bot, 16.22, 5.7, arch_panel_h + 0.05, 0.05)

    # Bingkai krem di tepi atas & bawah panel
    color(0.95, 0.92, 0.78)
    draw_box(0, arch_panel_bot + arch_panel_h - 0.04, 16.39,
             5.5, 0.04, 0.04)
    draw_box(0, arch_panel_bot, 16.39, 5.5, 0.04, 0.04)

    # Tulisan "TAMAN KOTA" — pusat tepat di tengah panel
    draw_text("TAMAN KOTA",
              cx=0.0, cy=arch_center_y, cz=16.42,
              height=0.50, depth=0.06,
              color_rgb=(0.95, 0.92, 0.78))

    # Lengkungan dekoratif kayu di bawah papan
    color(0.55, 0.40, 0.26)
    draw_box(0, arch_panel_bot - 0.40, 16.30, 5.4, 0.12, 0.16)

    # ── Papan informasi (kiri gerbang) ──────────────────────────
    # Panel: y_bottom = 1.5, tinggi 1.5 → spans 1.5..3.0, pusat 2.25
    info_x         = -7.5
    info_z         = 16.6
    info_panel_bot = 1.5
    info_panel_h   = 1.5
    info_center_y  = info_panel_bot + info_panel_h * 0.5   # 2.25

    color(0.30, 0.20, 0.10)
    draw_cylinder(info_x, 0, info_z, 0.08, 2.2, 6)
    # Latar hijau
    color(0.20, 0.55, 0.22)
    draw_box(info_x, info_panel_bot, info_z + 0.10,
             2.0, info_panel_h, 0.15)
    # Papan tempel kayu di tengah
    color(0.55, 0.40, 0.20)
    draw_box(info_x, info_panel_bot + 0.10, info_z + 0.18,
             1.8, info_panel_h - 0.20, 0.05)

    # Judul "INFO" di atas (offset +0.40 dari pusat)
    draw_text("INFO",
              cx=info_x, cy=info_center_y + 0.40, cz=info_z + 0.22,
              height=0.30, depth=0.04,
              color_rgb=(0.95, 0.92, 0.78))
    # "TAMAN" di tengah
    draw_text("TAMAN",
              cx=info_x, cy=info_center_y, cz=info_z + 0.22,
              height=0.20, depth=0.03,
              color_rgb=(0.95, 0.92, 0.78))
    # "KOTA" di bawah (offset -0.30 dari pusat)
    draw_text("KOTA",
              cx=info_x, cy=info_center_y - 0.35, cz=info_z + 0.22,
              height=0.20, depth=0.03,
              color_rgb=(0.95, 0.92, 0.78))
