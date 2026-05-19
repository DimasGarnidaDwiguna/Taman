"""
  TAMAN KOTA - Simulasi 3D OpenGL
  Entry Point Utama

  Kontrol:
    W/S       - Maju / Mundur
    A/D       - Geser Kiri / Kanan
    Q/E       - Naik / Turun
    Panah ←→  - Putar Kiri / Kanan
    Panah ↑↓  - Tengok Atas / Bawah
    Klik kiri + geser mouse - Rotasi kamera
    ESC       - Keluar

  Jalankan: python main.py
"""

import sys

def check_dependencies():
    missing = []
    try:
        import pygame
    except ImportError:
        missing.append("pygame")
    try:
        from OpenGL.GL import glClear
    except ImportError:
        missing.append("PyOpenGL")

    if missing:
        print("ERROR: Library berikut tidak ditemukan:")
        for m in missing:
            print(f"  - {m}")
        print("\nJalankan: pip install -r requirements.txt")
        sys.exit(1)

check_dependencies()

import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

from core.renderer import Renderer
from core.camera import Camera
from core.state import AnimationState
from core.lighting import setup_lighting


WIDTH, HEIGHT = 1280, 720
TARGET_FPS   = 144


def print_controls():
    print("=" * 52)
    print("   TAMAN KOTA - Simulasi 3D OpenGL (Python)")
    print("=" * 52)
    print("  W / S        - Maju / Mundur")
    print("  A / D        - Geser Kiri / Kanan")
    print("  Q / E        - Naik / Turun")
    print("  Panah ← →   - Putar Kiri / Kanan")
    print("  Panah ↑ ↓   - Tengok Atas / Bawah")
    print("  Klik kiri + geser mouse - Rotasi kamera")
    print("  ESC          - Keluar")
    print("=" * 52)


def init_opengl():
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
    glShadeModel(GL_SMOOTH)
    glEnable(GL_NORMALIZE)
    glEnable(GL_FOG)
    glFogi(GL_FOG_MODE, GL_LINEAR)
    glFogfv(GL_FOG_COLOR, [0.78, 0.90, 0.99, 1.0])  # menyatu ke horizon cyan
    glFogf(GL_FOG_START, 55.0)
    glFogf(GL_FOG_END, 110.0)
    glClearColor(0.78, 0.90, 0.99, 1.0)   # cyan cerah
    setup_lighting()
    _set_projection(WIDTH, HEIGHT)


def _set_projection(w, h):
    if h == 0:
        h = 1
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(55.0, w / h, 0.5, 150.0)
    glMatrixMode(GL_MODELVIEW)


def main():
    print_controls()

    pygame.init()
    # Minta depth buffer 24-bit (default pygame sering 16-bit → z-fighting parah
    # antara rumput dan jalur yang ketinggiannya berdekatan).
    pygame.display.gl_set_attribute(pygame.GL_DEPTH_SIZE, 24)
    pygame.display.gl_set_attribute(pygame.GL_DOUBLEBUFFER, 1)
    # VSync = frame pacing halus (tanpa ini, walau FPS tinggi gerakan
    # bisa terasa stutter karena waktu antar frame tidak konsisten).
    try:
        pygame.display.gl_set_attribute(pygame.GL_SWAP_CONTROL, 1)
    except Exception:
        pass
    pygame.display.set_mode((WIDTH, HEIGHT), DOUBLEBUF | OPENGL | RESIZABLE)
    pygame.display.set_caption("Taman Kota — OpenGL 3D | Python")

    init_opengl()

    camera    = Camera(x=0.0, y=16.0, z=30.0, angle_y=0.0, angle_x=-28.0)
    anim      = AnimationState()
    renderer  = Renderer(anim)
    clock     = pygame.time.Clock()
    running   = True
    was_dragging = False

    while running:
        dt = clock.tick(TARGET_FPS) / 1000.0

        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                running = False
            elif event.type == VIDEORESIZE:
                _set_projection(event.w, event.h)

        # ── Rotasi kamera via drag mouse (klik kiri tahan + geser) ──
        # Pakai polling, bukan event MOUSEMOTION, supaya:
        #  1. Tidak ada "lonjakan" di frame pertama drag (event.rel
        #     menumpuk gerakan sebelum klik).
        #  2. Rotasi kontinu setiap frame, mirip arrow keys.
        mouse_pressed = pygame.mouse.get_pressed()[0]
        mdx, mdy = pygame.mouse.get_rel()   # selalu dipanggil agar reset tiap frame
        if mouse_pressed and was_dragging:
            camera.rotate_by_mouse(mdx, mdy)
        was_dragging = mouse_pressed

        keys = pygame.key.get_pressed()
        camera.update(keys, dt)
        anim.update(dt)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        camera.apply()
        renderer.draw_scene()
        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
