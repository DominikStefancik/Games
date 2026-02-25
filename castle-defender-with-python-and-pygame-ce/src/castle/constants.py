from enum import Enum


class CastleState(Enum):
    FULLY_RESTORED = 100
    DAMAGED = 50
    SEVERELY_DAMAGED = 25


CASTLE_STARTING_HEALTH = 1000
