"""
objects/playground.py
---------------------
Area bermain anak: pasir, perosotan, ayunan (animasi), jungkat-jungkit,
palang panjat. Warna saturated cerah (kuning, merah, biru).
"""

import math
from OpenGL.GL  import (glBegin, glEnd, glVertex3f, glNormal3f,
                        GL_QUADS, GL_TRIANGLES,
                        glPushMatrix, glPopMatrix, glTranslatef, glRotatef)
from OpenGL.GLU import gluNewQuadric, gluCylinder, gluDisk, gluDeleteQuadric

from core.primitives import color, draw_box, draw_cylinder, draw_sphere


_PX, _PZ = 13.0, -14.0   # pusat area bermain


# ────────────────────────────────────────────────────────────────
# Helper: silinder horizontal (axle sepanjang sumbu X atau Z)
# ────────────────────────────────────────────────────────────────
def _hcyl(x: float, y: float, z: float,
          radius: float, length: float,
          axis: str = 'z', slices: int = 10):
    """Silinder horizontal. Pusat di (x, y, z), panjang `length`
    sepanjang sumbu `axis`."""
    glPushMatrix()
    glTranslatef(x, y, z)
    if axis == 'z':
        glTranslatef(0, 0, -length * 0.5)
    elif axis == 'x':
        glRotatef(90.0, 0, 1, 0)
        glTranslatef(0, 0, -length * 0.5)
    q = gluNewQuadric()
    gluCylinder(q, radius, radius, length, slices, 1)
    gluDisk(q, 0, radius, slices, 1)
    glTranslatef(0, 0, length)
    gluDisk(q, 0, radius, slices, 1)
    gluDeleteQuadric(q)
    glPopMatrix()


# ────────────────────────────────────────────────────────────────
# Playground utama
# ────────────────────────────────────────────────────────────────
def draw_playground(anim_time: float):
    px, pz = _PX, _PZ

    # ── Alas pasir ───────────────────────────────────────────────
    color(0.94, 0.82, 0.55)
    glBegin(GL_QUADS)
    glNormal3f(0, 1, 0)
    for vx, vz in [(-4, -3), (4, -3), (4, 3), (-4, 3)]:
        glVertex3f(px + vx, 0.04, pz + vz)
    glEnd()

    # Batu pembatas pasir
    color(0.62, 0.58, 0.50)
    for ix in range(-4, 5):
        draw_box(px + ix, 0.0, pz - 3, 0.85, 0.18, 0.20)
        draw_box(px + ix, 0.0, pz + 3, 0.85, 0.18, 0.20)
    for iz in range(-3, 4):
        draw_box(px - 4, 0.0, pz + iz, 0.20, 0.18, 0.85)
        draw_box(px + 4, 0.0, pz + iz, 0.20, 0.18, 0.85)

    _draw_slide(px, pz)
    _draw_swings(px, pz, anim_time)
    _draw_seesaw(px, pz, anim_time)
    _draw_monkey_bars(px, pz)


