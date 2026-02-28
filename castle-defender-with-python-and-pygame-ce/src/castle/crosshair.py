from helpers import scale_image
from settings import pygame

from .constants import CROSSHAIR_IMAGE_SCALE


class Crosshair(pygame.sprite.Sprite):
    def __init__(self, group, image):
        super().__init__(group)

        self.image = scale_image(image, CROSSHAIR_IMAGE_SCALE)
        self.rect = self.image.get_frect()
        # Hide the mouse cursor
        pygame.mouse.set_visible(False)

    def update(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.rect.center = (mouse_x, mouse_y)
