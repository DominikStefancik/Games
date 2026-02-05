from random import randint, uniform

from asset_manager.asset_manager import get_asset_manager
from asset_manager.constants import ImageAsset, SoundAsset
from settings import play_sound, Vector2, WINDOW_HEIGHT, WINDOW_WIDTH
from sprites.asteroid import Asteroid
from .laser import Laser


def create_stars_data():
    return [
        (
            Vector2(randint(0, WINDOW_WIDTH), randint(0, WINDOW_HEIGHT)),  # position
            uniform(0.5, 1.8),  # size
        )
        for index in range(25)
    ]


def create_asteroid(group):
    asset_manager = get_asset_manager()
    Asteroid(group=group, texture=asset_manager.textures[ImageAsset.ASTEROID])


def create_laser(group, position):
    asset_manager = get_asset_manager()
    Laser(
        group=group,
        texture=asset_manager.textures[ImageAsset.LASER],
        position=position,
    )
    play_sound(asset_manager.sounds[SoundAsset.LASER])
