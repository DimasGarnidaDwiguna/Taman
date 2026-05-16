"""
objects/person.py
-----------------
Karakter manusia sederhana dengan animasi berjalan realistis:
- Kaki berayun berlawanan fase
- Lengan berayun berlawanan kaki
- Sedikit gerakan naik-turun badan
"""

import math
from OpenGL.GL import glPushMatrix, glTranslatef, glRotatef, glPopMatrix
from core.primitives import color, draw_cylinder, draw_sphere, draw_box, draw_cone
from core.layout     import is_blocked, register_zone


def draw_person(x: float, z: float, shirt_r: float, shirt_g: float, shirt_b: float,
                angle_deg: float = 0.0, anim_phase: float = 0.0,
                is_running: bool = False, seed: float | None = None):
    """
    Gambar satu orang berdiri/berjalan.
    anim_phase : offset fase animasi (radian)
    is_running : kaki ayun lebih lebar jika berlari
    seed       : nilai stabil untuk pemilihan rambut & topi (gunakan ini
                 untuk karakter beranimasi/berpindah; jika None,
                 dihitung dari posisi awal)
    """
    glPushMatrix()
    glTranslatef(x, 0, z)
    glRotatef(angle_deg, 0, 1, 0)

    swing_amp = 0.40 if is_running else 0.22
    leg_swing  = math.sin(anim_phase) * swing_amp
    arm_swing  = -leg_swing * 0.7
    bob_y      = abs(math.sin(anim_phase)) * 0.04   # sedikit naik-turun

    # ── Sepatu ──────────────────────────────────────────────────
    color(0.20, 0.16, 0.12)
    draw_box(-0.07, 0.02, leg_swing  * 0.3, 0.12, 0.06, 0.18)
    draw_box( 0.07, 0.02, -leg_swing * 0.3, 0.12, 0.06, 0.18)

    # ── Celana ──────────────────────────────────────────────────
    color(0.24, 0.28, 0.38)
    draw_cylinder(-0.07, 0.06, leg_swing  * 0.2, 0.07, 0.52, 7)
    draw_cylinder( 0.07, 0.06, -leg_swing * 0.2, 0.07, 0.52, 7)

    # ── Badan / kemeja ───────────────────────────────────────────
    color(shirt_r, shirt_g, shirt_b)
    draw_cylinder(0, 0.58 + bob_y, 0, 0.155, 0.60, 8)

    # ── Lengan ───────────────────────────────────────────────────
    skin = (0.82, 0.66, 0.52)
    # Lengan kiri
    color(shirt_r * 0.85, shirt_g * 0.85, shirt_b * 0.85)
    draw_cylinder(-0.19, 0.68 + bob_y, arm_swing * 0.25, 0.055, 0.45, 6)
    color(*skin)
    draw_cylinder(-0.20, 0.55 + bob_y, arm_swing * 0.35, 0.048, 0.22, 6)

    # Lengan kanan
    color(shirt_r * 0.85, shirt_g * 0.85, shirt_b * 0.85)
    draw_cylinder( 0.19, 0.68 + bob_y, -arm_swing * 0.25, 0.055, 0.45, 6)
    color(*skin)
    draw_cylinder( 0.20, 0.55 + bob_y, -arm_swing * 0.35, 0.048, 0.22, 6)

    # ── Leher & kepala ───────────────────────────────────────────
    color(*skin)
    draw_cylinder(0, 1.18 + bob_y, 0, 0.07, 0.12, 7)
    draw_sphere(0, 1.44 + bob_y, 0, 0.185)

    # ── Rambut ───────────────────────────────────────────────────
    hair_colors = [
        (0.10, 0.08, 0.06),
        (0.35, 0.22, 0.10),
        (0.80, 0.72, 0.52),
    ]
    # Gunakan seed stabil agar rambut/topi tidak berubah saat orang
    # bergerak (kalau pakai x,z langsung, tiap frame nilai berubah →
    # topi kelap-kelip).
    sd = seed if seed is not None else (x * 3 + z * 7)
    hc_idx     = abs(int(sd * 11)) % 3
    hat_choice = abs(int(sd * 17 + 5)) % 4
    color(*hair_colors[hc_idx])
    draw_sphere(0, 1.52 + bob_y, 0, 0.155)
    # Topi (deterministic by seed)
    if hat_choice == 0:
        color(0.18, 0.38, 0.68)
        draw_cylinder(0, 1.58 + bob_y, 0, 0.20, 0.20, 8)
        draw_cylinder(0, 1.56 + bob_y, 0, 0.26, 0.05, 8)

    glPopMatrix()


