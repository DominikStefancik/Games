from asset_manager.asset_manager import get_asset_manager
from asset_manager.constants import ImageAssetGroup
from castle.castle import Castle
from settings import pygame, WINDOW_HEIGHT, WINDOW_WIDTH


class SpritesManager:
    def __init__(self):
        # The main surface on which we will be drawing sprites
        self.display_surface = pygame.display.get_surface()
        self.all_sprites = pygame.sprite.Group()
        self.clock = pygame.time.Clock()

        asset_manager = get_asset_manager()
        Castle(
            group=self.all_sprites,
            images=asset_manager.graphics[ImageAssetGroup.CASTLE],
            position=(WINDOW_WIDTH - 430, WINDOW_HEIGHT - 470),
            image_scale=0.3,
        )

    def update(self):
        delta_time = self.clock.tick() / 1000

        self.all_sprites.update(delta_time)

    def draw(self):
        self.all_sprites.draw(self.display_surface)
