"""
objects/fountain.py
-------------------
Air mancur tier-tiga bergaya kartun (wedding cake fountain):
  - Tier 1 (bawah): basin lebar dengan bibir putih, dinding abu-biru
  - Tier 2 (tengah): basin lebih kecil di atas tier 1
  - Tier 3 (atas): basin kecil lagi, dengan tiang/spout di pusat
  - Air berwarna cyan terang di setiap tier
"""

import math
from OpenGL.GL  import (glPushMatrix, glPopMatrix, glTranslatef, glRotatef)
from OpenGL.GLU import gluNewQuadric, gluCylinder, gluDeleteQuadric

from core.primitives import color, draw_cylinder, draw_disk, draw_sphere


_CX, _CZ = 0.0, 0.0   # pusat air mancur

# ── Palet warna (mengikuti referensi) ────────────────────────────
WALL_BLUEGRAY  = (0.52, 0.62, 0.68)   # dinding abu-biru
WALL_DARKER    = (0.42, 0.52, 0.58)   # bayangan dinding
RIM_WHITE      = (0.96, 0.96, 0.94)   # bibir putih
RIM_SHADOW     = (0.82, 0.84, 0.84)   # garis bawah bibir
WATER_LIGHT    = (0.42, 0.78, 0.95)   # air cyan terang
WATER_DARK     = (0.28, 0.62, 0.82)   # air dasar (lebih gelap)

# ── Geometri tier ────────────────────────────────────────────────
# Tier 1 (basin bawah)
T1_R           = 2.80
T1_WALL_BOTTOM = 0.10        # dinding mulai di y=0.10 (di atas alas)
T1_WALL_HEIGHT = 0.55        # tinggi dinding
T1_WATER_Y     = T1_WALL_BOTTOM + T1_WALL_HEIGHT - 0.08   # 0.57

# Tier 2 (basin tengah)
T2_CY          = T1_WATER_Y + 0.10   # alas tier 2 berada di atas air tier 1
T2_R           = 1.65
T2_WALL_HEIGHT = 0.65
T2_WATER_Y     = T2_CY + T2_WALL_HEIGHT - 0.08

# Tier 3 (top — cylinder kecil sebagai dudukan spout)
T3_CY          = T2_WATER_Y + 0.10
T3_R           = 0.65
T3_WALL_HEIGHT = 0.55
T3_WATER_Y     = T3_CY + T3_WALL_HEIGHT - 0.08

# Tiang pusat
SPOUT_R        = 0.18
SPOUT_TOP      = T3_WATER_Y + 1.80   # ujung tiang


def draw_fountain(fountain_angle_deg: float):
    cx, cz = _CX, _CZ
    fa = math.radians(fountain_angle_deg)

    _draw_tier(cx, cz, T1_R, T1_WALL_BOTTOM, T1_WALL_HEIGHT, T1_WATER_Y, fa, ripple=True)
    _draw_tier(cx, cz, T2_R, T2_CY,          T2_WALL_HEIGHT, T2_WATER_Y, fa, ripple=True)
    _draw_tier(cx, cz, T3_R, T3_CY,          T3_WALL_HEIGHT, T3_WATER_Y, fa, ripple=False)

    _draw_central_spout(cx, cz, fa)
    _draw_water_jets(cx, cz, fa)


