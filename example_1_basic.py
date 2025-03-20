# Main Developer: Esmail Jamshidiasl (NNE)
# Github: https://github.com/ejamshidiasl/ray_engine
# License: MIT


from ray_engine import *
from pyray import *


# Define the update function for moving and rotating the parent node (blue)
def move_with_wasd(node: Node, dt: float):
    speed = 200 * dt  # Movement speed (200 units per second)

    # Move
    if is_key_down(KeyboardKey.KEY_W):
        node.pos.y -= speed
    if is_key_down(KeyboardKey.KEY_S):
        node.pos.y += speed
    if is_key_down(KeyboardKey.KEY_A):
        node.pos.x -= speed
    if is_key_down(KeyboardKey.KEY_D):
        node.pos.x += speed

    # Rotate
    if is_key_down(KeyboardKey.KEY_E):
        node.do_rotate(250 * dt)  # Or node.rot += speed
    if is_key_down(KeyboardKey.KEY_Q):
        node.do_rotate(-250 * dt)


# Initialize the scene
scene = Scene()

# Create the blue node (parent)
blue = Node(
    draw_fn=DrawFuncs.draw_rectangle,
    update_fn=move_with_wasd,  # Assign the update function
    pos=Vector2(300, 300),
    size=Vector2(100, 100),
    color=Color(0, 0, 255, 255),
    name="Blue"
)

# Create the red node (child of blue)
red = Node(
    draw_fn=DrawFuncs.draw_rectangle,
    pos=Vector2(100, 50),  # Relative position to blue
    size=Vector2(50, 50),
    color=Color(255, 0, 0, 255),
    name="Red"
)

# Set red as a child of blue
blue.add_child(red)

# Add the blue node (and implicitly its child) to the scene
scene.add_node(blue)

# Main game loop
init_window(800, 600, "Ray Engine Example")
set_target_fps(60)

while not window_should_close():
    dt = get_frame_time()

    # Update the scene
    scene.update(dt)

    begin_drawing()
    clear_background(RAYWHITE)

    # Render the scene
    scene.draw()

    end_drawing()

close_window()
