import random

import pygame

from constants import WINDOW_HEIGHT, WINDOW_WIDTH
from .constants import PLATFORM_MOVE_COUNTER_LIMIT

class Platform(pygame.sprite.Sprite):
    def __init__(self, image, position, width, is_moving=False):
        pygame.sprite.Sprite.__init__(self)
        # For each platform, the width will be different so we can have randomness in platforms sizes
        self.image = pygame.transform.scale(image, (width, 10))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = position
        self.is_moving = is_moving
        self.move_counter = random.randint(0, 50)
        self.movement_direction = random.choice([-1, 1])
        self.movement_speed = random.randint(1, 2)

    def update(self, scroll):
        # If the platform is a moving platform, move it side to side
        if self.is_moving:
            self.move_counter += 1
            self.rect.x += self.movement_direction * self.movement_speed

        # Change platform's direction if it reached the move limit
        # or it reached the edge of the window
        if self.move_counter >= PLATFORM_MOVE_COUNTER_LIMIT or self.rect.left < 0 or self.rect.right > WINDOW_WIDTH:
            self.movement_direction *= -1 # the movement direction changes to the opposite
            self.move_counter = 0

        # Update platform's vertical position depending on if we scroll the window or not
        self.rect.y += scroll

        # If the platform has gone off the window screen, destroy the object and remove it from the memory.
        # By doing that, it will also be removed from the "platform_group".
        # This way we achieve there will be infinite number of platform generated, because those which
        # will go off the screen will be destroyed.
        if self.rect.top > WINDOW_HEIGHT:
            self.kill()
