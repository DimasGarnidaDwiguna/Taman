"""
core/layout.py
--------------
Sistem manajemen tabrakan posisi antar-aset.

Tiga jenis zona:
  - CIRCLE_ZONES & BOX_ZONES : statis (struktur besar)
  - PATH_SEGMENTS, PATH_RING : jalur setapak / jogging (statis)
  - _dynamic_zones           : ditambahkan saat runtime oleh aset
    yang sudah digambar duluan.

Renderer memanggil `clear_dynamic_zones()` di awal setiap frame.
"""

import math


# ── Struktur besar (statis) ───────────────────────────────────────
CIRCLE_ZONES = [
    (0.0,   0.0, 3.30),    # Fountain
    (11.0, -3.0, 4.20),    # Pond
    (14.0,  5.0, 3.30),    # Gazebo
]

BOX_ZONES = [
    (-15.0, -10.5,   2.6,   5.6),    # Pergola
    (  9.0,  18.5, -18.5, -10.0),    # Playground
    (  1.0,   7.0, -17.0, -13.0),    # Toilet
    (-16.0, -12.0,   6.4,   9.6),    # Bike rack
    ( -3.5,   3.5,  16.0,  17.5),    # Gerbang
]

# ── Jalur setapak (statis) ───────────────────────────────────────
# Jalur direpresentasikan sebagai segmen garis dengan setengah-lebar.
# Sinkron dengan environment/ground.py:draw_all_paths()
_PATH_HALF_WIDTH_MAIN  = 1.5     # jalur masuk utama (lebar 3.0)
_PATH_HALF_WIDTH_RING  = 0.8     # jalur melingkar (lebar 1.6)
_PATH_HALF_WIDTH_RADIAL = 0.7    # jalur radial (lebar 1.4)

# (x1, z1, x2, z2, half_width)
PATH_SEGMENTS = [
    # Jalur masuk utama
    (0.0, 16.0, 0.0, 5.0, _PATH_HALF_WIDTH_MAIN),
    # Radial (semua lebar 0.7)
    ( 0.0,  5.0,  -8.0, -2.0, _PATH_HALF_WIDTH_RADIAL),
    ( 0.0,  5.0,   8.0, -2.0, _PATH_HALF_WIDTH_RADIAL),
    ( 0.0,  5.0, -12.0,  8.0, _PATH_HALF_WIDTH_RADIAL),
    ( 0.0,  5.0,  12.0,  8.0, _PATH_HALF_WIDTH_RADIAL),
    (-8.0, -2.0, -14.0,-10.0, _PATH_HALF_WIDTH_RADIAL),
    ( 8.0, -2.0,  14.0,-10.0, _PATH_HALF_WIDTH_RADIAL),
    ( 0.0, -7.0,   0.0,-16.0, _PATH_HALF_WIDTH_RADIAL),
]

# Cincin melingkar di sekitar fountain
PATH_RING = (0.0, 0.0, 7.0, _PATH_HALF_WIDTH_RING)   # (cx, cz, radius, half_w)


# ── Zona dinamis ─────────────────────────────────────────────────
_dynamic_zones: list = []   # list of (cx, cz, radius)


def clear_dynamic_zones() -> None:
    _dynamic_zones.clear()


def register_zone(x: float, z: float, radius: float) -> None:
    _dynamic_zones.append((x, z, radius))


def _dist_to_segment(px: float, pz: float,
                     x1: float, z1: float,
                     x2: float, z2: float) -> float:
    """Jarak titik (px,pz) ke segmen garis (x1,z1)–(x2,z2)."""
    dx, dz = x2 - x1, z2 - z1
    seg_len_sq = dx * dx + dz * dz
    if seg_len_sq < 1e-9:
        return math.hypot(px - x1, pz - z1)
    t = ((px - x1) * dx + (pz - z1) * dz) / seg_len_sq
    t = max(0.0, min(1.0, t))
    cx = x1 + t * dx
    cz = z1 + t * dz
    return math.hypot(px - cx, pz - cz)


def is_on_path(x: float, z: float, buffer: float = 0.0) -> bool:
    """True jika titik berada di atas jalur setapak (atau dekat dengannya)."""
    # Segmen lurus
    for x1, z1, x2, z2, hw in PATH_SEGMENTS:
        if _dist_to_segment(x, z, x1, z1, x2, z2) < (hw + buffer):
            return True
    # Cincin lingkaran
    cx, cz, r, hw = PATH_RING
    d = math.hypot(x - cx, z - cz)
    if abs(d - r) < (hw + buffer):
        return True
    return False


def is_blocked(x: float, z: float, buffer: float = 0.0) -> bool:
    """True jika (x, z) menabrak struktur, jalur, atau aset dinamis."""
    # Statis lingkaran
    for cx, cz, r in CIRCLE_ZONES:
        if (x - cx) ** 2 + (z - cz) ** 2 < (r + buffer) ** 2:
            return True
    # Statis kotak
    for x_min, x_max, z_min, z_max in BOX_ZONES:
        if (x_min - buffer) <= x <= (x_max + buffer) and \
           (z_min - buffer) <= z <= (z_max + buffer):
            return True
    # Jalur setapak
    if is_on_path(x, z, buffer):
        return True
    # Dinamis lingkaran
    for cx, cz, r in _dynamic_zones:
        if (x - cx) ** 2 + (z - cz) ** 2 < (r + buffer) ** 2:
            return True
    return False
