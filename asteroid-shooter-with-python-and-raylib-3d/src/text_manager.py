from asset_manager.asset_manager import get_asset_manager
from asset_manager.constants import FontAsset
from game_state.game_state import GameState
from game_state.game_state_manager import get_game_state_manager
from settings import (
    BIGGER_FONT_SIZE,
    draw_rectangle_rounded_lines_ex,
    draw_text_ex,
    FONT_SIZE,
    FONT_SPACING,
    get_time,
    Rectangle,
    SMALLER_FONT_SIZE,
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

        draw_text_ex(
            font,
            score,
            Vector2(WINDOW_WIDTH - 320, WINDOW_HEIGHT - 108.5),
            FONT_SIZE,
            FONT_SPACING,
            WHITE,
        )

        draw_rectangle_rounded_lines_ex(
            Rectangle(
                WINDOW_WIDTH - 330,
                WINDOW_HEIGHT - 115,
                self.get_rectangle_width(score),
                80,
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
        draw_text_ex(
            font,
            text,
            Vector2(WINDOW_WIDTH / 2 - 450, WINDOW_HEIGHT / 2 - 120),
            BIGGER_FONT_SIZE,
            FONT_SPACING,
            WHITE,
        )

        text = "PRESS SPACE TO START"
        draw_text_ex(
            font,
            text,
            Vector2(WINDOW_WIDTH / 2 - 335, WINDOW_HEIGHT / 2 + 30),
            SMALLER_FONT_SIZE,
            FONT_SPACING,
            WHITE,
        )

    def draw_game_over_text(self):
        asset_manager = get_asset_manager()

        font = asset_manager.fonts[FontAsset.STORMFAZE]
        text = "GAME OVER!"
        draw_text_ex(
            font,
            text,
            Vector2(WINDOW_WIDTH / 2 - 250, WINDOW_HEIGHT / 2 - 120),
            BIGGER_FONT_SIZE,
            FONT_SPACING,
            WHITE,
        )

        text = "PRESS SPACE TO PLAY AGAIN"
        draw_text_ex(
            font,
            text,
            Vector2(WINDOW_WIDTH / 2 - 400, WINDOW_HEIGHT / 2 + 30),
            SMALLER_FONT_SIZE,
            FONT_SPACING,
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

    # This is an ugly hack to calculate the width of the rounded rectangle manually
    # because calling the Raylib function "measure_text_ex" on the score text somehow returns
    # always Vector(0, 0)
    def get_rectangle_width(self, score):
        length = len(score)

        match length:
            case 1:
                divider = 1.3
            case 2:
                divider = 0.75
            case 3:
                divider = 0.51
            case 4:
                divider = 0.385
            case 5:
                divider = 0.32
            case 6:
                divider = 0.267
            case _:
                divider = 0.1

        return FONT_SIZE / divider
