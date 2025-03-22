# Main Developer: Esmail Jamshidiasl (call me NNE)
# Github: https://github.com/ejamshidiasl/ray_engine
# License: MIT


from pyray import *
import math
import json
import uuid


class Node:
    def __init__(self, draw_fn=None, update_fn=None, texture=None, pos=None, rot=0, scale=None, origin=None, size=None, to=None, tickness=1, color=None, name="New Node", tag="", order=0):
        self.uuid = str(uuid.uuid4())
        self.name = name
        self.tag = tag

        self.draw_fn = draw_fn
        self.update_fn = update_fn

        self.pos = pos if pos else Vector2(0, 0)
        self.rot = rot
        self.scale = scale if scale else Vector2(1, 1)
        self.origin = origin if origin else Vector2(0.5, 0.5)
        self.size = size if size else Vector2(100, 50)
        self.color = color if color else Color(255, 255, 255, 255)
        self.to = to if to else Vector2(0, 0)
        self.tickness = tickness
        self.texture = texture

        self.global_pos = Vector2(self.pos.x, self.pos.y)
        self.global_rot = self.rot
        self.global_scale = Vector2(self.scale.x, self.scale.y)

        self.visible = True
        self.enabled = True
        self.order = order

        self.parent = None
        self.children = []

    def add_child(self, child):
        """Add a child node."""
        child.parent = self
        self.children.append(child)

    def remove_child(self, child):
        """Remove a child node."""
        child.parent = None
        self.children.remove(child)

    def _update_global_transform(self):
        """DO NOT CALL THIS FUNCTION. FOR-DEVS: Update and store global pos, rot, and scale."""

        if self.parent is None:
            self.global_pos = Vector2(self.pos.x, self.pos.y)
            self.global_rot = self.rot
            self.global_scale = Vector2(self.scale.x, self.scale.y)
        else:
            p_pos = self.parent.global_pos
            p_rot = self.parent.global_rot
            p_scale = self.parent.global_scale

            adjusted_pos = Vector2(
                self.pos.x - self.origin.x * self.size.x * self.scale.x,
                self.pos.y - self.origin.y * self.size.y * self.scale.y
            )

            sin_rot = math.sin(math.radians(p_rot))
            cos_rot = math.cos(math.radians(p_rot))
            x = adjusted_pos.x * p_scale.x
            y = adjusted_pos.y * p_scale.y
            rotated_x = cos_rot * x - sin_rot * y
            rotated_y = sin_rot * x + cos_rot * y

            self.global_pos = Vector2(p_pos.x + rotated_x, p_pos.y + rotated_y)

            self.global_rot = p_rot + self.rot

            self.global_scale = Vector2(
                p_scale.x * self.scale.x, p_scale.y * self.scale.y
            )

    def update(self, delta_time):
        """Execute the user-defined update function."""
        if not self.enabled:
            return

        if self.update_fn:
            self.update_fn(self, delta_time)

        # Update children recursively
        for child in self.children:
            child.update(delta_time)

    def draw(self):
        """Render the node and its children. just call for parent nodes."""
        if not self.enabled:
            return

        self._update_global_transform()

        # Call the draw function
        if self.visible and self.draw_fn:
            self.draw_fn(self)

        # Recursively draw children
        for child in self.children:
            child.draw()

    def do_move(self, dx, dy):
        """Move the node by (dx, dy)."""
        self.pos.x += dx
        self.pos.y += dy

    def do_rotate(self, delta_angle):
        """Rotate the node by delta_angle (in degrees)."""
        self.rot += delta_angle

    def do_scale(self, sx, sy):
        """Scale the node by factors (sx, sy)."""
        self.scale.x *= sx
        self.scale.y *= sy

    def do_look_at(self, target_pos: Vector2, rot_speed: float):
        """Rotate the node to face a specific position."""
        direction = self.get_direction_to(target_pos)
        target_angle = math.degrees(math.atan2(direction.y, direction.x))
        angle_difference = target_angle - self.rot

        # Normalize the angle difference to the range (-180, 180)
        if angle_difference > 180:
            angle_difference -= 360
        elif angle_difference < -180:
            angle_difference += 360

        # Apply rotation speed
        if abs(angle_difference) < rot_speed:
            # Snap to target if within rotation speed range
            self.rot = target_angle
        else:
            # Rotate towards the target angle at fixed speed
            self.rot += rot_speed if angle_difference > 0 else -rot_speed

    def do_move_to(self, target_pos: Vector2, speed: float):
        """Gradually move the node towards a target position at a given speed."""
        direction = self.get_direction_to(target_pos)

        # Calculate the distance to the target
        distance = self.get_distance_to(target_pos)

        # Normalize the direction vector
        if distance > 0:
            direction.x /= distance
            direction.y /= distance

        # Move the node towards the target at the specified speed
        move_x = direction.x * speed
        move_y = direction.y * speed

        # If the distance is less than the speed, snap to the target
        if distance < speed:
            self.pos = Vector2(target_pos.x, target_pos.y)
        else:
            self.pos.x += move_x
            self.pos.y += move_y

    def do_move_forward(self, speed: float):
        """Move the node forward in the direction of its rotation."""
        # Calculate the direction based on the current rotation
        radian_angle = math.radians(self.rot)
        forward_x = math.cos(radian_angle) * speed
        forward_y = math.sin(radian_angle) * speed

        # Update the node's position
        self.pos.x += forward_x
        self.pos.y += forward_y

    def get_direction_to(self, target_pos: Vector2):
        return Vector2(
            target_pos.x - self.global_pos.x,
            target_pos.y - self.global_pos.y
        )

    def get_distance_to(self, target_pos: Vector2) -> float:
        """Calculate the distance from this node to a target position."""
        dx = target_pos.x - self.global_pos.x
        dy = target_pos.y - self.global_pos.y
        return math.sqrt(dx**2 + dy**2)


