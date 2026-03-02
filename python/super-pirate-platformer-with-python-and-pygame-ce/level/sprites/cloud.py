from random import randint

from settings import pygame, Z_Layer
from sprites.sprite import Sprite


class Cloud(Sprite):
    def __init__(self, groups, surface, position):
        super().__init__(groups, surface, position, Z_Layer.CLOUDS.value)

        self.rect.midbottom = position
        self.speed = randint(50, 120)
        self.direction = -1

    def update(self, delta_time):
        self.rect.x += self.direction * self.speed * delta_time

        if self.rect.right < 0:
            self.kill()
