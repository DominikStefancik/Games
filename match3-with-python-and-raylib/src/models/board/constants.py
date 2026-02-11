from enum import Enum

from settings import Vector2

BOARD_SIZE = 10
BOARD_OFFSET = Vector2(-20, -10)
TILE_SIZE = 5
TILE_TYPES_COUNT = 7


class Match(Enum):
    HORIZONTAL = "horizontal"
    VERTICAL = "vertical"
