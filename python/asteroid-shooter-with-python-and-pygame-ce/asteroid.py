import random

import pygame

from constants import WINDOW_HEIGHT


class Asteroid(pygame.sprite.Sprite):
    def __init__(self, groups, image, position):
        # Initialise the parent class
        # When passing sprite groups to the parent class Pygame automatically adds this custom Sprite class to them
        super().__init__(groups)
        self.original_image = image
        # Rotating an image often causes lost of the image quality which will become noticeable.
        # That's why we want to store image into two properties, where one of them will store the original image
        # which angle will not change.
        self.image = self.original_image
        self.rect = self.image.get_frect(center=position)
        self.movement_speed = random.randint(300, 500)
        # The method "uniform" goes from the starting to the ending value
        self.movement_direction = pygame.Vector2(random.uniform(-0.5, 0.5), 1)
        self.rotation_angle = 0
        self.rotation_direction = random.choice([-1, 1])
        self.rotation_speed = random.randint(100, 300)

    def update(self, delta_time):
        self.rect.center += self.movement_direction * self.movement_speed * delta_time

        # Continuous rotation
        #
        # The method "rotozoom" does 2 things:
        #   1. Scales and rotates the imae at the same time
        #   2. On top of that it applies filter when doing that. That effectivelly means it smooths out
        #      the entire image and gets rid of pixels, which for most graphics looks much better most of the time.
        self.image = pygame.transform.rotozoom(
            self.original_image, self.rotation_angle, 1
        )
        self.rotation_angle += (
            self.rotation_direction * self.rotation_speed * delta_time
        )
        # To make rotation look smooth, we also have to updte the image rectangle after rotation.
        # Otherwise, with a higher speed, the rotation look interrupted and unnatural.
        self.rect = self.image.get_frect(center=self.rect.center)

        if self.rect.top > WINDOW_HEIGHT:
            self.kill()
