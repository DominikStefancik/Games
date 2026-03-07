from enum import Enum


class ImageAsset(Enum):
    BACKGROUND = "background"
    TABLE = "table"
    CURTAIN_TOP = "curtain_top"
    CURTAIN_SIDE = "curtain_side"
    WATER_BACK = "water_back"
    WATER_FRONT = "water_front"
    GRASS = "grass"
    DUCK_BROWN = "duck_brown"
    DUCK_BROWN_TARGET = "duck_brown_target"
    DUCK_YELLOW = "duck_yellow"
    DUCK_YELLOW_TARGET = "duck_yellow_target"
    STICK = "stick"
    CROSSHAIR = "crosshair"
    BULLET = "bullet"


class FontAsset(Enum):
    FONT = "font"


class AudioAsset(Enum):
    AUDIO = "audio"
