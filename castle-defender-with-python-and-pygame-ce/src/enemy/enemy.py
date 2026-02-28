from math import cos, radians, sin

from castle.constants import BULLET_DAMAGE
from game_state.game_state_manager import get_game_state_manager
from settings import pygame, WINDOW_HEIGHT, WINDOW_WIDTH
from timer import Timer

from .constants import (
    EnemyAnimation,
    ENEMY_ANIMATION_SPEED,
    ENEMY_ATTACK_COOLDOWN_INTERVAL,
    ENEMY_ATTACK_DAMAGE,
    ENEMY_SPEED,
)
from .helpers import get_enemy_health, scale_animation_frames


class Enemy(pygame.sprite.Sprite):
    def __init__(self, group, animation_frames, type, position):
        super().__init__(group)

        self.type = type
        self.animation = EnemyAnimation.WALK
        self.animation_frames = scale_animation_frames(animation_frames)
        self.frame_index = 0
        self.image = self.animation_frames[self.animation.value][self.frame_index]
        # We have to create rectangle manually and not derive it from an image,
        # because every image contains a lot of white space on the top and right sides
        # which would complicate collision detection
        #
        # Theyn, in the EnemyGroup class we will draw the enemy so it fits into thos rectangle
        self.rect = pygame.FRect(0, 0, 25, 45)
        self.rect.center = position
        self.health = get_enemy_health(self.type)
        self.speed = ENEMY_SPEED
        self.is_alive = True
        self.attack_timer = Timer(ENEMY_ATTACK_COOLDOWN_INTERVAL)

    def animate(self, delta_time):
        animation_frames = self.animation_frames[self.animation.value]
        self.frame_index += ENEMY_ANIMATION_SPEED * delta_time
        self.image = animation_frames[int(self.frame_index % len(animation_frames))]

        if self.animation == EnemyAnimation.DEATH:
            if self.frame_index >= len(animation_frames):
                self.image = animation_frames[len(animation_frames) - 1]

    def move(self, delta_time):
        self.rect.x += self.speed * delta_time

    def attack(self, castle):
        if not self.attack_timer.active:
            castle.health -= ENEMY_ATTACK_DAMAGE
            self.attack_timer.activate()

    def take_action(self, delta_time, castle):
        if self.rect.right < castle.rect.left:
            self.move(delta_time)
        elif self.animation == EnemyAnimation.ATTACK:
            self.attack(castle)

    def detect_collisions(self, castle, bullet_sprites):
        if self.rect.right > castle.rect.left:
            self.rect.right = castle.rect.left
            self.update_animation(EnemyAnimation.ATTACK)
            self.attack_timer.activate()

        # With the last argument set to True, we destroy each bullet which collided with an enemy
        if pygame.sprite.spritecollide(self, bullet_sprites, True):
            self.health -= BULLET_DAMAGE

            if self.health <= 0:
                self.update_animation(EnemyAnimation.DEATH)
                self.is_alive = False
                self.attack_timer.deactivate()

                game_state_manager = get_game_state_manager()
                game_state_manager.update_after_enemy_dead(self.type)

    def update_animation(self, new_animation):
        if self.animation != new_animation:
            self.animation = new_animation
            self.frame_index = 0

    def update(self, delta_time, castle, bullet_sprites):
        self.attack_timer.update()

        if self.is_alive:
            self.take_action(delta_time, castle)
            self.detect_collisions(castle, bullet_sprites)

        self.animate(delta_time)
