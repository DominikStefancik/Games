from math import sin

from settings import (
    draw_cylinder,
    draw_model_ex,
    is_key_down,
    is_key_pressed,
    KEY_DOWN,
    KEY_LEFT,
    KEY_RIGHT,
    KEY_SPACE,
    KEY_UP,
    Vector3,
    Vector3Add,
    WHITE,
)

from .constants import FLOOR_VERTICAL_VALUE, SHADOW_COLOR

from .constants import SPACESHIP_SPEED
from .model import Model


class Spaceship(Model):
    def __init__(self, group, model, create_laser_function):
        super().__init__(group, model, Vector3(), SPACESHIP_SPEED)
        self.create_laser = create_laser_function
        self.rotation_angle = 0

    def process_key_input(self):
        self.direction.x = int(is_key_down(KEY_RIGHT)) - int(is_key_down(KEY_LEFT))
        self.direction.z = int(is_key_down(KEY_DOWN)) - int(is_key_down(KEY_UP))

        if is_key_pressed(KEY_SPACE):
            self.create_laser(Vector3Add(self.position, Vector3(0, 0.25, -1)))

    def constraint_movement(self):
        self.position.x = max(-6, min(self.position.x, 10))
        self.position.z = max(-8, min(self.position.z, 2))
        self.rotation_angle = max(-17, min(self.rotation_angle, 17))

    def update(self, delta_time):
        self.process_key_input()
        self.position.y += sin(delta_time * 10) * delta_time * 0.2
        self.rotation_angle -= self.direction.x * 10 * delta_time
        self.constraint_movement()
        self.move(delta_time)

    def draw(self):
        # We want to rotate around Z-axis
        draw_model_ex(
            self.model,
            self.position,
            Vector3(0, 0, 1),
            self.rotation_angle,
            Vector3(1, 1, 1),
            WHITE,
        )
        self.draw_shadow()

    def draw_shadow(self):
        shadow_radius = 0.5 + self.position.y
        # Position the shadow above the floor (Y-coordinate) and follow the spaceship's
        # position (X and Z coordinates)
        draw_cylinder(
            Vector3(self.position.x, FLOOR_VERTICAL_VALUE + 0.5, self.position.z),
            shadow_radius,
            shadow_radius,
            0.1,
            20,
            SHADOW_COLOR,
        )
