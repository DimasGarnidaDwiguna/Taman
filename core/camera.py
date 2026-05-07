"""
core/camera.py
--------------
Sistem kamera FPS sederhana: posisi + yaw + pitch.
"""

import math
from OpenGL.GLU import gluLookAt
from pygame.locals import (
    K_w, K_s, K_a, K_d, K_q, K_e,
    K_LEFT, K_RIGHT, K_UP, K_DOWN,
)

SPEED_BASE   = 8.0   # unit/detik
ROTATE_SPEED = 90.0  # derajat/detik


class Camera:
    def __init__(self, x=0.0, y=16.0, z=30.0,
                 angle_y=0.0, angle_x=-28.0):
        self.x       = x
        self.y       = y
        self.z       = z
        self.angle_y = angle_y   # yaw   (horizontal)
        self.angle_x = angle_x   # pitch (vertical)

    # ----------------------------------------------------------------
    def update(self, keys, dt: float):
        speed  = SPEED_BASE * dt
        rot_sp = ROTATE_SPEED * dt

        ry = math.radians(self.angle_y)
        fwd_x  =  math.sin(ry)
        fwd_z  = -math.cos(ry)
        right_x =  math.cos(ry)
        right_z =  math.sin(ry)

        if keys[K_w]:
            self.x += fwd_x  * speed
            self.z += fwd_z  * speed
        if keys[K_s]:
            self.x -= fwd_x  * speed
            self.z -= fwd_z  * speed
        if keys[K_a]:
            self.x -= right_x * speed
            self.z -= right_z * speed
        if keys[K_d]:
            self.x += right_x * speed
            self.z += right_z * speed
        if keys[K_q]: self.y += speed
        if keys[K_e]: self.y -= speed

        if keys[K_LEFT]:  self.angle_y -= rot_sp
        if keys[K_RIGHT]: self.angle_y += rot_sp
        if keys[K_UP]:
            self.angle_x = min(89.0, self.angle_x + rot_sp * 0.7)
        if keys[K_DOWN]:
            self.angle_x = max(-89.0, self.angle_x - rot_sp * 0.7)

    # ----------------------------------------------------------------
    def apply(self):
        """Panggil setelah glLoadIdentity() untuk menempatkan kamera."""
        ry = math.radians(self.angle_y)
        rx = math.radians(self.angle_x)
        lx =  math.sin(ry) * math.cos(rx)
        ly =  math.sin(rx)
        lz = -math.cos(ry) * math.cos(rx)
        gluLookAt(
            self.x, self.y, self.z,
            self.x + lx, self.y + ly, self.z + lz,
            0, 1, 0,
        )