# ────────────────────────────────────────────────────────────────
# Perosotan
# ────────────────────────────────────────────────────────────────
def _draw_slide(px, pz):
    """
    Perosotan klasik dengan platform, tangga, perosotan kuning, dan atap.

    Orientasi:
      - Tangga di sisi -X (belakang platform)
      - Perosotan meluncur ke +X (depan)

    Tinggi-tinggi penting:
      0.00       = tanah
      deck_y      = 1.60   permukaan atas deck (tempat anak berdiri)
      rail_y      = 2.45   bagian atas railing pengaman deck
      eave_y      = 2.50   pangkal kemiringan atap
      ridge_y     = 3.10   puncak atap
    """

    # ── Konstanta geometri ─────────────────────────────────────
    deck_y      = 1.60               # permukaan atas deck (pijakan anak)
    deck_th     = 0.10               # ketebalan papan deck
    plat_x      = px - 1.6           # x-pusat deck
    plat_w      = 0.95               # ukuran deck sumbu X
    plat_d      = 1.05               # ukuran deck sumbu Z
    slide_x_end = plat_x + 2.80      # ujung bawah perosotan
    slide_w     = 0.85               # lebar bidang luncur (sumbu Z)
    rail_h      = 0.85               # tinggi railing pengaman dari deck
    post_t      = 0.12               # tebal tiang biru

    BLUE     = (0.18, 0.55, 0.92)
    BLUE_D   = (0.14, 0.45, 0.80)
    YELLOW   = (0.98, 0.82, 0.12)
    YELLOW_D = (0.95, 0.65, 0.10)
    RED      = (0.92, 0.22, 0.18)
    RED_D    = (0.78, 0.16, 0.12)

    rail_y = deck_y + rail_h         # 2.45 — atas railing
    deck_top = deck_y                # alias untuk kejelasan
    deck_bot = deck_y - deck_th      # bagian bawah papan deck

    # ── 4 tiang sudut (membentang dari tanah ke atap) ──────────
    # Tiang ini SEKALIGUS jadi tiang penyangga atap, jadi tingginya
    # sampai eave (2.50). Atap akan duduk persis di atasnya.
    eave_y = rail_y + 0.05
    color(*BLUE)
    posts = [
        (plat_x - plat_w * 0.5, -plat_d * 0.5),  # back-left
        (plat_x - plat_w * 0.5,  plat_d * 0.5),  # back-right
        (plat_x + plat_w * 0.5, -plat_d * 0.5),  # front-left
        (plat_x + plat_w * 0.5,  plat_d * 0.5),  # front-right
    ]
    for ox, oz in posts:
        draw_box(ox, 0.0, pz + oz, post_t, eave_y, post_t)

    # ── Papan deck (biru gelap) ────────────────────────────────
    color(*BLUE_D)
    draw_box(plat_x, deck_bot, pz, plat_w, deck_th, plat_d)

    # ── Railing samping (kiri & kanan deck, sumbu X) ───────────
    # Top rail di rail_y, mid rail di rail_y - 0.45 (sekitar pinggang)
    # Hanya dipasang di sisi -Z dan +Z; sisi belakang (-X) terbuka untuk
    # arch tangga; sisi depan (+X) terbuka karena slide-nya keluar dari sana.
    color(*BLUE)
    for oz in (-plat_d * 0.5, plat_d * 0.5):
        # Top rail
        draw_box(plat_x, rail_y - 0.04, pz + oz, plat_w, 0.08, 0.06)
        # Mid rail
        draw_box(plat_x, deck_y + rail_h * 0.45, pz + oz,
                 plat_w, 0.06, 0.05)
        # Vertical balusters (3 buah per sisi)
        for ix in (-plat_w * 0.30, 0.0, plat_w * 0.30):
            draw_box(plat_x + ix, deck_y, pz + oz,
                     0.04, rail_h, 0.04)

    # ── Arch belakang (di atas mulut tangga, sisi -X) ──────────
    # Hanya 2 tiang vertikal pendek + palang horizontal, semuanya
    # di BAWAH eave agar tidak menerobos atap.
    color(*BLUE)
    for oz in (-plat_d * 0.5, plat_d * 0.5):
        draw_box(plat_x - plat_w * 0.5, deck_y, pz + oz,
                 post_t, rail_h, post_t)
    # Palang atas tepat di rail_y
    draw_box(plat_x - plat_w * 0.5, rail_y - 0.04, pz,
             post_t, 0.08, plat_d)

    # ── Atap pelana (gable roof) ───────────────────────────────
    # Pangkal atap (eave) sedikit di atas top rail; ridge di tengah Z.
    ridge_y     = eave_y + 0.60
    overhang_x  = 0.18
    overhang_z  = 0.18
    rx_min = plat_x - plat_w * 0.5 - overhang_x
    rx_max = plat_x + plat_w * 0.5 + overhang_x
    rz_left  = pz - plat_d * 0.5 - overhang_z
    rz_right = pz + plat_d * 0.5 + overhang_z

    # Sisi kiri (-Z) miring ke ridge
    color(*RED)
    glBegin(GL_QUADS)
    glNormal3f(0, 0.7, -0.7)
    glVertex3f(rx_min, eave_y,  rz_left)
    glVertex3f(rx_max, eave_y,  rz_left)
    glVertex3f(rx_max, ridge_y, pz)
    glVertex3f(rx_min, ridge_y, pz)
    glEnd()

    # Sisi kanan (+Z)
    color(*RED_D)
    glBegin(GL_QUADS)
    glNormal3f(0, 0.7, 0.7)
    glVertex3f(rx_min, ridge_y, pz)
    glVertex3f(rx_max, ridge_y, pz)
    glVertex3f(rx_max, eave_y,  rz_right)
    glVertex3f(rx_min, eave_y,  rz_right)
    glEnd()

    # Tutup gable (segitiga) di sisi -X dan +X
    color(*RED_D)
    for x_face, nx in ((rx_min, -1.0), (rx_max, 1.0)):
        glBegin(GL_TRIANGLES)
        glNormal3f(nx, 0, 0)
        glVertex3f(x_face, eave_y,  rz_left)
        glVertex3f(x_face, eave_y,  rz_right)
        glVertex3f(x_face, ridge_y, pz)
        glEnd()

    # ── Tangga miring di belakang platform (sisi -X) ───────────
    n_steps     = 5
    stair_run   = 0.28              # jarak horizontal antar anak tangga
    stair_x_top = plat_x - plat_w * 0.5
    stair_x_bot = stair_x_top - n_steps * stair_run
    stair_d     = plat_d * 0.92     # lebar tangga (sumbu Z)

    # Stringer (panel segitiga di kedua sisi tangga)
    color(*BLUE_D)
    for side_z in (-stair_d * 0.5, stair_d * 0.5):
        glBegin(GL_TRIANGLES)
        glNormal3f(0, 0, 1 if side_z > 0 else -1)
        glVertex3f(stair_x_top, deck_y, pz + side_z)
        glVertex3f(stair_x_top, 0.0,    pz + side_z)
        glVertex3f(stair_x_bot, 0.0,    pz + side_z)
        glEnd()

    # Anak tangga merah
    color(*RED)
    rise = deck_y / n_steps
    for i in range(n_steps):
        sy = rise * (i + 1) - 0.04
        sx = stair_x_bot + i * stair_run + stair_run * 0.5
        draw_box(sx, sy, pz, stair_run, 0.06, stair_d)

    # Handrail tangga
    color(*BLUE)
    for side_z in (-stair_d * 0.5 - 0.04, stair_d * 0.5 + 0.04):
        # Tiang atas (sebagai sambungan ke deck)
        draw_box(stair_x_top, deck_y, pz + side_z,
                 post_t * 0.7, rail_h, post_t * 0.7)
        # Tiang bawah (di tanah)
        draw_box(stair_x_bot, 0.04, pz + side_z,
                 post_t * 0.7, rail_h, post_t * 0.7)
        # Pegangan miring (top rail)
        _draw_slanted_bar(stair_x_top, deck_y + rail_h, pz + side_z,
                          stair_x_bot, 0.04   + rail_h, pz + side_z,
                          radius=0.04)

    # ── Bidang luncur kuning ───────────────────────────────────
    x_top    = plat_x + plat_w * 0.5
    y_top    = deck_y                  # rata dengan deck
    x_bottom = slide_x_end
    y_bottom = 0.18                    # sedikit di atas tanah
    half_w   = slide_w * 0.5
    side_h   = 0.18                    # tinggi dinding samping perosotan

    # Permukaan luncur (atas)
    color(*YELLOW)
    glBegin(GL_QUADS)
    glNormal3f(-0.5, 0.7, 0)           # arahnya ke kiri-atas
    glVertex3f(x_top,    y_top,    pz - half_w)
    glVertex3f(x_top,    y_top,    pz + half_w)
    glVertex3f(x_bottom, y_bottom, pz + half_w)
    glVertex3f(x_bottom, y_bottom, pz - half_w)
    glEnd()

    # Dinding samping perosotan (di atas permukaan, kiri & kanan)
    color(*YELLOW_D)
    for side in (-half_w, half_w):
        outer_n = 1 if side > 0 else -1
        glBegin(GL_QUADS)
        glNormal3f(0, 0, outer_n)
        glVertex3f(x_top,    y_top,             pz + side)
        glVertex3f(x_bottom, y_bottom,          pz + side)
        glVertex3f(x_bottom, y_bottom + side_h, pz + side)
        glVertex3f(x_top,    y_top    + side_h, pz + side)
        glEnd()
        # Tutup tepi atas dinding
        glBegin(GL_QUADS)
        glNormal3f(0, 1, 0)
        glVertex3f(x_top,    y_top    + side_h, pz + side - 0.04 * outer_n)
        glVertex3f(x_top,    y_top    + side_h, pz + side + 0.04 * outer_n)
        glVertex3f(x_bottom, y_bottom + side_h, pz + side + 0.04 * outer_n)
        glVertex3f(x_bottom, y_bottom + side_h, pz + side - 0.04 * outer_n)
        glEnd()
        # Tutup luar (samping luar dinding)
        glBegin(GL_QUADS)
        glNormal3f(0, 0, outer_n)
        glVertex3f(x_top,    y_top,             pz + side + 0.04 * outer_n)
        glVertex3f(x_top,    y_top    + side_h, pz + side + 0.04 * outer_n)
        glVertex3f(x_bottom, y_bottom + side_h, pz + side + 0.04 * outer_n)
        glVertex3f(x_bottom, y_bottom,          pz + side + 0.04 * outer_n)
        glEnd()

    # Bibir bawah perosotan (run-out lip) — landai datar
    color(*YELLOW)
    lip_x = slide_x_end + 0.20
    draw_box(lip_x, 0.04, pz, 0.36, 0.06, slide_w)


