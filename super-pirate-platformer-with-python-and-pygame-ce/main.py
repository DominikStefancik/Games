# PyTMX is a map loader for python/pygame designed for games.
# It provides smart tile loading with a fast and efficient storage base.
# It supports Pygame, Pyglet and Pysdl2
#
# The module allows us to load map data as Pygame surfaces
from pytmx.util_pygame import load_pygame

from import_helpers import *
from levels.constants import LevelObjectAssetGroup, OMNI_PATH
from levels.level import Level
from settings import pygame, sys, WINDOW_HEIGHT, WINDOW_WIDTH


class Game:
    def __init__(self):
        # The "pygame" module is imported from "settings.py" where there is "import pygame" statement
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Python Super Pirate Platformer")
        self.clock = pygame.time.Clock()
        self.import_assets()
        self.level_maps = {0: load_pygame(OMNI_PATH)}

        self.current_stage = Level(self.level_maps[0], self.level_frames)

    def import_assets(self):
        self.level_frames = {
            LevelObjectAssetGroup.FLAG.value: import_folder(
                "assets", "graphics", "level", "flag"
            ),
            LevelObjectAssetGroup.SAW.value: import_folder(
                "assets", "graphics", "enemies", "saw", "animation"
            ),
            LevelObjectAssetGroup.FLOOR_SPIKE.value: import_folder(
                "assets", "graphics", "enemies", "floor_spikes"
            ),
            LevelObjectAssetGroup.PALM.value: import_subfolders_as_dict(
                "assets", "graphics", "level", "palms"
            ),
            LevelObjectAssetGroup.CANDLE.value: import_folder(
                "assets", "graphics", "level", "candle"
            ),
            LevelObjectAssetGroup.WINDOW.value: import_folder(
                "assets", "graphics", "level", "window"
            ),
            LevelObjectAssetGroup.BIG_CHAIN.value: import_folder(
                "assets", "graphics", "level", "big_chains"
            ),
            LevelObjectAssetGroup.SMALL_CHAIN.value: import_folder(
                "assets", "graphics", "level", "small_chains"
            ),
            LevelObjectAssetGroup.CANDLE_LIGHT.value: import_folder(
                "assets", "graphics", "level", "candle_light"
            ),
            LevelObjectAssetGroup.PLAYER.value: import_subfolders_as_dict(
                "assets", "graphics", "player"
            ),
        }

    def run(self):
        while True:
            delta_time = self.clock.tick() / 1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.current_stage.run(delta_time)

            pygame.display.update()


# To make sure we are running only main.py and not anything else
if __name__ == "__main__":
    game = Game()
    game.run()
