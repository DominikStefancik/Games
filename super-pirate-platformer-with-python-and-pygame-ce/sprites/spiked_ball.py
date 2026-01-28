from math import sin, cos, radians

from settings import pygame, Z_Layer

from .sprite import Sprite


class SpikedBall(Sprite):
    def __init__(
        self,
        groups,
        surface,
        position,
        radius,
        start_angle,
        end_angle,
        speed,
        z_index=Z_Layer.MAIN.value,
    ):
        self.center = position
        self.radius = radius
        self.start_angle = start_angle
        self.end_angle = end_angle
        self.current_angle = start_angle
        self.speed = speed
        self.direction = 1
        self.move_full_circle = self.end_angle == -1

        # Trigonometry
        x = self.center[0] + self.radius * cos(radians(self.current_angle))
        y = self.center[1] + self.radius * sin(radians(self.current_angle))
        super().__init__(groups, surface, (x, y), z_index)

    def update(self, delta_time):
        self.current_angle += self.direction * self.speed * delta_time

        if not self.move_full_circle:
            if self.current_angle >= self.end_angle:
                self.direction = -1
            if self.current_angle < self.start_angle:
                self.direction = 1

        x = self.center[0] + self.radius * cos(radians(self.current_angle))
        y = self.center[1] + self.radius * sin(radians(self.current_angle))
        self.rect.center = (x, y)
