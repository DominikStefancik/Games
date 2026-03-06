import pygame

from asset_manager.asset_manager import get_asset_manager
from asset_manager.constants import ImageAsset
from settings import WINDOW_HEIGHT, WINDOW_WIDTH

from .constants import MAX_DUCKS_ON_SCREEN
from .helpers import create_brown_duck, create_yellow_duck


class SceneManager:
    def __init__(self):
        # The main surface on which we will be drawing elements
        self.display_surface = pygame.display.get_surface()

        self.asset_manager = get_asset_manager()
        self.all_sprites = pygame.sprite.Group()
        self.brown_duck_sprites = pygame.sprite.Group()
        self.yellow_duck_sprites = pygame.sprite.Group()

        self.create_brown_ducks()
        self.create_yellow_ducks()

    def create_brown_ducks(self):
        for index in range(MAX_DUCKS_ON_SCREEN):
            create_brown_duck((self.all_sprites, self.brown_duck_sprites), index)

    def create_yellow_ducks(self):
        for index in range(MAX_DUCKS_ON_SCREEN):
            create_yellow_duck((self.all_sprites, self.yellow_duck_sprites), index)

    def restart(self):
        pass

    def draw_background(self):
        background = self.asset_manager.graphics[ImageAsset.BACKGROUND]
        image_width, image_height = background.get_width(), background.get_height()

        for x in range(0, WINDOW_WIDTH, image_width):
            for y in range(0, WINDOW_HEIGHT, image_height):
                self.display_surface.blit(background, (x, y))

    def draw_grass(self):
        grass = self.asset_manager.graphics[ImageAsset.GRASS]
        image_width = grass.get_width()

        for x in range(0, WINDOW_WIDTH, image_width):
            self.display_surface.blit(grass, (x, WINDOW_HEIGHT - 260))

    def draw_back_water(self):
        water_back = self.asset_manager.graphics[ImageAsset.WATER_BACK]

        for x in range(0, WINDOW_WIDTH, water_back.get_width()):
            self.display_surface.blit(water_back, (x, WINDOW_HEIGHT - 180))

    def draw_front_water(self):
        water_front = self.asset_manager.graphics[ImageAsset.WATER_FRONT]

        for x in range(-70, WINDOW_WIDTH, water_front.get_width()):
            self.display_surface.blit(water_front, (x, WINDOW_HEIGHT - 155))

    def draw_table(self):
        table = self.asset_manager.graphics[ImageAsset.TABLE]

        for x in range(0, WINDOW_WIDTH, table.get_width()):
            self.display_surface.blit(table, (x, WINDOW_HEIGHT - 80))

    def draw_curtains(self):
        curtain_top = self.asset_manager.graphics[ImageAsset.CURTAIN_TOP]
        curtain_side = self.asset_manager.graphics[ImageAsset.CURTAIN_SIDE]

        self.display_surface.blit(curtain_side, (0, 50))
        self.display_surface.blit(
            pygame.transform.flip(curtain_side, True, False),
            (WINDOW_WIDTH - curtain_side.get_width(), 50),
        )

        for x in range(0, WINDOW_WIDTH, curtain_top.get_width()):
            self.display_surface.blit(curtain_top, (x, 0))

    def update(self):
        self.all_sprites.update()

        if len(self.brown_duck_sprites) < MAX_DUCKS_ON_SCREEN:
            create_brown_duck(
                (self.all_sprites, self.brown_duck_sprites), MAX_DUCKS_ON_SCREEN
            )

        if len(self.yellow_duck_sprites) < MAX_DUCKS_ON_SCREEN:
            create_yellow_duck((self.all_sprites, self.yellow_duck_sprites), -0.5)

    def draw(self):
        self.draw_background()
        self.draw_grass()

        for duck in self.brown_duck_sprites:
            duck.draw()

        self.draw_back_water()

        for duck in self.yellow_duck_sprites:
            duck.draw()

        self.draw_front_water()
        self.draw_table()
        self.draw_curtains()
