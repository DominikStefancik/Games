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
    is_mouse_button_pressed,
    matrix_multiply,
    matrix_scale,
    matrix_translate,
    MOUSE_LEFT_BUTTON,
    Vector2,
    Vector3,
    Vector3Add,
)

from .constants import (
    BoardState,
    BOARD_OFFSET,
    BOARD_SIZE,
    Match,
    TILE_SIZE,
    TILE_TYPES_COUNT,
)
from .helpers import (
    are_items_adjacent,
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
                            if not self.selected_item:
                                item.is_selected = True
                                self.selected_item = item
                            else:
                                if are_items_adjacent(self.selected_item, item):
                                    self.swap_items(self.selected_item, item)

                                    # We only allow swapping items if it results in 3 or more matches
                                    # otherwise, we have to swap items back
                                    if self.find_matches():
                                        self.resolve_matches(group)
                                    else:
                                        self.swap_items(self.selected_item, item)

                                # Deselect item which was previously selected
                                self.selected_item.is_selected = False
                                self.selected_item = None

                            break

    def find_matches(self):
        clear_matched_items(self.matched_items)
        found_match = False

        # Check horizontal matches
        for y_index in range(BOARD_SIZE):
            for x_index in range(BOARD_SIZE - 2):
                if check_matched_items(self.grid, x_index, y_index, Match.HORIZONTAL):
                    self.matched_items[y_index][x_index] = 1
                    self.matched_items[y_index][x_index + 1] = 1
                    self.matched_items[y_index][x_index + 2] = 1
                    found_match = True

        # Check vertical matches
        for x_index in range(BOARD_SIZE):
            for y_index in range(BOARD_SIZE - 2):
                if check_matched_items(self.grid, x_index, y_index, Match.VERTICAL):
                    self.matched_items[y_index][x_index] = 1
                    self.matched_items[y_index + 1][x_index] = 1
                    self.matched_items[y_index + 2][x_index] = 1
                    found_match = True

        return found_match

    def resolve_matches(self, group):
        self.state = BoardState.UPDATING

        for x_index in range(BOARD_SIZE):
            move_y = BOARD_SIZE - 1
            for y_index in range(BOARD_SIZE - 1, -1, -1):
                item = self.grid[y_index][x_index]
                if item.is_matched:
                    item.to_be_removed = True
                else:
                    item.fall_position_z = BOARD_OFFSET.z - (move_y * TILE_SIZE)
                    item.grid_position.y = move_y
                    self.grid[move_y][x_index] = item
                    move_y -= 1

            # Fill empty spots with new items
            while move_y >= 0:
                self.grid[move_y][x_index] = create_random_item(
                    group=group,
                    models_selection=self.models_selection,
                    row=move_y - get_matched_items_count(self.matched_items, x_index),
                    column=x_index,
                    fall_position_z=BOARD_OFFSET.z - (move_y * TILE_SIZE),
                )
                move_y -= 1

    def swap_items(self, item1, item2):
        temp_position = Vector3(item1.position.x, item1.position.y, item1.position.z)
        temp_grid_position = Vector2(item1.grid_position.x, item1.grid_position.y)
        temp_fall_position_z = item1.fall_position_z

        item1.position = item2.position
        item1.grid_position = item2.grid_position
        item1.fall_position_z = item2.fall_position_z

        item2.position = temp_position
        item2.grid_position = temp_grid_position
        item2.fall_position_z = temp_fall_position_z

        self.grid[int(item1.grid_position.y)][int(item1.grid_position.x)] = item2
        self.grid[int(item2.grid_position.y)][int(item2.grid_position.x)] = item1

    def update(self, group):
        self.state = get_state(self)

        if self.state == BoardState.IDLE:
            self.check_selected_item()

            if self.find_matches():
                self.resolve_matches(group)
