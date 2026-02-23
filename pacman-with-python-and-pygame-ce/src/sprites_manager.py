from asset_manager.asset_manager import get_asset_manager
from asset_manager.constants import ImageAsset
from game_state.game_state_manager import get_game_state_manager
from ghost.constants import GhostType
from ghost.ghost import Ghost
from pacman.pacman import PacMan
from settings import pygame
from timers.timers_manager import get_timers_manager


class SpritesManager:
    def __init__(self):
        # The main surface on which we will be drawing sprites
        self.clock = pygame.time.Clock()
        self.timers_manager = get_timers_manager()
        self.game_state_manager = get_game_state_manager()

        self.display_surface = pygame.display.get_surface()
        self.all_sprites = pygame.sprite.Group()
        self.create_sprites()

        self.game_state_manager.subscribe(self)

    def create_sprites(self):
        # First we have to remove sprites we created before, so the old objects don't have old references
        # (this is necessary when we restart the game)
        self.all_sprites.empty()

        asset_manager = get_asset_manager()
        pacman = PacMan(
            groups=self.all_sprites,
            animation_frames=asset_manager.graphics[ImageAsset.PACMAN],
        )
        Ghost(groups=self.all_sprites, type=GhostType.BLINKY, pacman=pacman)
        Ghost(groups=self.all_sprites, type=GhostType.PINKY, pacman=pacman)
        Ghost(groups=self.all_sprites, type=GhostType.INKY, pacman=pacman)
        Ghost(groups=self.all_sprites, type=GhostType.CLYDE, pacman=pacman)

    def restart_all(self):
        for sprite in self.all_sprites:
            sprite.restart()

    def recreate_all(self):
        self.create_sprites()

    def update(self):
        delta_time = self.clock.tick() / 1000

        if not self.timers_manager.startup_timer.active:
            self.all_sprites.update(delta_time)

    def draw(self):
        self.all_sprites.draw(self.display_surface)
