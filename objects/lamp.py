"""
objects/lamp.py
---------------
Lampu taman model tiang besi dengan kepala lentera.
"""

from core.primitives import color, draw_cylinder, draw_sphere, draw_box, draw_cone


def draw_lamp(x: float, z: float, height: float = 3.2):
    # Tiang
    color(0.18, 0.18, 0.22)
    draw_cylinder(x, 0.0, z, 0.055, height, 7)

    # Flange (cincin dekorasi) di 1/3 tinggi
    color(0.22, 0.22, 0.28)
    draw_cylinder(x, height * 0.33, z, 0.09, 0.06, 7)

    # Lengan bengkok (mock: box kecil)
    color(0.18, 0.18, 0.22)
    draw_box(x + 0.12, height - 0.04, z, 0.28, 0.06, 0.06)

    # Kepala lentera (rumah lampu)
    color(0.22, 0.22, 0.28)
    draw_cylinder(x + 0.20, height, z, 0.18, 0.22, 8)
    draw_cone(x + 0.20, height + 0.22, z, 0.22, 0.16, 8)

    # Cahaya (bola glowing)
    color(1.00, 0.98, 0.82)
    draw_sphere(x + 0.20, height + 0.10, z, 0.10)

    # Plat dasar
    color(0.20, 0.20, 0.24)
    draw_cylinder(x, 0.0, z, 0.12, 0.08, 8)


def draw_all_lamps():
    positions = [
        # Jalur masuk
        (-2.5, 14), (2.5, 14), (-2.5, 10), (2.5, 10),
        # Sekitar air mancur
        (-3.5, 1), (3.5, 1), (-3.5, -4), (3.5, -4),
        # Jogging track
        (-18, 4), (-18, -4),
        # Area bermain & fasilitas
        (-5, -6), (5, -6), (0, -10),
        # Kolam
        (8, -1), (14, -1), (8, -6), (14, -6),
        # Perimeter
        (-15, 8), (15, 8), (-15, -8), (15, -8),
    ]
    for lx, lz in positions:
        draw_lamp(lx, lz)
