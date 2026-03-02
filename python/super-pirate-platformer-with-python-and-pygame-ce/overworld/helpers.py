from random import randint

from asset_manager.constants import ImageAssetGroup
from settings import pygame, TILE_SIZE, vector, Z_Layer
from sprites.animated_sprite import AnimatedSprite
from sprites.sprite import Sprite

from .constants import OVERWORLD_NODE_NAME, OverworldObjectName
from .sprites.constants import (
    OverworldNodeProperty,
    OverworldPathImage,
    OverworldPathProperty,
)
from .sprites.node import Node
from .sprites.path_sprite import PathSprite
from .sprites.player_icon import PlayerIcon


def create_main_layer(overworld, surface, x, y):
    # "x" and "y" are the position coordinates in a Tiles grid. We have to transform them into pixels position
    Sprite(
        groups=overworld.all_sprites,
        surface=surface,
        position=(x * TILE_SIZE, y * TILE_SIZE),
        z_index=Z_Layer.BACKGROUND_TILES.value,
    )


def create_water(overworld, tmx_map, overworld_frames):
    for column in range(tmx_map.width):
        for row in range(tmx_map.height):
            AnimatedSprite(
                groups=overworld.all_sprites,
                position=(column * TILE_SIZE, row * TILE_SIZE),
                animation_frames=overworld_frames[
                    ImageAssetGroup.OVERWORLD_WATER.value
                ],
                z_index=Z_Layer.BACKGROUND.value,
            )


def create_objects_layer(overworld, overworld_frames, object):
    if object.name == OverworldObjectName.PALM.value:
        frames = overworld_frames[object.name]
        animation_speed = randint(4, 7)

        AnimatedSprite(
            groups=overworld.all_sprites,
            position=(object.x, object.y),
            animation_frames=frames,
            animation_speed=animation_speed,
        )
    else:
        z_index = (
            Z_Layer.BACKGROUND_DETAILS.value
            if object.name == OverworldObjectName.GRASS.value
            else Z_Layer.BACKGROUND_TILES.value
        )
        Sprite(
            groups=overworld.all_sprites,
            surface=object.image,
            position=(object.x, object.y),
            z_index=z_index,
        )


def create_paths_layer(overworld, overworld_frames, object):
    # In Tiled, all the paths start and end in the top left corner of a node,
    # which is more convenient for the Tiled grid system.
    # However, in our overworld map, the nodes are positioned with regards to their center,
    # which is why we need to add "TILE_SIZE / 2" to each coordinates when extracting them from
    # a point.
    position = [(int(point.x), int(point.y)) for point in object.points]
    path_start = object.properties[OverworldNodeProperty.START.value]
    path_end = object.properties[OverworldNodeProperty.END.value]
    overworld.paths[path_end] = {
        OverworldPathProperty.POSITION_POINT: position,
        OverworldPathProperty.START: path_start,
    }


def create_nodes_layer(overworld, overworld_frames, object, game_state):
    if (
        object.name == OVERWORLD_NODE_NAME
        and object.properties[OverworldNodeProperty.STAGE.value]
        == game_state.current_level
    ):
        overworld.player_icon = PlayerIcon(
            groups=overworld.all_sprites,
            position=(object.x + TILE_SIZE / 2, object.y + TILE_SIZE / 2),
            animation_frames=overworld_frames[ImageAssetGroup.ICON.value],
            node_sprites=overworld.node_sprites,
            paths=overworld.paths,
        )

    if object.name == OVERWORLD_NODE_NAME:
        surface = overworld_frames[ImageAssetGroup.PATH.value][
            OVERWORLD_NODE_NAME.lower()
        ]
        # Represents all available paths that lead from a node to another node.
        #
        # Note: In Tiled, the value can contain letter "r" which means reverse.
        # That means this particular paths leaads to a node of a previous level.
        available_paths = {
            key: value
            for key, value in object.properties.items()
            if key
            in [
                OverworldNodeProperty.LEFT.value,
                OverworldNodeProperty.RIGHT.value,
                OverworldNodeProperty.UP.value,
                OverworldNodeProperty.DOWN.value,
            ]
        }

        Node(
            groups=(overworld.all_sprites, overworld.node_sprites),
            surface=surface,
            position=(object.x, object.y),
            level=object.properties[OverworldNodeProperty.STAGE.value],
            available_paths=available_paths,
        )


