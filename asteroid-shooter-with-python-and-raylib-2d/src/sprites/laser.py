from settings import Vector2

from .constants import LASER_SPEED
from .sprite import Sprite


class Laser(Sprite):
    def __init__(self, group, texture, position):
        # Laser will always go one direction, up vertically.
        # That's why we set "Vector2(0, -1)"
        super().__init__(group, texture, position, LASER_SPEED, Vector2(0, -1))
