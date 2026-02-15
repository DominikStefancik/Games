from os.path import join

from settings import pygame

from .constants import AudioAsset, ImageAsset
from .import_helpers import import_folder_as_list


def load_graphics():
    return {
        ImageAsset.PACMAN: import_folder_as_list("assets", "images", "pacman"),
    }


def load_font():
    return pygame.font.Font("freesansbold.ttf", 20)


def load_audio():
    return {
        AudioAsset.SOUND: pygame.mixer.Sound(join("assets", "audio", "sound.wav")),
    }
