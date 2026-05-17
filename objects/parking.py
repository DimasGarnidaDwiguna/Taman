"""
objects/parking.py
------------------
Mobil-mobil di area parkir sebelah kiri taman (slot di antara
pagar kiri & jalan utama). Layout sesuai gambar referensi:
deretan vertikal warna-warni cerah.
"""

from OpenGL.GL  import (glPushMatrix, glPopMatrix, glTranslatef, glRotatef,
                        glScalef, glEnable, glDisable, glBlendFunc,
                        glDepthMask, glColor4f,
                        GL_BLEND, GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA,
                        GL_FALSE, GL_TRUE)
from OpenGL.GLU import gluNewQuadric, gluCylinder, gluDisk, gluDeleteQuadric
from core.primitives import (
    color, draw_box, draw_cylinder, draw_sphere, draw_cone
)


def _draw_wheel(x: float, y_center: float, z: float,
                radius: float, width: float, axle_axis: str = 'z'):
    """
    Roda mobil — silinder horizontal dengan axle sepanjang sumbu Z
    (default) atau X. Pakai gluCylinder agar normalnya halus.
    Posisi (x, y_center, z) adalah PUSAT roda.
    """
    glPushMatrix()
    glTranslatef(x, y_center, z)
    if axle_axis == 'z':
        # Cylinder default OpenGL tumbuh di +Z. Geser supaya pusat roda
        # tepat di z, lalu gambar.
        glTranslatef(0, 0, -width * 0.5)
    else:  # axle = 'x'
        glRotatef(90.0, 0, 1, 0)
        glTranslatef(0, 0, -width * 0.5)
    q = gluNewQuadric()
    # Ban (silinder)
    color(0.10, 0.10, 0.12)
    gluCylinder(q, radius, radius, width, 16, 1)
    # Tutup samping (cakram ban)
    gluDisk(q, 0, radius, 16, 1)
    glTranslatef(0, 0, width)
    gluDisk(q, 0, radius, 16, 1)
    gluDeleteQuadric(q)
    glPopMatrix()

    # Pelek (silver) di tengah ban — silinder lebih kecil & lebih tipis
    glPushMatrix()
    glTranslatef(x, y_center, z)
    if axle_axis == 'z':
        glTranslatef(0, 0, -width * 0.55)
        rim_offset_axis = (0, 0, 1)
    else:
        glRotatef(90.0, 0, 1, 0)
        glTranslatef(0, 0, -width * 0.55)
        rim_offset_axis = (0, 0, 1)
    q = gluNewQuadric()
    color(0.78, 0.78, 0.78)
    gluCylinder(q, radius * 0.55, radius * 0.55, width * 1.10, 12, 1)
    gluDisk(q, 0, radius * 0.55, 12, 1)
    glTranslatef(0, 0, width * 1.10)
    gluDisk(q, 0, radius * 0.55, 12, 1)
    gluDeleteQuadric(q)
    glPopMatrix()


def draw_car(x: float, z: float, cr: float, cg: float, cb: float,
             angle_deg: float = 0.0):
    """Mobil low-poly chunky bergaya cartoon (referensi)."""
    glPushMatrix()
    glTranslatef(x, 0, z)
    glRotatef(angle_deg, 0, 1, 0)

    # Badan bawah
    color(cr, cg, cb)
    draw_box(0, 0.32, 0, 2.10, 0.45, 1.05)

    # Kabine atap
    color(cr * 0.90, cg * 0.90, cb * 0.90)
    draw_box(0.05, 0.78, 0, 1.30, 0.48, 0.95)

    # Kap mesin
    color(cr, cg, cb)
    draw_box(0.85, 0.62, 0, 0.50, 0.18, 1.00)

    # Bagasi belakang
    draw_box(-0.85, 0.60, 0, 0.50, 0.14, 1.00)

    # Kaca depan/belakang/samping
    color(0.55, 0.82, 0.95)
    draw_box(0.55, 0.92, 0, 0.05, 0.32, 0.90)
    draw_box(-0.50, 0.90, 0, 0.05, 0.30, 0.90)
    draw_box(0.05, 0.92,  0.49, 1.18, 0.30, 0.04)
    draw_box(0.05, 0.92, -0.49, 1.18, 0.30, 0.04)

    # ── Roda (4 buah, axle horizontal sejajar sumbu Z mobil) ────
    wheel_r = 0.22
    wheel_w = 0.18
    wheel_y = wheel_r          # pusat roda = radius (agar menyentuh tanah)
    for wx in (-0.68, 0.68):
        # Sisi kiri (-Z) dan kanan (+Z)
        _draw_wheel(wx, wheel_y, -0.55, wheel_r, wheel_w, axle_axis='z')
        _draw_wheel(wx, wheel_y,  0.55 - wheel_w, wheel_r, wheel_w, axle_axis='z')

    # Lampu depan/belakang
    color(1.0, 0.96, 0.78)
    draw_box(1.06, 0.48, -0.36, 0.04, 0.13, 0.20)
    draw_box(1.06, 0.48,  0.36, 0.04, 0.13, 0.20)
    color(0.92, 0.12, 0.10)
    draw_box(-1.06, 0.48, -0.36, 0.04, 0.13, 0.18)
    draw_box(-1.06, 0.48,  0.36, 0.04, 0.13, 0.18)

    glPopMatrix()


