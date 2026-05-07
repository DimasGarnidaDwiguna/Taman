"""
objects/parking.py
------------------
Area parkir: garis parkir, meter, palang, dan mobil.
"""

from core.primitives import color, draw_box, draw_cylinder, draw_sphere, draw_flat_quad


def draw_car(x: float, z: float, cr: float, cg: float, cb: float, angle_deg: float = 0.0):
    from OpenGL.GL import glPushMatrix, glTranslatef, glRotatef, glPopMatrix
    glPushMatrix()
    glTranslatef(x, 0, z)
    glRotatef(angle_deg, 0, 1, 0)

    # Badan bawah
    color(cr, cg, cb)
    draw_box(0, 0.20, 0, 2.10, 0.55, 1.00)

    # Kabine / atap
    color(cr * 0.88, cg * 0.88, cb * 0.88)
    draw_box(0.05, 0.72, 0, 1.30, 0.44, 0.92)

    # Kap mesin (sedikit miring ke depan — model box)
    color(cr, cg, cb)
    draw_box(0.80, 0.62, 0, 0.48, 0.16, 0.98)

    # Bagasi belakang
    draw_box(-0.80, 0.58, 0, 0.48, 0.10, 0.98)

    # Kaca depan
    color(0.55, 0.80, 0.94)
    draw_box(0.55, 0.82, 0, 0.04, 0.32, 0.88)

    # Kaca belakang
    draw_box(-0.48, 0.80, 0, 0.04, 0.28, 0.88)

    # Kaca samping (kiri & kanan)
    color(0.60, 0.82, 0.94)
    draw_box(0.02, 0.82,  0.47, 1.15, 0.30, 0.04)
    draw_box(0.02, 0.82, -0.47, 1.15, 0.30, 0.04)

    # Empat roda
    color(0.12, 0.12, 0.14)
    for wx, wz in [(-0.68, -0.53), (0.68, -0.53), (-0.68, 0.53), (0.68, 0.53)]:
        draw_cylinder(wx, 0.08, wz, 0.24, 0.12, 12)

    # Pelek roda (silver)
    color(0.72, 0.70, 0.68)
    for wx, wz in [(-0.68, -0.53), (0.68, -0.53), (-0.68, 0.53), (0.68, 0.53)]:
        draw_cylinder(wx, 0.12, wz, 0.16, 0.07, 8)

    # Lampu depan (kuning putih)
    color(1.0, 0.98, 0.82)
    draw_box(1.04, 0.44, -0.35, 0.04, 0.12, 0.20)
    draw_box(1.04, 0.44,  0.35, 0.04, 0.12, 0.20)

    # Lampu belakang (merah)
    color(0.88, 0.10, 0.10)
    draw_box(-1.05, 0.44, -0.35, 0.04, 0.12, 0.18)
    draw_box(-1.05, 0.44,  0.35, 0.04, 0.12, 0.18)

    glPopMatrix()


def draw_parking():
    # Garis parkir putih
    color(0.88, 0.88, 0.86)
    px = -17.5
    while px <= 16.0:
        draw_box(px, 0.002, 19.0, 0.08, 0.005, 2.80)
        px += 2.90

    # Slot difabel (biru)
    color(0.20, 0.38, 0.82)
    draw_flat_quad(4.5, 17.3, 7.4, 20.0, y=0.002)

    # Meter parkir (kiri area)
    color(0.45, 0.45, 0.48)
    draw_cylinder(-17.8, 0.0, 17.8, 0.05, 1.30, 6)
    color(0.82, 0.52, 0.10)
    draw_box(-17.8, 1.18, 17.8, 0.28, 0.40, 0.20)

    # Palang otomatis
    color(0.78, 0.14, 0.14)
    draw_cylinder(-16.0, 0.0, 17.5, 0.06, 1.10, 6)
    draw_box(-14.0, 1.05, 17.5, 4.0, 0.10, 0.10)
    draw_box(-16.0, 1.05, 17.5, 0.10, 0.06, 0.10)

    # Mobil-mobil terparkir
    cars = [
        (-15.0, 19.0, 0.95, 0.95, 0.95),   # putih
        (-12.0, 19.0, 0.80, 0.14, 0.14),   # merah
        ( -9.0, 19.0, 0.32, 0.32, 0.36),   # abu-abu
        ( -6.0, 19.0, 0.14, 0.28, 0.82),   # biru
        ( -3.0, 19.0, 0.18, 0.52, 0.22),   # hijau
        (  0.0, 19.0, 0.88, 0.75, 0.10),   # kuning
        (  3.0, 19.0, 0.55, 0.20, 0.70),   # ungu
        (  6.0, 19.0, 0.95, 0.50, 0.10),   # oranye
    ]
    for cx, cz, cr, cg, cb in cars:
        draw_car(cx, cz, cr, cg, cb)

    # Mobil difabel (slot biru)
    draw_car(5.8, 19.0, 0.92, 0.92, 0.92)
