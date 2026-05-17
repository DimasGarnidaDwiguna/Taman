"""
objects/fountain.py
-------------------
Air mancur tier-tiga (wedding-cake fountain) bergaya kartun.

Struktur (dari bawah ke atas):
  - Step plinth: alas berundak warna putih krem
  - Tier 1 : basin terbesar dengan dinding abu-biru, bibir putih
             menjorok, dan permukaan air cyan
  - Tier 2 : basin sedang, duduk di tengah air tier 1
  - Tier 3 : basin kecil di puncak tiang
  - Tiang  : kolom abu-biru ramping dari tier 2 menuju tier 3
  - Finial : kerucut + bola kecil di puncak

Animasi: riak melingkar pada permukaan air tier 1 dan 2.

Catatan permukaan air:
  Permukaan air digambar SEDIKIT DI ATAS bibir (rim) basin
  sehingga benar-benar terlihat sebagai genangan dari atas. Lapisan
  rim (cylinder berwarna putih) muncul sebagai cincin tipis di
  sekeliling air.
"""

import math

from core.primitives import (
    color, draw_cylinder, draw_disk, draw_sphere, draw_cone,
)


_CX, _CZ = 0.0, 0.0      # pusat air mancur


# ── Palet warna (matching referensi) ─────────────────────────────
WALL_BLUEGRAY = (0.55, 0.66, 0.72)    # dinding abu-biru lembut
WALL_DARKER   = (0.45, 0.56, 0.62)    # bayangan dinding
RIM_WHITE     = (0.96, 0.96, 0.94)    # bibir putih
RIM_SHADOW    = (0.84, 0.86, 0.86)    # bayangan tipis di bawah bibir
WATER_LIGHT   = (0.40, 0.78, 0.96)    # air cyan terang
WATER_HILITE  = (0.78, 0.94, 1.00)    # highlight permukaan air


# ── Geometri (sinkron dengan CIRCLE_ZONE radius 3.30 di layout) ──
# Plinth (alas berundak)
PLINTH_R       = 3.10
PLINTH_H       = 0.18

# Tier 1 (basin bawah)
T1_R           = 2.80
T1_WALL_BOT    = PLINTH_H                     # 0.18
T1_WALL_H      = 0.55
T1_RIM_Y       = T1_WALL_BOT + T1_WALL_H      # 0.73 (bottom of rim cyl)
T1_RIM_TOP_Y   = T1_RIM_Y + 0.10              # 0.83 (top of rim cyl)
T1_WATER_Y     = T1_RIM_TOP_Y + 0.002         # 0.832 (air sedikit di atas rim)

# Tier 2 (basin tengah, duduk di permukaan air tier 1)
T2_R           = 1.55
T2_WALL_BOT    = T1_WATER_Y - 0.04            # 0.792 (sedikit menyelam ke air)
T2_WALL_H      = 0.65
T2_RIM_Y       = T2_WALL_BOT + T2_WALL_H      # 1.442
T2_RIM_TOP_Y   = T2_RIM_Y + 0.10              # 1.542
T2_WATER_Y     = T2_RIM_TOP_Y + 0.002         # 1.544

# Tiang pusat (dari air tier 2)
PILLAR_R       = 0.30
PILLAR_TOP_Y   = T2_WATER_Y + 0.95            # ~2.49

# Tier 3 (basin kecil di puncak tiang)
T3_R           = 0.55
T3_WALL_BOT    = PILLAR_TOP_Y - 0.05
T3_WALL_H      = 0.28
T3_RIM_Y       = T3_WALL_BOT + T3_WALL_H
T3_RIM_TOP_Y   = T3_RIM_Y + 0.10
T3_WATER_Y     = T3_RIM_TOP_Y + 0.002

# Finial (kerucut + bola di puncak)
FINIAL_BASE_Y  = T3_WATER_Y + 0.02
FINIAL_TOP_Y   = FINIAL_BASE_Y + 0.85


