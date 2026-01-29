from settings import pygame, vector, Z_Layer
from timer import Timer

from .constants import PearlTimerType


class Pearl(pygame.sprite.Sprite):
    def __init__(self, groups, position, surface, direction, collision_sprites, player):
        super().__init__(groups)
        self.image = surface
        self.rect = self.image.get_frect(center=position + vector(45 * direction, 0))
        self.direction = direction
        self.speed = 150
        self.z_index = Z_Layer.MAIN.value
        self.collision_sprites = collision_sprites
        self.player = player

        self.timers = {PearlTimerType.LIFETIME: Timer(5000)}
        self.timers[PearlTimerType.LIFETIME].activate()

    def move(self, delta_time):
        self.rect.x += self.direction * self.speed * delta_time

    def detect_collision(self):
        if len(pygame.sprite.spritecollide(self, self.collision_sprites, False)) > 0:
            self.kill()

        if self.rect.colliderect(self.player.hitbox_rect):
            self.kill()

    def update_timers(self):
        for timer in self.timers.values():
            timer.update()

    def update(self, delta_time):
        self.update_timers()
        self.move(delta_time)
        self.detect_collision()

        if not self.timers[PearlTimerType.LIFETIME].active:
            self.kill()
