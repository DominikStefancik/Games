from game_state import get_game_state
from settings import pygame, TILE_SIZE, Z_Layer

from .constants import PlayerIconAnimation


class PlayerIcon(pygame.sprite.Sprite):
    def __init__(self, groups, position, animation_frames):
        super().__init__(groups)

        self.frames = animation_frames
        self.frame_index = 0
        self.animation = PlayerIconAnimation.IDLE.value
        self.image = self.frames[self.animation][self.frame_index]
        self.rect = self.image.get_frect(center=position)
        self.z_index = Z_Layer.MAIN.value