def _draw_slanted_bar(x1, y1, z1, x2, y2, z2, radius=0.04):
    """Silinder ramping antara dua titik — untuk pegangan miring."""
    dx, dy, dz = x2 - x1, y2 - y1, z2 - z1
    length = math.sqrt(dx * dx + dy * dy + dz * dz)
    if length < 1e-6:
        return
    glPushMatrix()
    glTranslatef(x1, y1, z1)
    nx, ny, nz = dx / length, dy / length, dz / length
    ax, ay = -ny, nx
    angle = math.degrees(math.acos(max(-1.0, min(1.0, nz))))
    if abs(ax) + abs(ay) > 1e-6:
        glRotatef(angle, ax, ay, 0)
    elif nz < 0:
        glRotatef(180.0, 1, 0, 0)
    q = gluNewQuadric()
    gluCylinder(q, radius, radius, length, 8, 1)
    gluDeleteQuadric(q)
    glPopMatrix()


# ────────────────────────────────────────────────────────────────
# Ayunan
# ────────────────────────────────────────────────────────────────
def _draw_swings(px, pz, t):
    """Ayunan rangka biru dengan dua A-frame & dudukan menggantung."""

    # Pusat rangka di z = pz - 2.0 (lebih jauh dari tepi pasir)
    swz = pz - 1.8
    frame_top_y = 2.6     # tinggi rel atas
    seat_y      = 0.55    # tinggi dudukan dari tanah

    # ── Empat tiang (dua A-frame: depan/belakang) ───────────────
    color(0.18, 0.55, 0.92)
    for dx in (1.0, 3.0):
        for dz in (-0.55, 0.55):
            draw_box(px + dx, 0.04, swz + dz, 0.12, frame_top_y, 0.12)

    # Rel atas (membujur sumbu X, menghubungkan dua A-frame)
    draw_box(px + 2.0, frame_top_y, swz, 2.20, 0.14, 0.14)

    # Penyangga miring (cross brace di kedua sisi)
    color(0.16, 0.50, 0.86)
    for dz in (-0.55, 0.55):
        draw_box(px + 2.0, frame_top_y + 0.07, swz + dz, 2.30, 0.06, 0.06)

    # ── Dua dudukan ayunan dengan tali (animasi) ────────────────
    sw_swing = math.sin(t * 1.6) * 0.30   # sudut ayun

    rope_top_y    = frame_top_y           # menggantung dari rel atas
    rope_length   = rope_top_y - seat_y   # ~2.05
    seat_thick    = 0.10
    seat_w        = 0.50
    seat_d        = 0.24

    for sw_x in (px + 1.5, px + 2.5):
        # Saat ayun, dudukan bergerak ke depan/belakang sepanjang sumbu Z
        # Tali tetap menggantung dari titik atap; titik bawah bergerak.
        offset_z = sw_swing * rope_length   # pergeseran horizontal seat
        seat_z   = swz + offset_z
        seat_top = seat_y + seat_thick

        # Tali kiri & kanan (dua tali per ayunan, tegang dari atap ke dudukan)
        for rope_dz in (-seat_d * 0.45, seat_d * 0.45):
            anchor_z = swz + rope_dz       # titik anchor di rel atas
            seat_anchor_z = seat_z + rope_dz
            _draw_rope(sw_x, rope_top_y, anchor_z,
                       sw_x, seat_top,    seat_anchor_z)

        # Dudukan kayu
        color(0.62, 0.40, 0.18)
        draw_box(sw_x, seat_y, seat_z, seat_w, seat_thick, seat_d)


