# PyTMX is a map loader for python/pygame designed for games.
# It provides smart tile loading with a fast and efficient storage base.
# It supports Pygame, Pyglet and Pysdl2
#
# The module allows us to load map data as Pygame surfaces
from pytmx.util_pygame import load_pygame

from game_state import get_game_state
from loaders import load_font, load_level_graphics, load_ui_graphics
from levels.constants import OMNI_PATH
from levels.level import Level
from settings import pygame, sys, WINDOW_HEIGHT, WINDOW_WIDTH
from ui.ui import Ui


class Game:
    def __init__(self):
        # The "pygame" module is imported from "settings.py" where there is "import pygame" statement
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Python Super Pirate Platformer")
        self.clock = pygame.time.Clock()
        self.import_assets()
        self.ui = Ui(self.font, self.ui_frames)
        self.level_maps = {0: load_pygame(OMNI_PATH)}

        self.current_stage = Level(self.level_maps[0], self.level_frames)

        game_state = get_game_state()
        game_state.subscribe(self.ui)

    def import_assets(self):
        self.level_frames = load_level_graphics()
        self.ui_frames = load_ui_graphics()
        self.font = load_font()

    def run(self):
        while True:
            delta_time = self.clock.tick() / 1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.current_stage.run(delta_time)
            self.ui.update(delta_time)

            pygame.display.update()


# To make sure we are running only main.py and not anything else
if __name__ == "__main__":
    game = Game()
    game.run()
