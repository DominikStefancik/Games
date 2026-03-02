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
