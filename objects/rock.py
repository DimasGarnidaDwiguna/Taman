"""
objects/rock.py
---------------
Batu alam dekoratif berbentuk tidak beraturan (spheroid distorsi).
"""

from OpenGL.GL import *
from OpenGL.GLU import *
from core.primitives import color
from core.layout     import is_blocked, register_zone


def draw_rock(x: float, z: float, scale: float = 0.4):
    r = 0.48 + (hash((x, z)) % 10) * 0.03   # sedikit variasi acak
    color(0.62, 0.58, 0.54)
    glPushMatrix()
    glTranslatef(x, scale * 0.45, z)
    glScalef(scale * 1.10, scale * 0.72, scale * 0.90)
    q = gluNewQuadric()
    gluQuadricNormals(q, GLU_SMOOTH)
    gluSphere(q, r, 10, 8)
    gluDeleteQuadric(q)
    glPopMatrix()

    # Batu kecil di sampingnya
    color(0.68, 0.64, 0.58)
    glPushMatrix()
    glTranslatef(x + scale * 0.5, scale * 0.25, z + scale * 0.3)
    glScalef(scale * 0.55, scale * 0.40, scale * 0.48)
    q = gluNewQuadric()
    gluSphere(q, r, 8, 6)
    gluDeleteQuadric(q)
    glPopMatrix()


def draw_all_rocks():
    data = [
        (-3, -13, 0.38), ( 3, -13, 0.32),
        (-14,  0, 0.42), (14,  0, 0.38),
        (-11, 10, 0.35), (11, 10, 0.40),
        ( -7, -7, 0.30), ( 7, -7, 0.28),
        (-17,  8, 0.45), (17,  8, 0.42),
        (-17, -8, 0.38), (17, -8, 0.35),
        (  5,-11, 0.28), (-5,-11, 0.32),
        ( 13,  7, 0.35), (-13,  7, 0.30),
    ]
    for rx, rz, sc in data:
        if is_blocked(rx, rz, 0.4):
            continue
        draw_rock(rx, rz, sc)
        register_zone(rx, rz, sc + 0.2)
