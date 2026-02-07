from asset_manager.asset_manager import get_asset_manager
from asset_manager.constants import FontAsset
from settings import (
    draw_rectangle_rounded_lines_ex,
    draw_text_ex,
    FONT_SIZE,
    FONT_SPACING,
    get_time,
    Rectangle,
    Vector2,
    WHITE,
    WINDOW_HEIGHT,
    WINDOW_WIDTH,
)


class TextManager:
    def draw_score(self):
        asset_manager = get_asset_manager()
        score = str(int(get_time()))
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

    def draw(self):
        self.draw_score()

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
