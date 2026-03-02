from asset_manager.asset_manager import get_asset_manager
from asset_manager.constants import FontAsset
from game_state.constants import (
    INCREASE_MAX_HEALTH_COST,
    REPAIR_HEALTH_COST,
    TOWER_COST,
)
from game_state.game_state import GameState
from game_state.game_state_manager import get_game_state_manager
from settings import pygame, WINDOW_HEIGHT, WINDOW_WIDTH


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
        font = self.asset_manager.fonts[FontAsset.FUTURA_25]
        self.draw_text(
            f"Level: {self.game_state_manager.current_level}",
            font,
            "black",
            (15, 15),
        )
        self.draw_text(
            f"Score: {self.game_state_manager.score}", font, "black", (185, 15)
        )
        self.draw_text(
            f"Best Score: {self.game_state_manager.best_score}",
            font,
            "black",
            (185, 45),
        )
        self.draw_text(
            f"Money: {self.game_state_manager.money}",
            font,
            "black",
            (WINDOW_HEIGHT / 2 + 120, 15),
        )
        self.draw_text(
            f"Health: {self.game_state_manager.health} / {self.game_state_manager.max_health}",
            font,
            "black",
            (WINDOW_WIDTH - 400, WINDOW_HEIGHT - 100),
        )
        self.draw_text(
            f"{REPAIR_HEALTH_COST}",
            font,
            "black",
            (WINDOW_WIDTH - 270, 60),
        )
        self.draw_text(
            f"{TOWER_COST}",
            font,
            "black",
            (WINDOW_WIDTH - 175, 60),
        )
        self.draw_text(
            f"{INCREASE_MAX_HEALTH_COST}",
            font,
            "black",
            (WINDOW_WIDTH - 80, 60),
        )

    def draw_new_level(self):
        font = self.asset_manager.fonts[FontAsset.FUTURA_60]
        self.draw_text(
            f"LEVEL {self.game_state_manager.current_level}",
            font,
            "white",
            (WINDOW_WIDTH / 2 - 150, WINDOW_HEIGHT / 2 + 20),
        )

    def draw_level_complete(self):
        font = self.asset_manager.fonts[FontAsset.FUTURA_60]
        self.draw_text(
            "LEVEL COMPLETE!",
            font,
            "white",
            (WINDOW_WIDTH / 2 - 300, WINDOW_HEIGHT / 2 + 20),
        )

    def draw_game_won(self):
        pass

    def draw_game_over(self):
        pass

    def draw(self):
        self.draw_status()

        match self.game_state_manager.game_state:
            case GameState.WAITING_TO_START:
                self.draw_new_level()
            case GameState.LEVEL_WON:
                self.draw_level_complete()
            case GameState.GAME_WON:
                self.draw_game_won()
            case GameState.GAME_OVER:
                self.draw_game_over()
