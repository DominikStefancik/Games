from random import choice, sample

from asset_manager.asset_manager import get_asset_manager
from settings import (
    BoundingBox,
    CAMERA_POSITION,
    check_collision_boxes,
    get_mesh_bounding_box,
    get_mouse_position,
    get_screen_height,
    get_screen_width,
    is_mouse_button_pressed,
    MOUSE_LEFT_BUTTON,
    Vector3,
    Vector3Add,
)

from .constants import (
    BOARD_SIZE,
    BOARD_OFFSET,
    MOUSE_BOUNDING_BOX_OFFSET,
    TILE_SIZE,
    TILE_TYPES,
)
from ..constants import FLOOR_VERTICAL_VALUE, MODEL_VERTICAL_VALUE
from ..model import Model


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
                            BOARD_OFFSET.x + (row_index * TILE_SIZE),
                            MODEL_VERTICAL_VALUE,
                            BOARD_OFFSET.y + (column_index * TILE_SIZE),
                        ),
                    )
                )

            board.append(row)

        return board

    def check_selected(self):
        if is_mouse_button_pressed(MOUSE_LEFT_BUTTON):
            mouse_position = get_mouse_position()
            mouse_click_bounding_box = BoundingBox(
                Vector3(
                    (mouse_position.x - get_screen_width() / 2) / CAMERA_POSITION.x
                    - MOUSE_BOUNDING_BOX_OFFSET,
                    MODEL_VERTICAL_VALUE - MOUSE_BOUNDING_BOX_OFFSET,
                    (mouse_position.y - get_screen_height() / 2) / CAMERA_POSITION.z
                    - MOUSE_BOUNDING_BOX_OFFSET,
                ),
                Vector3(
                    (mouse_position.x - get_screen_width() / 2) / CAMERA_POSITION.x
                    + MOUSE_BOUNDING_BOX_OFFSET,
                    MODEL_VERTICAL_VALUE + MOUSE_BOUNDING_BOX_OFFSET,
                    (mouse_position.y - get_screen_height() / 2) / CAMERA_POSITION.z
                    + MOUSE_BOUNDING_BOX_OFFSET,
                ),
            )

            for row in range(BOARD_SIZE):
                for column in range(BOARD_SIZE):
                    item = self.grid[row][column]
                    # This bounding box doesn't have item's position. We have to add it manually.
                    item_bounding_box = get_mesh_bounding_box(item.model.meshes[0])
                    # A collision box which has the position of the item
                    collision_box = BoundingBox(
                        Vector3Add(item_bounding_box.min, item.position),
                        Vector3Add(item_bounding_box.max, item.position),
                    )

                    if check_collision_boxes(collision_box, mouse_click_bounding_box):
                        item.is_selected = True
                        break
