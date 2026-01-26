from player.player import Player
from settings import pygame, TILE_SIZE
from sprites.sprite import Sprite

from .constants import LevelLayer, LevelObject


class Level:
    def __init__(self, tmx_map):
        # The main surface on which we will be drawing level elements
        self.display_surface = pygame.display.get_surface()

        # Groups
        self.all_sprites = pygame.sprite.Group()
        # Represents all sprites with which the player object can collide
        self.collision_sprite = pygame.sprite.Group()

        self.setup(tmx_map)

    def setup(self, tmx_map):
        # Get tiles from one specific layer inside the map
        for x, y, surface in tmx_map.get_layer_by_name(str(LevelLayer.TERRAIN.value)).tiles():
            # "x" and "y" are the position coordinates in a Tiles grid. We have to transform them into pixels position
            Sprite((self.all_sprites, self.collision_sprite), surface, (x * TILE_SIZE, y * TILE_SIZE))

        for object in tmx_map.get_layer_by_name(LevelLayer.OBJECTS.value):
            if object.name == LevelObject.PLAYER.value:
                # "x" and "y" are already in pixels position
                Player(self.all_sprites, (object.x, object.y), self.collision_sprite)

    def run(self, delta_time):
        self.all_sprites.update(delta_time)
        self.display_surface.fill("black")
        self.all_sprites.draw(self.display_surface)
