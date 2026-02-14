from enum import Enum

from settings import Vector3

from ..constants import FLOOR_VERTICAL_VALUE

BOARD_SIZE = 10
BOARD_OFFSET = Vector3(25, 0, 35)
ITEM_VERTICAL_VALUE = FLOOR_VERTICAL_VALUE + 3
ITEM_SCALE = 3
OUTLINE_SCALE = ITEM_SCALE + 0.7
TILE_SIZE = 5
TILE_TYPES_COUNT = 7
TILE_FALL_SPEED = 0.07


class Match(Enum):
    HORIZONTAL = "horizontal"
    VERTICAL = "vertical"


class BoardState(Enum):
    IDLE = "idle"
    UPDATING = "updating"
