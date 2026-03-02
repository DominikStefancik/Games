from .loaders import load_models, load_textures


class AssetManager:
    def __init__(self):
        self._textures = None
        self._models = None

    @property
    def textures(self):
        if self._textures == None:
            self._textures = load_textures()

        return self._textures

    @property
    def models(self):
        if self._models == None:
            self._models = load_models()

        return self._models


ASSET_MANAGER = AssetManager()


def get_asset_manager():
    return ASSET_MANAGER
