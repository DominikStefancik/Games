from game_state.game_state_manager import get_game_state_manager
from settings import pygame
from timers.timers_manager import get_timers_manager

from .constants import GhostImageType
from .helpers import get_ghost_images


class Ghost(pygame.sprite.Sprite):
    def __init__(self, groups, type):
        super().__init__(groups)

        self.type = type

        self.game_state_manager = get_game_state_manager()
        ghost_config = self.game_state_manager.get_level_config()[self.type.value]
        level_layout = self.game_state_manager.get_level_layout()

        self.possible_images = get_ghost_images(self.type)
        self.image = self.possible_images[GhostImageType.MAIN]

        position = ghost_config["position"]
        # Represents a rectangle to figure out where the ghost will be drawn in a current frame
        self.rect = self.image.get_rect(center=position)

        self.level_layout = level_layout
        self.direction = ghost_config["direction"]
        self.speed = ghost_config["speed"]
        self.is_in_box = ghost_config["is_in_box"]
        self.target = ghost_config["target"]
        self.is_dead = False
        self.is_eaten = False

        self.timers_manager = get_timers_manager()

    def update_image(self):
        if (not self.timers_manager.power_up_timer.active and not self.is_dead) or (
            self.timers_manager.power_up_timer.active
            and self.is_eaten
            and not self.is_dead
        ):
            self.image = self.possible_images[GhostImageType.MAIN]
        elif (
            self.timers_manager.power_up_timer.active
            and not self.is_dead
            and not self.is_eaten
        ):
            self.image = self.possible_images[GhostImageType.SPOOKED]
        else:
            self.image = self.possible_images[GhostImageType.DEAD]

        self.rect = self.image.get_rect(center=(self.rect.centerx, self.rect.centery))

    def update(self, delta_time):
        self.update_image()
