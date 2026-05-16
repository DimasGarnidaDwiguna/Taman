"""
core/lighting.py
----------------
Setup pencahayaan OpenGL bergaya kartun low-poly:
- Matahari hangat dari atas-depan-kanan
- Fill light biru lembut dari arah berlawanan
- Ambient besar agar warna terlihat cerah & saturated
- Specular dimatikan untuk look matte / cartoon
"""

from OpenGL.GL import *


def setup_lighting():
    """Dipanggil sekali saat init."""

    # ── Matahari (directional, hangat) ──
    glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_POSITION, [10.0, 28.0, 14.0, 0.0])  # w=0 directional
    glLightfv(GL_LIGHT0, GL_DIFFUSE,  [0.95, 0.92, 0.85, 1.0])
    glLightfv(GL_LIGHT0, GL_SPECULAR, [0.05, 0.05, 0.05, 1.0])  # nyaris matte
    glLightfv(GL_LIGHT0, GL_AMBIENT,  [0.0,  0.0,  0.0,  1.0])

    # ── Fill light dari arah berlawanan (warna langit) ──
    glEnable(GL_LIGHT1)
    glLightfv(GL_LIGHT1, GL_POSITION, [-8.0, 12.0, -10.0, 0.0])
    glLightfv(GL_LIGHT1, GL_DIFFUSE,  [0.30, 0.38, 0.50, 1.0])
    glLightfv(GL_LIGHT1, GL_SPECULAR, [0.0,  0.0,  0.0,  1.0])
    glLightfv(GL_LIGHT1, GL_AMBIENT,  [0.0,  0.0,  0.0,  1.0])

    # ── Ambient global tinggi → look cartoon, tidak ada bayangan keras ──
    glLightModelfv(GL_LIGHT_MODEL_AMBIENT, [0.55, 0.58, 0.60, 1.0])
    glLightModeli(GL_LIGHT_MODEL_LOCAL_VIEWER, GL_FALSE)
    glLightModeli(GL_LIGHT_MODEL_TWO_SIDE, GL_TRUE)
