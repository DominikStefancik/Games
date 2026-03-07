from random import choice

import pygame

from asset_manager.asset_manager import get_asset_manager
from asset_manager.constants import ImageAsset
from duck.brown_duck import BrownDuck
from duck.yellow_duck import YellowDuck

from .constants import (
    BROWN_DUCK_VERTICAL_LINE,
    GAP_BETWEEN_DUCKS,
    YELLOW_DUCK_VERTICAL_LINE,
)


def create_brown_duck(groups, index):
    asset_manager = get_asset_manager()
    has_target = choice([False, False, False, True])
    image = (
        asset_manager.graphics[ImageAsset.DUCK_BROWN_TARGET]
        if has_target
        else asset_manager.graphics[ImageAsset.DUCK_BROWN]
    )
    position_x = index * (image.get_width() + GAP_BETWEEN_DUCKS) * 2

    return BrownDuck(
        groups,
        pygame.transform.flip(image, True, False),
        (position_x, BROWN_DUCK_VERTICAL_LINE),
        has_target,
    )


def create_yellow_duck(groups, index):
    asset_manager = get_asset_manager()
    has_target = choice([False, True])
    image = (
        asset_manager.graphics[ImageAsset.DUCK_YELLOW_TARGET]
        if has_target
        else asset_manager.graphics[ImageAsset.DUCK_YELLOW]
    )
    position_x = index * (image.get_width() + GAP_BETWEEN_DUCKS) * 2

    return YellowDuck(
        groups, image, (position_x, YELLOW_DUCK_VERTICAL_LINE), has_target
    )


def get_digit_image(digit):
    asset_manager = get_asset_manager()

    match digit:
        case "0":
            return asset_manager.graphics[ImageAsset.NUMBER_0]
        case "1":
            return asset_manager.graphics[ImageAsset.NUMBER_1]
        case "2":
            return asset_manager.graphics[ImageAsset.NUMBER_2]
        case "3":
            return asset_manager.graphics[ImageAsset.NUMBER_3]
        case "4":
            return asset_manager.graphics[ImageAsset.NUMBER_4]
        case "5":
            return asset_manager.graphics[ImageAsset.NUMBER_5]
        case "6":
            return asset_manager.graphics[ImageAsset.NUMBER_6]
        case "7":
            return asset_manager.graphics[ImageAsset.NUMBER_7]
        case "8":
            return asset_manager.graphics[ImageAsset.NUMBER_8]
        case "9":
            return asset_manager.graphics[ImageAsset.NUMBER_9]
