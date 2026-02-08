from random import choice, randint, uniform

from settings import draw_texture_pro, Rectangle, Vector2, WHITE, WINDOW_WIDTH

from .constants import ASTEROID_MOVEMENT_SPEED_RANGE, ASTEROID_ROTATION_SPEED_RANGE
from .sprite import Sprite


class Asteroid(Sprite):
    def __init__(self, group, texture):
        position = Vector2(randint(0, WINDOW_WIDTH), randint(-150, -50))
        speed = randint(*ASTEROID_MOVEMENT_SPEED_RANGE)
        direction = Vector2(uniform(-0.5, 0.5), 1)

        super().__init__(group, texture, position, speed, direction)
        self.rotation = 0
        self.rotation_direction = choice([-1, 1])
        self.rotation_speed = randint(*ASTEROID_ROTATION_SPEED_RANGE)
        self.rectangle = Rectangle(0, 0, self.size.x, self.size.y)

    def get_center(self):
        return self.position

    def update(self, delta_time):
        super().update(delta_time)
        self.rotation += self.rotation_direction * self.rotation_speed * delta_time

    def draw(self):
        destination_rectangle = Rectangle(self.position.x, self.position.y, self.size.x, self.size.y)
        origin_rotation_point = Vector2(self.size.x / 2, self.size.y / 2)
        draw_texture_pro(
            self.texture,
            self.rectangle,
            destination_rectangle,
            origin_rotation_point,
            self.rotation,
            WHITE
        )
