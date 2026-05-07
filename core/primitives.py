"""
core/primitives.py
------------------
Fungsi menggambar bentuk dasar (primitif) pakai OpenGL murni.
Semua fungsi menerima posisi dunia dan ukuran, lalu menggambar
langsung — tidak ada state tersimpan.

Konvensi koordinat:
  x = kanan, y = atas, z = keluar layar (OpenGL default)
  Posisi y yang diterima selalu merupakan ALAS objek (y_bottom),
  kecuali sphere yang menggunakan titik PUSAT.
"""

import math
from OpenGL.GL  import *
from OpenGL.GLU import *


# ────────────────────────────────────────────────────────────────
# Warna
# ────────────────────────────────────────────────────────────────
def color(r, g, b):
    glColor3f(r, g, b)


# ────────────────────────────────────────────────────────────────
# Kubus / Box
# ────────────────────────────────────────────────────────────────
def draw_box(x, y_bottom, z, width, height, depth):
    """Menggambar kotak solid. y_bottom = alas kotak."""
    glPushMatrix()
    glTranslatef(x, y_bottom + height * 0.5, z)
    glScalef(width, height, depth)
    _unit_cube()
    glPopMatrix()


def _unit_cube():
    h = 0.5
    glBegin(GL_QUADS)
    # Depan (+Z)
    glNormal3f( 0,  0,  1)
    glVertex3f(-h, -h,  h); glVertex3f( h, -h,  h)
    glVertex3f( h,  h,  h); glVertex3f(-h,  h,  h)
    # Belakang (-Z)
    glNormal3f( 0,  0, -1)
    glVertex3f( h, -h, -h); glVertex3f(-h, -h, -h)
    glVertex3f(-h,  h, -h); glVertex3f( h,  h, -h)
    # Atas (+Y)
    glNormal3f( 0,  1,  0)
    glVertex3f(-h,  h,  h); glVertex3f( h,  h,  h)
    glVertex3f( h,  h, -h); glVertex3f(-h,  h, -h)
    # Bawah (-Y)
    glNormal3f( 0, -1,  0)
    glVertex3f(-h, -h, -h); glVertex3f( h, -h, -h)
    glVertex3f( h, -h,  h); glVertex3f(-h, -h,  h)
    # Kanan (+X)
    glNormal3f( 1,  0,  0)
    glVertex3f( h, -h,  h); glVertex3f( h, -h, -h)
    glVertex3f( h,  h, -h); glVertex3f( h,  h,  h)
    # Kiri (-X)
    glNormal3f(-1,  0,  0)
    glVertex3f(-h, -h, -h); glVertex3f(-h, -h,  h)
    glVertex3f(-h,  h,  h); glVertex3f(-h,  h, -h)
    glEnd()


# ────────────────────────────────────────────────────────────────
# Silinder
# ────────────────────────────────────────────────────────────────
def draw_cylinder(x, y_bottom, z, radius, height, slices=16):
    """Silinder tegak lurus sumbu-Y."""
    glPushMatrix()
    glTranslatef(x, y_bottom, z)
    glRotatef(-90.0, 1, 0, 0)      # putar agar sumbu Z → Y
    q = gluNewQuadric()
    gluQuadricNormals(q, GLU_SMOOTH)
    gluCylinder(q, radius, radius, height, slices, 1)
    gluDisk(q, 0, radius, slices, 1)               # tutup bawah
    glTranslatef(0, 0, height)
    gluDisk(q, 0, radius, slices, 1)               # tutup atas
    gluDeleteQuadric(q)
    glPopMatrix()


# ────────────────────────────────────────────────────────────────
# Kerucut
# ────────────────────────────────────────────────────────────────
def draw_cone(x, y_bottom, z, radius, height, slices=16):
    glPushMatrix()
    glTranslatef(x, y_bottom, z)
    glRotatef(-90.0, 1, 0, 0)
    q = gluNewQuadric()
    gluQuadricNormals(q, GLU_SMOOTH)
    gluCylinder(q, radius, 0.0, height, slices, 1)
    gluDisk(q, 0, radius, slices, 1)
    gluDeleteQuadric(q)
    glPopMatrix()


# ────────────────────────────────────────────────────────────────
# Bola
# ────────────────────────────────────────────────────────────────
def draw_sphere(x, y_center, z, radius, slices=16, stacks=12):
    glPushMatrix()
    glTranslatef(x, y_center, z)
    q = gluNewQuadric()
    gluQuadricNormals(q, GLU_SMOOTH)
    gluSphere(q, radius, slices, stacks)
    gluDeleteQuadric(q)
    glPopMatrix()


# ────────────────────────────────────────────────────────────────
# Disk (lingkaran datar)
# ────────────────────────────────────────────────────────────────
def draw_disk(x, y, z, radius, slices=32):
    glPushMatrix()
    glTranslatef(x, y, z)
    glRotatef(-90.0, 1, 0, 0)
    q = gluNewQuadric()
    gluQuadricNormals(q, GLU_SMOOTH)
    gluDisk(q, 0, radius, slices, 1)
    gluDeleteQuadric(q)
    glPopMatrix()


# ────────────────────────────────────────────────────────────────
# Quad datar (lantai, jalan, bidang)
# ────────────────────────────────────────────────────────────────
def draw_flat_quad(x1, z1, x2, z2, y=0.0):
    """Persegi panjang datar di ketinggian y."""
    glBegin(GL_QUADS)
    glNormal3f(0, 1, 0)
    glVertex3f(x1, y, z1)
    glVertex3f(x2, y, z1)
    glVertex3f(x2, y, z2)
    glVertex3f(x1, y, z2)
    glEnd()


# ────────────────────────────────────────────────────────────────
# Helper jalur (strip)
# ────────────────────────────────────────────────────────────────
def draw_path_segment(x1, z1, x2, z2, width, y=0.02):
    dx = x2 - x1
    dz = z2 - z1
    length = math.hypot(dx, dz)
    if length < 1e-6:
        return
    nx = -dz / length * width * 0.5
    nz =  dx / length * width * 0.5
    glBegin(GL_QUADS)
    glNormal3f(0, 1, 0)
    glVertex3f(x1 + nx, y, z1 + nz)
    glVertex3f(x2 + nx, y, z2 + nz)
    glVertex3f(x2 - nx, y, z2 - nz)
    glVertex3f(x1 - nx, y, z1 - nz)
    glEnd()
