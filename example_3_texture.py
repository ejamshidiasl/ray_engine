from pyray import *
from ray_engine import *


def node1_update(node: Node, dt: float):
    if is_key_down(KeyboardKey.KEY_Q):
        node.do_scale(1.05, 1.05)
    elif is_key_down(KeyboardKey.KEY_W):
        node.do_scale(0.95, 0.95)

    if is_key_down(KeyboardKey.KEY_E):
        node.do_rotate(1)


def node2_update(node: Node, dt: float):
    if is_key_down(KeyboardKey.KEY_A):
        node.do_scale(1.05, 1.05)
    elif is_key_down(KeyboardKey.KEY_S):
        node.do_scale(0.95, 0.95)

    if is_key_down(KeyboardKey.KEY_D):
        node.do_rotate(1)


init_window(600, 600, "ray_engine test")
set_target_fps(60)

scene = Scene()

texture1 = load_texture("ray_engine.jpg")

node1 = Node(
    draw_fn=DrawFuncs.draw_texture,
    update_fn=node1_update,
    pos=Vector2(300, 300),
    texture=texture1,
    size=Vector2(256, 256)
)

node2 = Node(
    draw_fn=DrawFuncs.draw_texture,
    update_fn=node2_update,
    pos=Vector2(64, 64),
    texture=texture1,
    size=Vector2(128, 128),
    color=RED
)
node1.add_child(node2)
scene.add_node(node1)

while not window_should_close():
    scene.update(get_frame_time())

    begin_drawing()
    clear_background(RAYWHITE)

    scene.draw()

    draw_text("Hold Q,W: scale parent", 10, 10, 20, BLACK)
    draw_text("Hold E: rotate parent", 10, 30, 20, BLACK)
    draw_text("Hold A,S: scale child", 10, 50, 20, BLACK)
    draw_text("Hold D: rotate child", 10, 70, 20, BLACK)

    end_drawing()

close_window()
