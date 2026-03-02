from enum import Enum


class ImageAssetGroup(Enum):
    BACKGROUND = "background"
    CASTLE = "castle"
    TOWER = "tower"
    BULLET = "bullet"
    CROSSHAIR = "crosshair"
    REPAIR_BUTTON = "repair_button"
    ARMOUR_BUTTON = "armour_button"
    KNIGHT = "knight"
    GOBLIN = "goblin"
    RED_GOBLIN = "red_goblin"
    PURPLE_GOBLIN = "purple_goblin"


class FontAsset(Enum):
    FUTURA_25 = "futura_25"
    FUTURA_35 = "futura_35"
    FUTURA_60 = "futura_60"


class AudioAsset(Enum):
    MARCH = "march"
    ATTACK = "attack"
    DEATH = "death"
