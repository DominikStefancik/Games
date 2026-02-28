from os.path import join

from settings import pygame

from .constants import AudioAsset, FontAsset, ImageAssetGroup
from .import_helpers import import_folder_as_dict, import_subfolders_as_dict


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
        ImageAssetGroup.CROSSHAIR: pygame.image.load(
            join("assets", "images", "crosshair.png")
        ).convert_alpha(),
        ImageAssetGroup.KNIGHT: import_subfolders_as_dict(
            join("assets", "images", "enemies", "knight")
        ),
        ImageAssetGroup.GOBLIN: import_subfolders_as_dict(
            join("assets", "images", "enemies", "goblin")
        ),
        ImageAssetGroup.RED_GOBLIN: import_subfolders_as_dict(
            join("assets", "images", "enemies", "red_goblin")
        ),
        ImageAssetGroup.PURPLE_GOBLIN: import_subfolders_as_dict(
            join("assets", "images", "enemies", "purple_goblin")
        ),
    }


def load_fonts():
    return {
        FontAsset.FONT: pygame.font.Font("font.ttf", 35),
    }


def load_sounds():
    return {
        AudioAsset.SOUND: pygame.mixer.Sound(join("assets", "sounds", "sound.wav")),
    }
