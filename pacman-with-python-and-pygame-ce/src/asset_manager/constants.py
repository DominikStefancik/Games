from enum import Enum


class ImageAsset(Enum):
    PACMAN = "pacman"
    BLINKY_GHOST = "blinky_ghost"
    PINKY_GHOST = "pinky_ghost"
    INKY_GHOST = "inky_ghost"
    CLYDE_GHOST = "clyde_ghost"
    SPOOKED_GHOST = "spooked_ghost"
    DEAD_GHOST = "dead_ghost"


class FontAsset(Enum):
    FREE_SANS_BOLD_20 = "freesansbold_20"
    FREE_SANS_BOLD_35 = "freesansbold_35"


class AudioAsset(Enum):
    SOUND = "sound"
