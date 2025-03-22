- **Class**: `Node`
```python
def add_child(child: Node)    # add a node as child of the node
```
```python
def remove_child(child: Node)    # remove a node from the node's children
```
```python
def update(delta_time: float)    # calls update_fn. it is called automaticaly by scene 
```
```python
def draw()    # calls draw_fn. it is called automaticaly by scene 
```
```python
def do_move(dx: float, dy: float)    # trainslate node by dx,dy pixels
```
```python
def do_rotate(delta_angle: float)    # rotate node by delta_angle (in degrees)
```
```python
def do_scale(sx: float, sy: float)    # scale node by sx,sy factor
```
```python
def do_look_at(target_pos: Vector2, rot_speed: float)    # rotate node towards target_pos smoothly by rot_speed
```
```python
def do_move_to(target_pos: Vector2, speed: float)    # move node towards target_pos by speed
```
```python
def do_move_forward(speed: float)    # move node towards its facing direction (its right side)
```
```python
def get_direction_to(target_pos: Vector2)    # calculate node direction to target_pos
```
```python
def get_distance_to(target_pos: Vector2)    # calculate distance between node and target_pos
```

- **Class**: `Scene`
```python
def add_node(node: Node)    # add node to scene
```
```python
def remove_node(node: Node)    # remove node from scene
```
```python
def draw()    # draw scene and all nodes inside
```
```python
def update(delta_time: Any)    # update all nodes inside
```
```python
def get_nodes_by_name(name: str)    # filter and returns all nodes in scene with specified name
```
```python
def get_nodes_by_tag(tag: str)    # filter and returns all nodes in scene with specified tag
```
```python
def save_to_file(filename: str)    # save scene data to file
```
```python
def load_from_file(filename: str)    # load scene from file
```
```python
def add_tween(node: Node, what: str, to_val: float, step: float, on_done: None)    # add tween to node
```

- **Class**: `DrawFuncs`
```python
def draw_rectangle(node: Node)    # asign to node.draw_fn. specify node type as a rectangle
```
```python
def draw_circle(node: Node)    # asign to node.draw_fn. specify node type as a circle
```
```python
def draw_line(node: Node)    # asign to node.draw_fn. specify node type as a line
```
```python
def draw_texture(node: Node)    # asign to node.draw_fn. specify node type as a texture
```

