from asset_manager.asset_manager import get_asset_manager
from asset_manager.constants import TextureAsset

from .floor import Floor


class ModelManager:
    def __init__(self):
        self.asset_manager = get_asset_manager()
        self.floor = Floor([], self.asset_manager.textures[TextureAsset.DARK])

    def get_all_models(self):
        return [self.floor]

    def update(self):
        delta_time = get_frame_time()

    def draw(self):
        for model in self.get_all_models():
            model.draw()
