from random import choice, uniform

from settings import (
    draw_cylinder,
    gen_mesh_sphere,
    load_model_from_mesh,
    MATERIAL_MAP_ALBEDO,
    matrix_rotate_xyz,
    set_material_texture,
    Vector3,
)

from .constants import (
    ASTEROID_MOVEMENT_SPEED_RANGE,
    ASTEROID_ROTATION_RANGE,
    ASTEROID_ROTATION_SPEED_RANGE,
    ASTEROID_SPHERE_RADIUS_RANGE,
    FLOOR_VERTICAL_VALUE,
    SHADOW_COLOR,
)
from .model import Model


class Asteroid(Model):
    def __init__(self, group, texture):
        position = Vector3(uniform(-6, 7), 0, uniform(-40, -20))
        speed = uniform(*ASTEROID_MOVEMENT_SPEED_RANGE)
        direction = Vector3(uniform(-0.5, 0.5), 0, uniform(0.75, 1.25))
        self.radius = uniform(*ASTEROID_SPHERE_RADIUS_RANGE)
        model = load_model_from_mesh(gen_mesh_sphere(self.radius, 8, 8))
        set_material_texture(model.materials[0], MATERIAL_MAP_ALBEDO, texture)

        super().__init__(group, model, position, speed, direction)
        self.rotation = Vector3(
            uniform(*ASTEROID_ROTATION_RANGE),
            uniform(*ASTEROID_ROTATION_RANGE),
            uniform(*ASTEROID_ROTATION_RANGE),
        )
        self.rotation_speed = Vector3(
            uniform(*ASTEROID_ROTATION_SPEED_RANGE),
            uniform(*ASTEROID_ROTATION_SPEED_RANGE),
            uniform(*ASTEROID_ROTATION_SPEED_RANGE),
        )

    def update(self, delta_time):
        super().update(delta_time)
        self.rotation.x += self.rotation_speed.x * delta_time
        self.rotation.y += self.rotation_speed.y * delta_time
        self.rotation.z += self.rotation_speed.z * delta_time
        self.model.transform = matrix_rotate_xyz(self.rotation)

    def draw(self):
        super().draw()
        self.draw_shadow()

    def draw_shadow(self):
        # Position the shadow above the floor (Y-coordinate) and follow the asteroid's
        # position (X and Z coordinates)
        draw_cylinder(
            Vector3(self.position.x, FLOOR_VERTICAL_VALUE + 0.5, self.position.z),
            self.radius * 0.8,
            self.radius * 0.8,
            0.1,
            20,
            SHADOW_COLOR,
        )
