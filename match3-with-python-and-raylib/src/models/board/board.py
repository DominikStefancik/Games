from random import sample

from asset_manager.asset_manager import get_asset_manager
from camera import get_camera
from settings import (
    BoundingBox,
    get_mesh_bounding_box,
    get_mouse_position,
    get_ray_collision_box,
    get_ray_collision_mesh,
    get_screen_to_world_ray,
    is_key_pressed,
    is_mouse_button_pressed,
    KEY_SPACE,
    matrix_multiply,
    matrix_scale,
    matrix_translate,
    MOUSE_LEFT_BUTTON,
    Vector3,
    Vector3Add,
)

from .constants import (
    BoardState,
    BOARD_SIZE,
    Match,
    TILE_TYPES_COUNT,
)
from .helpers import (
    check_matched_items,
    clear_matched_items,
    create_random_item,
    get_matched_items_count,
    get_state,
)


class Board:
    def __init__(self, group):
        asset_manager = get_asset_manager()
        self.models_selection = sample(
            list(asset_manager.models.items()), TILE_TYPES_COUNT
        )
        self.grid = self.create_grid(group)
        self.selected_item = None
        self.state = BoardState.IDLE
        self.matched_items = self.create_matched_grid()

    def create_grid(self, group):
        board = []

        for row_index in range(BOARD_SIZE):
            row = []
            for column_index in range(BOARD_SIZE):
                item = create_random_item(
                    group=group,
                    models_selection=self.models_selection,
                    row=row_index,
                    column=column_index,
                )
                row.append(item)

            board.append(row)

        return board

    def create_matched_grid(self):
        board = []

        for row_index in range(BOARD_SIZE):
            row = []
            for column_index in range(BOARD_SIZE):
                row.append(0)

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
        clear_matched_items(self.matched_items)

        # Check horizontal matches
        for y_index in range(BOARD_SIZE):
            for x_index in range(BOARD_SIZE - 2):
                if check_matched_items(self.grid, x_index, y_index, Match.HORIZONTAL):
                    self.matched_items[y_index][x_index] = 1
                    self.matched_items[y_index][x_index + 1] = 1
                    self.matched_items[y_index][x_index + 2] = 1

        # Check vertical matches
        for x_index in range(BOARD_SIZE):
            for y_index in range(BOARD_SIZE - 2):
                if check_matched_items(self.grid, x_index, y_index, Match.VERTICAL):
                    self.matched_items[y_index][x_index] = 1
                    self.matched_items[y_index + 1][x_index] = 1
                    self.matched_items[y_index + 2][x_index] = 1

    def resolve_matches(self, group):
        self.state = BoardState.UPDATING

        for x_index in range(BOARD_SIZE):
            move_y = BOARD_SIZE - 1
            for y_index in range(BOARD_SIZE - 1, -1, -1):
                item = self.grid[y_index][x_index]
                if item.is_matched:
                    item.to_be_removed = True
                else:
                    item.fall_position_z = move_y
                    self.grid[move_y][x_index] = item
                    move_y -= 1

            # Fill empty spots with new items
            while move_y >= 0:
                self.grid[move_y][x_index] = create_random_item(
                    group=group,
                    models_selection=self.models_selection,
                    row=move_y - get_matched_items_count(self.matched_items, x_index),
                    column=x_index,
                    fall_position_z=move_y,
                )
                move_y -= 1

    def update(self, group):
        self.state = get_state(self)

        if self.state == BoardState.IDLE:
            self.check_selected_item()
            self.find_matches()

            if is_key_pressed(KEY_SPACE):
                self.resolve_matches(group)
