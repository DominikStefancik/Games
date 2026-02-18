from asset_manager.asset_manager import get_asset_manager
from asset_manager.constants import ImageAsset
from settings import pygame

from .constants import GhostImageType, GhostType


def get_ghost_images(ghost_type):
    asset_manager = get_asset_manager()
    main_image = None

    match ghost_type:
        case GhostType.BLINKY:
            main_image = asset_manager.graphics[ImageAsset.BLINKY_GHOST]
        case GhostType.PINKY:
            main_image = asset_manager.graphics[ImageAsset.PINKY_GHOST]
        case GhostType.INKY:
            main_image = asset_manager.graphics[ImageAsset.INKY_GHOST]
        case GhostType.CLYDE:
            main_image = asset_manager.graphics[ImageAsset.CLYDE_GHOST]

    return {
        # We have to scale an original ghost images, because they are too big
        GhostImageType.MAIN: pygame.transform.scale(main_image, (45, 45)),
        GhostImageType.SPOOKED: pygame.transform.scale(
            asset_manager.graphics[ImageAsset.SPOOKED_GHOST], (45, 45)
        ),
        GhostImageType.DEAD: pygame.transform.scale(
            asset_manager.graphics[ImageAsset.DEAD_GHOST], (45, 45)
        ),
    }
