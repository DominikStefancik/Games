from player.player import Player
from settings import pygame, TILE_SIZE
from sprites.constants import MovingDirection
from sprites.moving_sprite import MovingSprite
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
        # Represents all sprites with which the player object can collide but only with his bottom part
        self.semi_collision_sprite = pygame.sprite.Group()

        self.process_level_layers(tmx_map)

    # Gets objects from the level map layers and creates related game objects
    def process_level_layers(self, tmx_map):
        # Get tiles from one specific layer inside the map
        for x, y, surface in tmx_map.get_layer_by_name(str(LevelLayer.TERRAIN.value)).tiles():
            # "x" and "y" are the position coordinates in a Tiles grid. We have to transform them into pixels position
            Sprite((self.all_sprites, self.collision_sprite), pygame.Surface((TILE_SIZE, TILE_SIZE)), (x * TILE_SIZE, y * TILE_SIZE))

        for object in tmx_map.get_layer_by_name(LevelLayer.MOVING_OBJECTS.value):
            if object.name == LevelObject.HELICOPTER.value:
                if object.width > object.height:
                    moving_direction = MovingDirection.HORIZONTAL
                    starting_position = (object.x, object.y + object.height / 2)
                    ending_position = (object.x + object.width, object.y + object.height / 2)
                else:
                    moving_direction = MovingDirection.VERTICAL
                    starting_position = (object.x + object.width / 2, object.y)
                    ending_position = (object.x + object.width / 2, object.y + object.height)

                speed = object.properties["speed"]
                MovingSprite((self.all_sprites, self.semi_collision_sprite), pygame.Surface((200, 50)), starting_position, ending_position, moving_direction, speed)

        for object in tmx_map.get_layer_by_name(LevelLayer.OBJECTS.value):
            if object.name == LevelObject.PLAYER.value:
                # "x" and "y" are already in pixels position
                Player(self.all_sprites, (object.x, object.y), self.collision_sprite, self.semi_collision_sprite)

    def run(self, delta_time):
        self.display_surface.fill("black")
        self.all_sprites.update(delta_time)
        self.all_sprites.draw(self.display_surface)
