from enum import Enum


class OverworldLayer(Enum):
    MAIN = "main"
    TOP = "top"
    OBJECTS = "Objects"
    NODES = "Nodes"
    PATHS = "Paths"


class OverworldObjectName(Enum):
    PALM = "palm"
    GRASS = "grass"


OVERWORLD_NODE_NAME = "Node"


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
