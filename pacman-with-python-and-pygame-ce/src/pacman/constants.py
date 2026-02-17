from enum import Enum


COLLISION_FUDGE_FACTOR = 15
TILE_CENTER_FACTOR_MIN = 12
TILE_CENTER_FACTOR_MAX = 18


class Direction(Enum):
    LEFT = "left"
    RIGHT = "right"
    UP = "up"
    DOWN = "down"
