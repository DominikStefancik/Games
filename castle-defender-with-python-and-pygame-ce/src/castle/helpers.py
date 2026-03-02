from settings import pygame

from .constants import CastleState, CastlePosition


def get_castle_image(images, state):
    return images[f"castle_{state.value}"]


def get_tower_image(images, state):
    return images[f"tower_{state.value}"]


def map_castle_position(state):
    match state:
        case CastleState.FULLY_RESTORED:
            return CastlePosition.FULLY_RESTORED.value
        case CastleState.DAMAGED:
            return CastlePosition.DAMAGED.value
        case CastleState.SEVERELY_DAMAGED:
            return CastlePosition.SEVERELY_DAMAGED.value