def create_path_sprites(overworld, overworld_frames):
    nodes = {node.level: vector(node.grid_position) for node in overworld.node_sprites}
    path_tiles = {}

    # Get tiles from path
    for path_id, data in overworld.paths.items():
        path = data[OverworldPathProperty.POSITION_POINT]
        start_node = nodes[data[OverworldPathProperty.START]]
        end_node = nodes[path_id]
        path_tiles[path_id] = [start_node]

        # Get points of all tiles which will be between start node and end node
        for index, points in enumerate(path):
            if index < len(path) - 1:
                start = vector(points)
                end = vector(path[index + 1])
                # The "path_direction" says how many tiles are on the path between start and end point
                path_direction = (end - start) / TILE_SIZE
                start_tile = vector(
                    int(start[0] / TILE_SIZE), int(start[1] / TILE_SIZE)
                )

                if path_direction.x:
                    direction_x = 1 if path_direction.x > 0 else -1
                    for x in range(
                        direction_x, int(path_direction.x) + direction_x, direction_x
                    ):
                        path_tiles[path_id].append(start_tile + vector(x, 0))

                if path_direction.y:
                    direction_y = 1 if path_direction.y > 0 else -1
                    for y in range(
                        direction_y, int(path_direction.y) + direction_y, direction_y
                    ):
                        path_tiles[path_id].append(start_tile + vector(0, y))

        path_tiles[path_id].append(end_node)

    # Create sprites for each of the tile on the path
    for key, path in path_tiles.items():
        for index, tile in enumerate(path):
            if index > 0 and index < len(path) - 1:
                # Using "path[index - 1] - tile" gives us the relationship between the tiles
                # more precisely, if a previous tile is left, right, above or below the next tile
                previous_tile = path[index - 1] - tile
                next_tile = path[index + 1] - tile

                # Tiles are both on the vertical axis
                if previous_tile.x == next_tile.x:
                    surface = overworld_frames[ImageAssetGroup.PATH.value][
                        OverworldPathImage.VERTICAL.value
                    ]
                # Tiles are both on the horizontal axis
                elif previous_tile.y == next_tile.y:
                    surface = overworld_frames[ImageAssetGroup.PATH.value][
                        OverworldPathImage.HORIZONTAL.value
                    ]
                else:
                    # One tile is on vertical and one on horizontal axis
                    # We have to figure out which one is where, so we can draw a correct "turn" tile
                    if (
                        previous_tile.x == -1
                        and next_tile.y == -1
                        or previous_tile.y == -1
                        and next_tile.x == -1
                    ):
                        surface = overworld_frames[ImageAssetGroup.PATH.value][
                            OverworldPathImage.TOP_LEFT.value
                        ]
                    elif (
                        previous_tile.x == 1
                        and next_tile.y == -1
                        or previous_tile.y == -1
                        and next_tile.x == 1
                    ):
                        surface = overworld_frames[ImageAssetGroup.PATH.value][
                            OverworldPathImage.TOP_RIGHT.value
                        ]
                    elif (
                        previous_tile.x == -1
                        and next_tile.y == 1
                        or previous_tile.y == 1
                        and next_tile.x == -1
                    ):
                        surface = overworld_frames[ImageAssetGroup.PATH.value][
                            OverworldPathImage.BOTTOM_LEFT.value
                        ]
                    elif (
                        previous_tile.x == 1
                        and next_tile.y == 1
                        or previous_tile.y == 1
                        and next_tile.x == 1
                    ):
                        surface = overworld_frames[ImageAssetGroup.PATH.value][
                            OverworldPathImage.BOTTOM_RIGHT.value
                        ]
                    else:
                        surface = overworld_frames[ImageAssetGroup.PATH.value][
                            OverworldPathImage.HORIZONTAL.value
                        ]

                PathSprite(
                    groups=overworld.all_sprites,
                    surface=surface,
                    position=(tile.x * TILE_SIZE, tile.y * TILE_SIZE),
                    level=key,
                )