class Scene:
    def __init__(self):
        self.nodes = []
        self.draw_fn_registry = {}

        self._register_draw_fn("draw_rectangle", DrawFuncs.draw_rectangle)
        self._register_draw_fn("draw_circle", DrawFuncs.draw_circle)

    def add_node(self, node: Node):
        """Add a node to the scene."""
        self.nodes.append(node)

    def remove_node(self, node: Node):
        """Remove a node from the scene."""
        if node in self.nodes:
            self.nodes.remove(node)

    def draw(self):
        """Draw all nodes in the scene."""
        sorted_nodes = sorted(self.nodes, key=lambda n: n.order)
        for node in sorted_nodes:
            node.draw()

    def update(self, delta_time):
        """Update all nodes in the scene."""
        for node in self.nodes:
            node.update(delta_time)

    def get_nodes_by_name(self, name: str):
        """Find all nodes with a given name."""
        return [node for node in self.nodes if node.name == name]

    def get_nodes_by_tag(self, tag: str):
        """Find all nodes with a specific tag."""
        return [node for node in self.nodes if node.tag == tag]

    def _register_draw_fn(self, name: str, fn):
        """Register a draw function by name."""
        self.draw_fn_registry[name] = fn

    def _get_draw_fn(self, name: str):
        """Get a draw function by name."""
        return self.draw_fn_registry.get(name, None)

    def save_to_file(self, filename: str):
        """Save the scene to a JSON file."""
        with open(filename, 'w') as file:
            # Save every node in the scene, including children
            all_nodes = self._get_all_nodes()
            data = [self._node_to_dict(node) for node in all_nodes]
            json.dump(data, file, indent=4)

    def load_from_file(self, filename: str):
        """Load the scene from a JSON file."""
        with open(filename, 'r') as file:
            data = json.load(file)

            # Create nodes but don't set relationships yet
            uuid_to_node = {node_data["uuid"]: self._dict_to_node(
                node_data) for node_data in data}
            self.nodes = list(uuid_to_node.values())

            # Reconstruct parent-child relationships
            for node_data in data:
                node = uuid_to_node[node_data["uuid"]]
                parent_uuid = node_data.get("parent")
                if parent_uuid:
                    parent_node = uuid_to_node[parent_uuid]
                    parent_node.add_child(node)

    def _get_all_nodes(self):
        """Retrieve all nodes in the scene, including children."""
        all_nodes = []

        # Traverse each node in the scene's node list
        for node in self.nodes:
            self._collect_nodes(node, all_nodes)

        return all_nodes

    def _collect_nodes(self, node: Node, all_nodes: list):
        """Recursively collect all nodes starting from the given node."""
        if node not in all_nodes:
            all_nodes.append(node)
        for child in node.children:
            self._collect_nodes(child, all_nodes)

    def _node_to_dict(self, node: Node) -> dict:
        """Convert a Node to a dictionary for serialization."""
        color = node.color
        if isinstance(color, tuple):
            color_data = {"r": color[0], "g": color[1],
                          "b": color[2], "a": color[3]}
        else:
            color_data = {"r": color.r, "g": color.g,
                          "b": color.b, "a": color.a}

        return {
            "uuid": node.uuid,
            "name": node.name,
            "tag": node.tag,
            "pos": {"x": node.pos.x, "y": node.pos.y},
            "rot": node.rot,
            "scale": {"x": node.scale.x, "y": node.scale.y},
            "size": {"x": node.size.x, "y": node.size.y},
            "color": color_data,
            "visible": node.visible,
            "enabled": node.enabled,
            "order": node.order,
            "draw_fn": node.draw_fn.__name__ if node.draw_fn else None,
            "update_fn": node.update_fn.__name__ if node.update_fn else None,
            "parent": node.parent.uuid if node.parent else None,
            "children": [child.uuid for child in node.children]
        }

    def _dict_to_node(self, data: dict) -> Node:
        """Convert a dictionary back to a Node object."""
        draw_fn = self._get_draw_fn(
            data["draw_fn"]) if data["draw_fn"] else None
        update_fn = self.get_update_fn(
            data["update_fn"]) if data["update_fn"] else None

        # Create the node
        node = Node(
            draw_fn=draw_fn,
            update_fn=update_fn,
            pos=Vector2(data["pos"]["x"], data["pos"]["y"]),
            rot=data["rot"],
            scale=Vector2(data["scale"]["x"], data["scale"]["y"]),
            size=Vector2(data["size"]["x"], data["size"]["y"]),
            color=Color(data["color"]["r"], data["color"]["g"],
                        data["color"]["b"], data["color"]["a"]),
            name=data["name"],
            tag=data["tag"],
            order=data["order"]
        )

        # Temporarily assign UUID (parent and children will resolve later)
        node.uuid = data["uuid"]
        return node


