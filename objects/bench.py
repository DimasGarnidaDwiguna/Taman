"""
objects/bench.py
----------------
Bangku taman kayu dengan kaki besi dan sandaran punggung.
"""

from OpenGL.GL import glPushMatrix, glTranslatef, glRotatef, glPopMatrix
from core.primitives import color, draw_box, draw_cylinder
from core.layout     import is_blocked, register_zone


def draw_bench(x: float, z: float, angle_deg: float = 0.0):
    glPushMatrix()
    glTranslatef(x, 0, z)
    glRotatef(angle_deg, 0, 1, 0)

    # Papan dudukan (tiga lajur kayu hangat)
    for iz in (-0.13, 0, 0.13):
        color(0.62, 0.40, 0.18)
        draw_box(0, 0.44, iz, 1.20, 0.07, 0.10)

    # Sandaran punggung (dua papan)
    for iz in (-0.02, 0.08):
        color(0.58, 0.36, 0.16)
        draw_box(0, 0.80, -0.22 + iz * 0.4, 1.20, 0.07, 0.07)

    # Kaki besi (4 buah, bentuk-L) — hitam
    color(0.16, 0.16, 0.18)
    for sx in (-0.48, 0.48):
        # Kaki depan
        draw_cylinder(sx, 0.0, 0.16, 0.04, 0.45, 5)
        # Kaki belakang
        draw_cylinder(sx, 0.0, -0.16, 0.04, 0.45, 5)
        # Penghubung bawah
        draw_box(sx, 0.06, 0.0, 0.05, 0.06, 0.36)

    # Sambungan ke sandaran
    color(0.16, 0.16, 0.18)
    for sx in (-0.48, 0.48):
        draw_cylinder(sx, 0.44, -0.17, 0.035, 0.52, 5)

    glPopMatrix()


def draw_all_benches():
    # Posisi bangku — semua harus berada di RUMPUT, menghadap jalur
    # tapi tidak menyentuh jalur. Bench panjang ~1.2m, jadi butuh
    # buffer lebar.
    data = [
        # Sekitar fountain (ring path r=7), bangku di r ~9 menghadap ke dalam
        ( -6.4,  6.4, -135),    # NW
        (  6.4,  6.4,  135),    # NE
        ( -6.4, -6.4,  -45),    # SW
        (  6.4, -6.4,   45),    # SE
        ( -8.5,  0.0,   90),    # W
        (  8.5,  0.0,  -90),    # E
        # Jalur masuk (z 9..14, x diset jauh dari jalur tengah)
        ( -2.5, 11.5,    0),
        (  2.5, 11.5,    0),
        # Belakang taman
        ( -3.0, 13.5,  180),
        (  3.0, 13.5,  180),
        # Pojok: jauh dari jalur
        (-16.5,   2.0,  90),
        ( 16.5,   2.0, -90),
        (-16.5,  -4.0,  90),
        ( 16.5,  -4.0, -90),
        # Dekat playground (di luar bounding box)
        (  6.5, -10.5,    0),
    ]

    # Bench butuh buffer cukup besar (lebar 1.2 + jarak aman 0.4)
    BUFFER = 1.0

    for x, z, a in data:
        if is_blocked(x, z, BUFFER):
            continue
        draw_bench(x, z, a)
        register_zone(x, z, 0.9)
