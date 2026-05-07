"""
objects/trash_bin.py
--------------------
Tempat sampah taman (model modern tiga warna: organik, anorganik, B3).
"""

from core.primitives import color, draw_cylinder, draw_box, draw_sphere


def draw_trash_bin(x: float, z: float, bin_type: str = 'organik'):
    """
    bin_type: 'organik' (hijau), 'anorganik' (kuning), 'b3' (merah)
    """
    _colors = {
        'organik':   (0.14, 0.52, 0.22),
        'anorganik': (0.88, 0.78, 0.08),
        'b3':        (0.82, 0.14, 0.14),
    }
    cr, cg, cb = _colors.get(bin_type, _colors['organik'])

    # Badan silinder (sedikit lebih lebar di atas — realistic)
    color(cr, cg, cb)
    draw_cylinder(x, 0.0, z, 0.16, 0.08, 8)    # dasar
    draw_cylinder(x, 0.0, z, 0.15, 0.62, 8)    # badan
    draw_cylinder(x, 0.60, z, 0.18, 0.06, 8)   # leher atas

    # Tutup (lebih terang)
    color(min(cr + 0.12, 1), min(cg + 0.12, 1), min(cb + 0.12, 1))
    draw_cylinder(x, 0.66, z, 0.20, 0.07, 8)
    draw_sphere(x, 0.76, z, 0.08)               # knob pegangan

    # Stiker label warna putih (mock: box tipis lebih terang)
    color(0.90, 0.90, 0.88)
    draw_box(x, 0.35, z + 0.16, 0.16, 0.22, 0.02)

    # Tiang penyangga (agar tidak copot)
    color(0.30, 0.30, 0.32)
    draw_cylinder(x, 0.0, z, 0.04, 0.12, 6)


def draw_all_trash():
    # Setiap lokasi: 3 bin berjejer (organik, anorganik, b3)
    clusters = [
        (-3, 12), (3, 12),
        (-8, 2),  (8, 2),
        (-4, -6), (4, -6),
        (0, -11),
        (-15, -2), (15, -2),
        (-10, -10), (10, -10),
    ]
    types = ['organik', 'anorganik', 'b3']
    for cx, cz in clusters:
        for i, t in enumerate(types):
            draw_trash_bin(cx + i * 0.52, cz, t)
