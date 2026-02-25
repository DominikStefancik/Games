from math import atan2, degrees

from helpers import scale_image
from settings import pygame

from .constants import CASTLE_IMAGE_SCALE, CASTLE_STARTING_HEALTH, CastleState
from .helpers import get_castle_image


class Castle(pygame.sprite.Sprite):
    def __init__(self, group, images, position, create_bullet_function):
        super().__init__(group)

        self.max_health = CASTLE_STARTING_HEALTH
        self.health = self.max_health
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
        self.rect = self.image.get_frect(topleft=position)
        self.create_bullet_function = create_bullet_function

    def shoot(self):
        if pygame.mouse.get_just_pressed()[0]:
            mouse_position = pygame.mouse.get_pos()
            distance_x = mouse_position[0] - self.rect.midleft[0]
            # Because the Y-coordinate increaces when going down, we have to use negativa value after calculation
            distance_y = -(mouse_position[1] - self.rect.midleft[1])
            angle = degrees(atan2(distance_y, distance_x))
            self.create_bullet_function(
                (self.rect.midleft[0], self.rect.midleft[1]), angle
            )

    def update(self, delta_time):
        self.image = self.images[self.state]
        self.shoot()
