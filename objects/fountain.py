"""
objects/fountain.py
-------------------
Air mancur dua tingkat realistis.

Kunci agar terlihat seperti air sungguhan:
  - Pancaran air dibuat dari KOLOM kontinu (cone/cylinder),
    bukan rangkaian bola kecil yang tampak seperti manik-manik.
  - Tirai kaskade pakai frustum (silinder dengan radius beda
    di atas dan bawah) sehingga seperti lembar air jatuh.
  - Riak permukaan minim, hanya 1–2 lapis lembut.
"""

import math
from OpenGL.GL  import (glPushMatrix, glPopMatrix, glTranslatef, glRotatef,
                        glScalef, glEnable, glDisable, glBlendFunc, GL_BLEND,
                        GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA, glColor4f,
                        glDepthMask, GL_FALSE, GL_TRUE)
from OpenGL.GLU import gluNewQuadric, gluCylinder, gluDisk, gluDeleteQuadric

from core.primitives import color, draw_cylinder, draw_disk, draw_sphere


_CX, _CZ = 0.0, 0.0   # pusat air mancur

# Geometri (mudah di-tune)
_BASIN_R       = 2.80
_WATER_LEVEL   = 0.50
_PEDESTAL_TOP  = 1.85   # bibir mangkuk atas
_BOWL_R        = 0.85
_NOZZLE_TOP    = 2.32


def draw_fountain(fountain_angle_deg: float):
    cx, cz = _CX, _CZ
    fa_rad = math.radians(fountain_angle_deg)

    _draw_basin(cx, cz)
    _draw_water_surface(cx, cz, fa_rad)
    _draw_pedestal(cx, cz)
    _draw_upper_bowl(cx, cz)
    _draw_cascade_veil(cx, cz, fa_rad)      # tirai air dari mangkuk atas
    _draw_central_column(cx, cz, fa_rad)    # kolom air vertikal
    _draw_mist_at_peak(cx, cz, fa_rad)      # percik di puncak


# ─────────────────────────────────────────────────────────────────
# Basin (kolam batu)
# ─────────────────────────────────────────────────────────────────
def _draw_basin(cx, cz):
    # Alas dekoratif sedikit lebih lebar
    color(0.55, 0.52, 0.48)
    draw_cylinder(cx, 0.00, cz, _BASIN_R + 0.18, 0.10, 36)

    # Dinding kolam
    color(0.74, 0.72, 0.68)
    draw_cylinder(cx, 0.10, cz, _BASIN_R, 0.45, 36)

    # Bibir atas (cerah, sedikit menonjol)
    color(0.84, 0.82, 0.78)
    draw_cylinder(cx, 0.55, cz, _BASIN_R + 0.05, 0.08, 36)

    # Garis dekoratif tengah
    color(0.58, 0.55, 0.50)
    draw_cylinder(cx, 0.30, cz, _BASIN_R + 0.005, 0.04, 36)


# ─────────────────────────────────────────────────────────────────
# Permukaan air basin (gradasi halus + 1 ripple lembut)
# ─────────────────────────────────────────────────────────────────
def _draw_water_surface(cx, cz, fa_rad):
    # Dasar agak gelap
    color(0.10, 0.28, 0.42)
    draw_disk(cx, 0.20, cz, _BASIN_R - 0.18, 40)

    # Lapisan menengah
    color(0.18, 0.42, 0.58)
    draw_disk(cx, 0.36, cz, _BASIN_R - 0.30, 40)

    # Permukaan utama
    color(0.30, 0.60, 0.80)
    draw_disk(cx, _WATER_LEVEL, cz, _BASIN_R - 0.20, 48)

    # Riak halus (1 cincin yang nafas)
    rr = 1.05 + 0.10 * math.sin(fa_rad * 2.0)
    if rr < _BASIN_R - 0.30:
        color(0.50, 0.78, 0.94)
        draw_disk(cx, _WATER_LEVEL + 0.004, cz, rr, 40)

    # Highlight kecil di tengah
    color(0.62, 0.86, 0.98)
    draw_disk(cx, _WATER_LEVEL + 0.008, cz, 0.32, 24)


