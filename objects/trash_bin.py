"""
objects/trash_bin.py
--------------------
Tempat sampah taman 3 warna (organik=hijau, anorganik=kuning, B3=merah).
Style cartoon cerah, tutup lebih terang, body silinder.
"""

from core.primitives import color, draw_cylinder, draw_box, draw_sphere
from core.layout     import is_blocked, register_zone


def draw_trash_bin(x: float, z: float, bin_type: str = 'organik'):
    """bin_type: 'organik' (hijau), 'anorganik' (kuning), 'b3' (merah)"""
    _colors = {
        'organik':   (0.18, 0.62, 0.26),
        'anorganik': (0.95, 0.85, 0.10),
        'b3':        (0.92, 0.18, 0.16),
    }
    cr, cg, cb = _colors.get(bin_type, _colors['organik'])

    # Dasar
    color(cr * 0.85, cg * 0.85, cb * 0.85)
    draw_cylinder(x, 0.0, z, 0.18, 0.10, 10)

    # Body
    color(cr, cg, cb)
    draw_cylinder(x, 0.10, z, 0.16, 0.62, 10)

    # Leher
    color(cr * 0.90, cg * 0.90, cb * 0.90)
    draw_cylinder(x, 0.70, z, 0.19, 0.08, 10)

    # Tutup
    color(min(cr + 0.15, 1), min(cg + 0.15, 1), min(cb + 0.15, 1))
    draw_cylinder(x, 0.78, z, 0.21, 0.08, 10)

    # Knob pegangan
    color(0.30, 0.30, 0.34)
    draw_sphere(x, 0.90, z, 0.08)

    # Stiker label putih
    color(0.95, 0.95, 0.92)
    draw_box(x, 0.36, z + 0.16, 0.18, 0.24, 0.02)


def draw_all_trash():
    # Setiap lokasi: 3 bin berjejer
    clusters = [
        (-3, 12), (3, 12),
        (-8, 2),  (8, 2),
        (-4, -6), (4, -6),
        (0, -11),
        (-15, -2), (15, -2),
        (-10, -10),
    ]
    types = ['organik', 'anorganik', 'b3']
    for cx, cz in clusters:
        # Cek center cluster maupun tepi terjauh (cx + 1.1)
        if is_blocked(cx, cz, 0.4) or is_blocked(cx + 1.1, cz, 0.4):
            continue
        for i, t in enumerate(types):
            draw_trash_bin(cx + i * 0.55, cz, t)
        # Register cluster (3 bin berjejer ~ 1.1 m, radius 0.9)
        register_zone(cx + 0.55, cz, 0.9)
