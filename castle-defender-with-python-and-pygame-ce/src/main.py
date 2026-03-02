from game_state.game_state import GameState
from game_state.game_state_manager import get_game_state_manager
from scene_manager.scene_manager import SceneManager
from settings import pygame, sys, WINDOW_HEIGHT, WINDOW_WIDTH
from sprites.constants import ButtonEvent
from sprites.sprites_manager import SpritesManager
from text_manager import TextManager


class Game:
    def __init__(self):
        # The "pygame" module is imported from "settings.py" where there is "import pygame" statement
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Python Castle Defender")

        self.game_state_manager = get_game_state_manager()
        self.scene_manager = SceneManager()
        self.sprites_manager = SpritesManager()
        self.text_manager = TextManager()

    def update(self):
        self.game_state_manager.update()

        if not self.game_state_manager.game_state in [
            GameState.GAME_WON,
            GameState.GAME_OVER,
        ]:
            self.sprites_manager.update()

    def draw(self):
        self.display_surface.fill("black")
        self.scene_manager.draw()
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
                    self.game_state_manager.restart()
                elif self.game_state_manager.game_state == GameState.RUNNING:
                    if event.type == ButtonEvent.REPAIR.value:
                        self.game_state_manager.repair_health()

                    if event.type == ButtonEvent.TOWER.value:
                        self.game_state_manager.add_tower()

                    if event.type == ButtonEvent.ARMOUR.value:
                        self.game_state_manager.increase_max_health()

            self.update()
            self.draw()

            pygame.display.update()

        pygame.quit()
        sys.exit()


# To make sure we are running only main.py and not anything else
if __name__ == "__main__":
    game = Game()
    game.run()