# ─────────────────────────────────────────────────────────────────
# Pedestal pilar
# ─────────────────────────────────────────────────────────────────
def _draw_pedestal(cx, cz):
    # Alas pedestal di dalam basin
    color(0.66, 0.64, 0.58)
    draw_cylinder(cx, 0.55, cz, 0.78, 0.18, 20)
    color(0.50, 0.48, 0.44)
    draw_cylinder(cx, 0.72, cz, 0.82, 0.04, 20)

    # Pilar utama (sedikit mengecil ke atas pakai dua silinder)
    color(0.78, 0.76, 0.70)
    draw_cylinder(cx, 0.76, cz, 0.30, 0.95, 18)

    # Cincin di tengah pilar
    color(0.55, 0.52, 0.48)
    draw_cylinder(cx, 1.20, cz, 0.34, 0.05, 18)


# ─────────────────────────────────────────────────────────────────
# Mangkuk atas
# ─────────────────────────────────────────────────────────────────
def _draw_upper_bowl(cx, cz):
    # Dasar bowl yang lebih kecil (bagian bawah mangkuk)
    color(0.66, 0.64, 0.58)
    _draw_frustum(cx, 1.65, cz, top_r=_BOWL_R - 0.05,
                  bottom_r=0.36, height=0.18, slices=24)

    # Bibir atas (paling lebar)
    color(0.84, 0.82, 0.78)
    draw_cylinder(cx, 1.83, cz, _BOWL_R, 0.07, 24)

    # Permukaan air di mangkuk
    color(0.30, 0.58, 0.78)
    draw_disk(cx, _PEDESTAL_TOP + 0.05, cz, _BOWL_R - 0.05, 28)
    color(0.55, 0.82, 0.96)
    draw_disk(cx, _PEDESTAL_TOP + 0.058, cz, 0.38, 20)

    # Nozel kecil pusat
    color(0.55, 0.52, 0.48)
    draw_cylinder(cx, _PEDESTAL_TOP + 0.05, cz, 0.09, 0.27, 12)
    color(0.72, 0.70, 0.64)
    draw_disk(cx, _NOZZLE_TOP, cz, 0.11, 12)


# ─────────────────────────────────────────────────────────────────
# Tirai kaskade dari bibir mangkuk
# ─────────────────────────────────────────────────────────────────
def _draw_cascade_veil(cx, cz, fa_rad):
    """
    Lembar air kontinu jatuh dari bibir mangkuk ke basin.
    Pakai frustum: radius atas = bibir mangkuk, radius bawah sedikit
    lebih lebar (efek air menyebar saat jatuh).
    Beberapa lapis dengan ketinggian + offset radius berbeda untuk
    memberi kesan tebal & beriak.
    """
    fall_top    = _PEDESTAL_TOP + 0.02
    fall_bottom = _WATER_LEVEL + 0.02
    height      = fall_top - fall_bottom

    # Lembar luar (utama) — semi transparan
    breathe = 0.04 * math.sin(fa_rad * 1.5)
    color(0.62, 0.84, 0.96)
    _draw_frustum(cx, fall_bottom, cz,
                  top_r=_BOWL_R + 0.00 + breathe,
                  bottom_r=_BOWL_R + 0.32,
                  height=height, slices=40)

    # Lembar dalam (lebih cerah, sedikit di belakang)
    color(0.78, 0.92, 1.00)
    _draw_frustum(cx, fall_bottom + 0.05, cz,
                  top_r=_BOWL_R - 0.02,
                  bottom_r=_BOWL_R + 0.20,
                  height=height - 0.05, slices=40)

    # Genangan air kecil di pangkal kaskade (cincin di permukaan)
    color(0.70, 0.90, 1.00)
    draw_disk(cx, _WATER_LEVEL + 0.011, cz, _BOWL_R + 0.42, 36)
    color(0.30, 0.60, 0.82)
    draw_disk(cx, _WATER_LEVEL + 0.010, cz, _BOWL_R + 0.05, 28)


