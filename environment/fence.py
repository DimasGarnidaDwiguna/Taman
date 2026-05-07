"""
environment/fence.py
--------------------
Pagar besi taman kota — tiang vertikal + rel horizontal.
"""

from core.primitives import color, draw_box, draw_cylinder, draw_sphere

_PARK = 20.0
_H    = 1.6    # tinggi pagar
_POST = 1.0    # jarak antar tiang
_RAIL_Y = [0.4, 0.9, 1.45]   # ketinggian rel horizontal


def _fence_segment(x1, z, x2, z2, vertical_axis='x'):
    """
    Gambar segmen pagar sepanjang satu sisi.
    vertical_axis='x' → sepanjang sumbu X; 'z' → sepanjang sumbu Z.
    """
    color(0.18, 0.18, 0.22)    # besi gelap

    if vertical_axis == 'x':
        pos = x1
        end = x2
        while pos <= end + 0.01:
            draw_cylinder(pos, 0.0, z, 0.04, _H, 6)
            draw_sphere(pos, _H + 0.06, z, 0.07)   # kepala tombak
            pos += _POST
        # rel horizontal
        color(0.22, 0.22, 0.28)
        for ry in _RAIL_Y:
            draw_box((x1 + x2) / 2, ry, z,
                     abs(x2 - x1) + _POST, 0.05, 0.05)

    else:  # sepanjang sumbu Z
        pos = z
        end = z2
        while pos <= end + 0.01:
            draw_cylinder(x1, 0.0, pos, 0.04, _H, 6)
            draw_sphere(x1, _H + 0.06, pos, 0.07)
            pos += _POST
        color(0.22, 0.22, 0.28)
        for ry in _RAIL_Y:
            draw_box(x1, ry, (z + z2) / 2,
                     0.05, 0.05, abs(z2 - z) + _POST)


def draw_fence():
    # Depan kiri (hindari lebar gerbang ±3)
    _fence_segment(-_PARK, 16.5, -3.5, 16.5, 'x')
    _fence_segment( 3.5, 16.5, _PARK, 16.5, 'x')

    # Belakang
    _fence_segment(-_PARK, -_PARK, _PARK, -_PARK, 'x')

    # Kiri & kanan
    _fence_segment(-_PARK, -_PARK, -_PARK, 16.0, 'z')
    _fence_segment( _PARK, -_PARK,  _PARK, 16.0, 'z')
