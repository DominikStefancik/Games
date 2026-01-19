from constants import WINDOW_HEIGHT, WINDOW_WIDTH
from .platform import Platform

def create_starting_platform(image):
    return Platform(image, (WINDOW_WIDTH // 2 - 50, WINDOW_HEIGHT - 50), 100)
