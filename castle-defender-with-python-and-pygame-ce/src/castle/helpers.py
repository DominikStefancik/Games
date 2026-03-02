from settings import pygame


def get_castle_image(images, state):
    return images[f"castle_{state.value}"]


def get_tower_image(images, state):
    return images[f"tower_{state.value}"]
