from os.path import join

from settings import pygame

from .constants import AudioAsset, FontAsset, ImageAssetGroup
from .import_helpers import import_folder_as_dict


def load_graphics():
    return {
        ImageAssetGroup.BACKGROUND: pygame.image.load(
            join("assets", "images", "background.png")
        ).convert_alpha(),
        ImageAssetGroup.CASTLE: import_folder_as_dict(
            join("assets", "images", "castle")
        ),
        ImageAssetGroup.BULLET: pygame.image.load(
            join("assets", "images", "bullet.png")
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
