"""
core/primitives.py
------------------
Fungsi menggambar bentuk dasar (primitif) pakai OpenGL murni.
Semua fungsi menerima posisi dunia dan ukuran, lalu menggambar
langsung — tidak ada state tersimpan di sisi kaller.

Konvensi koordinat:
  x = kanan, y = atas, z = keluar layar (OpenGL default)
  Posisi y yang diterima selalu merupakan ALAS objek (y_bottom),
  kecuali sphere yang menggunakan titik PUSAT.

Optimasi:
  - Satu quadric GLU di-cache (dulu dibuat & dihapus tiap panggilan).
  - Bentuk unit (cube, sphere, cylinder, cone, disk) dikompilasi ke
    display list sekali, lalu dipanggil ulang dengan glScalef. Ini
    memangkas ribuan panggilan Python→GL per frame.
  - GL_NORMALIZE harus aktif (sudah di-enable di main.init_opengl)
    supaya lighting tetap benar saat shape di-scale non-uniform.
"""

import math
from OpenGL.GL  import *
from OpenGL.GLU import *


# ────────────────────────────────────────────────────────────────
# Cache: quadric tunggal + display list per bentuk unit
# ────────────────────────────────────────────────────────────────
_quadric = None
_display_lists: dict = {}


def _get_quadric():
    global _quadric
    if _quadric is None:
        _quadric = gluNewQuadric()
        gluQuadricNormals(_quadric, GLU_SMOOTH)
    return _quadric


def _get_or_build_list(key, build_fn):
    lid = _display_lists.get(key)
    if lid is None:
        lid = glGenLists(1)
        glNewList(lid, GL_COMPILE)
        build_fn()
        glEndList()
        _display_lists[key] = lid
    return lid


# ────────────────────────────────────────────────────────────────
# Warna
# ────────────────────────────────────────────────────────────────
def color(r, g, b):
    glColor3f(r, g, b)


# ────────────────────────────────────────────────────────────────
# Builder bentuk unit (dipanggil sekali saat list pertama dibuat)
# ────────────────────────────────────────────────────────────────
def _build_unit_cube():
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


def _build_unit_cylinder(slices):
    q = _get_quadric()
    # gluCylinder digenerate sepanjang sumbu +Z lokal, kita rotasi
    # supaya jadi sepanjang +Y dunia (sebelum di-scale oleh kaller).
    glRotatef(-90.0, 1, 0, 0)
    gluCylinder(q, 1.0, 1.0, 1.0, slices, 1)
    gluDisk(q, 0, 1.0, slices, 1)
    glTranslatef(0, 0, 1.0)
    gluDisk(q, 0, 1.0, slices, 1)


def _build_unit_cone(slices):
    q = _get_quadric()
    glRotatef(-90.0, 1, 0, 0)
    gluCylinder(q, 1.0, 0.0, 1.0, slices, 1)
    gluDisk(q, 0, 1.0, slices, 1)


def _build_unit_sphere(slices, stacks):
    q = _get_quadric()
    gluSphere(q, 1.0, slices, stacks)


def _build_unit_disk(slices):
    q = _get_quadric()
    glRotatef(-90.0, 1, 0, 0)
    gluDisk(q, 0, 1.0, slices, 1)


# ────────────────────────────────────────────────────────────────
# Kubus / Box
# ────────────────────────────────────────────────────────────────
def draw_box(x, y_bottom, z, width, height, depth):
    """Menggambar kotak solid. y_bottom = alas kotak."""
    lid = _get_or_build_list(("cube",), _build_unit_cube)
    glPushMatrix()
    glTranslatef(x, y_bottom + height * 0.5, z)
    glScalef(width, height, depth)
    glCallList(lid)
    glPopMatrix()


# ────────────────────────────────────────────────────────────────
# Silinder
# ────────────────────────────────────────────────────────────────
def draw_cylinder(x, y_bottom, z, radius, height, slices=16):
    """Silinder tegak lurus sumbu-Y."""
    lid = _get_or_build_list(
        ("cyl", slices),
        lambda s=slices: _build_unit_cylinder(s),
    )
    glPushMatrix()
    glTranslatef(x, y_bottom, z)
    glScalef(radius, height, radius)
    glCallList(lid)
    glPopMatrix()


# ────────────────────────────────────────────────────────────────
# Kerucut
# ────────────────────────────────────────────────────────────────
def draw_cone(x, y_bottom, z, radius, height, slices=16):
    lid = _get_or_build_list(
        ("cone", slices),
        lambda s=slices: _build_unit_cone(s),
    )
    glPushMatrix()
    glTranslatef(x, y_bottom, z)
    glScalef(radius, height, radius)
    glCallList(lid)
    glPopMatrix()


# ────────────────────────────────────────────────────────────────
# Bola
# ────────────────────────────────────────────────────────────────
def draw_sphere(x, y_center, z, radius, slices=16, stacks=12):
    lid = _get_or_build_list(
        ("sph", slices, stacks),
        lambda s=slices, st=stacks: _build_unit_sphere(s, st),
    )
    glPushMatrix()
    glTranslatef(x, y_center, z)
    glScalef(radius, radius, radius)
    glCallList(lid)
    glPopMatrix()


# ────────────────────────────────────────────────────────────────
# Disk (lingkaran datar)
# ────────────────────────────────────────────────────────────────
def draw_disk(x, y, z, radius, slices=32):
    lid = _get_or_build_list(
        ("disk", slices),
        lambda s=slices: _build_unit_disk(s),
    )
    glPushMatrix()
    glTranslatef(x, y, z)
    glScalef(radius, 1.0, radius)
    glCallList(lid)
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
