from math import atan2, degrees

from game_state.game_state_manager import get_game_state_manager
from helpers import scale_image
from settings import pygame
from timer import Timer

from .constants import TOWER_IMAGE_SCALE, TOWER_SHOOT_BULLET_DELAY, TowerState
from .helpers import get_tower_image


class Tower(pygame.sprite.Sprite):
    def __init__(self, group, images, position, create_bullet_function):
        super().__init__(group)

        self.game_state_manager = get_game_state_manager()
        self.state = TowerState.FULLY_RESTORED

        self.images = {
            TowerState.FULLY_RESTORED: scale_image(
                get_tower_image(images, TowerState.FULLY_RESTORED), TOWER_IMAGE_SCALE
            ),
            TowerState.DAMAGED: scale_image(
                get_tower_image(images, TowerState.DAMAGED), TOWER_IMAGE_SCALE
            ),
            TowerState.SEVERELY_DAMAGED: scale_image(
                get_tower_image(images, TowerState.SEVERELY_DAMAGED),
                TOWER_IMAGE_SCALE,
            ),
        }
        self.image = self.images[self.state]
        self.rect = self.image.get_frect(topleft=position)
        self.create_bullet_function = create_bullet_function
        self.target = None
        self.shoot_bullet_timer = Timer(TOWER_SHOOT_BULLET_DELAY)

    def shoot(self, enemy_group):
        self.target = None

        for enemy in enemy_group:
            # Take the very fist enemy who is still alive
            if enemy.is_alive:
                self.target = enemy
                break

        if self.target and not self.shoot_bullet_timer.active:
            tower_window_x, tower_window_y = (
                self.rect.center[0] - 7,
                self.rect.center[1] - 2,
            )

            distance_x = self.target.rect.midbottom[0] - tower_window_x
            # Because the Y-coordinate increaces when going down, we have to use negative value after calculation
            distance_y = -(self.target.rect.midbottom[1] - tower_window_y)
            angle = degrees(atan2(distance_y, distance_x))
            self.create_bullet_function((tower_window_x, tower_window_y), angle)
            self.shoot_bullet_timer.activate()

    def update_state(self):
        if self.game_state_manager.health <= 250:
            self.state = TowerState.SEVERELY_DAMAGED
        elif self.game_state_manager.health <= 500:
            self.state = TowerState.DAMAGED
        else:
            self.state = TowerState.FULLY_RESTORED

        self.image = self.images[self.state]

    def update(self, enemy_group):
        self.shoot_bullet_timer.update()
        self.update_state()
        self.shoot(enemy_group)
