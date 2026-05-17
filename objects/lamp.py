"""
objects/lamp.py
---------------
Lampu taman tinggi bergaya klasik (Victorian street lamp) dengan
kepala lentera bersangkar logam + 4 panel kaca transparan, dan
bohlam kuning hangat di dalamnya.

Posisi kandidat dicek dengan `is_blocked()` agar lampu tidak
menimpa aset lain (fountain, gazebo, pergola, pond, toilet,
playground, bike-rack, jalur, pohon, batu, bangku, tong sampah).
"""

import math

from OpenGL.GL import (
    glPushMatrix, glPopMatrix, glTranslatef, glRotatef,
    glEnable, glDisable, glBlendFunc, glDepthMask, glColor4f,
    GL_BLEND, GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA, GL_FALSE, GL_TRUE,
)

from core.primitives import (
    color, draw_cylinder, draw_sphere, draw_box, draw_cone,
)
from core.layout import is_blocked, register_zone


# ────────────────────────────────────────────────────────────────
# Helper: kepala lentera dengan kaca transparan + bohlam
# ────────────────────────────────────────────────────────────────
def _draw_lantern_head(x: float, y_base: float, z: float,
                       cage_w: float = 0.34, cage_h: float = 0.55):
    """
    Kepala lentera dimulai dari `y_base` (alas pelat penyangga).
    Strukturnya:
        y_base                 : pelat penyangga (metal, lebih lebar)
        + 0.06 (cage_y)        : alas sangkar
        + 0.06 + cage_h        : tutup atas sangkar
        + 0.06 + cage_h + ...  : cornice & atap kerucut & finial
    """

    METAL_DARK = (0.14, 0.14, 0.16)
    METAL_MID  = (0.20, 0.20, 0.22)
    METAL_LITE = (0.30, 0.30, 0.34)

    # ── 1. Pelat penyangga (metal solid) ───────────────────────
    color(*METAL_MID)
    draw_box(x, y_base, z, cage_w + 0.12, 0.06, cage_w + 0.12)

    cage_y      = y_base + 0.06
    bulb_y      = cage_y + cage_h * 0.55
    cage_top_y  = cage_y + cage_h
    half_w      = cage_w * 0.5
    post_t      = 0.04                  # tebal tiang sudut

    # ── 2. Empat tiang sudut (rangka logam tegak) ──────────────
    color(*METAL_DARK)
    for sx in (-half_w + post_t * 0.5, half_w - post_t * 0.5):
        for sz in (-half_w + post_t * 0.5, half_w - post_t * 0.5):
            draw_box(x + sx, cage_y, z + sz, post_t, cage_h, post_t)

    # ── 3. Rangka horizontal atas & bawah sangkar ──────────────
    rim_t = 0.04
    rim_h = 0.04
    color(*METAL_MID)
    # Bawah (4 batang sepanjang tepi)
    draw_box(x, cage_y, z - half_w + rim_t * 0.5,
             cage_w, rim_h, rim_t)
    draw_box(x, cage_y, z + half_w - rim_t * 0.5,
             cage_w, rim_h, rim_t)
    draw_box(x - half_w + rim_t * 0.5, cage_y, z,
             rim_t, rim_h, cage_w - rim_t * 2)
    draw_box(x + half_w - rim_t * 0.5, cage_y, z,
             rim_t, rim_h, cage_w - rim_t * 2)
    # Atas (4 batang sepanjang tepi)
    rim_top_y = cage_top_y - rim_h
    draw_box(x, rim_top_y, z - half_w + rim_t * 0.5,
             cage_w, rim_h, rim_t)
    draw_box(x, rim_top_y, z + half_w - rim_t * 0.5,
             cage_w, rim_h, rim_t)
    draw_box(x - half_w + rim_t * 0.5, rim_top_y, z,
             rim_t, rim_h, cage_w - rim_t * 2)
    draw_box(x + half_w - rim_t * 0.5, rim_top_y, z,
             rim_t, rim_h, cage_w - rim_t * 2)

    # Palang silang horizontal di tengah (mid rail dekoratif)
    mid_y = cage_y + cage_h * 0.50 - rim_h * 0.5
    color(*METAL_LITE)
    draw_box(x, mid_y, z - half_w + rim_t * 0.5,
             cage_w - post_t * 2, rim_h * 0.6, rim_t * 0.6)
    draw_box(x, mid_y, z + half_w - rim_t * 0.5,
             cage_w - post_t * 2, rim_h * 0.6, rim_t * 0.6)
    draw_box(x - half_w + rim_t * 0.5, mid_y, z,
             rim_t * 0.6, rim_h * 0.6, cage_w - post_t * 2)
    draw_box(x + half_w - rim_t * 0.5, mid_y, z,
             rim_t * 0.6, rim_h * 0.6, cage_w - post_t * 2)

    # ── 4. Bohlam pijar di dalam sangkar ───────────────────────
    # Bentuk klasik: kepala bulat → leher pendek → ulir logam.
    # Posisi y_anchor = pusat envelope kaca (kepala bulat).
    bulb_base_y = cage_y + 0.05                   # alas ulir logam
    base_h      = 0.06                            # ulir logam
    neck_h      = 0.05                            # leher kaca
    bulb_r      = 0.10                            # radius envelope
    bulb_center_y = bulb_base_y + base_h + neck_h + bulb_r

    # 4a. Ulir logam (silver mengkilap)
    color(0.78, 0.78, 0.82)
    draw_cylinder(x, bulb_base_y, z, 0.045, base_h, 10)
    # Garis ulir tipis (3 cincin)
    color(0.55, 0.55, 0.58)
    for i in range(3):
        draw_cylinder(x, bulb_base_y + 0.012 + i * 0.018, z,
                      0.048, 0.006, 10)
    # Tip kontak hitam di bawah ulir
    color(0.10, 0.10, 0.12)
    draw_cylinder(x, bulb_base_y - 0.018, z, 0.030, 0.018, 8)

    # 4b. Leher kaca yang menyempit (cone)
    color(1.00, 0.92, 0.55)
    draw_cone(x, bulb_base_y + base_h, z, bulb_r * 0.55, neck_h, 12)

    # 4c. Envelope kaca (kepala bulat) — kuning hangat
    color(1.00, 0.93, 0.50)
    draw_sphere(x, bulb_center_y, z, bulb_r, slices=16, stacks=12)

    # 4d. Highlight kecil di bagian atas (lebih cerah, seperti pantulan)
    color(1.00, 1.00, 0.82)
    draw_sphere(x, bulb_center_y + bulb_r * 0.45, z,
                bulb_r * 0.35, slices=12, stacks=8)

    # Update bulb_y reference untuk perhitungan panel di bawah
    bulb_y = bulb_center_y

    # ── 5. Empat panel kaca (transparan, blending) ─────────────
    # Digambar SETELAH bohlam supaya menutupinya secara tembus pandang.
    # Depth write dimatikan agar urutan antar panel tidak bermasalah.
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glDepthMask(GL_FALSE)

    # Warna kaca: biru-pucat, alpha rendah → bohlam tetap terlihat
    glColor4f(0.82, 0.92, 1.00, 0.28)

    pane_h = cage_h - rim_h * 2 - 0.01
    pane_w = cage_w - post_t * 2 - 0.01
    pane_t = 0.015
    pane_y = cage_y + rim_h + pane_h * 0.5 - pane_h * 0.5  # bawah pane
    pane_cy = cage_y + cage_h * 0.5

    # Panel sumbu Z (depan & belakang)
    draw_box(x, pane_cy - pane_h * 0.0, z - half_w + pane_t,
             pane_w, pane_h, pane_t)
    draw_box(x, pane_cy - pane_h * 0.0, z + half_w - pane_t,
             pane_w, pane_h, pane_t)
    # Panel sumbu X (kiri & kanan)
    draw_box(x - half_w + pane_t, pane_cy, z,
             pane_t, pane_h, pane_w)
    draw_box(x + half_w - pane_t, pane_cy, z,
             pane_t, pane_h, pane_w)

    glDepthMask(GL_TRUE)
    glDisable(GL_BLEND)

    # ── 6. Cornice (lis di atas sangkar) ───────────────────────
    color(*METAL_MID)
    draw_box(x, cage_top_y, z, cage_w + 0.10, 0.05, cage_w + 0.10)
    color(*METAL_DARK)
    draw_box(x, cage_top_y + 0.05, z, cage_w + 0.04, 0.04, cage_w + 0.04)

    # ── 7. Atap kerucut + finial ───────────────────────────────
    roof_y = cage_top_y + 0.09
    color(*METAL_DARK)
    draw_cone(x, roof_y, z, cage_w * 0.62, 0.22, 8)

    neck_y = roof_y + 0.22
    color(*METAL_MID)
    draw_cylinder(x, neck_y, z, 0.06, 0.06, 8)

    color(*METAL_LITE)
    draw_sphere(x, neck_y + 0.10, z, 0.07)
    color(*METAL_DARK)
    draw_cone(x, neck_y + 0.14, z, 0.04, 0.30, 6)
    color(0.85, 0.70, 0.30)             # tip emas
    draw_sphere(x, neck_y + 0.46, z, 0.035)


