from all_sprites_group import AllSpritesGroup
from player.player import Player
from settings import pygame, TILE_SIZE, Z_Layer
from sprites.animated_sprite import AnimatedSprite
from sprites.constants import MovingDirection
from sprites.moving_sprite import MovingSprite
from sprites.sprite import Sprite

from .constants import (
    LevelLayer,
    LevelObject,
    LevelObjectAssetGroup,
    LevelObjectProperty,
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
                groups = [self.all_sprites]

                match layer:
                    case LevelLayer.BACKGROUND | LevelLayer.FOREGROUND:
                        z_index = Z_Layer.BACKGROUND_TILES.value
                        break
                    case _:
                        z_index = Z_Layer.MAIN.value

                if layer == LevelLayer.TERRAIN:
                    groups.append(self.collision_sprites)
                if layer == LevelLayer.PLATFORMS:
                    groups.append(self.semi_collision_sprites)

                # "x" and "y" are the position coordinates in a Tiles grid. We have to transform them into pixels position
                Sprite(
                    groups=groups,
                    surface=surface,
                    position=(x * TILE_SIZE, y * TILE_SIZE),
                    z_index=z_index,
                )

        for object in tmx_map.get_layer_by_name(LevelLayer.MOVING_OBJECTS.value):
            if object.name == LevelObject.SPIKE.value:
                pass
            else:
                animation_frames = level_frames[object.name]
                groups = (
                    (self.all_sprites, self.semi_collision_sprites)
                    if object.properties[LevelObjectProperty.PLATFORM.value]
                    else (self.all_sprites, self.damage_sprites)
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

                speed = object.properties["speed"]
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
                                groups=self.all_sprites,
                                surface=surface,
                                position=(index, top),
                                z_index=Z_Layer.BACKGROUND_DETAILS.value,
                            )
                    else:
                        left = starting_position[0] - surface.get_width() / 2
                        top, bottom = int(starting_position[1]), int(ending_position[1])

                        for index in range(top, bottom, 20):
                            Sprite(
                                groups=self.all_sprites,
                                surface=surface,
                                position=(left, index),
                                z_index=Z_Layer.BACKGROUND_DETAILS.value,
                            )

        for object in tmx_map.get_layer_by_name(LevelLayer.OBJECTS.value):
            if object.name == LevelObject.PLAYER.value:
                animation_frames = level_frames[object.name]
                # "x" and "y" are already in pixels position
                self.player = Player(
                    groups=self.all_sprites,
                    position=(object.x, object.y),
                    collision_sprites=self.collision_sprites,
                    semi_collision_sprites=self.semi_collision_sprites,
                    animation_frames=animation_frames,
                )
            else:
                if object.name in [LevelObject.BARREL.value, LevelObject.CRATE.value]:
                    Sprite(
                        groups=(self.all_sprites, self.collision_sprites),
                        surface=object.image,
                        position=(object.x, object.y),
                    )
                else:
                    if not LevelObject.PALM.value in object.name:
                        frames = level_frames[object.name]
                        AnimatedSprite(
                            groups=self.all_sprites,
                            position=(object.x, object.y),
                            animation_frames=frames,
                        )

    def run(self, delta_time):
        self.display_surface.fill("black")
        self.all_sprites.update(delta_time)
        self.all_sprites.draw(self.player.hitbox_rect.center)
