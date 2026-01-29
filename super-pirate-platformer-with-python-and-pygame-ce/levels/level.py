from all_sprites_group import AllSpritesGroup
from settings import pygame

from .constants import LevelLayer
from .helpers import (
    create_enemies_layer,
    create_items_layer,
    create_moving_objects_layer,
    create_objects_layer,
    create_scenery_layer,
)


class Level:
    def __init__(self, tmx_map, level_frames):
        # The main surface on which we will be drawing level elements
        self.display_surface = pygame.display.get_surface()

        # Groups
        self.all_sprites = AllSpritesGroup()
        # Represents all sprites with which the player object can collide
        self.collision_sprites = pygame.sprite.Group()
        # Represents all sprites with which the player object can collide but only with his bottom part
        self.semi_collision_sprites = pygame.sprite.Group()
        self.damage_sprites = pygame.sprite.Group()
        self.tooth_sprites = pygame.sprite.Group()

        # The player object will be assigned during processing level layers
        self.player = None

        self.process_level_layers(tmx_map, level_frames)

    # Gets objects from the level map layers and creates related game objects
    def process_level_layers(self, tmx_map, level_frames):
        for layer in [
            LevelLayer.BACKGROUND,
            LevelLayer.TERRAIN,
            LevelLayer.FOREGROUND,
            LevelLayer.PLATFORMS,
        ]:
            # Get tiles from one specific layer inside the map
            for x, y, surface in tmx_map.get_layer_by_name(layer.value).tiles():
                create_scenery_layer(self, layer, surface, x, y)

        for object in tmx_map.get_layer_by_name(LevelLayer.MOVING_OBJECTS.value):
            create_moving_objects_layer(self, level_frames, object)

        for object in tmx_map.get_layer_by_name(LevelLayer.OBJECTS.value):
            create_objects_layer(self, level_frames, object)

        for object in tmx_map.get_layer_by_name(LevelLayer.ENEMIES.value):
            create_enemies_layer(self, level_frames, object)

        for object in tmx_map.get_layer_by_name(LevelLayer.ITEMS.value):
            create_items_layer(self, level_frames, object)
    def run(self, delta_time):
        self.display_surface.fill("black")
        self.all_sprites.update(delta_time)
        self.all_sprites.draw(self.player.hitbox_rect.center)
