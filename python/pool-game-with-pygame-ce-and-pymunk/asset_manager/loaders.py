from os.path import join

import pygame

from .constants import ImageAsset


def load_graphics():
    return {
        ImageAsset.TABLE: pygame.image.load(
            join("assets", "images", "table.png")
        ).convert_alpha(),
    }


def load_fonts():
    return {}


def load_sounds():
    return {}
