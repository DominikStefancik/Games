from random import choice, sample

from asset_manager.asset_manager import get_asset_manager
from camera import get_camera
from settings import (
    BoundingBox,
    get_mesh_bounding_box,
    get_mouse_position,
    get_ray_collision_box,
    get_ray_collision_mesh,
    get_screen_to_world_ray,
    is_mouse_button_pressed,
    matrix_multiply,
    matrix_scale,
    matrix_translate,
    MOUSE_LEFT_BUTTON,
    Vector3,
    Vector3Add,
)

from .constants import (
    BOARD_OFFSET,
    BOARD_SIZE,
    Match,
    TILE_SIZE,
    TILE_TYPES_COUNT,
)
from ..constants import MODEL_VERTICAL_VALUE
from ..model import Model


class Board:
    def __init__(self, group):
        asset_manager = get_asset_manager()
        self.models_in_board = sample(
            list(asset_manager.models.items()), TILE_TYPES_COUNT
        )
        self.grid = self.create_grid(group)
        self.selected_item = None
        self.found_three_matches = False

    def create_grid(self, group):
        board = []

        for row_index in range(BOARD_SIZE):
            row = []
            for column_index in range(BOARD_SIZE):
                model_pick = choice(self.models_in_board)

                row.append(
                    Model(
                        group=group,
                        model=model_pick[1],
                        type=model_pick[0],
                        position=Vector3(
                            BOARD_OFFSET.x + (row_index * TILE_SIZE),
                            MODEL_VERTICAL_VALUE,
                            BOARD_OFFSET.y + (column_index * TILE_SIZE),
                        ),
                    )
                )

            board.append(row)

        return board

    def check_selected_item(self):
        if is_mouse_button_pressed(MOUSE_LEFT_BUTTON):
            camera = get_camera()
            ray = get_screen_to_world_ray(get_mouse_position(), camera)

            for row in range(BOARD_SIZE):
                for column in range(BOARD_SIZE):
                    item = self.grid[row][column]
                    item_bounding_box = get_mesh_bounding_box(item.model.meshes[0])

                    item_bounding_box_with_position = BoundingBox(
                        Vector3Add(item_bounding_box.min, item.position),
                        Vector3Add(item_bounding_box.max, item.position),
                    )

                    # Do the "cheap" test first
                    # This test only does just 6 plane checks. It's fast.
                    bounding_box_hit = get_ray_collision_box(
                        ray, item_bounding_box_with_position
                    )

                    # Only if the cheap test passes, we have to do another, expensive test
                    if bounding_box_hit.hit:
                        transform = matrix_multiply(
                            matrix_scale(item.scale.x, item.scale.y, item.scale.z),
                            matrix_translate(
                                item.position.x, item.position.y, item.position.z
                            ),
                        )

                        # A mesh can contain hundreds, thousands, sometimes millions of triangles.
                        # The function "get_ray_collision_mesh" must:
                        #   Transform the ray into mesh space
                        #   Loop through every triangle in the mesh
                        #   Do a ray–triangle intersection test for each one
                        #   Keep the closest hit
                        # This test is performance demaning if ous game has many objects.
                        # Without doing the "cheap" test above first, we would be checking
                        # "number of models" x "number of triangles in each model" every frame of the game loop
                        mesh_hit = get_ray_collision_mesh(
                            ray, item.model.meshes[0], transform
                        )

                        if mesh_hit.hit:
                            # Deselect item which was previously selected
                            if self.selected_item:
                                self.selected_item.is_selected = False

                            item.is_selected = True
                            self.selected_item = item
                            break

    def find_matches(self):
        # Check horizontal metches
        for y_index in range(BOARD_SIZE):
            for x_index in range(BOARD_SIZE - 2):
                self.check_matched_items(x_index, y_index, Match.HORIZONTAL)

        # Check vertical metches
        for x_index in range(BOARD_SIZE):
            for y_index in range(BOARD_SIZE - 2):
                    self.check_matched_items(x_index, y_index, Match.VERTICAL)

    def check_matched_items(self, x_index, y_index, match):
        items = []

        for add_on in range(3):
            item = self.grid[x_index + add_on if match == Match.HORIZONTAL else x_index][y_index + add_on if match == Match.VERTICAL else y_index]
            items.append(item)

        item1, item2, item3 = items

        if item1.type == item2.type and item1.type == item3.type:
            item1.is_matched = True
            item2.is_matched = True
            item3.is_matched = True
            self.found_three_matches = True

    def update(self):
        self.check_selected_item()
        self.find_matches()