def _draw_rope(x1, y1, z1, x2, y2, z2):
    """Tali tegang antara dua titik (silinder ramping)."""
    dx, dy, dz = x2 - x1, y2 - y1, z2 - z1
    length = math.sqrt(dx * dx + dy * dy + dz * dz)
    if length < 1e-6:
        return
    color(0.22, 0.22, 0.24)
    glPushMatrix()
    glTranslatef(x1, y1, z1)
    # gluCylinder default arah +Z. Kita perlu rotasi agar arah ke (dx,dy,dz).
    # Hitung sudut rotasi sumbu Z → vektor target.
    # Pakai cross product Z × dir.
    # Z = (0,0,1)
    nx, ny, nz = dx / length, dy / length, dz / length
    # axis = Z × dir = (-ny, nx, 0)
    ax, ay, az = -ny, nx, 0.0
    angle = math.degrees(math.acos(max(-1.0, min(1.0, nz))))
    if abs(ax) + abs(ay) > 1e-6:
        glRotatef(angle, ax, ay, az)
    elif nz < 0:
        glRotatef(180.0, 1, 0, 0)
    q = gluNewQuadric()
    gluCylinder(q, 0.025, 0.025, length, 6, 1)
    gluDeleteQuadric(q)
    glPopMatrix()


# ────────────────────────────────────────────────────────────────
# Jungkat-jungkit
# ────────────────────────────────────────────────────────────────
def _draw_seesaw(px, pz, t):
    """Jungkat-jungkit dengan papan oranye."""
    color(0.20, 0.20, 0.22)
    draw_cylinder(px + 2.5, 0.04, pz + 1.8, 0.07, 0.55, 6)
    draw_sphere(px + 2.5, 0.62, pz + 1.8, 0.12)

    tilt = math.sin(t * 0.8) * 0.25
    color(0.92, 0.42, 0.16)
    glPushMatrix()
    glTranslatef(px + 2.5, 0.62, pz + 1.8)
    glRotatef(math.degrees(tilt), 0, 0, 1)
    draw_box(0, 0.05, 0, 2.50, 0.12, 0.30)
    color(0.18, 0.55, 0.92)
    draw_cylinder(-1.1, 0.14, 0, 0.05, 0.32, 6)
    draw_cylinder( 1.1, 0.14, 0, 0.05, 0.32, 6)
    glPopMatrix()


