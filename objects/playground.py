"""
objects/playground.py
---------------------
Area bermain anak: pasir, perosotan, ayunan (animasi), jungkat-jungkit,
dan palang panjat.
"""

import math
from OpenGL.GL import *
from core.primitives import color, draw_box, draw_cylinder, draw_sphere


_PX, _PZ = -2.0, -8.0   # pusat area bermain


def draw_playground(anim_time: float):
    px, pz = _PX, _PZ

    # ── Alas pasir ───────────────────────────────────────────────
    color(0.86, 0.76, 0.52)
    glBegin(GL_QUADS)
    glNormal3f(0, 1, 0)
    for vx, vz in [(-4, -3), (4, -3), (4, 3), (-4, 3)]:
        glVertex3f(px + vx, 0.03, pz + vz)
    glEnd()
    # Batu pembatas pasir
    color(0.50, 0.48, 0.46)
    for ix in range(-4, 5):
        draw_box(px + ix, 0.0, pz - 3, 0.90, 0.14, 0.18)
        draw_box(px + ix, 0.0, pz + 3, 0.90, 0.14, 0.18)
    for iz in range(-3, 4):
        draw_box(px - 4, 0.0, pz + iz, 0.18, 0.14, 0.90)
        draw_box(px + 4, 0.0, pz + iz, 0.18, 0.14, 0.90)

    # ── Perosotan biru ────────────────────────────────────────────
    _draw_slide(px, pz)

    # ── Ayunan (animasi) ─────────────────────────────────────────
    _draw_swings(px, pz, anim_time)

    # ── Jungkat-jungkit ──────────────────────────────────────────
    _draw_seesaw(px, pz, anim_time)

    # ── Palang panjat ────────────────────────────────────────────
    _draw_monkey_bars(px, pz)


def _draw_slide(px, pz):
    # Tiang penyangga
    color(0.20, 0.52, 0.88)
    draw_box(px - 2.0, 0.04, pz + 0.5, 0.10, 2.6, 0.10)
    draw_box(px - 2.0, 0.04, pz - 0.5, 0.10, 2.6, 0.10)
    draw_box(px - 2.0, 2.55, pz, 0.10, 0.10, 1.10)   # palang atas

    # Tangga
    color(0.88, 0.75, 0.12)
    for step in range(5):
        sy = 0.50 + step * 0.42
        sx = px - 2.0 + step * 0.22
        draw_box(sx, sy, pz, 0.36, 0.07, 0.90)

    # Bidang perosotan (kuning)
    color(0.95, 0.80, 0.10)
    glBegin(GL_QUADS)
    glNormal3f(0, 0.6, 0.8)
    for vx, vy, vz in [
        (px - 2.28, 2.52, pz - 0.45),
        (px - 2.28, 2.52, pz + 0.45),
        (px + 0.60, 0.12, pz + 0.45),
        (px + 0.60, 0.12, pz - 0.45),
    ]:
        glVertex3f(vx, vy, vz)
    glEnd()
    # Sisi samping perosotan
    color(0.92, 0.70, 0.08)
    for side in (-0.46, 0.46):
        glBegin(GL_QUADS)
        glNormal3f(0, 0, 1 if side > 0 else -1)
        glVertex3f(px - 2.28, 0.12, pz + side)
        glVertex3f(px + 0.60, 0.12, pz + side)
        glVertex3f(px + 0.60, 0.12, pz + side)
        glVertex3f(px - 2.28, 2.52, pz + side)
        glEnd()


def _draw_swings(px, pz, t):
    # Rangka A-frame
    color(0.20, 0.52, 0.88)
    draw_box(px + 1.0, 0.04, pz - 2.5, 0.10, 2.6, 0.10)
    draw_box(px + 3.0, 0.04, pz - 2.5, 0.10, 2.6, 0.10)
    draw_box(px + 2.0, 2.55, pz - 2.5, 2.20, 0.10, 0.10)  # palang atas

    sw_angle = math.sin(t * 1.6) * 0.35

    for i, sw_x in enumerate([px + 1.5, px + 2.5]):
        # Tali (dua silinder tipis)
        color(0.30, 0.30, 0.30)
        draw_box(sw_x + sw_angle * 0.8, 2.50, pz - 2.5, 0.03, 1.6, 0.03)

        # Dudukan (kayu)
        color(0.52, 0.32, 0.14)
        draw_box(sw_x + sw_angle, 0.80, pz - 2.5, 0.38, 0.08, 0.20)


def _draw_seesaw(px, pz, t):
    # Tiang tengah
    color(0.30, 0.30, 0.30)
    draw_cylinder(px + 2.5, 0.04, pz + 1.8, 0.06, 0.55, 6)
    draw_sphere(px + 2.5, 0.60, pz + 1.8, 0.10)   # pivot

    # Papan (berayun)
    tilt = math.sin(t * 0.8) * 0.25
    color(0.88, 0.40, 0.14)
    glPushMatrix()
    glTranslatef(px + 2.5, 0.60, pz + 1.8)
    glRotatef(math.degrees(tilt), 0, 0, 1)
    draw_box(0, 0.05, 0, 2.50, 0.10, 0.28)
    # Pegangan
    color(0.20, 0.52, 0.88)
    draw_cylinder(-1.1, 0.12, 0, 0.04, 0.30, 6)
    draw_cylinder( 1.1, 0.12, 0, 0.04, 0.30, 6)
    glPopMatrix()


def _draw_monkey_bars(px, pz):
    """Palang panjat horizontal."""
    bx, bz = px + 3.2, pz - 0.5
    h_post = 2.0

    color(0.20, 0.52, 0.88)
    # Empat tiang sudut
    for dx, dz in [(-0.8, -0.6), (0.8, -0.6), (-0.8, 0.6), (0.8, 0.6)]:
        draw_cylinder(bx + dx, 0.04, bz + dz, 0.06, h_post, 6)

    # Dua rel panjang
    draw_box(bx, h_post + 0.04, bz - 0.6, 1.80, 0.08, 0.08)
    draw_box(bx, h_post + 0.04, bz + 0.6, 1.80, 0.08, 0.08)

    # Palang melintang
    color(0.88, 0.75, 0.12)
    for i in range(5):
        rx = bx - 0.65 + i * 0.32
        draw_cylinder(rx, h_post + 0.04, bz - 0.6, 0.04, 1.2, 6)
