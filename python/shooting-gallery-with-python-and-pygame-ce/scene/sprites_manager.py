from random import choice

import pygame

from asset_manager.asset_manager import get_asset_manager
from asset_manager.constants import AudioAsset, ImageAsset
from crosshair import Crosshair
from game_state.game_state import GameState
from game_state.game_state_manager import get_game_state_manager
from settings import WINDOW_WIDTH

from .constants import DUCK_IMAGE_WIDTH, GAP_BETWEEN_DUCKS, MAX_DUCKS_IN_SCENE
from .helpers import create_brown_duck, create_yellow_duck


class SpritesManager:
    def __init__(self):
        self.asset_manager = get_asset_manager()
        self.game_state_manager = get_game_state_manager()
        self.crosshair = Crosshair(
            group=self.game_state_manager.static_sprites,
            image=self.asset_manager.graphics[ImageAsset.CROSSHAIR],
        )

        self.create_brown_ducks()
        self.create_yellow_ducks()

        self.game_state_manager.subscribe(self)

    def create_brown_ducks(self):
        for index in range(MAX_DUCKS_IN_SCENE):
            position_x = (
                index * (DUCK_IMAGE_WIDTH + GAP_BETWEEN_DUCKS) * 2
            ) + WINDOW_WIDTH / 2
            create_brown_duck(
                self.game_state_manager.brown_duck_sprites,
                position_x,
            )

    def create_yellow_ducks(self):
        for index in range(MAX_DUCKS_IN_SCENE):
            position_x = (
                index * (DUCK_IMAGE_WIDTH + GAP_BETWEEN_DUCKS) * 2 - WINDOW_WIDTH / 2
            )
            create_yellow_duck(
                self.game_state_manager.yellow_duck_sprites,
                -position_x,
            )

    def restart(self):
        self.create_brown_ducks()
        self.create_yellow_ducks()
        self.crosshair = Crosshair(
            group=self.game_state_manager.static_sprites,
            image=self.asset_manager.graphics[ImageAsset.CROSSHAIR],
        )

    def new_round(self):
        self.create_brown_ducks()
        self.create_yellow_ducks()

    def detect_collision_with_duck(self):
        if pygame.mouse.get_just_pressed()[0]:
            self.game_state_manager.remaining_bullets_count -= 1
            duck_shot = False
            mouse_position = pygame.mouse.get_pos()

            for duck in (
                self.game_state_manager.yellow_duck_sprites.sprites()
                + self.game_state_manager.brown_duck_sprites.sprites()
            ):
                if not duck.is_hit and duck.rect.collidepoint(mouse_position):
                    duck.is_hit = True
                    self.game_state_manager.score += duck.points
                    duck_shot = True

                    random_hit_sound = choice(
                        [
                            AudioAsset.METAL_HIT_1,
                            AudioAsset.METAL_HIT_2,
                            AudioAsset.METAL_HIT_3,
                            AudioAsset.METAL_HIT_4,
                            AudioAsset.METAL_HIT_5,
                            AudioAsset.METAL_HIT_6,
                            AudioAsset.METAL_HIT_7,
                            AudioAsset.METAL_HIT_8,
                            AudioAsset.METAL_HIT_9,
                        ]
                    )
                    hit_sound = self.asset_manager.sounds[random_hit_sound]
                    hit_sound.play()
                    break

            if not duck_shot:
                shot_sound = self.asset_manager.sounds[AudioAsset.GUN_SHOT]
                shot_sound.play()

    def update(self):
        if self.game_state_manager.game_state != GameState.GAME_OVER:
            self.game_state_manager.static_sprites.update()
            self.game_state_manager.brown_duck_sprites.update()
            self.game_state_manager.yellow_duck_sprites.update()

        if self.game_state_manager.game_state == GameState.RUNNING:
            # With the higher round difficulty (and the speed of ducks's movement),
            # it happens that the group is empty that's why we have to use creating ducks as a group
            if len(self.game_state_manager.brown_duck_sprites) == 0:
                self.create_brown_ducks()
            elif (
                0 < len(self.game_state_manager.brown_duck_sprites) < MAX_DUCKS_IN_SCENE
            ):
                last_duck = self.game_state_manager.brown_duck_sprites.sprites()[-1]

                create_brown_duck(
                    self.game_state_manager.brown_duck_sprites,
                    last_duck.rect.left
                    + (DUCK_IMAGE_WIDTH + GAP_BETWEEN_DUCKS) * 2
                    + DUCK_IMAGE_WIDTH / 2,
                )

            # With the higher round difficulty (and the speed of ducks's movement),
            # it happens that the group is empty that's why we have to use creating ducks as a group
            if len(self.game_state_manager.yellow_duck_sprites) == 0:
                self.create_yellow_ducks()
            elif (
                0
                < len(self.game_state_manager.yellow_duck_sprites)
                < MAX_DUCKS_IN_SCENE
            ):
                last_duck = self.game_state_manager.yellow_duck_sprites.sprites()[-1]

                create_yellow_duck(
                    self.game_state_manager.yellow_duck_sprites,
                    last_duck.rect.right
                    - (DUCK_IMAGE_WIDTH + GAP_BETWEEN_DUCKS) * 2
                    - DUCK_IMAGE_WIDTH / 2,
                )

            self.detect_collision_with_duck()

    def draw(self):
        if self.game_state_manager.game_state != GameState.GAME_OVER:
            self.crosshair.draw()
