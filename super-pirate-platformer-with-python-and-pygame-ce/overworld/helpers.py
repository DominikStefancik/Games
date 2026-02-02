from random import randint

from asset_manager.constants import ImageAssetGroup
from settings import pygame, TILE_SIZE, Z_Layer
from sprites.animated_sprite import AnimatedSprite
from sprites.node import Node
from sprites.player_icon import PlayerIcon
from sprites.sprite import Sprite

from .constants import OverworldObjectName, OverworldNodeProperty, OverworldPathProperty


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
        object.name == OverworldObjectName.NODE.value
        and object.properties[OverworldNodeProperty.STAGE.value]
        == game_state.current_level
    ):
        overworld.player_icon = PlayerIcon(
            groups=overworld.all_sprites,
            position=(object.x + TILE_SIZE / 2, object.y + TILE_SIZE / 2),
            animation_frames=overworld_frames[ImageAssetGroup.ICON.value],
        )

    if object.name == OverworldObjectName.NODE.value:
        surface = overworld_frames[ImageAssetGroup.PATH.value][
            OverworldObjectName.NODE.value.lower()
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
