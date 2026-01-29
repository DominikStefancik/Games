from enemies.shell import Shell
from enemies.tooth import Tooth
from player.player import Player
from settings import TILE_SIZE, Z_Layer
from sprites.animated_sprite import AnimatedSprite
from sprites.constants import MovingDirection
from sprites.item import Item
from sprites.moving_sprite import MovingSprite
from sprites.spiked_ball import SpikedBall
from sprites.spiked_chain import SpikedChain
from sprites.sprite import Sprite

from .constants import (
    LevelLayer,
    LevelObject,
    LevelObjectAssetGroup,
    LevelObjectProperty,
)


def create_scenery_layer(level, layer, surface, x, y):
    groups = [level.all_sprites]

    match layer:
        case LevelLayer.BACKGROUND | LevelLayer.FOREGROUND:
            z_index = Z_Layer.BACKGROUND_TILES.value
        case _:
            z_index = Z_Layer.MAIN.value

    if layer == LevelLayer.TERRAIN:
        groups.append(level.collision_sprites)
    if layer == LevelLayer.PLATFORMS:
        groups.append(level.semi_collision_sprites)

    # "x" and "y" are the position coordinates in a Tiles grid. We have to transform them into pixels position
    Sprite(
        groups=groups,
        surface=surface,
        position=(x * TILE_SIZE, y * TILE_SIZE),
        z_index=z_index,
    )


def create_objects_layer(level, level_frames, object):
    if object.name == LevelObject.PLAYER.value:
        animation_frames = level_frames[object.name]

        # "x" and "y" are already in pixels position
        level.player = Player(
            groups=level.all_sprites,
            position=(object.x, object.y),
            collision_sprites=level.collision_sprites,
            semi_collision_sprites=level.semi_collision_sprites,
            attackable_sprites=level.attackable_sprites,
            damage_sprites=level.damage_sprites,
            animation_frames=animation_frames,
        )
    else:
        if object.name in [LevelObject.BARREL.value, LevelObject.CRATE.value]:
            Sprite(
                groups=(level.all_sprites, level.collision_sprites),
                surface=object.image,
                position=(object.x, object.y),
            )
        else:
            frames = level_frames[object.name]
            AnimatedSprite(
                groups=level.all_sprites,
                position=(object.x, object.y),
                animation_frames=frames,
            )


def create_moving_objects_layer(level, level_frames, object):
    if object.name == LevelObject.SPIKE.value:
        radius = object.properties[LevelObjectProperty.RADIUS.value]

        SpikedBall(
            groups=(level.all_sprites, level.damage_sprites),
            surface=level_frames[LevelObjectAssetGroup.SPIKED_BALL.value],
            position=(
                object.x + object.width / 2,
                object.y + object.height / 2,
            ),
            radius=radius,
            start_angle=object.properties[LevelObjectProperty.START_ANGLE.value],
            end_angle=object.properties[LevelObjectProperty.END_ANGLE.value],
            speed=object.properties[LevelObjectProperty.SPEED.value],
        )
        for radius in range(0, radius, 20):
            SpikedChain(
                groups=level.all_sprites,
                surface=level_frames[LevelObjectAssetGroup.SPIKED_CHAIN.value],
                position=(
                    object.x + object.width / 2,
                    object.y + object.height / 2,
                ),
                radius=radius,
                start_angle=object.properties[LevelObjectProperty.START_ANGLE.value],
                end_angle=object.properties[LevelObjectProperty.END_ANGLE.value],
                speed=object.properties[LevelObjectProperty.SPEED.value],
                z_index=Z_Layer.BACKGROUND_DETAILS.value,
            )

    else:
        animation_frames = level_frames[object.name]
        groups = (
            (level.all_sprites, level.semi_collision_sprites)
            if object.properties[LevelObjectProperty.PLATFORM.value]
            else (level.all_sprites, level.damage_sprites)
        )

        if object.width > object.height:
            moving_direction = MovingDirection.HORIZONTAL
            starting_position = (object.x, object.y + object.height / 2)
            ending_position = (
                object.x + object.width,
                object.y + object.height / 2,
            )
        else:
            moving_direction = MovingDirection.VERTICAL
            starting_position = (object.x + object.width / 2, object.y)
            ending_position = (
                object.x + object.width / 2,
                object.y + object.height,
            )

        speed = object.properties[LevelObjectProperty.SPEED.value]
        MovingSprite(
            groups=groups,
            start_position=starting_position,
            end_position=ending_position,
            moving_direction=moving_direction,
            speed=speed,
            animation_frames=animation_frames,
            flip=object.properties[LevelObjectProperty.FLIP.value],
        )

        if object.name == LevelObject.SAW.value:
            surface = level_frames[LevelObjectAssetGroup.SAW_CHAIN.value]

            if moving_direction == MovingDirection.HORIZONTAL:
                top = starting_position[1] - surface.get_height() / 2
                left, right = int(starting_position[0]), int(ending_position[0])

                for index in range(left, right, 20):
                    Sprite(
                        groups=level.all_sprites,
                        surface=surface,
                        position=(index, top),
                        z_index=Z_Layer.BACKGROUND_DETAILS.value,
                    )
            else:
                left = starting_position[0] - surface.get_width() / 2
                top, bottom = int(starting_position[1]), int(ending_position[1])

                for index in range(top, bottom, 20):
                    Sprite(
                        groups=level.all_sprites,
                        surface=surface,
                        position=(left, index),
                        z_index=Z_Layer.BACKGROUND_DETAILS.value,
                    )


def create_enemies_layer(level, level_frames, object):
    animation_frames = level_frames[object.name]

    if object.name == LevelObject.TOOTH.value:
        Tooth(
            groups=(level.all_sprites, level.damage_sprites, level.attackable_sprites),
            position=(object.x, object.y),
            collision_sprites=level.collision_sprites,
            animation_frames=animation_frames,
        )
    elif object.name == LevelObject.SHELL.value:
        Shell(
            groups=(level.all_sprites, level.collision_sprites),
            position=(object.x, object.y),
            animation_frames=animation_frames,
            reverse=object.properties[LevelObjectProperty.REVERSE.value],
            player=level.player,
            pearl_groups=(
                level.all_sprites,
                level.damage_sprites,
                level.attackable_sprites,
            ),
            pearl_animation_frames=level_frames[LevelObjectAssetGroup.PEARL.value],
            collision_sprites=level.collision_sprites,
        )


def create_items_layer(level, level_frames, object):
    Item(
        groups=level.all_sprites,
        item_type=object.name,
        position=(object.x + TILE_SIZE / 2, object.y + TILE_SIZE / 2),
        animation_frames=level_frames[LevelObjectAssetGroup.ITEMS.value][object.name],
        particle_groups=level.all_sprites,
        particle_effect_animation_frames=level_frames[
            LevelObjectAssetGroup.PARTICLE.value
        ],
        player=level.player,
    )
