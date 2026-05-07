"""
objects/pond.py
---------------
Kolam ikan oval dengan tepi batu alam, tanaman air,
angsa berenang (animasi), dan jembatan kayu.
"""

import math
from OpenGL.GL import *
from OpenGL.GLU import *
from core.primitives import color, draw_box, draw_sphere, draw_cylinder, draw_disk


_PX, _PZ = 11.0, -3.0   # pusat kolam


def draw_pond(anim_time: float, bird_angle_deg: float):
    px, pz = _PX, _PZ

    # ── Tanah basah di sekitar kolam ─────────────────────────────
    color(0.28, 0.22, 0.14)
    glPushMatrix()
    glTranslatef(px, 0.00, pz)
    glScalef(4.5, 0.04, 3.2)
    q = gluNewQuadric()
    gluSphere(q, 1.0, 24, 8)
    gluDeleteQuadric(q)
    glPopMatrix()

    # ── Batu tepi kolam ──────────────────────────────────────────
    color(0.48, 0.46, 0.43)
    n_stones = 24
    for i in range(n_stones):
        a = i / n_stones * 2 * math.pi
        rx = px + 3.8 * math.cos(a)
        rz = pz + 2.6 * math.sin(a)
        size = 0.22 + 0.18 * (i % 3) / 2.0
        draw_sphere(rx, size * 0.5, rz, size)

    # ── Air kolam (elipsoid pipih) ────────────────────────────────
    color(0.22, 0.52, 0.72)
    glPushMatrix()
    glTranslatef(px, 0.08, pz)
    glScalef(3.4, 0.06, 2.3)
    q = gluNewQuadric()
    gluSphere(q, 1.0, 32, 12)
    gluDeleteQuadric(q)
    glPopMatrix()

    # Permukaan air (lapisan atas lebih terang)
    color(0.36, 0.68, 0.90)
    draw_disk(px, 0.14, pz, 3.3, 36)

    # ── Tanaman air (teratai) ────────────────────────────────────
    lily_pos = [
        (px - 1.2, pz - 0.6, 0.30, 0.92, 0.40, 0.52),
        (px + 0.9, pz + 0.7, 0.28, 0.30, 0.65, 0.92),
        (px - 0.4, pz + 1.0, 0.25, 0.92, 0.88, 0.20),
    ]
    for lx, lz, lr, cr, cg, cb in lily_pos:
        color(0.14, 0.52, 0.18)
        draw_disk(lx, 0.16, lz, lr, 10)
        color(cr, cg, cb)
        draw_sphere(lx, 0.26, lz, 0.10)

    # ── Angsa berenang (animasi berputar) ─────────────────────────
    ba = math.radians(bird_angle_deg)
    for idx, offset_a in enumerate([0.0, math.pi * 0.8]):
        a = ba + offset_a
        sx = px + 1.8 * math.cos(a)
        sz = pz + 1.2 * math.sin(a)
        _draw_swan(sx, sz, a + math.pi * 0.5, anim_time + idx * 1.5)

    # ── Jembatan kayu ─────────────────────────────────────────────
    _draw_wooden_bridge(px, pz)


def _draw_swan(x, z, face_angle_rad, t):
    """Angsa sederhana: badan elipsoid + leher melengkung + kepala."""
    glPushMatrix()
    glTranslatef(x, 0.0, z)
    glRotatef(-math.degrees(face_angle_rad), 0, 1, 0)

    bob = math.sin(t * 1.2) * 0.03   # gerak naik-turun pelan

    # Badan
    color(0.96, 0.96, 0.94)
    glPushMatrix()
    glTranslatef(0, 0.25 + bob, 0)
    glScalef(0.45, 0.22, 0.28)
    q = gluNewQuadric(); gluSphere(q, 1.0, 12, 8); gluDeleteQuadric(q)
    glPopMatrix()

    # Leher (silinder miring ke depan)
    color(0.94, 0.94, 0.92)
    glPushMatrix()
    glTranslatef(0.15, 0.30 + bob, 0)
    glRotatef(55, 1, 0, 0)   # miring ke depan
    q = gluNewQuadric(); gluCylinder(q, 0.06, 0.04, 0.40, 8, 1); gluDeleteQuadric(q)
    glPopMatrix()

    # Kepala
    color(0.96, 0.96, 0.94)
    draw_sphere(0.20, 0.64 + bob, -0.22, 0.09)

    # Paruh jingga
    color(0.95, 0.52, 0.12)
    draw_sphere(0.20, 0.63 + bob, -0.31, 0.05)

    glPopMatrix()


def _draw_wooden_bridge(px, pz):
    """Jembatan kayu kecil melintasi ujung kolam."""
    bx = px + 2.8
    color(0.48, 0.30, 0.14)

    # Lantai jembatan
    draw_box(bx, 0.0, pz, 2.4, 0.14, 0.80)

    # Papan lantai (garis melintang)
    color(0.40, 0.25, 0.10)
    bz = pz - 0.38
    while bz <= pz + 0.38:
        draw_box(bx, 0.12, bz, 2.4, 0.03, 0.06)
        bz += 0.16

    # Tiang pegangan
    color(0.42, 0.26, 0.12)
    for side_z in (pz - 0.38, pz + 0.38):
        for post_x in (bx - 1.0, bx, bx + 1.0):
            draw_box(post_x, 0.14, side_z, 0.08, 0.72, 0.08)

    # Rel atas
    color(0.46, 0.28, 0.12)
    draw_box(bx, 0.82, pz - 0.38, 2.4, 0.07, 0.06)
    draw_box(bx, 0.82, pz + 0.38, 2.4, 0.07, 0.06)
