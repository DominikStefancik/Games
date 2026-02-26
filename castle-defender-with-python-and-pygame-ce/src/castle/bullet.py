from math import cos, radians, sin

from helpers import scale_image
from settings import pygame, WINDOW_HEIGHT, WINDOW_WIDTH

from .constants import BULLET_IMAGE_SCALE, BULLET_SPEED


class Bullet(pygame.sprite.Sprite):
    def __init__(self, group, image, position, angle):
        super().__init__(group)

        self.image = scale_image(image, BULLET_IMAGE_SCALE)
        self.rect = self.image.get_frect(topleft=position)
        self.angle = angle
        self.speed = BULLET_SPEED

        # Horizontal and vertical deltas based on the angle
        self.delta_x = cos(radians(self.angle))
        # Because the Y-coordinate increaces when going down, we have to use negativa value after calculation
        self.delta_y = -sin(radians(self.angle))

    def move(self, delta_time):
        self.rect.x += self.delta_x * self.speed * delta_time
        self.rect.y += self.delta_y * self.speed * delta_time

    def update(self, delta_time):
        self.move(delta_time)

        # If a bullet got out of the screen, destroy it
        if (
            self.rect.right < 0
            or self.rect.left > WINDOW_WIDTH
            or self.rect.bottom < 0
            or self.rect.top > WINDOW_HEIGHT
        ):
            self.kill()
