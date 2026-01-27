from settings import pygame, TILE_SIZE, vector

from .constants import MovingDirection
from .sprite import Sprite


class MovingSprite(Sprite):
    def __init__(self, groups, surface, start_position, end_position, moving_direction, speed):
        super().__init__(groups, surface, start_position)
        self.is_moving = True
        self.moving_direction = moving_direction

        if self.moving_direction == MovingDirection.HORIZONTAL:
            self.rect.midleft = start_position
        else:
            self.rect.midtop = start_position

        self.start_position = start_position
        self.end_position = end_position
        self.speed = speed
        self.direction = vector(1, 0) if self.moving_direction == MovingDirection.HORIZONTAL else vector(0, 1)

    def check_moving_distance(self):
        if self.moving_direction == MovingDirection.HORIZONTAL:
            if self.rect.left <= self.start_position[0] and self.direction.x == -1:
                self.direction.x = 1
                self.rect.left = self.start_position[0]
            if self.rect.right >= self.end_position[0] and self.direction.x == 1:
                self.direction.x = -1
                self.rect.right = self.end_position[0]
        else:
            if self.rect.top <= self.start_position[1] and self.direction.y == -1:
                self.direction.y = 1
                self.rect.top = self.start_position[1]
            if self.rect.bottom >= self.end_position[1] and self.direction.y == 1:
                self.direction.y = -1
                self.rect.bottom = self.end_position[1]

    def update(self, delta_time):
        # Before updating the movement, store the position of the current rectangle
        # This will be then used for a collision detection
        self.previous_rect = self.rect.copy()
        self.rect.topleft += self.direction * self.speed * delta_time
        self.check_moving_distance()
