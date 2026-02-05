from enum import Enum


class ImageAsset(Enum):
    SPACESHIP = "spaceship"
    STAR = "star"
    LASER = "laser"
    ASTEROID = "asteroid"
    EXPLOSION = "explosion"


class FontAsset(Enum):
    STORMFAZE = "stormfaze"


class SoundAsset(Enum):
    LASER = "laser"
    ASTEROID_EXPLOSION = "asteroid_explosion"
    SPACESHIP_EXPLOSION = "spaceship_explosion"
    BACKGROUND_MUSIC = "background_music"
