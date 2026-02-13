from enum import Enum

from settings import Vector3

BOARD_SIZE = 10
BOARD_OFFSET = Vector3(-20, 0, -10)
TILE_SIZE = 5
TILE_TYPES_COUNT = 7
TILE_FALL_SPEED = 0.25


class Match(Enum):
    HORIZONTAL = "horizontal"
    VERTICAL = "vertical"


class BoardState(Enum):
    IDLE = "idle"
    UPDATING = "updating"
