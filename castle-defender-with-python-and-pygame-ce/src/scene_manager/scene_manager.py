from asset_manager.asset_manager import get_asset_manager
from asset_manager.constants import ImageAsset
from settings import pygame

from .helpers import scale_image


class SceneManager:
    def __init__(self):
        # The main surface on which we will be drawing elements
        self.display_surface = pygame.display.get_surface()

        self.asset_manager = get_asset_manager()
        self.background = scale_image(
            self.asset_manager.graphics[ImageAsset.BACKGROUND], 1.21
        )

    def update(self):
        pass

    def draw(self):
        self.display_surface.blit(self.background, (0, 0))