def draw_fountain(fountain_angle_deg: float):
    cx, cz = _CX, _CZ
    fa = math.radians(fountain_angle_deg)

    _draw_plinth(cx, cz)
    _draw_tier(cx, cz, T1_R, T1_WALL_BOT, T1_WALL_H, T1_WATER_Y, fa,
               ripple=True)
    _draw_tier(cx, cz, T2_R, T2_WALL_BOT, T2_WALL_H, T2_WATER_Y, fa,
               ripple=True)
    _draw_pillar(cx, cz)
    _draw_tier(cx, cz, T3_R, T3_WALL_BOT, T3_WALL_H, T3_WATER_Y, fa,
               ripple=False)
    _draw_finial(cx, cz, fa)

    # Pancuran air halus dari mulut tiang ke basin tier 2 (animasi)
    _draw_water_streams(cx, cz, fa)


# ─────────────────────────────────────────────────────────────────
# Plinth (alas berundak)
# ─────────────────────────────────────────────────────────────────
def _draw_plinth(cx, cz):
    """Dua tingkat alas putih krem di tanah, lebih lebar dari tier 1."""
    # Tingkat luar (paling lebar)
    color(*RIM_SHADOW)
    draw_cylinder(cx, 0.0, cz, PLINTH_R, 0.08, 48)
    # Tingkat dalam (lebih sempit)
    color(*RIM_WHITE)
    draw_cylinder(cx, 0.06, cz, PLINTH_R - 0.18, 0.12, 48)


# ─────────────────────────────────────────────────────────────────
# Tier (basin lingkaran dengan dinding + bibir + air)
# ─────────────────────────────────────────────────────────────────
def _draw_tier(cx, cz, radius, y_bottom, wall_h, water_y, fa,
               ripple=True):
    # ── Dinding utama (abu-biru) ────────────────────────────────
    color(*WALL_BLUEGRAY)
    draw_cylinder(cx, y_bottom, cz, radius, wall_h, 36)

    # Bayangan tipis di bagian bawah dinding (efek shading)
    color(*WALL_DARKER)
    draw_cylinder(cx, y_bottom, cz, radius + 0.003, 0.08, 36)

    # ── Bibir putih (rim) di atas dinding, menjorok keluar ──────
    rim_y = y_bottom + wall_h
    # Strip bayangan di bawah bibir (membuat bibir terlihat tebal)
    color(*RIM_SHADOW)
    draw_cylinder(cx, rim_y - 0.04, cz, radius + 0.14, 0.06, 36)
    # Bibir utama putih
    color(*RIM_WHITE)
    draw_cylinder(cx, rim_y, cz, radius + 0.10, 0.10, 36)

    # ── Permukaan air (di ATAS bibir agar terlihat sebagai genangan)
    inner_r = radius - 0.10   # sedikit di dalam tepi rim → ada cincin putih
    rim_outer = radius + 0.10

    # Sentuhan basah / lembab di tepi rim (sedikit kecyan-an)
    color(0.86, 0.94, 0.97)
    draw_disk(cx, water_y - 0.001, cz, rim_outer, 36)

    # Air dasar
    color(*WATER_LIGHT)
    draw_disk(cx, water_y, cz, inner_r, 36)

    # Riak melingkar (cincin nafas) di tengah
    if ripple:
        rr = inner_r * 0.55 + 0.10 * math.sin(fa * 2.0)
        color(*WATER_HILITE)
        draw_disk(cx, water_y + 0.005, cz, rr, 36)
        # Cincin highlight kedua, fase berbeda
        rr2 = inner_r * 0.30 + 0.06 * math.sin(fa * 2.0 + 1.5)
        draw_disk(cx, water_y + 0.010, cz, rr2, 36)


