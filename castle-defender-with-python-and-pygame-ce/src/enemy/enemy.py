from math import cos, radians, sin

from settings import pygame, WINDOW_HEIGHT, WINDOW_WIDTH

from .constants import EnemyAnimation, ENEMY_ANIMATION_SPEED, ENEMY_SPEED
from .helpers import get_enemy_health, scale_animation_frames


class Enemy(pygame.sprite.Sprite):
    def __init__(self, groups, animation_frames, type, position):
        super().__init__(groups)

        self.type = type
        self.animation = EnemyAnimation.WALK
        self.animation_frames = scale_animation_frames(animation_frames)
        self.frame_index = 0
        self.image = self.animation_frames[self.animation.value][self.frame_index]
        self.rect = self.image.get_frect(center=position)
        self.health = get_enemy_health(self.type)
        self.speed = ENEMY_SPEED

    def animate(self, delta_time):
        animation_frames = self.animation_frames[self.animation.value]
        self.frame_index += ENEMY_ANIMATION_SPEED * delta_time
        self.image = animation_frames[int(self.frame_index % len(animation_frames))]

    def move(self, delta_time):
        self.rect.x += self.speed * delta_time

    def update(self, delta_time):
        self.move(delta_time)
        self.animate(delta_time)

        # If a bullet got out of the screen, destroy it
        if (
            self.rect.right < 0
            or self.rect.left > WINDOW_WIDTH
            or self.rect.bottom < 0
            or self.rect.top > WINDOW_HEIGHT
        ):
            self.kill()
