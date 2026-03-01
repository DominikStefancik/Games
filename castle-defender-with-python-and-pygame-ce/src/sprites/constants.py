from enum import Enum

from settings import pygame

CROSSHAIR_IMAGE_SCALE = 0.025
REPAIR_BUTTON_IMAGE_SCALE = 0.5
ARMOUR_BUTTON_IMAGE_SCALE = 1.2
ENEMY_CREATION_INTERVAL = 1000


class ButtonEvent(Enum):
    REPAIR = pygame.event.custom_type()
    ARMOUR = pygame.event.custom_type()
