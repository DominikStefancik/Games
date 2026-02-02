from asset_manager.asset_manager import get_asset_manager
from asset_manager.constants import ImageAssetGroup
from game_state.game_state import get_game_state
from settings import pygame
from timer import Timer

from .heart import Heart


class Ui:
    def __init__(self):
        asset_manager = get_asset_manager()

        # The main surface on which we will be drawing UI elements
        self.display_surface = pygame.display.get_surface()
        self.font = asset_manager.font
        self.sprites = pygame.sprite.Group()
        self.heart_frames = asset_manager.ui_graphics[ImageAssetGroup.HEART.value]

        self.coin_surface = asset_manager.ui_graphics[ImageAssetGroup.COIN.value]
        self.coins = 0

        game_state = get_game_state()
        game_state.subscribe_ui(self)

    def create_hearts(self, amount):
        for sprite in self.sprites:
            sprite.kill()

        heart_surface_width = self.heart_frames[0].get_width()
        heart_padding = 5

        for heart_index in range(amount):
            x = 10 + heart_index * (heart_surface_width + heart_padding)
            Heart(self.sprites, (x, 10), self.heart_frames)

    def update_coins(self, amount):
        self.coins = amount

    def display_coins_text(self):
        text_surface = self.font.render(str(self.coins), False, "#33323d")
        text_rect = text_surface.get_frect(topleft=(40, 34))
        self.display_surface.blit(text_surface, text_rect)
        coins_rect = self.coin_surface.get_frect(center=text_rect.midleft).move(-20, -3)
        self.display_surface.blit(self.coin_surface, coins_rect)

    def refresh(self, game_state):
        self.create_hearts(game_state.player_health)
        self.update_coins(game_state.collected_coins)

    def update(self, delta_time):
        self.sprites.update(delta_time)
        self.sprites.draw(self.display_surface)
        self.display_coins_text()
