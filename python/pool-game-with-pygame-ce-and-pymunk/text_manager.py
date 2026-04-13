import pygame

from asset_manager.asset_manager import get_asset_manager
from asset_manager.constants import FontAsset
from game_state.game_state import GameState
from game_state.game_state_manager import get_game_state_manager
from settings import WHITE_COLOR, WINDOW_HEIGHT, WINDOW_WIDTH


class TextManager:
    def __init__(self):
        # The main surface on which we will be drawing text
        self.display_surface = pygame.display.get_surface()

        self.asset_manager = get_asset_manager()
        self.game_state_manager = get_game_state_manager()

    def draw_text(self, text, font, text_color, position):
        image = font.render(text, True, text_color)
        self.display_surface.blit(image, position)

    def draw_status(self):
        font = self.asset_manager.fonts[FontAsset.FUTURA_30]
        self.draw_text(
            f"LIVES: {self.game_state_manager.lives}",
            font,
            WHITE_COLOR,
            (WINDOW_WIDTH - 200, WINDOW_HEIGHT + 5),
        )

    def draw_game_won(self):
        font = self.asset_manager.fonts[FontAsset.FUTURA_60]
        self.draw_text(
            f"YOU WIN!",
            font,
            WHITE_COLOR,
            (WINDOW_WIDTH / 2 - 160, WINDOW_HEIGHT / 2 - 130),
        )
        font = self.asset_manager.fonts[FontAsset.FUTURA_30]
        self.draw_text(
            f"Press Space bar to play again",
            font,
            WHITE_COLOR,
            (WINDOW_WIDTH / 2 - 210, WINDOW_HEIGHT / 2 + 60),
        )

    def draw_game_over(self):
        font = self.asset_manager.fonts[FontAsset.FUTURA_60]
        self.draw_text(
            f"GAME OVER",
            font,
            WHITE_COLOR,
            (WINDOW_WIDTH / 2 - 200, WINDOW_HEIGHT / 2 - 130),
        )
        font = self.asset_manager.fonts[FontAsset.FUTURA_30]
        self.draw_text(
            f"Press Space bar to play again",
            font,
            WHITE_COLOR,
            (WINDOW_WIDTH / 2 - 210, WINDOW_HEIGHT / 2 + 60),
        )

    def draw(self):
        self.draw_status()
        self.draw_game_won()

        match self.game_state_manager.game_state:
            case GameState.WAITING_TO_START:
                pass
            case GameState.GAME_WON:
                self.draw_game_won()
            case GameState.GAME_OVER:
                self.draw_game_over()
