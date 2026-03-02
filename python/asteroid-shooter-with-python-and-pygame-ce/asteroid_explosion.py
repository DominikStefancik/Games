import random

import pygame


class AnimatedAsteroidExplosion(pygame.sprite.Sprite):
    def __init__(self, groups, frame_list, position):
        # Initialise the parent class
        # When passing sprite groups to the parent class Pygame automatically adds this custom Sprite class to them
        super().__init__(groups)
        self.frame_list = frame_list
        self.frame_index = 0
        self.image = self.frame_list[self.frame_index]
        self.rect = self.image.get_frect(center=position)
        self.animation_speed = 20

    def update(self, delta_time):
        # An alternative way to use timer.
        # Instead of checking if a certain amount of time passed, we are using the delta time
        # to update the frame index.
        self.frame_index += self.animation_speed * delta_time

        if self.frame_index <= len(self.frame_list):
            self.image = self.frame_list[int(self.frame_index)]
        else:
            self.kill()
