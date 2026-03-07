import pygame

from asset_manager.asset_manager import get_asset_manager
from asset_manager.constants import ImageAsset
from game_state.game_state_manager import get_game_state_manager
from settings import WINDOW_HEIGHT

from .helpers import get_digit_image


class StatusManager:
    def __init__(self):
        # The main surface on which we will be drawing elements
        self.display_surface = pygame.display.get_surface()

        self.asset_manager = get_asset_manager()
        self.game_state_manager = get_game_state_manager()

    def draw_score(self):
        score = self.asset_manager.graphics[ImageAsset.SCORE]
        colon = self.asset_manager.graphics[ImageAsset.COLON]

        self.display_surface.blit(score, (5, 5))
        self.display_surface.blit(colon, (5 + score.get_width() + 1, 8))

        digit_x = score.get_width() + colon.get_width() + 21
        for digit in str(self.game_state_manager.score):
            self.display_surface.blit(get_digit_image(digit), (digit_x, 5))
            digit_x += 25

    def draw_bullets(self):
        bullet = self.asset_manager.graphics[ImageAsset.BULLET]

        for index in range(self.game_state_manager.remaining_bullets_count):
            self.display_surface.blit(bullet, (index * 30 + 100, WINDOW_HEIGHT - 60))

    def draw(self):
        self.draw_score()
        self.draw_bullets()
