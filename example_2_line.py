from pyray import *
from ray_engine import *


def node1_to_mouse(node: Node, dt: float):
    if is_mouse_button_pressed(MouseButton.MOUSE_BUTTON_LEFT):
        node.to = get_mouse_position()

    if is_mouse_button_pressed(MouseButton.MOUSE_BUTTON_RIGHT):
        node.pos = get_mouse_position()

    if is_key_down(KeyboardKey.KEY_E):
        node.tickness += 1
    elif is_key_down(KeyboardKey.KEY_Q):
        node.tickness -= 1


init_window(600, 600, "ray_engine test")
set_target_fps(60)

scene = Scene()

node1 = Node(
    draw_fn=DrawFuncs.draw_line,
    update_fn=node1_to_mouse,
    pos=Vector2(300, 300),
    to=Vector2(400, 300),
    tickness=4
)
node2 = Node(
    draw_fn=DrawFuncs.draw_circle,
    pos=Vector2(10, 10),
    size=Vector2(20, 20),
    color=BLUE
)
node1.add_child(node2)
scene.add_node(node1)

while not window_should_close():
    scene.update(get_frame_time())

    begin_drawing()
    clear_background(RAYWHITE)

    scene.draw()

    draw_text("Hold Q,E: change line tickness", 10, 10, 20, BLACK)
    draw_text("left click: change [to] position", 10, 30, 20, BLACK)
    draw_text("right click: change [from] position", 10, 50, 20, BLACK)

    end_drawing()

close_window()
