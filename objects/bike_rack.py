"""
objects/bike_rack.py
--------------------
Rak parkir sepeda + sepeda terparkir dilihat dari samping.

Setiap sepeda berorientasi sepanjang sumbu Z (perpendikular terhadap
rel rak yang membentang sumbu X). Roda berputar pada poros sumbu X
sehingga terlihat sebagai lingkaran tegak dari samping.
"""

import math

from OpenGL.GL  import (
    glPushMatrix, glPopMatrix, glTranslatef, glRotatef,
)
from OpenGL.GLU import (
    gluNewQuadric, gluCylinder, gluDisk, gluDeleteQuadric,
)

from core.primitives import color, draw_box, draw_cylinder, draw_sphere


# ────────────────────────────────────────────────────────────────
# Helper: silinder horizontal (axle sepanjang sumbu X / Z)
# ────────────────────────────────────────────────────────────────
def _hcyl(x: float, y: float, z: float,
          radius: float, length: float,
          axis: str = 'x', slices: int = 12):
    """Silinder horizontal dengan PUSAT di (x, y, z)."""
    glPushMatrix()
    glTranslatef(x, y, z)
    if axis == 'x':
        glRotatef(90.0, 0, 1, 0)
        glTranslatef(0, 0, -length * 0.5)
    elif axis == 'z':
        glTranslatef(0, 0, -length * 0.5)
    q = gluNewQuadric()
    gluCylinder(q, radius, radius, length, slices, 1)
    gluDisk(q, 0, radius, slices, 1)
    glTranslatef(0, 0, length)
    gluDisk(q, 0, radius, slices, 1)
    gluDeleteQuadric(q)
    glPopMatrix()


# ────────────────────────────────────────────────────────────────
# Helper: silinder ramping miring (untuk tube rangka)
# ────────────────────────────────────────────────────────────────
def _bar(x1, y1, z1, x2, y2, z2, radius=0.03):
    dx, dy, dz = x2 - x1, y2 - y1, z2 - z1
    length = math.sqrt(dx * dx + dy * dy + dz * dz)
    if length < 1e-6:
        return
    glPushMatrix()
    glTranslatef(x1, y1, z1)
    nx, ny, nz = dx / length, dy / length, dz / length
    ax, ay = -ny, nx
    angle = math.degrees(math.acos(max(-1.0, min(1.0, nz))))
    if abs(ax) + abs(ay) > 1e-6:
        glRotatef(angle, ax, ay, 0)
    elif nz < 0:
        glRotatef(180.0, 1, 0, 0)
    q = gluNewQuadric()
    gluCylinder(q, radius, radius, length, 8, 1)
    gluDeleteQuadric(q)
    glPopMatrix()


# ────────────────────────────────────────────────────────────────
# Sepeda (orientasi sumbu Z, dilihat dari +X / -X)
# ────────────────────────────────────────────────────────────────
def draw_bicycle(x: float, z: float,
                 color_rgb=(0.18, 0.38, 0.70)):
    """
    Sepeda profil samping. Pusat sepeda di (x, z).
      - Roda depan di z + 0.42 (ke +Z)
      - Roda belakang di z - 0.42 (ke -Z)
      - Lebar ke samping (handlebar) sepanjang sumbu X
    """
    cr, cg, cb = color_rgb

    # ── Geometri dasar ───────────────────────────────────────────
    wheel_r  = 0.26
    tire_w   = 0.06
    rim_w    = 0.03
    fz       = z + 0.42        # roda depan
    rz       = z - 0.42        # roda belakang
    wy       = wheel_r         # pusat roda menyentuh tanah

    # ── Roda (poros sumbu X) ─────────────────────────────────────
    # Ban hitam
    color(0.10, 0.10, 0.12)
    _hcyl(x, wy, fz, wheel_r, tire_w, axis='x', slices=18)
    _hcyl(x, wy, rz, wheel_r, tire_w, axis='x', slices=18)
    # Pelek silver tipis di tengah ban
    color(0.78, 0.78, 0.80)
    _hcyl(x, wy, fz, wheel_r * 0.62, rim_w, axis='x', slices=14)
    _hcyl(x, wy, rz, wheel_r * 0.62, rim_w, axis='x', slices=14)
    # Hub poros (silver gelap)
    color(0.42, 0.42, 0.44)
    _hcyl(x, wy, fz, 0.045, tire_w * 1.5, axis='x', slices=8)
    _hcyl(x, wy, rz, 0.045, tire_w * 1.5, axis='x', slices=8)

    # ── Bottom bracket (pusat crank, di bawah seat tube) ────────
    bb_y = 0.30
    bb_z = z + 0.05
    color(0.30, 0.30, 0.34)
    _hcyl(x, bb_y, bb_z, 0.05, 0.10, axis='x', slices=8)

    # ── Titik referensi rangka ──────────────────────────────────
    saddle_y    = 0.92                       # tinggi sadel
    saddle_z    = z - 0.08                   # geser ke belakang
    head_top_y  = 0.86                       # ujung atas headtube
    head_bot_y  = wy + 0.18                  # ujung bawah headtube (atas roda)
    head_z      = fz - 0.06                  # depan, dekat roda depan

    # ── Rangka utama (warna sepeda) ─────────────────────────────
    color(cr, cg, cb)
    # Down tube  : BB → head bottom
    _bar(x, bb_y, bb_z, x, head_bot_y, head_z, radius=0.038)
    # Seat tube  : BB → saddle
    _bar(x, bb_y, bb_z, x, saddle_y, saddle_z, radius=0.038)
    # Top tube   : saddle ↔ head top
    _bar(x, saddle_y - 0.04, saddle_z, x, head_top_y, head_z, radius=0.038)
    # Chain stay : BB → roda belakang
    _bar(x, bb_y, bb_z, x, wy, rz, radius=0.028)
    # Seat stay  : sadel → roda belakang
    _bar(x, saddle_y - 0.04, saddle_z, x, wy, rz, radius=0.026)

    # ── Fork depan (head bottom → hub roda depan, dua bilah) ────
    color(0.45, 0.45, 0.48)
    for fx_off in (-tire_w * 0.7, tire_w * 0.7):
        _bar(x + fx_off, head_bot_y, head_z,
             x + fx_off, wy,         fz,
             radius=0.022)

    # ── Headtube (silinder pendek) ──────────────────────────────
    color(0.30, 0.30, 0.34)
    _bar(x, head_bot_y, head_z, x, head_top_y, head_z, radius=0.045)

    # ── Stem & handlebar ────────────────────────────────────────
    stem_top_y = head_top_y + 0.08
    stem_top_z = head_z + 0.06
    color(0.30, 0.30, 0.34)
    _bar(x, head_top_y, head_z, x, stem_top_y, stem_top_z, radius=0.028)

    # Handlebar membentang sumbu X
    color(0.18, 0.18, 0.20)
    _hcyl(x, stem_top_y, stem_top_z, 0.024, 0.40, axis='x', slices=10)
    # Grip karet hitam di kedua ujung
    color(0.08, 0.08, 0.10)
    for hx in (-0.18, 0.18):
        _hcyl(x + hx, stem_top_y, stem_top_z, 0.030, 0.06, axis='x', slices=8)

    # ── Sadel ───────────────────────────────────────────────────
    color(0.10, 0.10, 0.12)
    draw_box(x, saddle_y, saddle_z, 0.10, 0.04, 0.24)
    # Lengkungan depan sadel (sphere kecil)
    draw_sphere(x, saddle_y + 0.02, saddle_z + 0.10, 0.05)

    # ── Crank arm + pedal (di sisi +X) ──────────────────────────
    color(0.20, 0.20, 0.22)
    crank_end_y = bb_y - 0.12
    crank_end_z = bb_z + 0.10
    _bar(x + 0.06, bb_y, bb_z,
         x + 0.06, crank_end_y, crank_end_z, radius=0.020)
    color(0.12, 0.12, 0.14)
    draw_box(x + 0.06, crank_end_y - 0.02, crank_end_z, 0.10, 0.03, 0.06)


