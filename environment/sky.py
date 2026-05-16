"""
environment/sky.py
------------------
Langit cyan cerah dengan gradient halus dari horizon ke atas.
Digambar tanpa depth test sehingga selalu di belakang semua objek.
"""

import math
from OpenGL.GL import *


# Warna langit (cyan cerah ala referensi)
_SKY_TOP    = (0.35, 0.65, 0.95)   # biru cyan kuat di atas
_SKY_MID    = (0.55, 0.78, 0.97)   # transisi
_SKY_HORIZ  = (0.78, 0.90, 0.99)   # putih kebiruan di horizon

_RADIUS = 120.0
_SEGS   = 36


def draw_skybox():
    """Gambar kubah langit (hemisphere) di sekitar scene."""
    glDepthMask(GL_FALSE)
    glDisable(GL_LIGHTING)
    glDisable(GL_FOG)

    # ── Kubah atas: ring tengah agar gradient lebih halus ──
    # Top → Mid (atas)
    glBegin(GL_TRIANGLE_FAN)
    glColor3f(*_SKY_TOP)
    glVertex3f(0, _RADIUS, 0)
    for i in range(_SEGS + 1):
        a = i / _SEGS * 2 * math.pi
        x = _RADIUS * 0.55 * math.cos(a)
        z = _RADIUS * 0.55 * math.sin(a)
        y = _RADIUS * 0.83
        glColor3f(*_SKY_MID)
        glVertex3f(x, y, z)
    glEnd()

    # Mid → Horizon (bawah kubah)
    glBegin(GL_QUAD_STRIP)
    for i in range(_SEGS + 1):
        a = i / _SEGS * 2 * math.pi
        cosA = math.cos(a); sinA = math.sin(a)
        # cincin atas (mid)
        glColor3f(*_SKY_MID)
        glVertex3f(_RADIUS * 0.55 * cosA, _RADIUS * 0.83, _RADIUS * 0.55 * sinA)
        # cincin bawah (horizon)
        glColor3f(*_SKY_HORIZ)
        glVertex3f(_RADIUS * cosA, 0.0, _RADIUS * sinA)
    glEnd()

    # ── "Dinding" bawah horizon (warna hijau pucat) ──
    glBegin(GL_QUAD_STRIP)
    for i in range(_SEGS + 1):
        a = i / _SEGS * 2 * math.pi
        cosA = math.cos(a); sinA = math.sin(a)
        glColor3f(*_SKY_HORIZ)
        glVertex3f(_RADIUS * cosA, 0.0, _RADIUS * sinA)
        glColor3f(0.45, 0.72, 0.40)
        glVertex3f(_RADIUS * cosA, -8.0, _RADIUS * sinA)
    glEnd()

    glEnable(GL_LIGHTING)
    glEnable(GL_FOG)
    glDepthMask(GL_TRUE)
