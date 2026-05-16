"""
environment/fence.py
--------------------
Pagar besi taman — tiang vertikal (picket) + rel horizontal,
ujung tombak (finial). Warna hitam pekat ala referensi.
"""

from core.primitives import color, draw_box, draw_cylinder, draw_sphere

_PARK = 20.0
_H    = 1.7    # tinggi pagar
_PICKET_GAP = 0.25  # jarak antar picket vertikal
_POST_GAP   = 4.0   # jarak antar tiang utama
_RAIL_Y = [0.30, 1.55]   # ketinggian rel horizontal

_FENCE_COLOR_DARK = (0.10, 0.10, 0.12)   # pagar utama hitam
_FENCE_COLOR_MID  = (0.16, 0.16, 0.18)   # rel horizontal
_PILLAR_COLOR     = (0.35, 0.35, 0.38)   # tiang utama beton/abu


def _draw_picket_x(x_start, x_end, z):
    """Picket vertikal sepanjang sumbu X."""
    # Tiang utama (post)
    color(*_PILLAR_COLOR)
    pos = x_start
    while pos <= x_end + 0.01:
        draw_box(pos, 0.0, z, 0.18, _H + 0.20, 0.18)
        # Topi tiang
        draw_box(pos, _H + 0.18, z, 0.26, 0.10, 0.26)
        pos += _POST_GAP

    # Picket (besi vertikal tipis)
    color(*_FENCE_COLOR_DARK)
    pos = x_start + _PICKET_GAP
    while pos < x_end - 0.01:
        # skip jika dekat dengan tiang utama
        nearest_post = round((pos - x_start) / _POST_GAP) * _POST_GAP + x_start
        if abs(pos - nearest_post) > 0.18:
            draw_box(pos, 0.04, z, 0.05, _H, 0.05)
            # Finial (ujung tombak)
            draw_sphere(pos, _H + 0.06, z, 0.05)
        pos += _PICKET_GAP

    # Rel horizontal
    color(*_FENCE_COLOR_MID)
    for ry in _RAIL_Y:
        draw_box((x_start + x_end) / 2, ry, z,
                 abs(x_end - x_start), 0.06, 0.06)


def _draw_picket_z(x, z_start, z_end):
    """Picket vertikal sepanjang sumbu Z."""
    # Tiang utama
    color(*_PILLAR_COLOR)
    pos = z_start
    while pos <= z_end + 0.01:
        draw_box(x, 0.0, pos, 0.18, _H + 0.20, 0.18)
        draw_box(x, _H + 0.18, pos, 0.26, 0.10, 0.26)
        pos += _POST_GAP

    # Picket
    color(*_FENCE_COLOR_DARK)
    pos = z_start + _PICKET_GAP
    while pos < z_end - 0.01:
        nearest_post = round((pos - z_start) / _POST_GAP) * _POST_GAP + z_start
        if abs(pos - nearest_post) > 0.18:
            draw_box(x, 0.04, pos, 0.05, _H, 0.05)
            draw_sphere(x, _H + 0.06, pos, 0.05)
        pos += _PICKET_GAP

    # Rel horizontal
    color(*_FENCE_COLOR_MID)
    for ry in _RAIL_Y:
        draw_box(x, ry, (z_start + z_end) / 2,
                 0.06, 0.06, abs(z_end - z_start))


def draw_fence():
    # Depan kiri & kanan (hindari lebar gerbang ±3.5)
    _draw_picket_x(-_PARK, -3.5, 16.5)
    _draw_picket_x( 3.5,  _PARK, 16.5)

    # Belakang
    _draw_picket_x(-_PARK, _PARK, -_PARK)

    # Kiri & kanan
    _draw_picket_z(-_PARK, -_PARK, 16.0)
    _draw_picket_z( _PARK, -_PARK, 16.0)
