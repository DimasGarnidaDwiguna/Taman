"""
objects/gazebo.py
-----------------
Gazebo / pendopo segi-enam dengan atap kerucut merah cerah ala referensi.
"""

import math
from OpenGL.GL import glPushMatrix, glPopMatrix, glTranslatef, glScalef
from core.primitives import (
    color, draw_cylinder, draw_cone, draw_disk, draw_box, draw_sphere
)


def draw_gazebo(x: float, z: float, radius: float = 2.2):
    posts = 6   # heksagonal, lebih cocok dengan gambar referensi

    # ── Pondasi / lantai (kayu coklat hangat) ────────────────────
    color(0.62, 0.42, 0.24)
    draw_disk(x, 0.05, z, radius + 0.55, posts)
    color(0.66, 0.46, 0.26)
    draw_disk(x, 0.13, z, radius + 0.25, posts)
    color(0.70, 0.50, 0.28)
    draw_disk(x, 0.22, z, radius + 0.05, posts)

    # ── Tiang (kayu coklat gelap) ────────────────────────────────
    post_h = 2.6
    color(0.45, 0.28, 0.14)
    for i in range(posts):
        a = i * 2 * math.pi / posts + math.pi / posts
        px = x + radius * math.cos(a)
        pz = z + radius * math.sin(a)
        draw_cylinder(px, 0.22, pz, 0.12, post_h, 8)
        # Umpak
        color(0.55, 0.38, 0.20)
        draw_box(px, 0.22, pz, 0.26, 0.16, 0.26)
        color(0.45, 0.28, 0.14)

    # ── Ring balok keliling ───────────────────────────────────────
    color(0.50, 0.32, 0.16)
    for i in range(posts):
        a1 = i       * 2 * math.pi / posts + math.pi / posts
        a2 = (i + 1) * 2 * math.pi / posts + math.pi / posts
        x1 = x + radius * math.cos(a1); z1 = z + radius * math.sin(a1)
        x2 = x + radius * math.cos(a2); z2 = z + radius * math.sin(a2)
        # Balok diposisikan tepat di tengah dua tiang
        midx = (x1 + x2) / 2
        midz = (z1 + z2) / 2
        length = math.hypot(x2 - x1, z2 - z1) + 0.08
        # Rotasi balok agar searah segmen
        glPushMatrix()
        glTranslatef(midx, 2.78, midz)
        # Hitung sudut dalam derajat
        ang = math.degrees(math.atan2(z2 - z1, x2 - x1))
        from OpenGL.GL import glRotatef
        glRotatef(-ang, 0, 1, 0)
        glScalef(length, 0.16, 0.18)
        draw_box(0, -0.08, 0, 1, 1, 1)
        glPopMatrix()

    # ── Atap kerucut merah (style referensi: pyramid runcing) ────
    # Atap utama (lebih lebar dari tiang untuk efek overhang)
    color(0.85, 0.18, 0.12)
    draw_cone(x, 2.85, z, radius + 0.55, 1.80, posts)

    # Lapisan kedua kecil di puncak (variasi)
    color(0.92, 0.25, 0.15)
    draw_cone(x, 4.30, z, 0.35, 0.40, posts)

    # Finial (ujung atap emas)
    color(0.95, 0.78, 0.22)
    draw_sphere(x, 4.78, z, 0.16)

    # ── Bangku dalam gazebo ───────────────────────────────────────
    color(0.50, 0.32, 0.16)
    for i in range(posts):
        a = i * 2 * math.pi / posts + math.pi / posts + math.pi / posts
        bx = x + (radius - 0.55) * math.cos(a)
        bz = z + (radius - 0.55) * math.sin(a)
        draw_box(bx, 0.42, bz, 0.80, 0.08, 0.32)
        # Kaki bangku
        color(0.40, 0.24, 0.10)
        for kx, kz in ((-0.32, -0.12), (0.32, -0.12), (-0.32, 0.12), (0.32, 0.12)):
            draw_cylinder(bx + kx, 0.22, bz + kz, 0.04, 0.21, 4)
        color(0.50, 0.32, 0.16)
