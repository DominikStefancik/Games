from .import_helpers import *
from .loaders import load_font, load_level_graphics, load_ui_graphics


class AssetManager:
    def __init__(self):
        self._level_graphics = None
        self._ui_graphics = None
        self._font = None

    @property
    def level_graphics(self):
        if self._level_graphics == None:
            self._level_graphics = load_level_graphics()

        return self._level_graphics

    @property
    def ui_graphics(self):
        if self._ui_graphics == None:
            self._ui_graphics = load_ui_graphics()

        return self._ui_graphics

    @property
    def font(self):
        if self._font == None:
            self._font = load_font()

        return self._font


ASSET_MANAGER = AssetManager()


def get_asset_manager():
    return ASSET_MANAGER
