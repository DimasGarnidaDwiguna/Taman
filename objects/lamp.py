"""
objects/lamp.py
---------------
Lampu taman tiang besi dengan kepala lentera (lentera klasik).
Warna gelap pekat untuk kontras pada rumput hijau cerah.
"""

from core.primitives import color, draw_cylinder, draw_sphere, draw_box, draw_cone
from core.layout    import is_blocked, register_zone


def draw_lamp(x: float, z: float, height: float = 3.4):
    # Plat dasar
    color(0.16, 0.16, 0.18)
    draw_cylinder(x, 0.0, z, 0.14, 0.12, 8)

    # Tiang utama
    color(0.14, 0.14, 0.16)
    draw_cylinder(x, 0.12, z, 0.06, height, 8)

    # Flange dekorasi di tengah tiang
    color(0.20, 0.20, 0.22)
    draw_cylinder(x, height * 0.5, z, 0.10, 0.08, 8)

    # Kepala lentera (rumah lampu — kotak prisma)
    color(0.18, 0.18, 0.20)
    draw_box(x, height + 0.20, z, 0.32, 0.40, 0.32)

    # Atap lentera (piramida kecil)
    color(0.14, 0.14, 0.16)
    draw_cone(x, height + 0.40, z, 0.22, 0.20, 4)

    # Bola lampu di dalam (krem terang — terlihat hangat)
    color(1.00, 0.96, 0.74)
    draw_sphere(x, height + 0.20, z, 0.13)


def draw_all_lamps():
    positions = [
        # Jalur masuk
        (-2.5, 14), (2.5, 14), (-2.5, 10), (2.5, 10),
        # Sekitar air mancur (4 lampu di sudut)
        (-3.5, 1), (3.5, 1), (-3.5, -4), (3.5, -4),
        # Sekitar pergola/playground
        (-9, 8), (9, 8), (-9, -7),
        # Kolam (kanan)
        (8, -1), (8, -6),
        # Perimeter dalam
        (-15, 8), (15, 8), (-15, -8),
        # Belakang
        (-5, -14), (0, -10),
    ]
    for lx, lz in positions:
        if is_blocked(lx, lz, 0.4):
            continue
        draw_lamp(lx, lz)
        register_zone(lx, lz, 0.5)
