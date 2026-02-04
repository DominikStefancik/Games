from .loaders import load_fonts, load_textures


class AssetManager:
    def __init__(self):
        self._textures = None
        self._fonts = None

    @property
    def textures(self):
        if self._textures == None:
            self._textures = load_textures()

        return self._textures

    @property
    def fonts(self):
        if self._fonts == None:
            self._fonts = load_fonts()

        return self._fonts


ASSET_MANAGER = AssetManager()


def get_asset_manager():
    return ASSET_MANAGER
