from os.path import join
from enum import Enum

# Map data paths
OMNI_PATH = join("assets", "map_data", "levels", "omni.tmx")

class LevelLayer(Enum):
    OBJECTS = "Objects"
    TERRAIN = "Terrain"
    MOVING_OBJECTS = "Moving Objects"

class LevelObject(Enum):
    PLAYER = "player"
    HELICOPTER = "helicopter"
