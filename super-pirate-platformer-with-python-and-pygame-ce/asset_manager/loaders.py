from os.path import join

from .import_helpers import *
from levels.constants import LevelObjectAssetGroup
from settings import pygame


def load_level_graphics():
    return {
        LevelObjectAssetGroup.FLAG.value: import_folder(
            "assets", "graphics", "level", "flag"
        ),
        LevelObjectAssetGroup.SAW.value: import_folder(
            "assets", "graphics", "enemies", "saw", "animation"
        ),
        LevelObjectAssetGroup.SAW_CHAIN.value: import_image(
            "assets", "graphics", "enemies", "saw", "saw_chain"
        ),
        LevelObjectAssetGroup.FLOOR_SPIKE.value: import_folder(
            "assets", "graphics", "enemies", "floor_spikes"
        ),
        LevelObjectAssetGroup.PALM.value: import_subfolders_as_dict(
            "assets", "graphics", "level", "palms"
        ),
        LevelObjectAssetGroup.CANDLE.value: import_folder(
            "assets", "graphics", "level", "candle"
        ),
        LevelObjectAssetGroup.WINDOW.value: import_folder(
            "assets", "graphics", "level", "window"
        ),
        LevelObjectAssetGroup.BIG_CHAIN.value: import_folder(
            "assets", "graphics", "level", "big_chains"
        ),
        LevelObjectAssetGroup.SMALL_CHAIN.value: import_folder(
            "assets", "graphics", "level", "small_chains"
        ),
        LevelObjectAssetGroup.CANDLE_LIGHT.value: import_folder(
            "assets", "graphics", "level", "candle_light"
        ),
        LevelObjectAssetGroup.PLAYER.value: import_subfolders_as_dict(
            "assets", "graphics", "player"
        ),
        LevelObjectAssetGroup.HELICOPTER.value: import_folder(
            "assets", "graphics", "level", "helicopter"
        ),
        LevelObjectAssetGroup.BOAT.value: import_folder(
            "assets", "graphics", "objects", "boat"
        ),
        LevelObjectAssetGroup.SPIKED_BALL.value: import_image(
            "assets", "graphics", "enemies", "spiked_ball", "spiked_ball"
        ),
        LevelObjectAssetGroup.SPIKED_CHAIN.value: import_image(
            "assets", "graphics", "enemies", "spiked_ball", "spiked_chain"
        ),
        LevelObjectAssetGroup.TOOTH.value: import_folder(
            "assets", "graphics", "enemies", "tooth", "run"
        ),
        LevelObjectAssetGroup.SHELL.value: import_subfolders_as_dict(
            "assets", "graphics", "enemies", "shell"
        ),
        LevelObjectAssetGroup.PEARL.value: import_image(
            "assets", "graphics", "enemies", "bullets", "pearl"
        ),
        LevelObjectAssetGroup.PALM_BACKGROUND.value: import_folder(
            "assets", "graphics", "level", "palms", "palm_bg"
        ),
        LevelObjectAssetGroup.PALM_BACKGROUND_LEFT.value: import_folder(
            "assets", "graphics", "level", "palms", "palm_bg_left"
        ),
        LevelObjectAssetGroup.PALM_BACKGROUND_RIGHT.value: import_folder(
            "assets", "graphics", "level", "palms", "palm_bg_right"
        ),
        LevelObjectAssetGroup.PALM_LEFT.value: import_folder(
            "assets", "graphics", "level", "palms", "palm_left"
        ),
        LevelObjectAssetGroup.PALM_RIGHT.value: import_folder(
            "assets", "graphics", "level", "palms", "palm_right"
        ),
        LevelObjectAssetGroup.PALM_SMALL.value: import_folder(
            "assets", "graphics", "level", "palms", "palm_small"
        ),
        LevelObjectAssetGroup.PALM_LARGE.value: import_folder(
            "assets", "graphics", "level", "palms", "palm_large"
        ),
        LevelObjectAssetGroup.ITEMS.value: import_subfolders_as_dict(
            "assets", "graphics", "items"
        ),
        LevelObjectAssetGroup.PARTICLE.value: import_folder(
            "assets", "graphics", "effects", "particle"
        ),
        LevelObjectAssetGroup.HEART.value: import_folder(
            "assets", "graphics", "ui", "heart"
        ),
    }


def load_ui_graphics():
    return {
        LevelObjectAssetGroup.HEART.value: import_folder(
            "assets", "graphics", "ui", "heart"
        ),
        LevelObjectAssetGroup.COIN.value: import_image(
            "assets", "graphics", "ui", "coin"
        ),
    }


def load_font():
    full_path = join("assets", "graphics", "ui", "runescape_uf.ttf")

    return pygame.font.Font(full_path, 40)
