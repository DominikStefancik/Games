from os.path import join

import pygame

from .constants import AudioAsset, FontAsset, ImageAsset


def load_graphics():
    return {
        ImageAsset.BACKGROUND: pygame.image.load(
            join("assets", "images", "background_blue.png")
        ).convert_alpha(),
        ImageAsset.TABLE: pygame.image.load(
            join("assets", "images", "background_wood.png")
        ).convert_alpha(),
        ImageAsset.CURTAIN_TOP: pygame.image.load(
            join("assets", "images", "curtain_top.png")
        ).convert_alpha(),
        ImageAsset.CURTAIN_SIDE: pygame.image.load(
            join("assets", "images", "curtain_side.png")
        ).convert_alpha(),
        ImageAsset.WATER_BACK: pygame.image.load(
            join("assets", "images", "water1.png")
        ).convert_alpha(),
        ImageAsset.WATER_FRONT: pygame.image.load(
            join("assets", "images", "water2.png")
        ).convert_alpha(),
        ImageAsset.GRASS: pygame.image.load(
            join("assets", "images", "grass.png")
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
