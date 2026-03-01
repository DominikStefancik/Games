from asset_manager.asset_manager import get_asset_manager
from asset_manager.constants import ImageAssetGroup
from castle.bullet import Bullet
from castle.castle import Castle
from enemy.enemy_group import EnemyGroup
from game_state.game_state import GameState
from game_state.game_state_manager import get_game_state_manager
from settings import pygame, WINDOW_HEIGHT, WINDOW_WIDTH
from timer import Timer

from .button import Button
from .constants import (
    ARMOUR_BUTTON_IMAGE_SCALE,
    ButtonEvent,
    ENEMY_CREATION_INTERVAL,
    REPAIR_BUTTON_IMAGE_SCALE,
)
from .crosshair import Crosshair
from .helpers import get_random_enemy


class SpritesManager:
    def __init__(self):
        # The main surface on which we will be drawing sprites
        self.display_surface = pygame.display.get_surface()
        self.static_sprites = pygame.sprite.Group()
        self.bullet_sprites = pygame.sprite.Group()
        self.enemy_sprites = EnemyGroup()
        self.clock = pygame.time.Clock()

        self.asset_manager = get_asset_manager()
        self.game_state_manager = get_game_state_manager()
        self.castle = Castle(
            group=self.static_sprites,
            images=self.asset_manager.graphics[ImageAssetGroup.CASTLE],
            position=(WINDOW_WIDTH - 430, WINDOW_HEIGHT - 470),
            create_bullet_function=self.create_bullet,
        )
        Crosshair(
            group=self.static_sprites,
            image=self.asset_manager.graphics[ImageAssetGroup.CROSSHAIR],
        )
        Button(
            group=self.static_sprites,
            image=self.asset_manager.graphics[ImageAssetGroup.REPAIR_BUTTON],
            position=(WINDOW_WIDTH - 220, 15),
            scale=REPAIR_BUTTON_IMAGE_SCALE,
            event=ButtonEvent.REPAIR,
        )
        Button(
            group=self.static_sprites,
            image=self.asset_manager.graphics[ImageAssetGroup.ARMOUR_BUTTON],
            position=(WINDOW_WIDTH - 75, 15),
            scale=ARMOUR_BUTTON_IMAGE_SCALE,
            event=ButtonEvent.ARMOUR,
        )
        self.create_enemies_timer = Timer(ENEMY_CREATION_INTERVAL)

        self.game_state_manager.subscribe(self)

    def create_bullet(self, position, angle):
        if self.game_state_manager.game_state == GameState.RUNNING:
            Bullet(
                group=self.bullet_sprites,
                image=self.asset_manager.graphics[ImageAssetGroup.BULLET],
                position=position,
                angle=angle,
            )

    def create_enemies(self):
        if self.game_state_manager.game_state == GameState.RUNNING:
            if (
                not self.game_state_manager.reached_level_difficulty()
                and not self.create_enemies_timer.active
            ):
                enemy = get_random_enemy(self.enemy_sprites, self.asset_manager)
                self.game_state_manager.level_difficulty += enemy.health
                self.game_state_manager.alive_enemies += 1
                self.create_enemies_timer.activate()

    def new_level(self):
        self.bullet_sprites.empty()
        self.enemy_sprites.empty()
        self.create_enemies_timer.deactivate()

    def update(self):
        delta_time = self.clock.tick() / 1000

        self.create_enemies_timer.update()

        self.static_sprites.update()
        self.enemy_sprites.update(delta_time, self.castle, self.bullet_sprites)
        self.bullet_sprites.update(delta_time)

        self.create_enemies()

    def draw(self):
        self.static_sprites.draw(self.display_surface)
        self.enemy_sprites.draw()
        self.bullet_sprites.draw(self.display_surface)
