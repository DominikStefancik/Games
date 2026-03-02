import random

from constants import WINDOW_HEIGHT, WINDOW_WIDTH
from .constants import PLATFORM_START_MOVING_THRESHOLD
from .platform import Platform


def create_starting_platform(image):
    return Platform(image, (WINDOW_WIDTH // 2 - 50, WINDOW_HEIGHT - 50), 100)


def create_platform(image, previous_platform, current_score):
    platform_width = random.randint(40, 60)
    platform_x = random.randint(0, WINDOW_WIDTH - platform_width)
    # Take the Y-coordinate of the previously created platform
    # and set the Y-coordinate of the next platform depending on the previous one
    platform_y = previous_platform.rect.y - random.randint(80, 120)
    platform_type = random.randint(1, 2)

    is_moving = platform_type == 1 and current_score > PLATFORM_START_MOVING_THRESHOLD

    return Platform(image, (platform_x, platform_y), platform_width, is_moving)
