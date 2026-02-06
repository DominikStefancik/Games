from asset_manager.asset_manager import get_asset_manager
from asset_manager.constants import ModelAsset, TextureAsset
from .laser import Laser


def create_laser(group, position):
    asset_manager = get_asset_manager()
    Laser(
        group=group,
        model=asset_manager.models[ModelAsset.LASER],
        texture=asset_manager.textures[TextureAsset.RED],
        position=position,
    )
