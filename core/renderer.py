"""
core/renderer.py
----------------
Merangkum semua pemanggilan draw_* menjadi satu metode draw_scene().
Ini satu-satunya tempat yang 'tahu' semua objek; modul objek tidak
tahu satu sama lain.
"""

from core.state  import AnimationState
from core.layout import clear_dynamic_zones

# Environment
from environment.ground      import draw_ground, draw_all_paths
from environment.fence        import draw_fence
from environment.gate         import draw_gate
from environment.sky          import draw_skybox

# Objects
from objects.tree             import draw_all_trees
from objects.flower           import draw_all_flowers
from objects.fountain         import draw_fountain
from objects.pond             import draw_pond
from objects.gazebo           import draw_gazebo
from objects.pergola          import draw_pergola
from objects.playground       import draw_playground
from objects.toilet           import draw_toilet
from objects.bench            import draw_all_benches
from objects.lamp             import draw_all_lamps
from objects.trash_bin        import draw_all_trash
from objects.rock             import draw_all_rocks
from objects.bike_rack        import draw_bike_rack
from objects.parking          import draw_parking
from objects.person           import draw_all_people


class Renderer:
    def __init__(self, anim: AnimationState):
        self.anim = anim

    def draw_scene(self):
        a = self.anim

        # Reset zona dinamis di awal frame agar tidak menumpuk
        clear_dynamic_zones()

        # Langit (harus pertama, tanpa depth write)
        draw_skybox()

        # Tanah & jalan
        draw_ground()
        draw_all_paths()

        # Infrastruktur
        draw_fence()
        draw_gate()

        # Vegetasi
        draw_all_trees()
        draw_all_flowers()

        # Fitur air
        draw_fountain(a.fountain_angle)
        draw_pond(a.time, a.bird_angle)

        # Struktur
        draw_gazebo(14.0, 5.0)         # gazebo atap merah di sisi kanan
        draw_pergola(-13.0, 4.0)       # pergola di sisi kiri
        draw_playground(a.time)
        draw_toilet()

        # Furnitur taman
        draw_all_benches()
        draw_all_lamps()
        draw_all_trash()
        draw_all_rocks()

        # Transportasi
        draw_bike_rack()
        draw_parking()

        # Manusia
        draw_all_people(a.time)
