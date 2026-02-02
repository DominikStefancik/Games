from asset_manager.asset_manager import get_asset_manager
from asset_manager.constants import AudioAssetFile
from game_state.constants import GameStage
from game_state.game_state import get_game_state
from level.level import Level
from overworld.overworld import Overworld
from settings import pygame, sys, WINDOW_HEIGHT, WINDOW_WIDTH
from ui.ui import Ui


class Game:
    def __init__(self):
        # The "pygame" module is imported from "settings.py" where there is "import pygame" statement
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Python Super Pirate Platformer")
        self.clock = pygame.time.Clock()

        asset_manager = get_asset_manager()
        self.level_maps = asset_manager.level_maps
        self.overworld_map = asset_manager.overworld_map

        self.game_state = get_game_state()
        self.game_state.subscribe_stage(self)
        self.update_stage(GameStage.LEVEL)

        self.ui = Ui()
        asset_manager.audio_files[AudioAssetFile.BACKGROUND_MUSIC].play(loops=-1)

    def update_stage(self, stage):
        match stage:
            case GameStage.LEVEL:
                self.current_stage = Level(
                    self.level_maps[self.game_state.unlocked_level]
                )
            case GameStage.OVERWORLD:
                self.current_stage = Overworld(self.overworld_map)

    def check_game_over(self):
        if self.game_state.player_health <= 0:
            pygame.quit()
            sys.exit()

    def run(self):
        while True:
            delta_time = self.clock.tick() / 1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.check_game_over()
            self.current_stage.run(delta_time)
            self.ui.update(delta_time)

            pygame.display.update()


# To make sure we are running only main.py and not anything else
if __name__ == "__main__":
    game = Game()
    game.run()
