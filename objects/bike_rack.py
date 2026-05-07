"""
objects/bike_rack.py
--------------------
Rak parkir sepeda + beberapa sepeda terparkir.
"""

from core.primitives import color, draw_box, draw_cylinder, draw_sphere


def draw_bicycle(x: float, z: float, color_rgb=(0.18, 0.38, 0.70)):
    """Sepeda realistis dengan dua roda, rangka, setang, dan sadel."""
    cr, cg, cb = color_rgb

    # Roda depan & belakang
    color(0.12, 0.12, 0.14)
    draw_cylinder(x - 0.32, 0.16, z, 0.22, 0.07, 14)
    draw_cylinder(x + 0.32, 0.16, z, 0.22, 0.07, 14)

    # Pelek
    color(0.70, 0.68, 0.62)
    draw_cylinder(x - 0.32, 0.22, z, 0.18, 0.03, 14)
    draw_cylinder(x + 0.32, 0.22, z, 0.18, 0.03, 14)

    # Rangka utama (body)
    color(cr, cg, cb)
    draw_box((x - 0.32 + x + 0.32) / 2, 0.30, z, 0.68, 0.04, 0.04)

    # Tiang sadel
    draw_box(x - 0.10, 0.25, z, 0.04, 0.32, 0.04)

    # Sadel
    color(0.12, 0.12, 0.14)
    draw_box(x - 0.10, 0.58, z, 0.24, 0.05, 0.10)

    # Setang
    color(0.70, 0.68, 0.62)
    draw_box(x + 0.30, 0.54, z, 0.06, 0.06, 0.38)
    draw_cylinder(x + 0.30, 0.38, z, 0.03, 0.18, 6)


def draw_bike_rack():
    bx, bz = -14.0, 5.0

    # Plat nama rak
    color(0.20, 0.20, 0.24)
    draw_box(bx - 1.6, 0.0, bz - 1.6, 0.90, 0.90, 0.12)
    # Tiang tanda
    draw_cylinder(bx - 1.6, 0.0, bz - 1.6, 0.06, 1.65, 6)

    # Rak besi (dua rel panjang + bracket)
    color(0.35, 0.35, 0.40)
    draw_box(bx, 0.0, bz, 3.2, 0.07, 0.12)     # rel bawah
    draw_box(bx, 0.50, bz, 3.2, 0.07, 0.12)    # rel atas

    for i in range(6):
        rx = bx - 1.5 + i * 0.60
        draw_cylinder(rx, 0.0, bz, 0.04, 0.52, 5)

    # Sepeda terparkir (5 buah, warna berbeda)
    bike_colors = [
        (0.18, 0.38, 0.70),
        (0.78, 0.14, 0.14),
        (0.14, 0.55, 0.22),
        (0.72, 0.56, 0.08),
        (0.50, 0.18, 0.70),
    ]
    for i, col in enumerate(bike_colors):
        draw_bicycle(bx - 1.2 + i * 0.60, bz + 0.55, col)