# ─────────────────────────────────────────────────────────────────
# Tiang pusat (dari air tier 2 ke basin tier 3)
# ─────────────────────────────────────────────────────────────────
def _draw_pillar(cx, cz):
    pillar_bot = T2_WATER_Y - 0.02
    pillar_h   = T3_WALL_BOT - pillar_bot

    # Tiang silinder
    color(*WALL_BLUEGRAY)
    draw_cylinder(cx, pillar_bot, cz, PILLAR_R, pillar_h, 24)

    # Cincin dekoratif di pangkal
    color(*RIM_WHITE)
    draw_cylinder(cx, pillar_bot + 0.05, cz, PILLAR_R + 0.06, 0.05, 24)
    color(*RIM_SHADOW)
    draw_cylinder(cx, pillar_bot + 0.03, cz, PILLAR_R + 0.07, 0.03, 24)

    # Cincin tengah tiang
    mid_y = pillar_bot + pillar_h * 0.50
    color(*WALL_DARKER)
    draw_cylinder(cx, mid_y, cz, PILLAR_R + 0.04, 0.06, 24)
    color(*RIM_WHITE)
    draw_cylinder(cx, mid_y + 0.06, cz, PILLAR_R + 0.05, 0.04, 24)

    # Cincin atas (tepat di bawah basin tier 3)
    color(*RIM_SHADOW)
    draw_cylinder(cx, T3_WALL_BOT - 0.10, cz, PILLAR_R + 0.05, 0.04, 24)
    color(*RIM_WHITE)
    draw_cylinder(cx, T3_WALL_BOT - 0.06, cz, PILLAR_R + 0.08, 0.06, 24)


# ─────────────────────────────────────────────────────────────────
# Finial (kerucut + bola di puncak basin tier 3)
# ─────────────────────────────────────────────────────────────────
def _draw_finial(cx, cz, fa):
    # Bola kecil sebagai dasar finial
    color(*WALL_BLUEGRAY)
    draw_sphere(cx, FINIAL_BASE_Y + 0.06, cz, 0.10)

    # Kerucut runcing menjulang ke atas
    cone_h = FINIAL_TOP_Y - (FINIAL_BASE_Y + 0.10)
    color(*WALL_DARKER)
    draw_cone(cx, FINIAL_BASE_Y + 0.10, cz, 0.09, cone_h, 18)

    # Highlight cyan di sisi kerucut (lapisan tipis lebih cerah)
    color(*WATER_LIGHT)
    draw_cone(cx, FINIAL_BASE_Y + 0.10, cz, 0.05, cone_h * 0.92, 16)

    # Tetes air kecil yang naik-turun di puncak (animasi)
    drop_y = FINIAL_TOP_Y + 0.05 + 0.10 * math.sin(fa * 2.0)
    color(*WATER_HILITE)
    draw_sphere(cx, drop_y, cz, 0.06)
    color(0.95, 0.99, 1.00)
    draw_sphere(cx, drop_y + 0.10, cz, 0.04)


# ─────────────────────────────────────────────────────────────────
# Pancuran air dari tier 3 → tier 2 (animasi droplet)
# ─────────────────────────────────────────────────────────────────
def _draw_water_streams(cx, cz, fa):
    """Tetesan air yang jatuh dari tepi tier 3 ke air tier 2."""
    n = 8
    for i in range(n):
        a   = (i / n) * 2 * math.pi
        # tetesan jatuh dari tepi rim tier 3
        r3  = T3_R + 0.05
        sx  = cx + r3 * math.cos(a)
        sz  = cz + r3 * math.sin(a)
        # variasi fase tiap tetes
        phase = math.sin(fa * 3.0 + i * 0.7) * 0.5 + 0.5  # 0..1
        # tetes turun dari T3_WATER_Y ke T2_WATER_Y
        drop_y = T3_WATER_Y - phase * (T3_WATER_Y - T2_WATER_Y - 0.05)
        color(*WATER_HILITE)
        draw_sphere(sx, drop_y, sz, 0.04)