def draw_all_people(anim_time: float):
    """Semua pejalan kaki dan pelari di taman."""

    # Fase animasi per-orang
    def phase(x, z): return anim_time * 2.5 + x * 1.3 + z * 0.9

    # Buffer person: 0.55 (radius badan ~0.2 + jarak personal ~0.35)
    PERSON_R = 0.55

    def try_draw(x, z, cr, cg, cb, a, ph, running=False):
        """Gambar orang hanya jika posisinya bebas, lalu register zone."""
        if is_blocked(x, z, 0.0):
            return False
        draw_person(x, z, cr, cg, cb, a, ph, is_running=running)
        register_zone(x, z, PERSON_R)
        return True

    # ── Pengunjung di jalur masuk ────────────────────────────────
    visitors_gate = [
        ( 0.3, 14.5, 0.90, 0.30, 0.30,   0),
        ( 1.3, 13.5, 0.30, 0.60, 0.90,  12),
        (-1.2, 13.0, 0.88, 0.72, 0.10, -10),
        ( 0.0, 11.5, 0.50, 0.78, 0.30,   5),
        (-1.5, 10.0, 0.70, 0.20, 0.55, -15),
    ]
    for x, z, cr, cg, cb, a in visitors_gate:
        try_draw(x, z, cr, cg, cb, a, phase(x, z))

    # ── Pengunjung di sekitar air mancur (di luar basin r=2.8) ──
    fountain_visitors = [
        (-3.4,  4.6, 0.82, 0.20, 0.80,  35),
        ( 3.4,  4.6, 0.10, 0.70, 0.32, -42),
        ( 4.6,  0.4, 0.88, 0.60, 0.12,  90),
        (-4.6,  0.4, 0.32, 0.32, 0.92, -90),
        ( 0.0, -4.6, 0.82, 0.50, 0.22, 180),
        ( 1.5,  5.5, 0.20, 0.65, 0.88,  60),
    ]
    for x, z, cr, cg, cb, a in fountain_visitors:
        try_draw(x, z, cr, cg, cb, a, phase(x, z))

    # ── Anak-anak di area bermain (animasi melingkar di pasir) ──
    PG_PX, PG_PZ = 13.0, -14.0   # sama dengan playground.py

    # Note: anak-anak di playground tidak perlu filter (sudah di
    # area khusus pasir), tapi posisi mereka kita register supaya
    # orang lain di luar tidak masuk
    for k_idx, (ofs, cr, cg, cb) in enumerate([
        (0.0,     0.90, 0.40, 0.12),
        (math.pi, 0.30, 0.70, 0.90),
    ]):
        t = anim_time * 1.0 + ofs
        ax, az = 1.4, 0.55
        cx, cz = PG_PX - 1.0, PG_PZ - 1.5
        kx = cx + ax * math.cos(t)
        kz = cz + az * math.sin(t)
        vx = -ax * math.sin(t)
        vz =  az * math.cos(t)
        face = math.degrees(math.atan2(vz, vx))
        draw_person(kx, kz, cr, cg, cb, face,
                    anim_time * 4.5 + ofs, is_running=True,
                    seed=100.0 + k_idx)
        register_zone(kx, kz, PERSON_R)

    t3 = anim_time * 0.6
    k3x = (PG_PX - 1.0) + math.sin(t3) * 1.8
    k3z = PG_PZ + 2.0
    k3_face = 0 if math.cos(t3) > 0 else 180
    draw_person(k3x, k3z, 0.70, 0.90, 0.22, k3_face,
                anim_time * 2.6, seed=102.0)
    register_zone(k3x, k3z, PERSON_R)

    t4 = anim_time * 0.55 + 1.7
    k4x = (PG_PX + 0.5) + math.sin(t4) * 1.2
    k4z = PG_PZ - 1.2
    k4_face = 0 if math.cos(t4) > 0 else 180
    draw_person(k4x, k4z, 0.90, 0.22, 0.55, k4_face,
                anim_time * 2.4, seed=103.0)
    register_zone(k4x, k4z, PERSON_R)

    # ── Pengunjung di area kolam (di luar pond r=4.2) ────────────
    pond_visitors = [
        (15.8, -5.5, 0.40, 0.62, 0.90, -45),
        (16.0, -1.0, 0.88, 0.32, 0.62,  90),
        ( 6.4, -2.0, 0.32, 0.78, 0.45, 150),
    ]
    for x, z, cr, cg, cb, a in pond_visitors:
        try_draw(x, z, cr, cg, cb, a, phase(x, z))

    # ── Pengunjung tersebar (otomatis filter struktur & furnitur)─
    scattered = [
        (-12.0,  6.0, 0.72, 0.60, 0.32,  48),
        (-11.0, -7.0, 0.30, 0.80, 0.62, 180),
        ( 12.0, -8.5, 0.90, 0.40, 0.32, -30),
        (  7.5,  9.0, 0.50, 0.50, 0.90,  62),
        ( -7.5,  9.0, 0.80, 0.32, 0.32, -62),
        (  2.5, -11.0, 0.30, 0.72, 0.40,  10),
        (-10.0, -13.0, 0.88, 0.70, 0.20,-120),
        ( -2.5, -7.0, 0.40, 0.50, 0.85,  90),
        (  4.5, -8.0, 0.85, 0.45, 0.60, -90),
        (-15.0,  0.5, 0.62, 0.30, 0.78,  30),
    ]
    for x, z, cr, cg, cb, a in scattered:
        try_draw(x, z, cr, cg, cb, a, phase(x, z))