def draw_parking():
    """Deretan mobil di slot parkir kiri (orientasi: nose menghadap pagar)."""

    cars = [
        # (z, R, G, B)
        ( 14.5, 0.95, 0.95, 0.95),   # putih
        ( 11.5, 0.85, 0.15, 0.15),   # merah
        (  8.5, 0.95, 0.55, 0.10),   # oranye
        (  5.5, 0.95, 0.85, 0.18),   # kuning
        (  2.5, 0.20, 0.62, 0.22),   # hijau
        ( -1.5, 0.92, 0.92, 0.92),   # mobil difabel
        ( -4.5, 0.18, 0.42, 0.85),   # biru
        ( -7.5, 0.55, 0.20, 0.78),   # ungu
        (-10.5, 0.18, 0.22, 0.30),   # abu gelap
    ]

    for cz, cr, cg, cb in cars:
        # angle 90: nose menghadap +x (ke pagar/taman)
        draw_car(-21.0, cz, cr, cg, cb, angle_deg=90.0)

    # ── Tiang lampu jalan parkir ─────────────────────────────────
    for sign_z in (12.0, -12.0):
        # Tiang
        color(0.30, 0.30, 0.34)
        draw_cylinder(-26.0, 0.0, sign_z, 0.07, 4.0, 6)

        # Lengan horizontal ke arah jalan (+X)
        color(0.20, 0.20, 0.22)
        draw_box(-25.55, 4.05, sign_z, 0.90, 0.07, 0.07)

        # Rumah lampu (rangka logam tipis)
        head_x = -25.10
        color(0.16, 0.16, 0.18)
        # 4 tiang sudut tipis
        for sx in (-0.11, 0.11):
            for sz in (-0.11, 0.11):
                draw_box(head_x + sx, 3.78, sign_z + sz,
                         0.03, 0.30, 0.03)
        # Rim atas & bawah
        color(0.22, 0.22, 0.24)
        draw_box(head_x, 3.76, sign_z, 0.26, 0.04, 0.26)
        draw_box(head_x, 4.06, sign_z, 0.26, 0.04, 0.26)
        # Atap kerucut kecil
        draw_cone(head_x, 4.10, sign_z, 0.16, 0.10, 6)

        # Bohlam pijar (kuning hangat) di dalam sangkar
        bulb_base_y = 3.80
        bulb_r      = 0.07
        bulb_cy     = bulb_base_y + 0.04 + 0.03 + bulb_r
        # Ulir logam silver
        color(0.78, 0.78, 0.82)
        draw_cylinder(head_x, bulb_base_y, sign_z, 0.030, 0.04, 10)
        color(0.55, 0.55, 0.58)
        for i in range(2):
            draw_cylinder(head_x, bulb_base_y + 0.008 + i * 0.012,
                          sign_z, 0.032, 0.004, 10)
        # Leher kaca
        color(1.00, 0.92, 0.55)
        draw_cone(head_x, bulb_base_y + 0.04, sign_z, bulb_r * 0.55,
                  0.03, 10)
        # Envelope bulat
        color(1.00, 0.93, 0.50)
        draw_sphere(head_x, bulb_cy, sign_z, bulb_r)
        # Highlight pantulan
        color(1.00, 1.00, 0.82)
        draw_sphere(head_x, bulb_cy + bulb_r * 0.40, sign_z,
                    bulb_r * 0.35)

        # Panel kaca transparan di 4 sisi
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glDepthMask(GL_FALSE)
        glColor4f(0.82, 0.92, 1.00, 0.30)
        draw_box(head_x, 3.92, sign_z - 0.105, 0.20, 0.26, 0.012)
        draw_box(head_x, 3.92, sign_z + 0.105, 0.20, 0.26, 0.012)
        draw_box(head_x - 0.105, 3.92, sign_z, 0.012, 0.26, 0.20)
        draw_box(head_x + 0.105, 3.92, sign_z, 0.012, 0.26, 0.20)
        glDepthMask(GL_TRUE)
        glDisable(GL_BLEND)

    # ── Palang otomatis di pintu masuk parkir ────────────────────
    color(0.20, 0.20, 0.22)
    draw_cylinder(-22.0, 0.0, 17.5, 0.08, 1.3, 6)
    color(0.85, 0.15, 0.15)
    draw_box(-19.0, 1.30, 17.5, 5.5, 0.10, 0.10)
    color(0.95, 0.95, 0.95)
    for i in range(6):
        draw_box(-21.5 + i * 1.0, 1.30, 17.5, 0.5, 0.11, 0.11)
