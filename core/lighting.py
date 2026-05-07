"""
core/lighting.py
----------------
Setup pencahayaan OpenGL: matahari + cahaya langit (fill light).
"""

from OpenGL.GL import *


def setup_lighting():
    """Dipanggil sekali saat init. Gunakan glLightfv dengan list Python."""

    # ── Matahari (directional, sinar datang dari kanan-atas-depan) ──
    glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_POSITION, [8.0, 25.0, 12.0, 0.0])   # w=0 = directional
    glLightfv(GL_LIGHT0, GL_DIFFUSE,  [1.00, 0.96, 0.88, 1.0])
    glLightfv(GL_LIGHT0, GL_SPECULAR, [0.50, 0.50, 0.45, 1.0])
    glLightfv(GL_LIGHT0, GL_AMBIENT,  [0.0,  0.0,  0.0,  1.0])  # ambient global di bawah

    # ── Cahaya langit / fill (arah berlawanan, warna biru dingin) ──
    glEnable(GL_LIGHT1)
    glLightfv(GL_LIGHT1, GL_POSITION, [-6.0, 10.0, -8.0, 0.0])
    glLightfv(GL_LIGHT1, GL_DIFFUSE,  [0.35, 0.40, 0.50, 1.0])
    glLightfv(GL_LIGHT1, GL_SPECULAR, [0.0,  0.0,  0.0,  1.0])
    glLightfv(GL_LIGHT1, GL_AMBIENT,  [0.0,  0.0,  0.0,  1.0])

    # ── Ambient global (simulasi radiosity sederhana) ──
    glLightModelfv(GL_LIGHT_MODEL_AMBIENT, [0.28, 0.30, 0.28, 1.0])
    glLightModeli(GL_LIGHT_MODEL_LOCAL_VIEWER, GL_TRUE)
