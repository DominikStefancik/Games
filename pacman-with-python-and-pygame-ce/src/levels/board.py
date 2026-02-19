import math

from settings import pygame

from .constants import (
    BIG_DOT_RADIUS,
    BoardTile,
    DOT_RADIUS,
    LINE_THICKNESS,
    TILE_HEIGHT,
    TILE_WIDTH,
)


def draw_board(surface, game_state_manager):
    config = game_state_manager.get_level_config()
    layout = game_state_manager.get_level_layout()

    for row in range(len(layout)):
        for column in range(len(layout[row])):
            layout_tile = layout[row][column]

            match layout_tile:
                case BoardTile.EMPTY_BLACK_RECTANGLE.value:
                    pass
                case BoardTile.DOT.value:
                    pygame.draw.circle(
                        surface,
                        config["dot_color"],
                        (
                            (column * TILE_WIDTH + TILE_WIDTH / 2),
                            (row * TILE_HEIGHT + TILE_HEIGHT / 2),
                        ),
                        DOT_RADIUS,
                    )
                case BoardTile.BIG_DOT.value:
                    pygame.draw.circle(
                        surface,
                        config["dot_color"],
                        (
                            (column * TILE_WIDTH + TILE_WIDTH / 2),
                            (row * TILE_HEIGHT + TILE_HEIGHT / 2),
                        ),
                        BIG_DOT_RADIUS,
                    )
                case BoardTile.VERTICAL_LINE.value:
                    pygame.draw.line(
                        surface,
                        config["wall_color"],
                        ((column * TILE_WIDTH + TILE_WIDTH / 2), (row * TILE_HEIGHT)),
                        (
                            (column * TILE_WIDTH + TILE_WIDTH / 2),
                            (row * TILE_HEIGHT + TILE_HEIGHT),
                        ),
                        LINE_THICKNESS,
                    )
                case BoardTile.HORIZONTAL_LINE.value:
                    pygame.draw.line(
                        surface,
                        config["wall_color"],
                        ((column * TILE_WIDTH), (row * TILE_HEIGHT + TILE_HEIGHT / 2)),
                        (
                            (column * TILE_WIDTH + TILE_WIDTH),
                            (row * TILE_HEIGHT + TILE_HEIGHT / 2),
                        ),
                        LINE_THICKNESS,
                    )
                case BoardTile.TOP_RIGHT.value:
                    pygame.draw.arc(
                        surface,
                        config["wall_color"],
                        # We have to define a rectangle which will represent a quarter of a circle
                        [
                            column * TILE_WIDTH - TILE_WIDTH / 2 - 2,
                            row * TILE_HEIGHT + TILE_HEIGHT / 2 - 2,
                            TILE_WIDTH + 4,
                            TILE_HEIGHT + 5,
                        ],
                        0,
                        math.pi / 2,
                        LINE_THICKNESS,
                    )
                case BoardTile.TOP_LEFT.value:
                    pygame.draw.arc(
                        surface,
                        config["wall_color"],
                        # We have to define a rectangle which will represent a quarter of a circle
                        [
                            column * TILE_WIDTH + TILE_WIDTH / 2 - 2,
                            row * TILE_HEIGHT + TILE_HEIGHT / 2 - 2,
                            TILE_WIDTH + 4,
                            TILE_HEIGHT + 5,
                        ],
                        math.pi / 2,
                        math.pi,
                        LINE_THICKNESS,
                    )
                case BoardTile.BOTTOM_LEFT.value:
                    pygame.draw.arc(
                        surface,
                        config["wall_color"],
                        # We have to define a rectangle which will represent a quartr of a circle
                        [
                            column * TILE_WIDTH + TILE_WIDTH / 2 - 2,
                            row * TILE_HEIGHT - TILE_HEIGHT / 2 - 3,
                            TILE_WIDTH + 4,
                            TILE_HEIGHT + 5,
                        ],
                        math.pi,
                        3 * math.pi / 2,
                        LINE_THICKNESS,
                    )
                case BoardTile.BOTTOM_RIGHT.value:
                    pygame.draw.arc(
                        surface,
                        config["wall_color"],
                        # We have to define a rectangle which will represent a quartr of a circle
                        [
                            column * TILE_WIDTH - TILE_WIDTH / 2 - 2,
                            row * TILE_HEIGHT - TILE_HEIGHT / 2 - 3,
                            TILE_WIDTH + 4,
                            TILE_HEIGHT + 5,
                        ],
                        3 * math.pi / 2,
                        2 * math.pi,
                        LINE_THICKNESS,
                    )
                case BoardTile.GATE.value:
                    pygame.draw.line(
                        surface,
                        config["gate_color"],
                        ((column * TILE_WIDTH), (row * TILE_HEIGHT + TILE_HEIGHT / 2)),
                        (
                            (column * TILE_WIDTH + TILE_WIDTH),
                            (row * TILE_HEIGHT + TILE_HEIGHT / 2),
                        ),
                        LINE_THICKNESS,
                    )
