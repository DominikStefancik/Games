from settings import (
    is_key_down,
    is_key_pressed,
    KEY_DOWN,
    KEY_LEFT,
    KEY_RIGHT,
    KEY_SPACE,
    KEY_UP,
    Vector2,
    Vector2Normalize,
    WINDOW_HEIGHT,
    WINDOW_WIDTH,
)

from .constants import SPACESHIP_SPEED
from .sprite import Sprite


class Spaceship(Sprite):
    def __init__(self, group, texture, position, create_laser_function):
        super().__init__(group, texture, position, SPACESHIP_SPEED, Vector2())
        self.create_laser = create_laser_function

    def process_key_input(self):
        self.direction.x = int(is_key_down(KEY_RIGHT)) - int(is_key_down(KEY_LEFT))
        self.direction.y = int(is_key_down(KEY_DOWN)) - int(is_key_down(KEY_UP))
        # We have to normalise the direction to make sure that the movement speed in a diagonal direction
        # will not be greater than in a horizontal or vertical direction
        self.direction = Vector2Normalize(self.direction)

        if is_key_pressed(KEY_SPACE):
            self.create_laser(
                Vector2(self.position.x + self.size.x / 2, self.position.y - 60)
            )

    def constraint_movement(self):
        self.position.x = max(0, min(self.position.x, WINDOW_WIDTH - self.size.x))
        self.position.y = max(0, min(self.position.y, WINDOW_HEIGHT - self.size.y))

    def update(self, delta_time):
        self.process_key_input()
        self.constraint_movement()
        self.move(delta_time)
