from asset_manager.asset_manager import get_asset_manager
from asset_manager.constants import FontAsset
from game_state.game_state import GameState
from game_state.game_state_manager import get_game_state_manager
from settings import (
    BIGGER_FONT_SIZE,
    draw_rectangle_rounded_lines_ex,
    draw_text_ex,
    FONT_SIZE,
    measure_text_ex,
    Rectangle,
    Vector2,
    WHITE,
    WINDOW_HEIGHT,
    WINDOW_WIDTH,
)


class TextManager:
    def __init__(self):
        self.game_state_manager = get_game_state_manager()

    def draw_score(self):
        asset_manager = get_asset_manager()
        score = str(self.game_state_manager.score)
        font = asset_manager.fonts[FontAsset.STORMFAZE]
        text_size = measure_text_ex(font, score, FONT_SIZE, 0)
        draw_text_ex(
            font,
            score,
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

    def draw_game_start_text(self):
        asset_manager = get_asset_manager()

        font = asset_manager.fonts[FontAsset.STORMFAZE]
        text = "ASTEROID SHOOTER"
        text_size = measure_text_ex(font, text, BIGGER_FONT_SIZE, 0)
        draw_text_ex(
            font,
            text,
            Vector2(WINDOW_WIDTH / 2 - text_size.x / 2, WINDOW_HEIGHT / 2 - 120),
            BIGGER_FONT_SIZE,
            0,
            WHITE,
        )

        text = "PRESS SPACE TO START"
        text_size = measure_text_ex(font, text, FONT_SIZE, 0)
        draw_text_ex(
            font,
            text,
            Vector2(WINDOW_WIDTH / 2 - text_size.x / 2, WINDOW_HEIGHT / 2 + 30),
            FONT_SIZE,
            0,
            WHITE,
        )

    def draw_game_over_text(self):
        asset_manager = get_asset_manager()

        font = asset_manager.fonts[FontAsset.STORMFAZE]
        text = "GAME OVER!"
        text_size = measure_text_ex(font, text, BIGGER_FONT_SIZE, 0)
        draw_text_ex(
            font,
            text,
            Vector2(WINDOW_WIDTH / 2 - text_size.x / 2, WINDOW_HEIGHT / 2 - 120),
            BIGGER_FONT_SIZE,
            0,
            WHITE,
        )

        text = "PRESS SPACE TO PLAY AGAIN"
        text_size = measure_text_ex(font, text, FONT_SIZE, 0)
        draw_text_ex(
            font,
            text,
            Vector2(WINDOW_WIDTH / 2 - text_size.x / 2, WINDOW_HEIGHT / 2 + 30),
            FONT_SIZE,
            0,
            WHITE,
        )

    def draw(self):
        match self.game_state_manager.game_state:
            case GameState.WAITING_TO_START:
                self.draw_game_start_text()
            case GameState.RUNNING:
                self.draw_score()
            case GameState.GAME_OVER:
                self.draw_score()
                self.draw_game_over_text()
