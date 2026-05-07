"""
core/state.py
-------------
Menyimpan semua variabel animasi global yang dipakai bersama
antar objek. Di-update sekali per frame oleh main loop.
"""

import math


class AnimationState:
    """Satu-satunya sumber kebenaran untuk waktu & sudut animasi."""

    def __init__(self):
        self.time          = 0.0    # detik akumulasi
        self.fountain_angle = 0.0   # derajat, 0-360
        self.bird_angle    = 0.0    # derajat, buat angsa / burung
        self.wind_phase    = 0.0    # fase angin (0-2π)

    def update(self, dt: float):
        self.time           += dt
        self.fountain_angle  = (self.fountain_angle + 120.0 * dt) % 360.0
        self.bird_angle      = (self.bird_angle     +  30.0 * dt) % 360.0
        self.wind_phase      = (self.wind_phase     +   1.2 * dt) % (2 * math.pi)
