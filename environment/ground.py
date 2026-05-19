"""
environment/ground.py
---------------------
Tanah berumput hijau cerah, jalan aspal mengelilingi SELURUH sisi
taman, trotoar di sekeliling pagar, area parkir di sisi kiri, dan
jalur setapak di dalam taman.

Layout (ring konsentris, dari dalam ke luar):
  - Park grass            : ±PARK_HALF (±20)
  - Trotoar (krem)        : ±PARK_HALF .. ±SW_OUTER  (lebar 2.0)
  - Jalan aspal           : ±SW_OUTER  .. ±RD_OUTER  (lebar 6.0)
  - Outer (rumput pucat)  : ±RD_OUTER  .. ±OUT_OUTER (lebar 4.0)

Di sisi kiri, strip trotoar diganti area parkir mobil (sama
lebarnya, x=-22..-20).
"""

import math
from OpenGL.GL import *
from core.primitives import (
    color, draw_flat_quad, draw_path_segment, draw_box, draw_disk
)


# ── Dimensi ring konsentris ──────────────────────────────────────
PARK_HALF   = 20.0
SIDEWALK_W  = 2.0
ROAD_W      = 6.0
OUTER_W     = 4.0

SW_INNER    = PARK_HALF                       # 20
SW_OUTER    = PARK_HALF + SIDEWALK_W          # 22
RD_INNER    = SW_OUTER                        # 22
RD_OUTER    = SW_OUTER + ROAD_W               # 28
OUT_OUTER   = RD_OUTER + OUTER_W              # 32

# Mid-line jalan (untuk marka putus-putus)
RD_MID_OUT  = (RD_INNER + RD_OUTER) * 0.5     # 25
RD_MID_NEG  = -RD_MID_OUT

# Warna
GRASS_LIGHT  = (0.42, 0.78, 0.30)
GRASS_BRIGHT = (0.48, 0.82, 0.34)
GRASS_OUTER  = (0.34, 0.62, 0.30)
SIDEWALK_C   = (0.92, 0.88, 0.78)
SIDEWALK_LN  = (0.82, 0.78, 0.68)
ROAD_C       = (0.42, 0.42, 0.45)
ROAD_EDGE    = (0.30, 0.30, 0.34)
MARK_WHITE   = (0.96, 0.96, 0.94)


