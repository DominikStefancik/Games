from os.path import join
from enum import Enum

# Map data paths
OMNI_PATH = join("assets", "map_data", "levels", "omni.tmx")


class LevelLayer(Enum):
    BACKGROUND = "BG"
    FOREGROUND = "FG"
    OBJECTS = "Objects"
    PLATFORMS = "Platforms"
    MOVING_OBJECTS = "Moving Objects"
    TERRAIN = "Terrain"
    ENEMIES = "Enemies"
    ITEMS = "Items"
    WATER = "Water"


class LevelObject(Enum):
    PLAYER = "player"
    HELICOPTER = "helicopter"
    BARREL = "barrel"
    CRATE = "crate"
    PALM = "palm"
    SPIKE = "spike"
    SAW = "saw"
    TOOTH = "tooth"
    SHELL = "shell"


class LevelObjectProperty(Enum):
    PLATFORM = "platform"
    FLIP = "flip"
    RADIUS = "radius"
    SPEED = "speed"
    START_ANGLE = "start_angle"
    END_ANGLE = "end_angle"
    REVERSE = "reverse"
