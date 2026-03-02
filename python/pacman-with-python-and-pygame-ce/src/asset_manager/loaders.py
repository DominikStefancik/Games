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


def load_sounds():
    return {
        AudioAsset.EAT_DOT: pygame.mixer.Sound(join("assets", "sounds", "eat_dot.wav")),
        AudioAsset.EAT_BIG_DOT: pygame.mixer.Sound(
            join("assets", "sounds", "eat_big_dot.wav")
        ),
        AudioAsset.EAT_GHOST: pygame.mixer.Sound(
            join("assets", "sounds", "eat_ghost.wav")
        ),
        AudioAsset.POWER_UP: pygame.mixer.Sound(
            join("assets", "sounds", "power_up.wav")
        ),
        AudioAsset.START: pygame.mixer.Sound(join("assets", "sounds", "start.wav")),
        AudioAsset.GAME_WON: pygame.mixer.Sound(
            join("assets", "sounds", "game_won.mp3")
        ),
        AudioAsset.GAME_OVER: pygame.mixer.Sound(
            join("assets", "sounds", "game_over.wav")
        ),
    }
