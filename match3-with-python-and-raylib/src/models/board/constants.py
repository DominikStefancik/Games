from enum import Enum

from settings import Vector3

BOARD_SIZE = 10
BOARD_OFFSET = Vector3(-20, 0, -10)
TILE_SIZE = 5
TILE_TYPES_COUNT = 7


class Match(Enum):
    HORIZONTAL = "horizontal"
    VERTICAL = "vertical"
