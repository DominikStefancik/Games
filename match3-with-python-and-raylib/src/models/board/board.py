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
    TILE_SIZE,
    TILE_TYPES_COUNT,
)
from ..constants import MODEL_VERTICAL_VALUE
from ..model import Model


class Board:
    def __init__(self, group):
        asset_manager = get_asset_manager()
        self.models_in_board = sample(
            list(asset_manager.models.values()), TILE_TYPES_COUNT
        )
        self.grid = self.create_grid(group)

    def create_grid(self, group):
        board = []

        for row_index in range(BOARD_SIZE):
            row = []
            for column_index in range(BOARD_SIZE):
                row.append(
                    Model(
                        group=group,
                        model=choice(self.models_in_board),
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
                            item.is_selected = True
                            break
