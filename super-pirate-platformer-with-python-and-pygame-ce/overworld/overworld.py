from asset_manager.asset_manager import get_asset_manager
from asset_manager.constants import ImageAssetGroup
from game_state import get_game_state
from settings import pygame

from .all_sprites_group import AllSpritesGroup
from .constants import OverworldLayer
from .helpers import (
    create_main_layer,
    create_nodes_layer,
    create_paths_layer,
    create_objects_layer,
    create_water,
)


class Overworld:
    def __init__(self, tmx_map):
        asset_manager = get_asset_manager()
        game_state = get_game_state()

        self.display_surface = pygame.display.get_surface()
        self.all_sprites = AllSpritesGroup()
        self.node_sprites = pygame.sprite.Group()
        self.paths = {}

        # The player icon object will be assigned during processing overworld layers
        self.player_icon = None

        self.process_overworld_layers(
            tmx_map, asset_manager.overworld_graphics, game_state
        )

    # Gets objects from the overworld map layers and creates related game objects
    def process_overworld_layers(self, tmx_map, overworld_frames, game_state):
        create_water(self, tmx_map, overworld_frames)

        for layer in [OverworldLayer.MAIN, OverworldLayer.TOP]:
            # Get tiles from one specific layer inside the map
            for x, y, surface in tmx_map.get_layer_by_name(layer.value).tiles():
                create_main_layer(self, surface, x, y)

        for object in tmx_map.get_layer_by_name(OverworldLayer.OBJECTS.value):
            create_objects_layer(self, overworld_frames, object)

        for object in tmx_map.get_layer_by_name(OverworldLayer.PATHS.value):
            create_paths_layer(self, overworld_frames, object)

        for object in tmx_map.get_layer_by_name(OverworldLayer.NODES.value):
            create_nodes_layer(self, overworld_frames, object, game_state)

    def run(self, delta_time):
        self.all_sprites.update(delta_time)
        self.all_sprites.draw(self.player_icon.rect.center)
