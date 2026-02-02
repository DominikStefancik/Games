from game_state import get_game_state
from settings import pygame, TILE_SIZE, Z_Layer


class Node(pygame.sprite.Sprite):
    def __init__(self, groups, surface, position, level, available_paths):
        super().__init__(groups)

        self.image = surface
        self.rect = self.image.get_frect(
            center=(position[0] + TILE_SIZE / 2, position[1] + TILE_SIZE / 2)
        )
        self.previous_rect = self.rect.copy()
        self.z_index = Z_Layer.PATH.value
        self.level = level
        self.available_paths = available_paths
        self.game_state = get_game_state()
        self.grid_position = (int(position[0] / TILE_SIZE), int(position[1] / TILE_SIZE))

    def has_path_in_direction(self, direction):
        return (
            direction in list(self.available_paths.keys())
            and int(self.available_paths[direction][0][0])
            <= self.game_state.unlocked_level
        )
