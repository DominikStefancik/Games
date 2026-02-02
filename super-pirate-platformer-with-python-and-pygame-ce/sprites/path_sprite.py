from settings import pygame, Z_Layer

from .sprite import Sprite


class PathSprite(Sprite):
    def __init__(self, groups, surface, position, level):
        super().__init__(groups, surface, position, Z_Layer.PATH.value)

        # This parameter determines if the path to its given level will be shown
        self.level = level
