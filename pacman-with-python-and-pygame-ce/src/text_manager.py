from asset_manager.asset_manager import get_asset_manager
from asset_manager.constants import FontAsset, ImageAsset
from game_state.game_state import GameState
from game_state.game_state_manager import get_game_state_manager
from levels.constants import Level
from settings import pygame, WINDOW_HEIGHT, WINDOW_WIDTH
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

    def draw_level(self):
        font = self.asset_manager.fonts[FontAsset.FREE_SANS_BOLD_20]
        level_text = font.render(
            f"Level: {self.game_state_manager.current_level.value}", True, "white"
        )
        self.display_surface.blit(level_text, (10, 920))

    def draw_score(self):
        font = self.asset_manager.fonts[FontAsset.FREE_SANS_BOLD_20]
        score_text = font.render(
            f"Score: {self.game_state_manager.score}", True, "white"
        )
        self.display_surface.blit(score_text, (110, 920))

    def draw_power_up(self):
        if self.timers_manager.power_up_timer.active:
            pygame.draw.circle(self.display_surface, "blue", (250, 930), 15)

    def draw_lives(self):
        for index in range(self.game_state_manager.lives):
            self.display_surface.blit(self.pacman_image, (650 + index * 40, 915))

    def draw_game_won(self):
        font = self.asset_manager.fonts[FontAsset.FREE_SANS_BOLD_35]
        pygame.draw.rect(
            self.display_surface,
            "white",
            (50, WINDOW_HEIGHT / 2 - 150, 800, 300),
            2,
            10,
        )
        pygame.draw.rect(
            self.display_surface,
            "dark gray",
            (70, WINDOW_HEIGHT / 2 - 130, 760, 260),
            0,
            10,
        )
        game_won_text = font.render("You won!!!", True, "green")
        restart_text = font.render("Press Space to restart", True, "green")
        self.display_surface.blit(
            game_won_text, (WINDOW_WIDTH / 2 - 80, WINDOW_HEIGHT / 2 - 60)
        )
        self.display_surface.blit(
            restart_text, (WINDOW_WIDTH / 2 - 180, WINDOW_HEIGHT / 2 + 20)
        )

    def draw_game_over(self):
        font = self.asset_manager.fonts[FontAsset.FREE_SANS_BOLD_35]
        pygame.draw.rect(
            self.display_surface,
            "white",
            (50, WINDOW_HEIGHT / 2 - 150, 800, 300),
            2,
            10,
        )
        pygame.draw.rect(
            self.display_surface,
            "dark gray",
            (70, WINDOW_HEIGHT / 2 - 130, 760, 260),
            0,
            10,
        )
        game_over_text = font.render("Game Over!", True, "red")
        restart_text = font.render("Press Space to restart", True, "red")
        self.display_surface.blit(
            game_over_text, (WINDOW_WIDTH / 2 - 100, WINDOW_HEIGHT / 2 - 60)
        )
        self.display_surface.blit(
            restart_text, (WINDOW_WIDTH / 2 - 180, WINDOW_HEIGHT / 2 + 20)
        )

    def draw(self):
        self.draw_level()
        self.draw_score()
        self.draw_power_up()
        self.draw_lives()

        if self.game_state_manager.game_state == GameState.GAME_WON:
            self.draw_game_won()
        elif self.game_state_manager.game_state == GameState.GAME_OVER:
            self.draw_game_over()
