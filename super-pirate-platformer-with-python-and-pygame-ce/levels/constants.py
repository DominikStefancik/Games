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
    SPIKED_BALL = "spiked_ball"
    SPIKED_CHAIN = "spiked_chain"
    TOOTH = "tooth"
    SHELL = "shell"
    PEARL = "pearl"
    PALM_BACKGROUND = "palm_bg"
    PALM_BACKGROUND_LEFT = "palm_bg_left"
    PALM_BACKGROUND_RIGHT = "palm_bg_right"
    PALM_LEFT = "palm_left"
    PALM_RIGHT = "palm_right"
    PALM_SMALL = "palm_small"
    PALM_LARGE = "palm_large"
    ITEMS = "items"
    PARTICLE = "particle"
    HEART = "heart"
    COIN = "coin"
