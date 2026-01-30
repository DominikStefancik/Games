from os.path import join

from .import_helpers import *
from asset_manager.constants import ImageAssetGroup
from settings import pygame


def load_level_graphics():
    return {
        ImageAssetGroup.FLAG.value: import_folder(
            "assets", "graphics", "level", "flag"
        ),
        ImageAssetGroup.SAW.value: import_folder(
            "assets", "graphics", "enemies", "saw", "animation"
        ),
        ImageAssetGroup.SAW_CHAIN.value: import_image(
            "assets", "graphics", "enemies", "saw", "saw_chain"
        ),
        ImageAssetGroup.FLOOR_SPIKE.value: import_folder(
            "assets", "graphics", "enemies", "floor_spikes"
        ),
        ImageAssetGroup.PALM.value: import_subfolders_as_dict(
            "assets", "graphics", "level", "palms"
        ),
        ImageAssetGroup.CANDLE.value: import_folder(
            "assets", "graphics", "level", "candle"
        ),
        ImageAssetGroup.WINDOW.value: import_folder(
            "assets", "graphics", "level", "window"
        ),
        ImageAssetGroup.BIG_CHAIN.value: import_folder(
            "assets", "graphics", "level", "big_chains"
        ),
        ImageAssetGroup.SMALL_CHAIN.value: import_folder(
            "assets", "graphics", "level", "small_chains"
        ),
        ImageAssetGroup.CANDLE_LIGHT.value: import_folder(
            "assets", "graphics", "level", "candle_light"
        ),
        ImageAssetGroup.PLAYER.value: import_subfolders_as_dict(
            "assets", "graphics", "player"
        ),
        ImageAssetGroup.HELICOPTER.value: import_folder(
            "assets", "graphics", "level", "helicopter"
        ),
        ImageAssetGroup.BOAT.value: import_folder(
            "assets", "graphics", "objects", "boat"
        ),
        ImageAssetGroup.SPIKED_BALL.value: import_image(
            "assets", "graphics", "enemies", "spiked_ball", "spiked_ball"
        ),
        ImageAssetGroup.SPIKED_CHAIN.value: import_image(
            "assets", "graphics", "enemies", "spiked_ball", "spiked_chain"
        ),
        ImageAssetGroup.TOOTH.value: import_folder(
            "assets", "graphics", "enemies", "tooth", "run"
        ),
        ImageAssetGroup.SHELL.value: import_subfolders_as_dict(
            "assets", "graphics", "enemies", "shell"
        ),
        ImageAssetGroup.PEARL.value: import_image(
            "assets", "graphics", "enemies", "bullets", "pearl"
        ),
        ImageAssetGroup.PALM_BACKGROUND.value: import_folder(
            "assets", "graphics", "level", "palms", "palm_bg"
        ),
        ImageAssetGroup.PALM_BACKGROUND_LEFT.value: import_folder(
            "assets", "graphics", "level", "palms", "palm_bg_left"
        ),
        ImageAssetGroup.PALM_BACKGROUND_RIGHT.value: import_folder(
            "assets", "graphics", "level", "palms", "palm_bg_right"
        ),
        ImageAssetGroup.PALM_LEFT.value: import_folder(
            "assets", "graphics", "level", "palms", "palm_left"
        ),
        ImageAssetGroup.PALM_RIGHT.value: import_folder(
            "assets", "graphics", "level", "palms", "palm_right"
        ),
        ImageAssetGroup.PALM_SMALL.value: import_folder(
            "assets", "graphics", "level", "palms", "palm_small"
        ),
        ImageAssetGroup.PALM_LARGE.value: import_folder(
            "assets", "graphics", "level", "palms", "palm_large"
        ),
        ImageAssetGroup.ITEMS.value: import_subfolders_as_dict(
            "assets", "graphics", "items"
        ),
        ImageAssetGroup.PARTICLE.value: import_folder(
            "assets", "graphics", "effects", "particle"
        ),
        ImageAssetGroup.HEART.value: import_folder(
            "assets", "graphics", "ui", "heart"
        ),
        ImageAssetGroup.WATER_TOP.value: import_folder(
            "assets", "graphics", "level", "water", "top"
        ),
        ImageAssetGroup.WATER_BODY.value: import_image(
            "assets", "graphics", "level", "water", "body"
        ),
    }


def load_ui_graphics():
    return {
        ImageAssetGroup.HEART.value: import_folder(
            "assets", "graphics", "ui", "heart"
        ),
        ImageAssetGroup.COIN.value: import_image(
            "assets", "graphics", "ui", "coin"
        ),
    }


def load_font():
    full_path = join("assets", "graphics", "ui", "runescape_uf.ttf")

    return pygame.font.Font(full_path, 40)
