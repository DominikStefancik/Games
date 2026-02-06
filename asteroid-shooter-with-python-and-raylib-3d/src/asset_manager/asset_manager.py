from .loaders import load_textures


class AssetManager:
    def __init__(self):
        self._textures = None

    @property
    def textures(self):
        if self._textures == None:
            self._textures = load_textures()

        return self._textures


ASSET_MANAGER = AssetManager()


def get_asset_manager():
    return ASSET_MANAGER
