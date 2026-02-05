from asset_manager.asset_manager import get_asset_manager
from asset_manager.constants import FontAsset, SoundAsset
from settings import (
    BACKGROUND_COLOR,
    begin_drawing,
    clear_background,
    close_audio_device,
    close_window,
    draw_rectangle_rounded_lines_ex,
    draw_text_ex,
    end_drawing,
    FONT_SIZE,
    get_time,
    init_audio_device,
    init_window,
    measure_text_ex,
    play_music_stream,
    Rectangle,
    unload_music_stream,
    update_music_stream,
    Vector2,
    WHITE,
    WINDOW_HEIGHT,
    WINDOW_WIDTH,
    window_should_close,
)
from sprites.sprite_manager import SpriteManager


class Game:
    def __init__(self):
        # The "init_window" function is imported from "settings.py" where there is "from pyray import *" statement
        init_window(WINDOW_WIDTH, WINDOW_HEIGHT, "Python Asteroid Shooter 2D")
        init_audio_device()

        self.asset_manager = get_asset_manager()
        self.sprite_manager = SpriteManager()
        play_music_stream(self.asset_manager.sounds[SoundAsset.BACKGROUND_MUSIC])

    def draw_score(self):
        score = int(get_time())
        font = self.asset_manager.fonts[FontAsset.STORMFAZE]
        text_size = measure_text_ex(font, str(score), FONT_SIZE, 0)
        draw_text_ex(
            font,
            str(score),
            Vector2(WINDOW_WIDTH / 2 - text_size.x / 2, 100),
            FONT_SIZE,
            0,
            WHITE,
        )

        draw_rectangle_rounded_lines_ex(
            Rectangle(
                WINDOW_WIDTH / 2 - text_size.x / 2 - 10, 95, text_size.x + 20, 80
            ),
            0.3,
            0,
            8,
            WHITE,
        )

    def update(self):
        self.sprite_manager.update()
        update_music_stream(self.asset_manager.sounds[SoundAsset.BACKGROUND_MUSIC])

    def draw(self):
        begin_drawing()
        clear_background(BACKGROUND_COLOR)
        self.draw_score()
        self.sprite_manager.draw()
        end_drawing()

    def run(self):
        while not window_should_close():
            self.update()
            self.draw()

        unload_music_stream(self.asset_manager.sounds[SoundAsset.BACKGROUND_MUSIC])
        close_audio_device()
        close_window()


# To make sure we are running only main.py and not anything else
if __name__ == "__main__":
    game = Game()
    game.run()
