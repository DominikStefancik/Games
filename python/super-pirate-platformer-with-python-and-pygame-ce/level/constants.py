from enum import Enum


class LevelLayer(Enum):
    BACKGROUND = "BG"
    BACKGROUND_DETAILS = "BG details"
    FOREGROUND = "FG"
    OBJECTS = "Objects"
    PLATFORMS = "Platforms"
    MOVING_OBJECTS = "Moving Objects"
    TERRAIN = "Terrain"
    ENEMIES = "Enemies"
    ITEMS = "Items"
    WATER = "Water"
    DATA = "Data"


class LevelObjectName(Enum):
    PLAYER = "player"
    HELICOPTER = "helicopter"
    FLOOR_SPIKE = "floor_spike"
    BARREL = "barrel"
    CRATE = "crate"
    PALM = "palm"
    SPIKE = "spike"
    SAW = "saw"
    TOOTH = "tooth"
    SHELL = "shell"
    FLAG = "flag"
    PALM_LEFT = "palm_left"
    PALM_RIGHT = "palm_right"
    PALM_SMALL = "palm_small"
    PALM_LARGE = "palm_large"
    STATIC = "static"


class LevelObjectProperty(Enum):
    PLATFORM = "platform"
    FLIP = "flip"
    RADIUS = "radius"
    SPEED = "speed"
    START_ANGLE = "start_angle"
    END_ANGLE = "end_angle"
    REVERSE = "reverse"
    INVERTED = "inverted"


class LevelDataProperty(Enum):
    BACKGROUND = "bg"
    TOP_LIMIT = "top_limit"
    HORIZON_LINE = "horizon_line"
    LEVEL_UNLOCK = "level_unlock"
