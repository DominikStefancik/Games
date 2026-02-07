from os.path import join
from random import choice, uniform

from settings import (
    draw_cylinder,
    ffi,
    gen_mesh_sphere,
    get_shader_location,
    load_model_from_mesh,
    load_shader,
    MATERIAL_MAP_ALBEDO,
    matrix_rotate_xyz,
    set_material_texture,
    set_shader_value,
    SHADER_UNIFORM_VEC2,
    Vector3,
)
from timer import Timer

from .constants import (
    ASTEROID_DESTRUCTION_TIMER_DURATION,
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
        self.is_hit = False
        self.destruction_timer = Timer(
            duration=ASTEROID_DESTRUCTION_TIMER_DURATION,
            repeat=False,
            autostart=False,
            function=self.destroy,
        )

        # We have to load the shader separately in every instance of the Asteroid class.
        # If we loaded it in the AssetManager and then updated it, it would updated all shaders
        # in all asteroids and it would flash all the meteors at once, which we don't want.
        # We want the shader of each asteroid to be updated independently.
        self.shader = load_shader(ffi.NULL, join("assets", "shaders", "flash.fs"))
        self.flash_location = get_shader_location(self.shader, "flash")
        self.flash_amount = ffi.new("struct Vector2 *", [1, 0])
        model.materials[0].shader = self.shader

    def update(self, delta_time):
        self.destruction_timer.update()

        # If an asteroid is hit, stop moving it and apply flash effect
        if self.is_hit:
            self.flash()
        else:
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

    def destroy(self):
        self.to_be_removed = True

    def flash(self):
        set_shader_value(
            self.shader, self.flash_location, self.flash_amount, SHADER_UNIFORM_VEC2
        )
