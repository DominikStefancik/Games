from random import choice

from asset_manager.asset_manager import get_asset_manager
from asset_manager.constants import ModelAsset, SoundAsset, TextureAsset
from settings import play_sound

from .asteroid import Asteroid
from .laser import Laser


def create_asteroid(group):
    asset_manager = get_asset_manager()
    texture_asset = choice(
        [
            TextureAsset.GREEN,
            TextureAsset.LIGHT,
            TextureAsset.ORANGE,
            TextureAsset.PURPLE,
        ]
    )
    Asteroid(group=group, texture=asset_manager.textures[texture_asset])


def create_laser(group, position):
    asset_manager = get_asset_manager()
    Laser(
        group=group,
        model=asset_manager.models[ModelAsset.LASER],
        texture=asset_manager.textures[TextureAsset.RED],
        position=position,
    )
    play_sound(asset_manager.sounds[SoundAsset.LASER])
