import pygame

from asset_manager.asset_manager import get_asset_manager
from asset_manager.constants import ImageAsset
from crosshair import Crosshair
from game_state.game_state import GameState
from game_state.game_state_manager import get_game_state_manager

from .constants import MAX_DUCKS_ON_SCREEN
from .helpers import create_brown_duck, create_yellow_duck


class SpritesManager:
    def __init__(self):
        self.asset_manager = get_asset_manager()
        self.game_state_manager = get_game_state_manager()
        self.crosshair = Crosshair(
            group=self.game_state_manager.all_sprites,
            image=self.asset_manager.graphics[ImageAsset.CROSSHAIR],
        )

        self.create_brown_ducks()
        self.create_yellow_ducks()

    def create_brown_ducks(self):
        for index in range(MAX_DUCKS_ON_SCREEN):
            create_brown_duck(
                (
                    self.game_state_manager.all_sprites,
                    self.game_state_manager.brown_duck_sprites,
                ),
                index,
            )

    def create_yellow_ducks(self):
        for index in range(MAX_DUCKS_ON_SCREEN):
            create_yellow_duck(
                (
                    self.game_state_manager.all_sprites,
                    self.game_state_manager.yellow_duck_sprites,
                ),
                index,
            )

    def detect_collision_with_duck(self):
        if pygame.mouse.get_just_pressed()[0]:
            mouse_position = pygame.mouse.get_pos()

            for duck in (
                self.game_state_manager.brown_duck_sprites.sprites()
                + self.game_state_manager.yellow_duck_sprites.sprites()
            ):
                if not duck.is_hit and duck.rect.collidepoint(mouse_position):
                    duck.is_hit = True
                    self.game_state_manager.score += duck.points
                    break

            self.game_state_manager.remaining_bullets_count -= 1

    def update(self):
        self.game_state_manager.all_sprites.update()

        if len(self.game_state_manager.brown_duck_sprites) < MAX_DUCKS_ON_SCREEN:
            create_brown_duck(
                (
                    self.game_state_manager.all_sprites,
                    self.game_state_manager.brown_duck_sprites,
                ),
                MAX_DUCKS_ON_SCREEN,
            )

        if len(self.game_state_manager.yellow_duck_sprites) < MAX_DUCKS_ON_SCREEN:
            create_yellow_duck(
                (
                    self.game_state_manager.all_sprites,
                    self.game_state_manager.yellow_duck_sprites,
                ),
                -0.5,
            )

        self.detect_collision_with_duck()

    def draw(self):
        self.crosshair.draw()
