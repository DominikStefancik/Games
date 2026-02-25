from settings import pygame


def get_castle_image(images, state):
    return images[f"castle_{state.value}"]
