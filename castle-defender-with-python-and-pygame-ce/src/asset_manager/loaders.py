from os.path import join

from settings import pygame

from .constants import AudioAsset, FontAsset, ImageAsset
from .import_helpers import import_folder_as_list


def load_graphics():
    return {
        ImageAsset.IMAGE: pygame.image.load(
            join("assets", "images", "image.png")
        ).convert_alpha(),
    }


def load_fonts():
    return {
        FontAsset.FONT: pygame.font.Font("font.ttf", 35),
    }


def load_sounds():
    return {
        AudioAsset.SOUND: pygame.mixer.Sound(join("assets", "sounds", "sound.wav")),
    }
