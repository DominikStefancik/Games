import random

import pygame

from constants import WINDOW_HEIGHT

class Asteroid(pygame.sprite.Sprite):
    def __init__(self, groups, image, position):
        # Initialise the parent class
        # When passing sprite groups to the parent class Pygame automatically adds this custom Sprite class to them
        super().__init__(groups)
        self.image = image
        self.rect = self.image.get_frect(center = position)
        self.speed = random.randint(300, 500)
        # The method "uniform" goes from the starting to the ending value
        self.direction = pygame.Vector2(random.uniform(-0.5, 0.5), 1)

    def update(self, delta_time):
        self.rect.center += self.direction * self.speed * delta_time

        if self.rect.top > WINDOW_HEIGHT:
            self.kill()
