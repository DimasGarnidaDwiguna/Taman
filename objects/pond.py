"""
objects/pond.py
---------------
Kolam ikan oval dengan tepi batu alam, teratai, angsa berenang
(animasi), dan jembatan kayu. Air berwarna cyan cerah ala referensi.
"""

import math
from OpenGL.GL import *
from OpenGL.GLU import *
from core.primitives import color, draw_box, draw_sphere, draw_cylinder, draw_disk


_PX, _PZ = 11.0, -3.0   # pusat kolam


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
    # Lapisan dasar
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
    ba = math.radians(bird_angle_deg)
    for idx, offset_a in enumerate([0.0, math.pi * 0.8]):
        a = ba + offset_a
        sx = px + 1.8 * math.cos(a)
        sz = pz + 1.2 * math.sin(a)
        _draw_swan(sx, sz, a + math.pi * 0.5, anim_time + idx * 1.5)

    # ── Jembatan kayu ─────────────────────────────────────────────
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
    """Jembatan kayu kecil melintasi ujung kolam."""
    bx = px + 2.9
    color(0.55, 0.35, 0.16)

    # Lantai jembatan
    draw_box(bx, 0.05, pz, 2.6, 0.16, 1.0)

    # Papan lantai (garis melintang)
    color(0.45, 0.28, 0.12)
    bz = pz - 0.46
    while bz <= pz + 0.46:
        draw_box(bx, 0.14, bz, 2.6, 0.04, 0.07)
        bz += 0.18

    # Tiang pegangan (dua sisi, tiga pasang)
    color(0.48, 0.30, 0.14)
    for side_z in (pz - 0.46, pz + 0.46):
        for post_x in (bx - 1.1, bx, bx + 1.1):
            draw_box(post_x, 0.16, side_z, 0.10, 0.78, 0.10)

    # Rel atas
    color(0.52, 0.32, 0.14)
    draw_box(bx, 0.92, pz - 0.46, 2.6, 0.08, 0.08)
    draw_box(bx, 0.92, pz + 0.46, 2.6, 0.08, 0.08)
