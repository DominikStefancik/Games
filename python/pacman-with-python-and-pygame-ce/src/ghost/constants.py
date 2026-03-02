from enum import Enum


class GhostType(Enum):
    BLINKY = "blinky"
    PINKY = "pinky"
    INKY = "inky"
    CLYDE = "clyde"


class GhostImageType(Enum):
    MAIN = "main"
    SPOOKED = "spooked"
    DEAD = "dead"
