"""
objects/pond.py
---------------
Kolam ikan oval dengan tepi batu alam, teratai, angsa berenang
(animasi), dan jembatan kayu yang TINGGI dengan gorong-gorong di
bawahnya — sehingga angsa lewat di bawah jembatan (tidak menembus).
"""

import math
from OpenGL.GL import *
from OpenGL.GLU import *
from core.primitives import color, draw_box, draw_sphere, draw_cylinder, draw_disk


_PX, _PZ = 11.0, -3.0   # pusat kolam

# ── Geometri jembatan (dipakai juga untuk validasi animasi angsa) ──
_BRIDGE_X       = _PX + 2.9          # 13.9
_BRIDGE_DECK_Y  = 1.10               # alas dek (cukup tinggi agar angsa lewat)
_BRIDGE_HALF_W  = 0.65               # setengah lebar dek di sumbu Z
_BRIDGE_HALF_L  = 1.40               # setengah panjang dek di sumbu X


def draw_pond(anim_time: float, bird_angle_deg: float):
    px, pz = _PX, _PZ

    # ── Tepi tanah basah di sekitar kolam ─────────────────────────
    color(0.42, 0.32, 0.20)
    glPushMatrix()
    glTranslatef(px, 0.01, pz)
    glScalef(4.5, 0.04, 3.2)
    q = gluNewQuadric()
    gluSphere(q, 1.0, 24, 8)
    gluDeleteQuadric(q)
    glPopMatrix()

    # ── Batu tepi kolam (abu-abu cerah) ──────────────────────────
    color(0.65, 0.62, 0.58)
    n_stones = 22
    for i in range(n_stones):
        a = i / n_stones * 2 * math.pi
        rx = px + 3.85 * math.cos(a)
        rz = pz + 2.65 * math.sin(a)
        size = 0.24 + 0.18 * (i % 3) / 2.0
        draw_sphere(rx, size * 0.5, rz, size)

    # ── Air kolam (cyan terang ala referensi) ─────────────────────
    color(0.30, 0.65, 0.85)
    glPushMatrix()
    glTranslatef(px, 0.10, pz)
    glScalef(3.4, 0.06, 2.3)
    q = gluNewQuadric()
    gluSphere(q, 1.0, 32, 12)
    gluDeleteQuadric(q)
    glPopMatrix()

    # Permukaan air (lebih terang)
    color(0.55, 0.85, 0.97)
    draw_disk(px, 0.16, pz, 3.30, 36)

    # Highlight cahaya di tengah
    color(0.78, 0.94, 1.00)
    draw_disk(px, 0.165, pz, 1.80, 32)

    # ── Tanaman air (teratai) ────────────────────────────────────
    lily_pos = [
        (px - 1.4, pz - 0.7, 0.32, 0.95, 0.45, 0.55),
        (px + 1.0, pz + 0.8, 0.30, 0.30, 0.65, 0.92),
        (px - 0.5, pz + 1.1, 0.28, 0.95, 0.88, 0.22),
        (px + 1.5, pz - 0.5, 0.26, 0.92, 0.32, 0.62),
    ]
    for lx, lz, lr, cr, cg, cb in lily_pos:
        color(0.18, 0.58, 0.22)
        draw_disk(lx, 0.18, lz, lr, 10)
        color(cr, cg, cb)
        draw_sphere(lx, 0.28, lz, 0.10)

    # ── Angsa berenang (animasi) ─────────────────────────────────
    # Orbit kompak di area air utama (sisi barat-tengah kolam).
    # Pusat orbit sengaja digeser ke kiri dari pusat kolam supaya
    # badan angsa TIDAK pernah masuk area jembatan di sisi timur,
    # sehingga aman dari pilar batu (x≈12.68) dan tembok batu
    # gorong-gorong (mulai x≈12.65, di z=-2.30 / z=-3.70).
    #
    #   batas timur orbit = swan_cx + swan_rx + body_half (≈0.45)
    #   12.10 + 0.45 = 12.55  <  12.65  → bebas tabrakan.
    ba = math.radians(bird_angle_deg)
    swan_cx, swan_cz = px - 0.5, pz
    swan_rx, swan_rz = 1.50, 0.55
    for idx, offset_a in enumerate([0.0, math.pi * 0.85]):
        a = ba + offset_a
        sx = swan_cx + swan_rx * math.cos(a)
        sz = swan_cz + swan_rz * math.sin(a)
        _draw_swan(sx, sz, a + math.pi * 0.5, anim_time + idx * 1.5)

    # ── Jembatan kayu TINGGI dengan gorong-gorong ────────────────
    _draw_wooden_bridge(px, pz)


def _draw_swan(x, z, face_angle_rad, t):
    """Angsa: badan elipsoid + leher melengkung + kepala."""
    glPushMatrix()
    glTranslatef(x, 0.0, z)
    glRotatef(-math.degrees(face_angle_rad), 0, 1, 0)

    bob = math.sin(t * 1.2) * 0.03

    # Badan
    color(0.98, 0.98, 0.96)
    glPushMatrix()
    glTranslatef(0, 0.28 + bob, 0)
    glScalef(0.45, 0.22, 0.28)
    q = gluNewQuadric(); gluSphere(q, 1.0, 12, 8); gluDeleteQuadric(q)
    glPopMatrix()

    # Leher
    color(0.96, 0.96, 0.94)
    glPushMatrix()
    glTranslatef(0.15, 0.32 + bob, 0)
    glRotatef(55, 1, 0, 0)
    q = gluNewQuadric(); gluCylinder(q, 0.06, 0.04, 0.40, 8, 1); gluDeleteQuadric(q)
    glPopMatrix()

    # Kepala
    color(0.98, 0.98, 0.96)
    draw_sphere(0.20, 0.66 + bob, -0.22, 0.09)

    # Paruh jingga
    color(0.95, 0.55, 0.12)
    draw_sphere(0.20, 0.65 + bob, -0.31, 0.05)

    glPopMatrix()


