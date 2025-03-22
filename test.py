from pyray import *
from ray_engine import *



init_window(600, 600, "ray_engine test")
set_target_fps(60)

scene = Scene()

while not window_should_close():
    scene.update(get_frame_time())

    begin_drawing()
    clear_background(RAYWHITE)

    scene.draw()

    end_drawing()

close_window()