# ─────────────────────────────────────────────────────────────────
# Tier (basin lingkaran dengan dinding + bibir + air)
# ─────────────────────────────────────────────────────────────────
def _draw_tier(cx, cz, radius, y_bottom, wall_h, water_y, fa, ripple=True):
    """
    Gambar satu tier:
      - Alas dasar (disk lebih besar sebagai bayangan)
      - Dinding silinder (warna bluegray)
      - Bibir atas putih (sedikit menonjol)
      - Permukaan air cyan dengan riak halus
    """
    # Bayangan dasar
    color(*WALL_DARKER)
    draw_cylinder(cx, max(0.0, y_bottom - 0.08), cz,
                  radius + 0.10, 0.10, 36)

    # Dinding silinder utama
    color(*WALL_BLUEGRAY)
    draw_cylinder(cx, y_bottom, cz, radius, wall_h, 36)

    # Garis bayangan di bawah dinding (efek shading)
    color(*WALL_DARKER)
    draw_cylinder(cx, y_bottom, cz, radius + 0.005, 0.06, 36)

    # Bibir putih di atas dinding (sedikit menjorok keluar)
    rim_y = y_bottom + wall_h
    color(*RIM_SHADOW)
    draw_cylinder(cx, rim_y - 0.02, cz, radius + 0.13, 0.05, 36)
    color(*RIM_WHITE)
    draw_cylinder(cx, rim_y, cz, radius + 0.10, 0.09, 36)

    # ── Permukaan air (di dalam dinding) ────────────────────────
    inner_r = radius - 0.12

    # Lapisan dasar gelap
    color(*WATER_DARK)
    draw_disk(cx, water_y - 0.02, cz, inner_r, 36)

    # Lapisan utama cyan terang
    color(*WATER_LIGHT)
    draw_disk(cx, water_y, cz, inner_r, 36)

    # Riak halus (cincin yang nafas) — hanya di tier yang `ripple=True`
    if ripple:
        rr = inner_r * 0.55 + 0.10 * math.sin(fa * 2.0)
        color(0.78, 0.94, 1.00)
        draw_disk(cx, water_y + 0.005, cz, rr, 32)


# ─────────────────────────────────────────────────────────────────
# Tiang pusat (dari tier 3 ke atas)
# ─────────────────────────────────────────────────────────────────
def _draw_central_spout(cx, cz, fa):
    # Tiang silinder abu-biru (dari permukaan air tier-3 ke atas)
    color(*WALL_BLUEGRAY)
    draw_cylinder(cx, T3_WATER_Y - 0.02, cz, SPOUT_R, SPOUT_TOP - T3_WATER_Y, 18)

    # Cincin dekoratif di sekitar tiang dekat dasar
    color(*RIM_WHITE)
    draw_cylinder(cx, T3_WATER_Y + 0.04, cz, SPOUT_R + 0.06, 0.05, 18)
    color(*RIM_SHADOW)
    draw_cylinder(cx, T3_WATER_Y + 0.02, cz, SPOUT_R + 0.07, 0.03, 18)

    # Cincin di tengah tiang (variasi)
    mid_y = T3_WATER_Y + (SPOUT_TOP - T3_WATER_Y) * 0.55
    color(*WALL_DARKER)
    draw_cylinder(cx, mid_y, cz, SPOUT_R + 0.03, 0.06, 18)


# ─────────────────────────────────────────────────────────────────
# Pancaran air dari puncak tiang
# ─────────────────────────────────────────────────────────────────
def _draw_water_jets(cx, cz, fa):
    """Air menyembur dari puncak spout, jatuh berbentuk parabola."""
    # Mahkota tetes air di puncak menyebar ke 12 arah
    n_drop = 12
    spread = 0.18 + 0.04 * math.sin(fa * 2.0)
    peak_y = SPOUT_TOP + 0.05

    # Inti pancaran vertikal kecil di atas spout
    color(0.78, 0.94, 1.00)
    glPushMatrix()
    glTranslatef(cx, peak_y, cz)
    glRotatef(-90.0, 1, 0, 0)
    q = gluNewQuadric()
    gluCylinder(q, 0.07, 0.02, 0.30, 12, 1)
    gluDeleteQuadric(q)
    glPopMatrix()

    for i in range(n_drop):
        a = fa * 0.6 + i * (2 * math.pi / n_drop)
        # Tetes-tetes berpola parabola (5 tetes per arah)
        for j in range(5):
            t = j * 0.13
            wx = cx + (spread + 0.55 * t) * math.cos(a)
            wz = cz + (spread + 0.55 * t) * math.sin(a)
            wy = peak_y + 0.20 - 4.5 * t * t
            if wy < T3_WATER_Y + 0.05:
                break
            r = max(0.025, 0.060 - j * 0.008)
            color(0.85, 0.96, 1.00)
            draw_sphere(wx, wy, wz, r, slices=6, stacks=4)
