from enum import Enum


class TextureAsset(Enum):
    DARK = "dark"
    GREEN = "green"
    LIGHT = "light"
    ORANGE = "orange"
    PURPLE = "purple"
    RED = "red"


class ModelAsset(Enum):
    SPACESHIP = "spaceship"
    LASER = "laser"


class FontAsset(Enum):
    STORMFAZE = "stormfaze"


class SoundAsset(Enum):
    LASER = "laser"
    ASTEROID_EXPLOSION = "asteroid_explosion"
    SPACESHIP_EXPLOSION = "spaceship_explosion"
    BACKGROUND_MUSIC = "background_music"
