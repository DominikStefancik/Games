from enum import Enum


class PlayerIconAnimation(Enum):
    IDLE = "idle"
    LEFT = "left"
    RIGHT = "right"
    UP = "up"
    DOWN = "down"


class NodePathDirection(Enum):
    LEFT = "left"
    RIGHT = "right"
    UP = "up"
    DOWN = "down"


class OverworldNodeProperty(Enum):
    STAGE = "stage"
    START = "start"
    END = "end"
    LEFT = "left"
    RIGHT = "right"
    UP = "up"
    DOWN = "down"


class OverworldPathProperty(Enum):
    POSITION_POINT = "position_point"
    START = "start"


class OverworldPathImage(Enum):
    BOTTOM_LEFT = "bl"
    BOTTOM_RIGHT = "br"
    TOP_LEFT = "tl"
    TOP_RIGHT = "tr"
    HORIZONTAL = "horizontal"
    VERTICAL = "vertical"
