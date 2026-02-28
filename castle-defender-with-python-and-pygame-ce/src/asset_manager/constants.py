from enum import Enum


class ImageAssetGroup(Enum):
    BACKGROUND = "background"
    CASTLE = "castle"
    BULLET = "bullet"
    CROSSHAIR = "crosshair"
    KNIGHT = "knight"
    GOBLIN = "goblin"
    RED_GOBLIN = "red_goblin"
    PURPLE_GOBLIN = "purple_goblin"


class FontAsset(Enum):
    FONT = "font"


class AudioAsset(Enum):
    SOUND = "sound"
