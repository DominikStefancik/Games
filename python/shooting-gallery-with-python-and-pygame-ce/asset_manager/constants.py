from enum import Enum


class ImageAsset(Enum):
    BACKGROUND = "background"
    TABLE = "table"
    CURTAIN_TOP = "curtain_top"
    CURTAIN_SIDE = "curtain_side"
    WATER_BACK = "water_back"
    WATER_FRONT = "water_front"
    GRASS = "grass"


class FontAsset(Enum):
    FONT = "font"


class AudioAsset(Enum):
    AUDIO = "audio"