# ────────────────────────────────────────────────────────────────
# Lampu taman klasik tinggi
# ────────────────────────────────────────────────────────────────
def draw_lamp(x: float, z: float, height: float = 5.6):
    """
    Lampu taman tinggi (default 5.6 m) dengan kepala lentera kaca
    dan bohlam kuning di dalamnya. `height` = jarak dari tanah ke
    pangkal kepala lentera.
    """

    METAL_DARK = (0.13, 0.13, 0.15)
    METAL_MID  = (0.22, 0.22, 0.24)
    METAL_LITE = (0.20, 0.20, 0.22)

    # ── 1. Basis berundak (pondasi 3 lapis) ────────────────────
    color(*METAL_MID)
    draw_box(x, 0.00, z, 0.62, 0.18, 0.62)
    color(0.18, 0.18, 0.20)
    draw_cylinder(x, 0.18, z, 0.26, 0.14, 12)
    color(*METAL_DARK)
    draw_cylinder(x, 0.32, z, 0.20, 0.10, 12)

    # ── 2. Tiang utama (panjang & ramping) ─────────────────────
    pole_base = 0.42
    pole_h    = height - pole_base
    color(*METAL_DARK)
    draw_cylinder(x, pole_base, z, 0.075, pole_h, 12)

    # ── 3. Flange / cincin dekorasi ─────────────────────────────
    color(*METAL_MID)
    draw_cylinder(x, pole_base + 0.05, z, 0.13, 0.10, 12)
    draw_cylinder(x, pole_base + pole_h * 0.50 - 0.06, z, 0.12, 0.12, 12)
    color(*METAL_LITE)
    draw_cylinder(x, pole_base + pole_h * 0.50 + 0.08, z, 0.10, 0.05, 12)
    draw_cylinder(x, pole_base + pole_h * 0.78, z, 0.11, 0.06, 12)

    # ── 4. Lengan ornamen (scroll) di bawah kepala lentera ─────
    head_base_y = height
    arm_y       = head_base_y - 0.10
    for ang in (0, 90, 180, 270):
        glPushMatrix()
        glTranslatef(x, arm_y, z)
        glRotatef(ang, 0, 1, 0)
        color(*METAL_LITE)
        draw_box(0.18, 0.00, 0.0, 0.32, 0.05, 0.05)
        color(*METAL_MID)
        draw_sphere(0.34, 0.00, 0.0, 0.06)
        glPopMatrix()

    # ── 5. Kepala lentera dengan kaca + bohlam ─────────────────
    _draw_lantern_head(x, head_base_y, z, cage_w=0.34, cage_h=0.55)


