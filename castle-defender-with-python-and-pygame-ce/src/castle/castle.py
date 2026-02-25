from helpers import scale_image
from settings import pygame

from .constants import CASTLE_STARTING_HEALTH, CastleState
from .helpers import get_castle_image


class Castle(pygame.sprite.Sprite):
    def __init__(self, group, images, position, image_scale):
        super().__init__(group)

        self.max_health = CASTLE_STARTING_HEALTH
        self.health = self.max_health
        self.state = CastleState.FULLY_RESTORED

        self.image = scale_image(get_castle_image(images, self.state), image_scale)
        self.rect = self.image.get_frect(topleft=position)
