from random import choice, sample

from asset_manager.asset_manager import get_asset_manager
from settings import Vector3

from .constants import BOARD_SIZE, FLOOR_VERTICAL_VALUE, TILE_SIZE, TILE_TYPES
from .model import Model


class Board:
    def __init__(self, group):
        self.grid = self.create_grid(group)

    def create_grid(self, group):
        asset_manager = get_asset_manager()
        models = sample(list(asset_manager.models.values()), TILE_TYPES)
        board = []

        for row_index in range(BOARD_SIZE):
            row = []
            for column_index in range(BOARD_SIZE):
                row.append(
                    Model(
                        group=group,
                        model=choice(models),
                        position=Vector3(
                            row_index * TILE_SIZE,
                            FLOOR_VERTICAL_VALUE + 3,
                            column_index * TILE_SIZE,
                        ),
                    )
                )

            board.append(row)

        return board