def _draw_wooden_bridge(px, pz):
    """Jembatan kayu tinggi melintasi ujung kolam.

    Struktur:
      - Pondasi batu (4 pilar silinder) menyangga dek di tiap sudut
      - Dinding/balok batu di kedua sisi panjang (wall) → membentuk
        gorong-gorong (culvert) tempat angsa lewat di bawah dek
      - Lantai dek kayu di y=1.10 (clearance ~0.85 di atas air)
      - Tiang pegangan + rel atas + rel tengah
      - Tangga pendek di kedua ujung agar terlihat naik ke dek
    """
    bx           = _BRIDGE_X
    deck_y       = _BRIDGE_DECK_Y
    deck_h       = 0.18
    half_w       = _BRIDGE_HALF_W
    half_l       = _BRIDGE_HALF_L
    rail_h       = 0.85

    # ── Pondasi batu — 4 pilar silinder di sudut dek ──────────────
    # Disusun di SISI LUAR jalur angsa supaya tidak menabrak.
    color(0.56, 0.53, 0.49)
    pillar_xs = (bx - half_l + 0.18, bx + half_l - 0.18)
    pillar_zs = (pz - half_w - 0.05, pz + half_w + 0.05)
    for cx in pillar_xs:
        for cz in pillar_zs:
            draw_cylinder(cx, 0.0, cz, 0.18, deck_y, 12)
            # Topi pilar
            color(0.72, 0.69, 0.64)
            draw_cylinder(cx, deck_y - 0.04, cz, 0.24, 0.08, 12)
            color(0.56, 0.53, 0.49)

    # ── Dinding batu / abutmen di sepanjang sisi z (gorong-gorong)
    #    Balok rendah hanya separuh tinggi pilar agar terlihat
    #    seperti tepian gorong-gorong di bawah dek.
    color(0.50, 0.47, 0.43)
    wall_h = 0.55
    for side_z in (pz - half_w - 0.05, pz + half_w + 0.05):
        draw_box(bx, 0.0, side_z, half_l * 2.0 - 0.30, wall_h, 0.10)
    # Bibir batu di atas dinding (highlight)
    color(0.78, 0.74, 0.68)
    for side_z in (pz - half_w - 0.05, pz + half_w + 0.05):
        draw_box(bx, wall_h, side_z, half_l * 2.0 - 0.30, 0.05, 0.14)

    # ── Lantai dek (kayu hangat) ──────────────────────────────────
    color(0.62, 0.40, 0.20)
    draw_box(bx, deck_y, pz, half_l * 2.0, deck_h, half_w * 2.0)

    # Bayangan bawah dek (sisi gelap)
    color(0.40, 0.24, 0.10)
    draw_box(bx, deck_y - 0.01, pz, half_l * 2.0 - 0.04, 0.04, half_w * 2.0 - 0.04)

    # Papan lantai melintang
    color(0.48, 0.30, 0.13)
    bz = pz - half_w + 0.05
    while bz <= pz + half_w - 0.05:
        draw_box(bx, deck_y + deck_h - 0.025, bz,
                 half_l * 2.0 - 0.04, 0.025, 0.08)
        bz += 0.20

    # ── Tiang pegangan (4 pasang) ─────────────────────────────────
    color(0.50, 0.32, 0.14)
    rail_bot = deck_y + deck_h
    posts_x = (bx - half_l + 0.10, bx - half_l * 0.40,
               bx + half_l * 0.40, bx + half_l - 0.10)
    for side_z in (pz - half_w + 0.04, pz + half_w - 0.04):
        for post_x in posts_x:
            draw_box(post_x, rail_bot, side_z, 0.10, rail_h, 0.10)

    # Rel atas
    color(0.55, 0.34, 0.14)
    for side_z in (pz - half_w + 0.04, pz + half_w - 0.04):
        draw_box(bx, rail_bot + rail_h - 0.04, side_z,
                 half_l * 2.0 - 0.06, 0.08, 0.08)
    # Rel tengah
    color(0.45, 0.28, 0.12)
    for side_z in (pz - half_w + 0.04, pz + half_w - 0.04):
        draw_box(bx, rail_bot + rail_h * 0.50, side_z,
                 half_l * 2.0 - 0.06, 0.05, 0.05)

    # ── Tangga di ujung LUAR (menghadap pagar, sisi +X) ──────────
    # Hanya satu sisi karena ujung -X langsung di atas air kolam.
    color(0.52, 0.34, 0.14)
    n_steps = 4
    step_h = deck_y / n_steps
    step_d = 0.32
    for i in range(n_steps):
        sx = bx + half_l + (i + 0.5) * step_d
        sy = i * step_h
        draw_box(sx, sy, pz, step_d, step_h, half_w * 2.0)
