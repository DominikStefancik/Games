from asset_manager.asset_manager import get_asset_manager
from asset_manager.constants import ImageAssetGroup
from game_state import get_game_state
from settings import pygame
from sprites.constants import NodePathDirection

from .all_sprites_group import AllSpritesGroup
from .constants import OverworldLayer, OverworldPathProperty
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

        # The player icon object will be assigned during processing overworld layers
        self.player_icon = None

        self.process_overworld_layers(
            tmx_map, asset_manager.overworld_graphics, game_state
        )

        # A node the player icon is currently standing on
        # At the start, the player will be standing on the node with the level 0
        self.current_node = [node for node in self.node_sprites if node.level == 0][0]

    # Gets objects from the overworld map layers and creates related game objects
    def process_overworld_layers(self, tmx_map, overworld_frames, game_state):
        create_water(self, tmx_map, overworld_frames)

        for layer in [OverworldLayer.MAIN, OverworldLayer.TOP]:
            # Get tiles from one specific layer inside the map
            for x, y, surface in tmx_map.get_layer_by_name(layer.value).tiles():
                create_main_layer(self, surface, x, y)

        for object in tmx_map.get_layer_by_name(OverworldLayer.OBJECTS.value):
            create_objects_layer(self, overworld_frames, object)

        self.paths = {}
        for object in tmx_map.get_layer_by_name(OverworldLayer.PATHS.value):
            create_paths_layer(self, overworld_frames, object)

        for object in tmx_map.get_layer_by_name(OverworldLayer.NODES.value):
            create_nodes_layer(self, overworld_frames, object, game_state)

    def process_key_input(self):
        keys = pygame.key.get_pressed()

        # Allow reaction to key strokes only if the player icon is standing on a node
        if self.current_node and not self.player_icon.current_path:
            if keys[pygame.K_LEFT] and self.current_node.has_path_in_direction(
                NodePathDirection.LEFT.value
            ):
                self.move(NodePathDirection.LEFT.value)
            if keys[pygame.K_RIGHT] and self.current_node.has_path_in_direction(
                NodePathDirection.RIGHT.value
            ):
                self.move(NodePathDirection.RIGHT.value)
            if keys[pygame.K_UP] and self.current_node.has_path_in_direction(
                NodePathDirection.UP.value
            ):
                self.move(NodePathDirection.UP.value)
            if keys[pygame.K_DOWN] and self.current_node.has_path_in_direction(
                NodePathDirection.DOWN.value
            ):
                self.move(NodePathDirection.DOWN.value)

    def move(self, direction):
        # In Tiled, the value can contain letter "r" which means reverse.
        # That means this particular paths leaads to a node of a previous level.
        # That also means we have to extract the number from a string.
        path_key = int(self.current_node.available_paths[direction][0])
        is_reverse_path = self.current_node.available_paths[direction][-1] == "r"
        # Get all position points from a path if it is not reverse
        # If it is reverse, get the points in a reverse order
        path_points = (
            self.paths[path_key][OverworldPathProperty.POSITION_POINT][:]
            if not is_reverse_path
            else self.paths[path_key][OverworldPathProperty.POSITION_POINT][::-1]
        )
        self.player_icon.start_move(path_points)

    def update_current_node(self):
        nodes = pygame.sprite.spritecollide(self.player_icon, self.node_sprites, False)

        if nodes:
            self.current_node = nodes[0]

    def run(self, delta_time):
        self.process_key_input()
        self.update_current_node()
        self.all_sprites.update(delta_time)
        self.all_sprites.draw(self.player_icon.rect.center)
