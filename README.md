📢Converting the code to `C & C++` is ongoing.
<br>
⚡The engine is progressing at a high pace with great energy
<br>
ℹ️ current version: `1.0`

# ray_engine
ray_engine is a fresh, innovative graphics library designed to be the **easiest**, **most enjoyable**, and **highly performant** tool for developers. Whether you're a game developer, software designer, or machine learning enthusiast, ray_engine offers versatility and power to bring your ideas to life effortlessly.

## Key Features
- **Node-Based Architecture**:
    - Manage hierarchical node relationships with ease (parent-child structure).
    - Transform properties such as position, rotation, scale, and origin.

- **Scene Management**:
    - Support for dynamic scene updates and rendering.
    - Serialize and deserialize scenes seamlessly via JSON.

- **Custom Updates and Drawing**:
    - Assign user-defined update_fn for dynamic behaviors.
    - Built-in support for custom drawing functions (draw_rectangle, draw_circle).

- **Smooth Node Movement**:
    - Functions for forward movement, look-at behavior, and position transitions.

- **Extensibility**:
    - Easily register new draw or update functions.

## Getting Started & Installation
First install raylib using `pip install raylib` then
clone the repository and include `ray_engine.py` file in your project.

## Dependencies
- **To use in Python**:
  - "raylib" library `pip install raylib`
  - python's standard libraries "math,json,uuid" (*no need to install*)
- **To use in C,C++ and other Languages**:
  - TODO

## Example
```python
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
        node.do_rotate(250 * dt) # Or node.rot += speed
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
    # Update the scene
    scene.update(get_frame_time())

    begin_drawing()
    clear_background(RAYWHITE)

    # Render the scene
    scene.draw()

    end_drawing()

close_window()
```

## Functions & Usage
TODO

## Custom Draw Functions
Currently, in version `1.0`, we only have two drawing functions: one for rectangles and one for circles. More functions will be added soon. Meanwhile, you can create custom functions as follows:
```python
def custom_draw(node: Node):
    draw_rectangle_pro(
        Rectangle(
            node.global_pos.x,
            node.global_pos.y,
            node.size.x *
            node.global_scale.x,
            node.size.y * node.global_scale.y
        ),
        Vector2(
            node.origin.x * node.size.x * node.global_scale.x,
            node.origin.y * node.size.y * node.global_scale.y
        ),
        node.global_rot,
        node.color
    )

    # We can add additional functions as well. For example:
    # Draw a line from node position to (0,0)
    draw_line(
        node.global_pos.x,
        node.global_pos.y,
        0,
        0,
        GREEN
    )

# Then:
my_node.draw_fn = custom_draw
```

## Contribution
ray_engine is open for contributions! If you'd like to enhance the engine, fix bugs, or add new features, feel free to submit a pull request. Please follow the guidelines in `CONTRIBUTING.md`.

## License
This project is licensed under the MIT License. See `LICENSE` for details.