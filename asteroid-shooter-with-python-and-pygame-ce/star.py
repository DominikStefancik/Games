import random

import pygame

from constants import WINDOW_HEIGHT, WINDOW_WIDTH

class Star(pygame.sprite.Sprite):
    def __init__(self, groups, image):
        # Initialise the parent class
        # When passing sprite groups to the parent class Pygame automatically adds this custom Sprite class to them
        super().__init__(groups)
        self.image = image
        self.rect = self.image.get_frect(center = (random.randint(0, WINDOW_WIDTH), random.randint(0, WINDOW_HEIGHT)))
