import pygame

from constants import BACKGROUND_IMAGE_HEIGHT


def draw_background(surface, background_image, scroll):
    # The second argument is a tuple with coordinates where the top left corner of the image
    # will be placed.
    surface.blit(background_image, (0, 0 + scroll))
    # We add the same background picture twice to achieve an infinite scrolling effect
    surface.blit(background_image, (0, -BACKGROUND_IMAGE_HEIGHT + scroll))
