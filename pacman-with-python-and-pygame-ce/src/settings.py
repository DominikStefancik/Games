from enum import Enum

import pygame, sys

WINDOW_WIDTH, WINDOW_HEIGHT = 900, 950
ANIMATION_SPEED = 8


class Direction(Enum):
    LEFT = "left"
    RIGHT = "right"
    UP = "up"
    DOWN = "down"
