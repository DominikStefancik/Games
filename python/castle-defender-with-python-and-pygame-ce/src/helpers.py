from settings import pygame


def scale_image(image, scale_factor):
    new_size = (
        round(image.get_width() * scale_factor),
        round(image.get_height() * scale_factor),
    )

    return pygame.transform.scale(image, new_size)
