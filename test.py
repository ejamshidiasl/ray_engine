from pyray import *
from ray_engine import *


def node1_update(node: Node, dt: float):
    if is_key_pressed(KeyboardKey.KEY_S):
        scene.add_tween(node, "size.x", 200, 0.758985, on_done)


def on_done(node: Node):
    print("done")
    
init_window(600, 600, "ray_engine test")
set_target_fps(60)

scene = Scene()

node1 = Node(
    draw_fn=DrawFuncs.draw_circle,
    update_fn=node1_update,
    pos=Vector2(300, 300),
    size=Vector2(100, 100),
    color=RED
)

scene.add_node(node1)

while not window_should_close():
    scene.update(get_frame_time())

    begin_drawing()
    clear_background(RAYWHITE)

    scene.draw()

    end_drawing()

close_window()
