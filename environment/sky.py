"""
environment/sky.py
------------------
Langit berwarna solid — gradient warna dari horizon ke atas.
Digambar tanpa depth test sehingga selalu di belakang semua objek.
"""

import math
from OpenGL.GL import *


# Warna langit
_SKY_TOP    = (0.40, 0.62, 0.92)   # biru tua di atas
_SKY_HORIZ  = (0.70, 0.85, 0.98)   # biru muda di horizon
_SUN_COLOR  = (1.00, 0.96, 0.75)   # cahaya matahari (sedikit kuning)

_RADIUS = 120.0
_SEGS   = 36


def draw_skybox():
    """
    Gambar kubah langit (hemisphere) di sekitar scene.
    Menggunakan GL_TRIANGLE_FAN; depth write dimatikan sementara.
    """
    glDepthMask(GL_FALSE)
    glDisable(GL_LIGHTING)
    glDisable(GL_FOG)

    # ── Kubah atas ──────────────────────────────────────────────
    glBegin(GL_TRIANGLE_FAN)
    glColor3f(*_SKY_TOP)
    glVertex3f(0, _RADIUS, 0)                         # titik puncak
    for i in range(_SEGS + 1):
        a = i / _SEGS * 2 * math.pi
        x = _RADIUS * math.cos(a)
        z = _RADIUS * math.sin(a)
        glColor3f(*_SKY_HORIZ)
        glVertex3f(x, 0.0, z)
    glEnd()

    # ── "Dinding" horizon — quad tipis menutup bagian bawah ──────
    glBegin(GL_QUADS)
    for i in range(_SEGS):
        a1 = i       / _SEGS * 2 * math.pi
        a2 = (i + 1) / _SEGS * 2 * math.pi
        x1 = _RADIUS * math.cos(a1); z1 = _RADIUS * math.sin(a1)
        x2 = _RADIUS * math.cos(a2); z2 = _RADIUS * math.sin(a2)
        glColor3f(*_SKY_HORIZ);  glVertex3f(x1, 0.0,  z1); glVertex3f(x2, 0.0,  z2)
        glColor3f(0.55, 0.72, 0.62);  glVertex3f(x2, -5.0, z2); glVertex3f(x1, -5.0, z1)
    glEnd()

    glEnable(GL_LIGHTING)
    glEnable(GL_FOG)
    glDepthMask(GL_TRUE)
