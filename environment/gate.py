"""
environment/gate.py
-------------------
Gerbang masuk taman — dua pilar bata di sisi pintu, papan nama
"TAMAN KOTA" di ATAS (sebagai arch), dan rambu informasi/parkir
di pinggir. Pintu di tengah dibiarkan terbuka.
"""

from core.primitives import color, draw_box, draw_cylinder, draw_sphere


def draw_gate():
    # Tinggi pilar
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

    # ── Arch atas: papan nama "TAMAN KOTA" di KETINGGIAN ────────
    # Berada di y=4.4, di atas kepala, sehingga pintu di bawahnya
    # tetap terbuka.
    arch_y = pillar_h + 0.90    # 4.40
    color(0.20, 0.55, 0.22)     # papan hijau
    draw_box(0, arch_y, 16.30, 5.6, 0.80, 0.18)
    color(0.16, 0.45, 0.18)     # bingkai tipis di belakang
    draw_box(0, arch_y, 16.22, 5.7, 0.85, 0.05)

    # Mock huruf (krem) — sekarang di atas, terlihat seperti signage
    color(0.95, 0.92, 0.78)
    for tx in (-1.8, -0.9, 0.0, 0.9, 1.8):
        draw_box(tx, arch_y, 16.40, 0.45, 0.50, 0.04)

    # Lengkungan dekoratif kayu di bawah papan (opsional, estetika)
    color(0.55, 0.40, 0.26)
    draw_box(0, arch_y - 0.50, 16.30, 5.4, 0.12, 0.16)

    # ── Papan informasi (jauh dari jalur, kiri gerbang) ─────────
    color(0.30, 0.20, 0.10)
    draw_cylinder(-7.5, 0, 16.6, 0.08, 2.2, 6)
    color(0.20, 0.55, 0.22)
    draw_box(-7.5, 1.2, 16.7, 2.0, 1.5, 0.15)
    color(0.55, 0.40, 0.20)
    draw_box(-7.5, 1.2, 16.74, 1.8, 1.3, 0.05)

    # ── Rambu parkir (jauh dari jalur, kanan gerbang) ────────────
    color(0.18, 0.18, 0.20)
    draw_cylinder(8.5, 0, 16.6, 0.06, 2.2, 6)
    color(0.16, 0.36, 0.78)
    draw_box(8.5, 1.5, 16.7, 0.85, 0.85, 0.10)
    color(0.96, 0.96, 0.94)
    draw_box(8.5, 1.5, 16.76, 0.40, 0.55, 0.03)
