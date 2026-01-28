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


class LevelObject(Enum):
    PLAYER = "player"
    HELICOPTER = "helicopter"
    BARREL = "barrel"
    CRATE = "crate"
    PALM = "palm"
    SPIKE = "spike"
    SAW = "saw"


class LevelObjectProperty(Enum):
    PLATFORM = "platform"
    FLIP = "flip"


class LevelObjectAssetGroup(Enum):
    FLAG = "flag"
    SAW = "saw"
    SAW_CHAIN = "saw_chain"
    FLOOR_SPIKE = "floor_spike"
    PALM = "palm"
    CANDLE = "candle"
    WINDOW = "window"
    BIG_CHAIN = "big_chain"
    SMALL_CHAIN = "small_chain"
    CANDLE_LIGHT = "candle_light"
    PLAYER = "player"
    HELICOPTER = "helicopter"
    BOAT = "boat"