class DrawFuncs:
    @staticmethod
    def draw_rectangle(node: Node):
        """Draw a rectangle using the Node object."""
        draw_rectangle_pro(
            Rectangle(
                node.global_pos.x,
                node.global_pos.y,
                node.size.x * node.global_scale.x,
                node.size.y * node.global_scale.y
            ),
            Vector2(
                node.origin.x * node.size.x * node.global_scale.x,
                node.origin.y * node.size.y * node.global_scale.y
            ),
            node.global_rot,
            node.color
        )

    @staticmethod
    def draw_circle(node: Node):
        """Draw a circle using the Node object."""
        radius = (node.size.x / 2) * node.global_scale.x
        draw_circle(
            int(node.global_pos.x),
            int(node.global_pos.y),
            int(radius),
            node.color
        )

    @staticmethod
    def draw_line(node: Node):
        """Draw a line using the Node object."""
        draw_line_ex(
            node.global_pos,
            node.to,
            node.tickness,
            node.color
        )

    @staticmethod
    def draw_texture(node: Node):
        """Draw a texture using the Node object."""
        pos = node.global_pos
        if node.texture:
            draw_texture_pro(
                node.texture,
                Rectangle(
                    0,
                    0,
                    node.texture.width,
                    node.texture.height,
                ),
                Rectangle(
                    pos.x,
                    pos.y,
                    node.size.x * node.global_scale.x,
                    node.size.y * node.global_scale.y
                ),
                Vector2(
                    node.origin.x * node.size.x * node.global_scale.x,
                    node.origin.y * node.size.y * node.global_scale.y
                ),
                node.global_rot,
                node.color
            )
