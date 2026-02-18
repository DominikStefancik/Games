from asset_manager.asset_manager import get_asset_manager
from asset_manager.constants import ImageAsset
from game_state.game_state_manager import get_game_state_manager
from ghost.constants import GhostType
from ghost.ghost import Ghost
from levels.board import draw_board
from pacman.pacman import PacMan
from settings import pygame, sys, WINDOW_HEIGHT, WINDOW_WIDTH
from text_manager import TextManager
from timers.timers_manager import get_timers_manager


class Game:
    def __init__(self):
        # The "pygame" module is imported from "settings.py" where there is "import pygame" statement
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Python Pac-Man")
        self.clock = pygame.time.Clock()

        asset_manager = get_asset_manager()
        self.text_manager = TextManager()
        self.timers_manager = get_timers_manager()
        self.all_sprites = pygame.sprite.Group()
        pacman = PacMan(
            groups=self.all_sprites,
            animation_frames=asset_manager.graphics[ImageAsset.PACMAN],
        )
        Ghost(groups=self.all_sprites, type=GhostType.BLINKY, pacman=pacman)
        Ghost(groups=self.all_sprites, type=GhostType.PINKY, pacman=pacman)
        Ghost(groups=self.all_sprites, type=GhostType.INKY, pacman=pacman)
        Ghost(groups=self.all_sprites, type=GhostType.CLYDE, pacman=pacman)

        game_state_manager = get_game_state_manager()
        self.level_config = game_state_manager.get_level_config()
        self.level_layout = game_state_manager.get_level_layout()

    def update(self, delta_time):
        self.timers_manager.update()
        self.all_sprites.update(delta_time)

    def draw(self):
        self.display_surface.fill("black")
        draw_board(self.display_surface, self.level_layout, self.level_config)
        self.all_sprites.draw(self.display_surface)
        self.text_manager.draw()

    def run(self):
        while True:
            delta_time = self.clock.tick() / 1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.update(delta_time)
            self.draw()

            pygame.display.update()

        pygame.quit()
        sys.exit()


# To make sure we are running only main.py and not anything else
if __name__ == "__main__":
    game = Game()
    game.run()
