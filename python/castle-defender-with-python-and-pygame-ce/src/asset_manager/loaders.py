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
        ImageAssetGroup.TOWER: import_folder_as_dict(join("assets", "images", "tower")),
        ImageAssetGroup.BULLET: pygame.image.load(
            join("assets", "images", "bullet.png")
        ).convert_alpha(),
        ImageAssetGroup.CROSSHAIR: pygame.image.load(
            join("assets", "images", "crosshair.png")
        ).convert_alpha(),
        ImageAssetGroup.REPAIR_BUTTON: pygame.image.load(
            join("assets", "images", "buttons", "repair.png")
        ).convert_alpha(),
        ImageAssetGroup.ARMOUR_BUTTON: pygame.image.load(
            join("assets", "images", "buttons", "armour.png")
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
        FontAsset.FUTURA_25: pygame.font.SysFont("Futura", 25),
        FontAsset.FUTURA_35: pygame.font.SysFont("Futura", 35),
        FontAsset.FUTURA_60: pygame.font.SysFont("Futura", 60),
    }


def load_sounds():
    return {
        AudioAsset.MARCH: pygame.mixer.Sound(join("assets", "sounds", "march.mp3")),
        AudioAsset.ATTACK: pygame.mixer.Sound(join("assets", "sounds", "attack.mp3")),
        AudioAsset.DEATH: pygame.mixer.Sound(join("assets", "sounds", "death.mp3")),
    }
