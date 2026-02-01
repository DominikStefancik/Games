from os.path import join
from enum import Enum

# Map data paths
OVERWORLD_MAP_PATH = join("assets", "map_data", "overworld", "overworld.tmx")


class OverworldLayer(Enum):
    MAIN = "main"
    TOP = "top"
    OBJECTS = "Objects"
    NODES = "Nodes"


class OverworldObjectName(Enum):
    PALM = "palm"
    GRASS = "grass"
    NODE = "Node"


class OverworldObjectProperty(Enum):
    STAGE = "stage"