def draw_ground():
    # ── Rumput taman (hijau saturated cerah) ─────────────────────
    color(*GRASS_LIGHT)
    draw_flat_quad(-PARK_HALF, -PARK_HALF, PARK_HALF, PARK_HALF, y=0.0)

    # Variasi rumput area tengah
    color(*GRASS_BRIGHT)
    draw_flat_quad(-9, -9, 9, 9, y=0.001)

    # ── Trotoar (krem) keliling pagar ────────────────────────────
    # Strip atas, bawah, kiri, kanan. Strip kiri akan ditimpa parkir
    # nanti.
    color(*SIDEWALK_C)
    # depan (z positif)
    draw_flat_quad(-SW_OUTER,  SW_INNER,  SW_OUTER,  SW_OUTER, y=0.01)
    # belakang (z negatif)
    draw_flat_quad(-SW_OUTER, -SW_OUTER,  SW_OUTER, -SW_INNER, y=0.01)
    # kanan (x positif)
    draw_flat_quad( SW_INNER, -SW_INNER,  SW_OUTER,  SW_INNER, y=0.01)
    # kiri (x negatif) — akan ditimpa area parkir
    draw_flat_quad(-SW_OUTER, -SW_INNER, -SW_INNER,  SW_INNER, y=0.01)

    # Garis pemisah ubin trotoar (depan)
    color(*SIDEWALK_LN)
    x = -SW_OUTER
    while x <= SW_OUTER:
        draw_flat_quad(x, SW_INNER, x + 0.04, SW_OUTER, y=0.012)
        x += 1.6
    # Garis ubin (belakang)
    x = -SW_OUTER
    while x <= SW_OUTER:
        draw_flat_quad(x, -SW_OUTER, x + 0.04, -SW_INNER, y=0.012)
        x += 1.6
    # Garis ubin (kanan, sumbu Z)
    z = -SW_INNER
    while z <= SW_INNER:
        draw_flat_quad(SW_INNER, z, SW_OUTER, z + 0.04, y=0.012)
        z += 1.6

    # ── Jalan aspal — ring penuh keliling taman ──────────────────
    color(*ROAD_C)
    # Strip atas (lebar penuh, mencakup pojok)
    draw_flat_quad(-RD_OUTER,  RD_INNER,  RD_OUTER,  RD_OUTER, y=-0.05)
    # Strip bawah
    draw_flat_quad(-RD_OUTER, -RD_OUTER,  RD_OUTER, -RD_INNER, y=-0.05)
    # Strip kanan (di antara strip atas & bawah)
    draw_flat_quad( RD_INNER, -RD_INNER,  RD_OUTER,  RD_INNER, y=-0.05)
    # Strip kiri
    draw_flat_quad(-RD_OUTER, -RD_INNER, -RD_INNER,  RD_INNER, y=-0.05)

    # ── Marka tepi jalan (cat putih solid di dekat trotoar & luar)
    color(*MARK_WHITE)
    edge = 0.10
    # Tepi DALAM (dekat trotoar)
    # atas
    draw_flat_quad(-RD_OUTER,  RD_INNER,        RD_OUTER,  RD_INNER + edge, y=0.005)
    # bawah
    draw_flat_quad(-RD_OUTER, -RD_INNER - edge, RD_OUTER, -RD_INNER,        y=0.005)
    # kanan
    draw_flat_quad( RD_INNER, -RD_INNER, RD_INNER + edge, RD_INNER, y=0.005)
    # kiri
    draw_flat_quad(-RD_INNER - edge, -RD_INNER, -RD_INNER, RD_INNER, y=0.005)

    # Tepi LUAR
    # atas
    draw_flat_quad(-RD_OUTER,  RD_OUTER - edge, RD_OUTER,  RD_OUTER, y=0.005)
    # bawah
    draw_flat_quad(-RD_OUTER, -RD_OUTER, RD_OUTER, -RD_OUTER + edge, y=0.005)
    # kanan
    draw_flat_quad( RD_OUTER - edge, -RD_OUTER, RD_OUTER, RD_OUTER, y=0.005)
    # kiri
    draw_flat_quad(-RD_OUTER, -RD_OUTER, -RD_OUTER + edge, RD_OUTER, y=0.005)

    # ── Marka putus-putus tengah jalan ───────────────────────────
    # Atas (sumbu X)
    pos = -RD_OUTER + 0.6
    while pos < RD_OUTER - 1.6:
        draw_flat_quad(pos,  RD_MID_OUT - 0.08, pos + 1.6, RD_MID_OUT + 0.08, y=0.005)
        pos += 3.6
    # Bawah (sumbu X)
    pos = -RD_OUTER + 0.6
    while pos < RD_OUTER - 1.6:
        draw_flat_quad(pos,  RD_MID_NEG - 0.08, pos + 1.6, RD_MID_NEG + 0.08, y=0.005)
        pos += 3.6
    # Kanan (sumbu Z)
    pos = -RD_OUTER + 0.6
    while pos < RD_OUTER - 1.6:
        draw_flat_quad(RD_MID_OUT - 0.08, pos, RD_MID_OUT + 0.08, pos + 1.6, y=0.005)
        pos += 3.6
    # Kiri (sumbu Z)
    pos = -RD_OUTER + 0.6
    while pos < RD_OUTER - 1.6:
        draw_flat_quad(RD_MID_NEG - 0.08, pos, RD_MID_NEG + 0.08, pos + 1.6, y=0.005)
        pos += 3.6

    # ── Outer (rumput pucat, di luar jalan) ──────────────────────
    color(*GRASS_OUTER)
    # atas
    draw_flat_quad(-OUT_OUTER, RD_OUTER, OUT_OUTER, OUT_OUTER, y=-0.06)
    # bawah
    draw_flat_quad(-OUT_OUTER, -OUT_OUTER, OUT_OUTER, -RD_OUTER, y=-0.06)
    # kanan
    draw_flat_quad(RD_OUTER, -RD_OUTER, OUT_OUTER, RD_OUTER, y=-0.06)
    # kiri
    draw_flat_quad(-OUT_OUTER, -RD_OUTER, -RD_OUTER, RD_OUTER, y=-0.06)

    # ── Area parkir (di sisi kiri, menggantikan trotoar kiri) ────
    color(0.36, 0.36, 0.40)
    draw_flat_quad(-22.0, -20.0, -20.0, 16.0, y=0.005)

    # Garis parkir putih (membatasi tiap slot)
    color(*MARK_WHITE)
    pz = -20.0
    while pz <= 16.0:
        draw_flat_quad(-22.0, pz - 0.05, -20.0, pz + 0.05, y=0.012)
        pz += 3.0

    # ── Driveway: hubungkan parkir dengan jalan atas ─────────────
    # Jalan atas: z=22..28, parkir berakhir di z=16. Driveway
    # menyambung x=-22..-20, z=16..22 sebagai aspal.
    color(*ROAD_C)
    draw_flat_quad(-22.0, 16.0, -20.0, 22.0, y=-0.04)
    # garis tepi driveway
    color(*MARK_WHITE)
    draw_flat_quad(-22.05, 16.0, -22.0, 22.0, y=0.005)
    draw_flat_quad(-20.0,  16.0, -19.95, 22.0, y=0.005)

    # ── Trotoar depan taman (di dalam pagar, plaza gerbang) ──────
    # Tetap dipertahankan sebagai plaza krem antara fountain & gate
    color(*SIDEWALK_C)
    draw_flat_quad(-PARK_HALF, PARK_HALF - 4, PARK_HALF, PARK_HALF - 3, y=0.03)
    color(*SIDEWALK_LN)
    x = -PARK_HALF
    while x <= PARK_HALF:
        draw_flat_quad(x, PARK_HALF - 4, x + 0.04, PARK_HALF - 3, y=0.04)
        x += 1.6


