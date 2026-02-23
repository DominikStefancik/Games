from asset_manager.asset_manager import get_asset_manager
from asset_manager.constants import AudioAsset
from game_state.game_state import GameState
from game_state.game_state_manager import get_game_state_manager
from levels.board import draw_board
from settings import pygame, sys, WINDOW_HEIGHT, WINDOW_WIDTH
from sprites_manager import SpritesManager
from text_manager import TextManager
from timers.timers_manager import get_timers_manager


class Game:
    def __init__(self):
        # The "pygame" module is imported from "settings.py" where there is "import pygame" statement
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Python Pac-Man")

        self.asset_manager = get_asset_manager()
        self.game_state_manager = get_game_state_manager()
        self.sprites_manager = SpritesManager()
        self.text_manager = TextManager()
        self.timers_manager = get_timers_manager()

    def update(self):
        self.timers_manager.update()
        self.sprites_manager.update()
        self.game_state_manager.is_game_won()

    def draw(self):
        self.display_surface.fill("black")
        draw_board(self.display_surface, self.game_state_manager)
        self.sprites_manager.draw()
        self.text_manager.draw()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if (
                    self.game_state_manager.game_state
                    in [GameState.GAME_WON, GameState.GAME_OVER]
                    and event.type == pygame.KEYDOWN
                    and event.key == pygame.K_SPACE
                ):
                    self.game_state_manager.restart_game()

            if self.game_state_manager.game_state == GameState.WAITING_TO_START:
                self.game_state_manager.game_state = GameState.RUNNING
                self.timers_manager.startup_timer.activate()
                self.asset_manager.sounds[AudioAsset.START].play()
            elif self.game_state_manager.game_state == GameState.RUNNING:
                self.update()
                self.draw()

            pygame.display.update()

        pygame.quit()
        sys.exit()


# To make sure we are running only main.py and not anything else
if __name__ == "__main__":
    game = Game()
    game.run()
