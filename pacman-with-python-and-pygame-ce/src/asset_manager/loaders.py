from os.path import join

from settings import pygame

from .constants import AudioAsset, FontAsset, ImageAsset
from .import_helpers import import_folder_as_list


def load_graphics():
    return {
        ImageAsset.PACMAN: import_folder_as_list("assets", "images", "pacman"),
        ImageAsset.BLINKY_GHOST: pygame.image.load(
            join("assets", "images", "ghosts", "red.png")
        ).convert_alpha(),
        ImageAsset.PINKY_GHOST: pygame.image.load(
            join("assets", "images", "ghosts", "pink.png")
        ).convert_alpha(),
        ImageAsset.INKY_GHOST: pygame.image.load(
            join("assets", "images", "ghosts", "blue.png")
        ).convert_alpha(),
        ImageAsset.CLYDE_GHOST: pygame.image.load(
            join("assets", "images", "ghosts", "orange.png")
        ).convert_alpha(),
        ImageAsset.SPOOKED_GHOST: pygame.image.load(
            join("assets", "images", "ghosts", "powerup.png")
        ).convert_alpha(),
        ImageAsset.DEAD_GHOST: pygame.image.load(
            join("assets", "images", "ghosts", "dead.png")
        ).convert_alpha(),
    }


def load_fonts():
    return {
        FontAsset.FREE_SANS_BOLD_20: pygame.font.Font("freesansbold.ttf", 20),
        FontAsset.FREE_SANS_BOLD_35: pygame.font.Font("freesansbold.ttf", 35),
    }


def load_audio():
    return {
        AudioAsset.SOUND: pygame.mixer.Sound(join("assets", "audio", "sound.wav")),
    }