def _ring_path(cx, cz, rx, rz, segs, width, y=0.02):
    """Annulus mulus: tepi dalam & luar pakai radius konstan, sehingga
    sambungan antar segmen share vertex (tidak ada 'gigi gergaji')."""
    half = width * 0.5
    rxi, rxo = rx - half, rx + half
    rzi, rzo = rz - half, rz + half
    glBegin(GL_QUAD_STRIP)
    glNormal3f(0, 1, 0)
    for i in range(segs + 1):
        a = i / segs * 2 * math.pi
        ca, sa = math.cos(a), math.sin(a)
        # Outer
        glVertex3f(cx + rxo * ca, y, cz + rzo * sa)
        # Inner
        glVertex3f(cx + rxi * ca, y, cz + rzi * sa)
    glEnd()


def draw_all_paths():
    glEnable(GL_POLYGON_OFFSET_FILL)
    glPolygonOffset(-1.0, -1.0)

    # Jalur krem-pucat (mirip pavers di referensi)
    color(0.93, 0.88, 0.74)

    # ── Jalur masuk utama dari gerbang (z=16 → 5) ────────────────
    draw_path_segment(0, 16.0, 0, 5.0, 3.0)

    # ── Jalur melingkar utama (r=7) ───────────────────────────────
    RING_R     = 7.0
    RING_WIDTH = 1.6
    _ring_path(0, 0, RING_R, RING_R, 96, RING_WIDTH)

    # ── Jalur radial ─────────────────────────────────────────────
    # Lebar 1.4 m. Disk simpul harus ≥ setengah lebar terbesar yang
    # bertemu di sana; pakai 0.9 m biar kawin halus dengan ring 1.6.
    PATH_W   = 1.4
    JOINT_R  = 0.90

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
        draw_path_segment(x1, z1, x2, z2, PATH_W)

    # ── Disk penutup di setiap simpul agar sudut tidak menganga ──
    # Kumpulkan endpoint unik dari semua radial.
    endpoints = set()
    for x1, z1, x2, z2 in radial:
        endpoints.add((x1, z1))
        endpoints.add((x2, z2))
    for ex, ez in endpoints:
        draw_disk(ex, 0.022, ez, JOINT_R, slices=20)

    # Tutup juga titik tempat radial menyentuh ring (menghilangkan
    # gigi gergaji di perpotongan ring × radial).
    ring_joints = [
        ( 0,  5),  ( 0, -7),
        (-5,  5),  ( 5,  5),    # perkiraan, tidak dipakai langsung
    ]
    for ex, ez in [( 0,  5), ( 0, -7)]:
        # Sudah ditutup di atas via endpoints, tapi pakai disk lebih
        # besar agar menutup pertemuan radial DAN ring sekaligus.
        draw_disk(ex, 0.024, ez, JOINT_R + 0.05, slices=20)

    glDisable(GL_POLYGON_OFFSET_FILL)
    glPolygonOffset(0.0, 0.0)
