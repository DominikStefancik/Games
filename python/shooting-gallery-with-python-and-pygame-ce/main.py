import pygame

from game_state.game_state import GameState
from game_state.game_state_manager import get_game_state_manager
from settings import FPS, WINDOW_HEIGHT, WINDOW_WIDTH
from scene_manager.scene_manager import SceneManager
from scene_manager.sprites_manager import SpritesManager


class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Python Shooting Gallery")
        self.clock = pygame.time.Clock()

        self.game_state_manager = get_game_state_manager()
        self.scene_manager = SceneManager()
        self.sprites_manager = SpritesManager()

    def update(self):
        self.game_state_manager.update()
        self.sprites_manager.update()

    def draw(self):
        self.scene_manager.draw()
        self.sprites_manager.draw()

    def run(self):
        is_running = True

        while is_running:
            self.clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    is_running = False

            self.update()
            self.draw()

            pygame.display.update()

        pygame.quit()


# To make sure we are running only main.py and not anything else
if __name__ == "__main__":
    game = Game()
    game.run()
