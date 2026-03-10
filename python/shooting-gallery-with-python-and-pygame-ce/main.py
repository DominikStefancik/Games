import pygame

from asset_manager.asset_manager import get_asset_manager
from asset_manager.constants import AudioAsset
from game_state.game_state import GameState
from game_state.game_state_manager import get_game_state_manager
from input_manager import get_input_manager
from settings import FPS, WINDOW_HEIGHT, WINDOW_WIDTH
from scene.scene_manager import SceneManager
from scene.sprites_manager import SpritesManager
from scene.status_manager import StatusManager


class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Python Shooting Gallery")
        self.clock = pygame.time.Clock()

        self.game_state_manager = get_game_state_manager()
        self.input_manager = get_input_manager()
        self.scene_manager = SceneManager()
        self.status_manager = StatusManager()
        self.sprites_manager = SpritesManager()

    def update(self):
        self.game_state_manager.update()
        self.input_manager.update()
        self.sprites_manager.update()

    def draw(self):
        self.scene_manager.draw()
        self.sprites_manager.draw()
        self.status_manager.draw()

    def run(self):
        is_running = True

        asset_manager = get_asset_manager()
        asset_manager.sounds[AudioAsset.FUN_FAIR].play(-1)

        while is_running:
            self.clock.tick(FPS)

            if self.input_manager.exit_button_clicked:
                is_running = False

            if (
                self.game_state_manager.game_state == GameState.GAME_OVER
                and self.input_manager.left_mouse_clicked
                and not self.game_state_manager.game_over_timer.active
            ):
                self.game_state_manager.restart()
                asset_manager.sounds[AudioAsset.FUN_FAIR].play(-1)

            self.update()
            self.draw()

            pygame.display.update()

        pygame.quit()


# To make sure we are running only main.py and not anything else
if __name__ == "__main__":
    game = Game()
    game.run()
