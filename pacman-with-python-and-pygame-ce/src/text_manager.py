from asset_manager.asset_manager import get_asset_manager
from asset_manager.constants import FontAsset
from game_state.game_state_manager import get_game_state_manager
from settings import pygame


class TextManager:
    def __init__(self):
        # The main surface on which we will be drawing text
        self.display_surface = pygame.display.get_surface()

        self.game_state_manager = get_game_state_manager()

    def draw_score(self):
        asset_manager = get_asset_manager()
        font = asset_manager.fonts[FontAsset.FREE_SANS_BOLD]
        score_text = font.render(
            f"Score: {self.game_state_manager.score}", True, "white"
        )
        self.display_surface.blit(score_text, (10, 920))

    def draw(self):
        self.draw_score()
