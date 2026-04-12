from os.path import join

import pygame

from .constants import ImageAsset


def load_graphics():
    return {
        ImageAsset.IMAGE: pygame.image.load(
            join("assets", "images", "image.png")
        ).convert_alpha(),
    }


def load_fonts():
    return {}


def load_sounds():
    return {}
