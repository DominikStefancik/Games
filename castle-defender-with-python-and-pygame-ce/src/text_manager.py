from asset_manager.asset_manager import get_asset_manager
from asset_manager.constants import FontAsset
from game_state.game_state import GameState
from game_state.game_state_manager import get_game_state_manager
from settings import pygame, WINDOW_HEIGHT, WINDOW_WIDTH


class TextManager:
    def __init__(self):
        # The main surface on which we will be drawing text
        self.display_surface = pygame.display.get_surface()

        self.asset_manager = get_asset_manager()
        self.game_state_manager = get_game_state_manager()

    def draw_new_level(self):
        font = self.asset_manager.fonts[FontAsset.FUTURA_60]
        level_text = font.render(
            f"LEVEL {self.game_state_manager.current_level}", True, "white"
        )
        self.display_surface.blit(
            level_text, (WINDOW_WIDTH / 2 - 150, WINDOW_HEIGHT / 2 + 20)
        )

    def draw_level_complete(self):
        font = self.asset_manager.fonts[FontAsset.FUTURA_60]
        level_text = font.render("LEVEL COMPLETE!", True, "white")
        self.display_surface.blit(
            level_text, (WINDOW_WIDTH / 2 - 300, WINDOW_HEIGHT / 2 + 20)
        )

    def draw_game_won(self):
        pass

    def draw_game_over(self):
        pass

    def draw(self):
        match self.game_state_manager.game_state:
            case GameState.WAITING_TO_START:
                self.draw_new_level()
            case GameState.LEVEL_WON:
                self.draw_level_complete()
            case GameState.GAME_WON:
                self.draw_game_won()
            case GameState.GAME_OVER:
                self.draw_game_over()
