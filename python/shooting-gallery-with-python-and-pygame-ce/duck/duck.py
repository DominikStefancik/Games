from random import randint

import pygame

from asset_manager.asset_manager import get_asset_manager
from asset_manager.constants import ImageAsset


class Duck(pygame.sprite.Sprite):
    def __init__(self, group, image, position):
        super().__init__(group)

        self.display_surface = pygame.display.get_surface()
        self.image = image
        self.rect = self.image.get_frect(center=position)
        # Randomly adjust the Y-coordinate to vary the heights of ducks
        self.rect.y += randint(0, 7) * 10

        self.is_hit = False

    def draw(self):
        if not self.is_hit:
            self.display_surface.blit(self.image, (self.rect.x, self.rect.y))

        asset_manager = get_asset_manager()
        stick_image = asset_manager.graphics[ImageAsset.STICK]
        # Draw the stick image
        stick_x = (
            self.rect.bottomleft[0] + self.image.width / 2 - stick_image.get_width() / 2
        )
        stick_y = self.rect.bottomleft[1]
        self.display_surface.blit(stick_image, (stick_x, stick_y))