# ─────────────────────────────────────────────────────────────────
# Kolom air vertikal pusat
# ─────────────────────────────────────────────────────────────────
def _draw_central_column(cx, cz, fa_rad):
    """
    Kolom air naik dari nozel pusat. Dua kerucut tumpuk:
      - bawah: radius mengecil dari nozel ke tinggi puncak
      - atas: ujung kerucut sangat tipis, kesan air melebar lalu jatuh
    """
    # Sedikit gerakan napas vertikal
    breathe = 0.10 * math.sin(fa_rad * 2.0)
    peak_y  = _NOZZLE_TOP + 1.60 + breathe

    # Bagian utama kolom (dari nozel ke puncak, mengecil)
    color(0.70, 0.90, 1.00)
    _draw_frustum(cx, _NOZZLE_TOP, cz,
                  top_r=0.04, bottom_r=0.13,
                  height=peak_y - _NOZZLE_TOP, slices=14)

    # Inti dalam kolom (lebih cerah, lebih tipis)
    color(0.90, 0.97, 1.00)
    _draw_frustum(cx, _NOZZLE_TOP, cz,
                  top_r=0.02, bottom_r=0.07,
                  height=peak_y - _NOZZLE_TOP - 0.05, slices=14)

    # Mahkota di puncak — bola pecah jadi tetesan menyebar
    n_drop = 14
    spread_rad = 0.22 + 0.04 * math.sin(fa_rad * 3.0)
    for i in range(n_drop):
        a = fa_rad * 0.8 + i * (2 * math.pi / n_drop)
        # Tetesan jatuh ke luar dari puncak (sedikit parabola)
        for j in range(5):
            t = j * 0.10
            wx = cx + (spread_rad + 0.55 * t) * math.cos(a)
            wz = cz + (spread_rad + 0.55 * t) * math.sin(a)
            wy = peak_y + 0.20 - 5.5 * t * t   # parabola turun
            if wy < _PEDESTAL_TOP + 0.10:
                break
            r = max(0.018, 0.045 - j * 0.005)
            color(0.85, 0.96, 1.00)
            draw_sphere(wx, wy, wz, r, slices=6, stacks=4)


# ─────────────────────────────────────────────────────────────────
# Mist halus di puncak kolom
# ─────────────────────────────────────────────────────────────────
def _draw_mist_at_peak(cx, cz, fa_rad):
    peak_y = _NOZZLE_TOP + 1.60
    n = 8
    for k in range(n):
        a = fa_rad * 0.5 + k * (2 * math.pi / n)
        rad = 0.10 + 0.05 * math.sin(fa_rad * 2 + k * 0.7)
        mx = cx + rad * math.cos(a)
        mz = cz + rad * math.sin(a)
        my = peak_y + 0.18 + 0.06 * math.sin(fa_rad * 3 + k)
        color(0.94, 0.98, 1.00)
        draw_sphere(mx, my, mz, 0.045, slices=6, stacks=4)


# ─────────────────────────────────────────────────────────────────
# Helper: frustum (silinder dengan radius atas != bawah)
# ─────────────────────────────────────────────────────────────────
def _draw_frustum(x, y_bottom, z, top_r, bottom_r, height, slices=20):
    """
    gluCylinder mendukung radius atas != bawah.
    bottom_r adalah radius pada y_bottom; top_r adalah radius pada
    y_bottom + height.
    """
    glPushMatrix()
    glTranslatef(x, y_bottom, z)
    glRotatef(-90.0, 1, 0, 0)   # Z-axis di OpenGL → Y di scene
    q = gluNewQuadric()
    gluCylinder(q, bottom_r, top_r, height, slices, 1)
    gluDeleteQuadric(q)
    glPopMatrix()
