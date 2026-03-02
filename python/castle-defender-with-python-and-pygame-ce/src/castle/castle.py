from math import atan2, degrees

from game_state.game_state_manager import get_game_state_manager
from helpers import scale_image
from settings import pygame

from .constants import CASTLE_IMAGE_SCALE, CastleState
from .helpers import get_castle_image, map_castle_position


class Castle(pygame.sprite.Sprite):
    def __init__(self, group, images, create_bullet_function):
        super().__init__(group)

        self.game_state_manager = get_game_state_manager()
        self.state = CastleState.FULLY_RESTORED

        self.images = {
            CastleState.FULLY_RESTORED: scale_image(
                get_castle_image(images, CastleState.FULLY_RESTORED), CASTLE_IMAGE_SCALE
            ),
            CastleState.DAMAGED: scale_image(
                get_castle_image(images, CastleState.DAMAGED), CASTLE_IMAGE_SCALE
            ),
            CastleState.SEVERELY_DAMAGED: scale_image(
                get_castle_image(images, CastleState.SEVERELY_DAMAGED),
                CASTLE_IMAGE_SCALE,
            ),
        }
        self.image = self.images[self.state]
        self.rect = self.image.get_frect(topleft=map_castle_position(self.state))
        self.create_bullet_function = create_bullet_function

    def shoot(self):
        if pygame.mouse.get_just_pressed()[0]:
            mouse_position = pygame.mouse.get_pos()

            if mouse_position[0] < self.rect.left + 25:
                distance_x = mouse_position[0] - self.rect.midleft[0]
                # Because the Y-coordinate increaces when going down, we have to use negative value after calculation
                distance_y = -(mouse_position[1] - self.rect.midleft[1])
                angle = degrees(atan2(distance_y, distance_x))
                self.create_bullet_function(
                    (self.rect.midleft[0], self.rect.midleft[1]), angle
                )

    def update_state(self):
        if self.game_state_manager.health <= 250:
            self.state = CastleState.SEVERELY_DAMAGED
        elif self.game_state_manager.health <= 500:
            self.state = CastleState.DAMAGED
        else:
            self.state = CastleState.FULLY_RESTORED

        self.image = self.images[self.state]
        self.rect = self.image.get_frect(topleft=map_castle_position(self.state))

    def update(self):
        self.update_state()
        self.shoot()
