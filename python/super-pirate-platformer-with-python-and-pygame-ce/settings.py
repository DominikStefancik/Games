import pygame, sys
from pygame.math import Vector2 as vector
from enum import Enum

WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
TILE_SIZE = 64
ANIMATION_SPEED = 6


# The values say which parts of the level map will be drawn on top
class Z_Layer(Enum):
    BACKGROUND = 0
    CLOUDS = 1
    BACKGROUND_TILES = 2
    PATH = 3
    BACKGROUND_DETAILS = 4
    MAIN = 5
    WATER = 6
    FOREGROUND = 7
