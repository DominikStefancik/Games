from asset_manager.asset_manager import get_asset_manager
from asset_manager.constants import AudioAsset, ImageAssetGroup
from castle.bullet import Bullet
from castle.castle import Castle
from castle.constants import TowerState
from castle.helpers import get_tower_image
from castle.tower import Tower
from enemy.constants import EnemyAnimation
from enemy.enemy_group import EnemyGroup
from game_state.constants import MAX_TOWER_COUNT
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
        self.tower_sprites = pygame.sprite.Group()
        self.bullet_sprites = pygame.sprite.Group()
        self.enemy_sprites = EnemyGroup()
        self.clock = pygame.time.Clock()

        self.asset_manager = get_asset_manager()
        self.game_state_manager = get_game_state_manager()
        self.castle = Castle(
            group=self.static_sprites,
            images=self.asset_manager.graphics[ImageAssetGroup.CASTLE],
            create_bullet_function=self.create_bullet,
        )
        self.crosshair = Crosshair(
            group=self.static_sprites,
            image=self.asset_manager.graphics[ImageAssetGroup.CROSSHAIR],
        )
        Button(
            group=self.static_sprites,
            image=self.asset_manager.graphics[ImageAssetGroup.REPAIR_BUTTON],
            position=(WINDOW_WIDTH - 270, 15),
            scale=REPAIR_BUTTON_IMAGE_SCALE,
            event=ButtonEvent.REPAIR,
        )
        Button(
            group=self.static_sprites,
            image=get_tower_image(
                self.asset_manager.graphics[ImageAssetGroup.TOWER],
                TowerState.FULLY_RESTORED,
            ),
            position=(WINDOW_WIDTH - 160, 10),
            scale=0.1,
            event=ButtonEvent.TOWER,
        )
        Button(
            group=self.static_sprites,
            image=self.asset_manager.graphics[ImageAssetGroup.ARMOUR_BUTTON],
            position=(WINDOW_WIDTH - 75, 15),
            scale=ARMOUR_BUTTON_IMAGE_SCALE,
            event=ButtonEvent.ARMOUR,
        )
        self.create_enemies_timer = Timer(ENEMY_CREATION_INTERVAL)

        self.tower_positions = [
            (WINDOW_WIDTH - 400, WINDOW_HEIGHT - 260),
            (WINDOW_WIDTH - 290, WINDOW_HEIGHT - 260),
            (WINDOW_WIDTH - 160, WINDOW_HEIGHT - 290),
            (WINDOW_WIDTH - 75, WINDOW_HEIGHT - 290),
        ]

        self.march_sound_started = False

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

                # Start marching sound when the first enemy is created
                if not self.march_sound_started:
                    self.asset_manager.sounds[AudioAsset.MARCH].play()
                    self.march_sound_started = True

    def create_tower(self):
        if (
            self.game_state_manager.game_state == GameState.RUNNING
            and len(self.tower_sprites) < MAX_TOWER_COUNT
        ):
            Tower(
                group=self.tower_sprites,
                images=self.asset_manager.graphics[ImageAssetGroup.TOWER],
                position=self.tower_positions[len(self.tower_sprites)],
                create_bullet_function=self.create_bullet,
            )

    def new_level(self):
        self.bullet_sprites.empty()
        self.enemy_sprites.empty()
        self.create_enemies_timer.deactivate()
        self.march_sound_started = False

    def restart(self):
        self.bullet_sprites.empty()
        self.enemy_sprites.empty()
        self.tower_sprites.empty()
        self.crosshair = Crosshair(
            group=self.static_sprites,
            image=self.asset_manager.graphics[ImageAssetGroup.CROSSHAIR],
        )
        self.create_enemies_timer.deactivate()
        self.march_sound_started = False

    def update(self):
        delta_time = self.clock.tick() / 1000

        self.create_enemies_timer.update()

        self.static_sprites.update()
        self.tower_sprites.update(self.enemy_sprites)
        self.enemy_sprites.update(delta_time, self.castle, self.bullet_sprites)
        self.bullet_sprites.update(delta_time)

        self.create_enemies()

        # At the end of the game don't show the Crosshair anymore
        if self.game_state_manager.game_state in [
            GameState.GAME_WON,
            GameState.GAME_OVER,
        ]:
            self.crosshair.kill()

        if self.game_state_manager.game_state in [
            GameState.LEVEL_WON,
            GameState.GAME_WON,
        ]:
            self.asset_manager.sounds[AudioAsset.MARCH].stop()

        for enemy in self.enemy_sprites:
            # Stop marching sound whenever the first enemy starts attacking the castle
            if enemy.animation == EnemyAnimation.ATTACK:
                self.asset_manager.sounds[AudioAsset.MARCH].stop()
                break

    def draw(self):
        self.static_sprites.draw(self.display_surface)
        self.tower_sprites.draw(self.display_surface)
        self.enemy_sprites.draw()
        self.bullet_sprites.draw(self.display_surface)