# ────────────────────────────────────────────────────────────────
# Rak parkir
# ────────────────────────────────────────────────────────────────
def draw_bike_rack():
    bx, bz = -14.0, 8.0

    # ── Papan tanda "Bike Parking" ──────────────────────────────
    sign_x = bx - 1.9
    sign_z = bz - 1.0
    color(0.20, 0.20, 0.24)
    draw_cylinder(sign_x, 0.0, sign_z, 0.05, 1.85, 6)

    # Latar biru
    color(0.18, 0.42, 0.78)
    draw_box(sign_x, 1.55, sign_z, 0.80, 0.55, 0.05)
    # Bingkai putih tipis
    color(0.95, 0.95, 0.95)
    draw_box(sign_x, 1.55, sign_z + 0.03, 0.74, 0.49, 0.01)
    # Latar biru di dalam bingkai
    color(0.18, 0.42, 0.78)
    draw_box(sign_x, 1.55, sign_z + 0.04, 0.70, 0.45, 0.01)

    # Tulisan "PARKIR" di bagian atas papan
    from core.text3d import draw_text
    draw_text("PARKIR",
              cx=sign_x, cy=1.68, cz=sign_z + 0.06,
              height=0.16, depth=0.02,
              color_rgb=(0.95, 0.95, 0.95))
    # "SEPEDA" di bawah
    draw_text("SEPEDA",
              cx=sign_x, cy=1.42, cz=sign_z + 0.06,
              height=0.16, depth=0.02,
              color_rgb=(0.95, 0.95, 0.95))

    # ── Rangka rak besi ─────────────────────────────────────────
    color(0.42, 0.42, 0.46)
    draw_box(bx, 0.0,  bz, 3.2, 0.07, 0.12)    # rel bawah
    draw_box(bx, 0.55, bz, 3.2, 0.07, 0.12)    # rel atas

    # Tiang vertikal (penyangga rak)
    color(0.32, 0.32, 0.36)
    for ox in (-1.55, 0.0, 1.55):
        draw_cylinder(bx + ox, 0.0, bz, 0.05, 0.62, 6)

    # "Loop" tempat mengunci roda depan — silinder vertikal pendek
    # di antara dua bike, sejajar rel bawah
    color(0.50, 0.50, 0.54)
    for i in range(6):
        rx = bx - 1.5 + i * 0.60
        draw_cylinder(rx, 0.07, bz, 0.035, 0.50, 6)

    # ── Sepeda terparkir (5 buah, warna berbeda) ────────────────
    bike_colors = [
        (0.88, 0.18, 0.18),    # merah
        (0.18, 0.42, 0.78),    # biru
        (0.96, 0.78, 0.10),    # kuning
        (0.18, 0.62, 0.30),    # hijau
        (0.62, 0.22, 0.74),    # ungu
    ]
    # Bikes berorientasi sepanjang sumbu Z, jadi disebar sepanjang X
    # dengan jarak 0.60 (cukup untuk handlebar lebar 0.40).
    for i, col in enumerate(bike_colors):
        bike_x = bx - 1.20 + i * 0.60
        bike_z = bz + 0.55          # bike center, back wheel ~ rel rak
        draw_bicycle(bike_x, bike_z, col)
