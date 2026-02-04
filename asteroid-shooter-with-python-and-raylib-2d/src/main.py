from asset_manager.asset_manager import get_asset_manager
from asset_manager.constants import ImageAsset
from settings import (
    BACKGROUND_COLOR,
    begin_drawing,
    clear_background,
    close_window,
    end_drawing,
    get_frame_time,
    init_window,
    Vector2,
    WINDOW_HEIGHT,
    WINDOW_WIDTH,
    window_should_close,
)
from sprites.spaceship import Spaceship


class Game:
    def __init__(self):
        # The "init_window" function is imported from "settings.py" where there is "from pyray import *" statement
        init_window(WINDOW_WIDTH, WINDOW_HEIGHT, "Python Asteroid Shooter 2D")

        asset_manager = get_asset_manager()
        self.spaceship = Spaceship(
            asset_manager.textures[ImageAsset.SPACESHIP],
            Vector2(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2),
        )

    def run(self):
        while not window_should_close():
            delta_time = get_frame_time()

            self.spaceship.update(delta_time)

            begin_drawing()
            clear_background(BACKGROUND_COLOR)
            self.spaceship.draw()
            end_drawing()

        close_window()


# To make sure we are running only main.py and not anything else
if __name__ == "__main__":
    game = Game()
    game.run()
