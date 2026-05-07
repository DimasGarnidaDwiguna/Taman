"""
objects/bench.py
----------------
Bangku taman kayu dengan kaki besi dan sandaran punggung.
"""

from OpenGL.GL import glPushMatrix, glTranslatef, glRotatef, glPopMatrix
from core.primitives import color, draw_box, draw_cylinder


def draw_bench(x: float, z: float, angle_deg: float = 0.0):
    glPushMatrix()
    glTranslatef(x, 0, z)
    glRotatef(angle_deg, 0, 1, 0)

    # Papan dudukan (tiga lajur kayu)
    for iz in (-0.13, 0, 0.13):
        color(0.52, 0.33, 0.14)
        draw_box(0, 0.44, iz, 1.20, 0.07, 0.10)

    # Sandaran punggung (dua papan)
    for iz in (-0.02, 0.08):
        color(0.48, 0.30, 0.12)
        draw_box(0, 0.80, -0.22 + iz * 0.4, 1.20, 0.07, 0.07)

    # Kaki besi (4 buah, bentuk-L)
    color(0.28, 0.28, 0.30)
    for sx in (-0.48, 0.48):
        # Kaki depan
        draw_cylinder(sx, 0.0, 0.16, 0.04, 0.45, 5)
        # Kaki belakang
        draw_cylinder(sx, 0.0, -0.16, 0.04, 0.45, 5)
        # Penghubung bawah
        draw_box(sx, 0.06, 0.0, 0.05, 0.06, 0.36)

    # Sambungan ke sandaran
    color(0.28, 0.28, 0.30)
    for sx in (-0.48, 0.48):
        draw_cylinder(sx, 0.44, -0.17, 0.035, 0.52, 5)

    glPopMatrix()


def draw_all_benches():
    data = [
        (-4,  2,  45), ( 4,  2, -45),
        (-5, -1,  90), ( 5, -1, -90),
        (-2, 11,   0), ( 2, 11,   0),
        (-9, -4,  30), ( 9, -4, -30),
        ( 8, -8,   0), (-8, -8,   0),
        (14, -5,  90), (-14, -5, -90),
        ( 0, 13, 180), (-6,  7,  60),
        ( 6,  7, -60),
    ]
    for x, z, a in data:
        draw_bench(x, z, a)
