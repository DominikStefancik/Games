from asset_manager.asset_manager import get_asset_manager
from asset_manager.constants import FontAsset, ImageAsset
from game_state.game_state_manager import get_game_state_manager
from settings import pygame
from timers.timers_manager import get_timers_manager


class TextManager:
    def __init__(self):
        # The main surface on which we will be drawing text
        self.display_surface = pygame.display.get_surface()

        self.asset_manager = get_asset_manager()
        self.game_state_manager = get_game_state_manager()
        self.timers_manager = get_timers_manager()

        original_pacman_image = self.asset_manager.graphics[ImageAsset.PACMAN][0]
        self.pacman_image = pygame.transform.scale(original_pacman_image, (30, 30))

    def draw_score(self):
        font = self.asset_manager.fonts[FontAsset.FREE_SANS_BOLD]
        score_text = font.render(
            f"Score: {self.game_state_manager.score}", True, "white"
        )
        self.display_surface.blit(score_text, (10, 920))

    def draw_power_up(self):
        if self.timers_manager.power_up_timer.active:
            pygame.draw.circle(self.display_surface, "blue", (150, 930), 15)

    def draw_lives(self):
        for index in range(self.game_state_manager.lives):
            self.display_surface.blit(self.pacman_image, (650 + index * 40, 915))

    def draw(self):
        self.draw_score()
        self.draw_power_up()
        self.draw_lives()
