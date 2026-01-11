import constants
from turret import Turret


def get_turret_spritesheet_path(index):
    return f"assets/images/turrets/turret_{index}.png"

def create_turret(turret_spritesheets, mouse_position, world, turret_group) -> None:
    # Convert mouse position into a tile on the map
    # "//" is a floor division
    mouse_tile_x = mouse_position[0] // constants.TILE_SIZE
    mouse_tile_y = mouse_position[1] // constants.TILE_SIZE

    # Calculate sequential number of a tile
    mouse_tile_number = (mouse_tile_y * constants.TILES_COLUMNS) + mouse_tile_x
    # Check if the tile we clicked on is grass
    # (the value 7 is defined in the "layers.data" array in the "level.tmj" JSON file)
    if world.tile_map[mouse_tile_number] == 7:
        # Check that on the tile we just clicked there is not a turret already
        #
        # At the beginning we assume that the space is not taken
        is_space_free = True
        for turret in turret_group:
            if (mouse_tile_x, mouse_tile_y) == (turret.tile_x, turret.tile_y):
                is_space_free = False
                break

        if is_space_free:
            new_turret = Turret(turret_spritesheets, mouse_tile_x, mouse_tile_y)
            turret_group.add(new_turret)

def select_turret(mouse_position, turret_group):
    mouse_tile_x = mouse_position[0] // constants.TILE_SIZE
    mouse_tile_y = mouse_position[1] // constants.TILE_SIZE

    # Check if the tile we just clicked on contains a turret
    for turret in turret_group:
        if (mouse_tile_x, mouse_tile_y) == (turret.tile_x, turret.tile_y):
            return turret

def clear_turret_selection(turret_group):
    for turret in turret_group:
        turret.is_selected = False
