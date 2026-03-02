from asset_manager.asset_manager import get_asset_manager
from asset_manager.constants import SoundAsset
from game_state.game_state import GameState
from game_state.game_state_manager import get_game_state_manager
from settings import (
    BACKGROUND_COLOR,
    begin_drawing,
    clear_background,
    close_audio_device,
    close_window,
    end_drawing,
    init_audio_device,
    init_window,
    is_key_pressed,
    KEY_SPACE,
    play_music_stream,
    unload_music_stream,
    update_music_stream,
    WINDOW_HEIGHT,
    WINDOW_WIDTH,
    window_should_close,
)
from sprites.sprite_manager import SpriteManager
from text_manager import TextManager


class Game:
    def __init__(self):
        # The "init_window" function is imported from "settings.py" where there is "from pyray import *" statement
        init_window(WINDOW_WIDTH, WINDOW_HEIGHT, "Python Asteroid Shooter 2D")
        init_audio_device()

        self.asset_manager = get_asset_manager()
        self.game_state_manager = get_game_state_manager()
        self.sprite_manager = SpriteManager()
        self.text_manager = TextManager()
        play_music_stream(self.asset_manager.sounds[SoundAsset.BACKGROUND_MUSIC])

    def update(self):
        if self.game_state_manager.game_state == GameState.RUNNING:
            self.game_state_manager.update_score()

        self.sprite_manager.update()
        update_music_stream(self.asset_manager.sounds[SoundAsset.BACKGROUND_MUSIC])

    def draw(self):
        begin_drawing()
        clear_background(BACKGROUND_COLOR)
        self.text_manager.draw()
        self.sprite_manager.draw()
        end_drawing()

    def run(self):
        while not window_should_close():
            if (
                self.game_state_manager.game_state != GameState.RUNNING
                and is_key_pressed(KEY_SPACE)
            ):
                self.game_state_manager.game_state = GameState.RUNNING

            self.update()
            self.draw()

        unload_music_stream(self.asset_manager.sounds[SoundAsset.BACKGROUND_MUSIC])
        close_audio_device()
        close_window()


# To make sure we are running only main.py and not anything else
if __name__ == "__main__":
    game = Game()
    game.run()
