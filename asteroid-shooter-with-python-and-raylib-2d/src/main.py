from asset_manager.asset_manager import get_asset_manager
from asset_manager.constants import ImageAsset
from helpers import create_stars_data
from settings import (
    BACKGROUND_COLOR,
    begin_drawing,
    clear_background,
    close_window,
    draw_texture_ex,
    end_drawing,
    get_frame_time,
    init_window,
    Vector2,
    WHITE,
    WINDOW_HEIGHT,
    WINDOW_WIDTH,
    window_should_close,
)
from sprites.spaceship import Spaceship


class Game:
    def __init__(self):
        # The "init_window" function is imported from "settings.py" where there is "from pyray import *" statement
        init_window(WINDOW_WIDTH, WINDOW_HEIGHT, "Python Asteroid Shooter 2D")

        self.asset_manager = get_asset_manager()
        self.all_sprites = []
        Spaceship(
            group=self.all_sprites,
            texture=self.asset_manager.textures[ImageAsset.SPACESHIP],
            position=Vector2(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2),
        )
        self.star_data = create_stars_data()

    def draw_stars(self):
        for star in self.star_data:
            # With the function "draw_texture_ex" we can set a texture's rotation and a scale
            draw_texture_ex(
                self.asset_manager.textures[ImageAsset.STAR], star[0], 0, star[1], WHITE
            )

    def update(self):
        delta_time = get_frame_time()

        for sprite in self.all_sprites:
            sprite.update(delta_time)

        self.remove_sprites()

    def draw(self):
        begin_drawing()
        clear_background(BACKGROUND_COLOR)
        self.draw_stars()

        for sprite in self.all_sprites:
            sprite.draw()
        end_drawing()

    def remove_sprites(self):
        for index, sprite in enumerate(self.all_sprites):
            if sprite.to_be_removed:
                self.all_sprites.pop(index)

    def run(self):
        while not window_should_close():
            self.update()
            self.draw()

        close_window()


# To make sure we are running only main.py and not anything else
if __name__ == "__main__":
    game = Game()
    game.run()
