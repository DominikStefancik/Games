from os.path import join

from settings import pygame

from .constants import AudioAsset, FontAsset, ImageAssetGroup
from .import_helpers import import_folder_as_dict, import_subfolders_as_dict


def load_graphics():
    return {
        ImageAsset.IMAGE: pygame.image.load(
            join("assets", "images", "image.png")
        ).convert_alpha(),
    }


def load_fonts():
    return {
        FontAsset.FONT: pygame.font.SysFont("Font", 25),
    }


def load_sounds():
    return {
        AudioAsset.SOUND: pygame.mixer.Sound(join("assets", "sounds", "sound.wav")),
    }
