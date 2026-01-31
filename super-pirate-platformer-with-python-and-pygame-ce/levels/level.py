from asset_manager.asset_manager import get_asset_manager
from asset_manager.constants import ImageAssetGroup
from settings import pygame, TILE_SIZE
from sprites.all_sprites_group import AllSpritesGroup
from sprites.background import Background

from .constants import LevelLayer, LevelDataProperty
from .helpers import (
    create_background_details_layer,
    create_enemies_layer,
    create_items_layer,
    create_moving_objects_layer,
    create_objects_layer,
    create_scenery_layer,
    create_water_layer,
)


class Level:
    def __init__(self, tmx_map):
        asset_manager = get_asset_manager()

        # The main surface on which we will be drawing level elements
        self.display_surface = pygame.display.get_surface()

        # The "tmx_map.width" and "tmx_map.height" are in Tiled columns,
        # we need to transform them into pixels
        self.level_map_width = tmx_map.width * TILE_SIZE
        self.level_map_bottom = tmx_map.height * TILE_SIZE
        # The finishing object rectangle will be assigned during processing level layers
        self.level_finish_rect = None
        tmx_level_properties = tmx_map.get_layer_by_name(LevelLayer.DATA.value)[
            0
        ].properties

        # Groups
        self.all_sprites = AllSpritesGroup(
            level_width=self.level_map_width,
            level_height=self.level_map_bottom,
            top_limit=tmx_level_properties[LevelDataProperty.TOP_LIMIT.value],
        )
        # Represents all sprites with which the player object can collide
        self.collision_sprites = pygame.sprite.Group()
        # Represents all sprites with which the player object can collide but only with his bottom part
        self.semi_collision_sprites = pygame.sprite.Group()
        self.damage_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()

        if tmx_level_properties[LevelDataProperty.BACKGROUND.value]:
            level_background_tile = asset_manager.level_graphics[
                ImageAssetGroup.BACKGROUND_TILES.value
            ][tmx_level_properties[LevelDataProperty.BACKGROUND.value]]
        else:
            level_background_tile = None

        self.background = Background(
            all_sprites_group=self.all_sprites,
            level_width=tmx_map.width,
            level_height=tmx_map.height,
            small_cloud_surfaces=asset_manager.level_graphics[
                ImageAssetGroup.CLOUD_SMALL.value
            ],
            large_cloud_surface=asset_manager.level_graphics[ImageAssetGroup.CLOUD_LARGE.value],
            horizon_line=tmx_level_properties[LevelDataProperty.HORIZON_LINE.value],
            level_background_tile=level_background_tile,
            top_limit=tmx_level_properties[LevelDataProperty.TOP_LIMIT.value],
        )

        # The player object will be assigned during processing level layers
        self.player = None

        self.process_level_layers(tmx_map, asset_manager.level_graphics)

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

        for object in tmx_map.get_layer_by_name(LevelLayer.BACKGROUND_DETAILS.value):
            create_background_details_layer(self, level_frames, object)

        for object in tmx_map.get_layer_by_name(LevelLayer.MOVING_OBJECTS.value):
            create_moving_objects_layer(self, level_frames, object)

        for object in tmx_map.get_layer_by_name(LevelLayer.OBJECTS.value):
            create_objects_layer(self, level_frames, object)

        for object in tmx_map.get_layer_by_name(LevelLayer.ENEMIES.value):
            create_enemies_layer(self, level_frames, object)

        for object in tmx_map.get_layer_by_name(LevelLayer.ITEMS.value):
            create_items_layer(self, level_frames, object)

        for object in tmx_map.get_layer_by_name(LevelLayer.WATER.value):
            create_water_layer(self, level_frames, object)

    def check_map_boundaries(self):
        if self.player.hitbox_rect.left <= 0:
            self.player.hitbox_rect.left = 0
        if self.player.hitbox_rect.right >= self.level_map_width:
            self.player.hitbox_rect.right = self.level_map_width
        if self.player.hitbox_rect.bottom >= self.level_map_width:
            print("Player died")

    def check_level_finish(self):
        if self.player.hitbox_rect.colliderect(self.level_finish_rect):
            print("Player reached the end of the level")

    def run(self, delta_time):
        self.display_surface.fill("black")
        self.all_sprites.update(self.player.hitbox_rect.center, delta_time)
        self.check_map_boundaries()
        self.check_level_finish()
        self.background.draw(delta_time)
        self.all_sprites.draw()