# ────────────────────────────────────────────────────────────────
# Palang panjat (monkey bars)
# ────────────────────────────────────────────────────────────────
def _draw_monkey_bars(px, pz):
    """Palang panjat horizontal: 4 tiang sudut + dua rel + rung horizontal."""
    bx, bz = px + 3.0, pz - 0.5
    h_post = 2.0

    # Empat tiang sudut
    color(0.18, 0.55, 0.92)
    for dx, dz in [(-0.8, -0.6), (0.8, -0.6), (-0.8, 0.6), (0.8, 0.6)]:
        draw_cylinder(bx + dx, 0.04, bz + dz, 0.07, h_post, 6)

    # Dua rel panjang (sumbu X, panjang 1.6m)
    rail_y = h_post + 0.04
    draw_box(bx, rail_y, bz - 0.6, 1.80, 0.10, 0.10)
    draw_box(bx, rail_y, bz + 0.6, 1.80, 0.10, 0.10)

    # Rung horizontal (kuning) — silinder pendek sepanjang sumbu Z
    # menghubungkan dua rel
    color(0.98, 0.82, 0.12)
    rung_y = rail_y + 0.05    # sedikit di atas rel
    for i in range(5):
        rx = bx - 0.65 + i * 0.32
        # Pusat rung di (rx, rung_y, bz), panjang 1.2 m sumbu Z
        _hcyl(rx, rung_y, bz, radius=0.04, length=1.20, axis='z')
