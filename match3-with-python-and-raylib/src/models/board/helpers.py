from random import choice

from settings import Vector3

from .constants import BoardState, BOARD_OFFSET, BOARD_SIZE, Match, TILE_SIZE
from ..constants import MODEL_VERTICAL_VALUE
from ..model import Model


def create_random_item(group, models_selection, row, column, fall_position_z=None):
    model_pick = choice(models_selection)

    return Model(
        group=group,
        model=model_pick[1],
        type=model_pick[0],
        position=Vector3(
            BOARD_OFFSET.x + (column * TILE_SIZE),
            MODEL_VERTICAL_VALUE,
            BOARD_OFFSET.z + (row * TILE_SIZE),
        ),
        fall_position_z=fall_position_z,
    )


def clear_matched_items(grid):
    for row in range(BOARD_SIZE):
        for column in range(BOARD_SIZE):
            grid[row][column] = 0


def check_matched_items(grid, x_index, y_index, match):
    found_three_matches = False
    items = []

    for add_on in range(3):
        item = grid[x_index + add_on if match == Match.HORIZONTAL else x_index][
            y_index + add_on if match == Match.VERTICAL else y_index
        ]
        items.append(item)

    item1, item2, item3 = items

    if item1.type == item2.type and item1.type == item3.type:
        item1.is_matched = True
        item2.is_matched = True
        item3.is_matched = True
        found_three_matches = True

    return found_three_matches


def get_state(board):
    # Check, if the board is still updating position of any of its items
    if board.state == BoardState.UPDATING:
        for row in range(BOARD_SIZE):
            for column in range(BOARD_SIZE):
                item = board.grid[row][column]

                if item.is_updating_position():
                    return BoardState.UPDATING

    return BoardState.IDLE