# ────────────────────────────────────────────────────────────────
# Penempatan lampu
# ────────────────────────────────────────────────────────────────
def draw_all_lamps():
    positions = [
        # ── Jalur masuk utama ──────────────────────────────────
        (-2.5, 14.5), ( 2.5, 14.5),
        (-2.5, 11.0), ( 2.5, 11.0),
        (-2.5,  7.5), ( 2.5,  7.5),

        # ── Cardinal di luar cincin fountain (r=7) ─────────────
        (-9.5,  0.0), ( 9.5,  0.0),

        # ── Sisi kiri (sekitar pergola & bike rack) ────────────
        (-13.0,   1.0),
        ( -9.0,   9.0),
        ( -7.0,  -9.5),

        # ── Sisi kanan (gazebo & pond) ─────────────────────────
        ( 14.0,   9.5),
        ( 18.0,   5.0),
        ( 11.0,   2.0),
        ( 16.0,  -8.0),

        # ── Area selatan ───────────────────────────────────────
        (  4.0, -12.0),
        ( -2.0, -14.5),
        ( -5.5, -16.5),

        # ── Pojok / perimeter ──────────────────────────────────
        (-17.0,  13.0), ( 17.0,  13.0),
        (-17.0, -16.0), ( 17.0, -16.0),
        (-17.0,   2.0), ( 17.0,   2.0),
    ]

    BUFFER = 0.5
    for lx, lz in positions:
        if is_blocked(lx, lz, BUFFER):
            continue
        draw_lamp(lx, lz)
        register_zone(lx, lz, 0.55)
