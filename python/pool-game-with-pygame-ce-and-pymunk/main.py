import pygame

from game_state.game_state_manager import get_game_state_manager
from input_manager import get_input_manager
from settings import BACKGROUND_COLOR, BOTTOM_PANEL, FPS, WINDOW_HEIGHT, WINDOW_WIDTH
from sprites_manager.sprites_manager import SpritesManager


class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode(
            (WINDOW_WIDTH, WINDOW_HEIGHT + BOTTOM_PANEL)
        )
        pygame.display.set_caption("Python Pool Game")
        self.clock = pygame.time.Clock()

        self.game_state_manager = get_game_state_manager()
        self.input_manager = get_input_manager()
        self.sprites_manager = SpritesManager()

    def update(self):
        self.game_state_manager.update()
        self.input_manager.update()
        self.sprites_manager.update()

    def draw(self):
        self.display_surface.fill(BACKGROUND_COLOR)
        self.sprites_manager.draw()

    def run(self):
        is_running = True

        while is_running:
            self.clock.tick(FPS)

            if self.input_manager.exit_button_clicked:
                is_running = False

            self.update()
            self.draw()

            pygame.display.update()

        pygame.quit()


# To make sure we are running only main.py and not anything else
if __name__ == "__main__":
    game = Game()
    game.run()
