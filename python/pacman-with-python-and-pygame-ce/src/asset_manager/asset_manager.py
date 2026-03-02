from .loaders import (
    load_fonts,
    load_graphics,
    load_sounds,
)


class AssetManager:
    def __init__(self):
        self._graphics = None
        self._fonts = None
        self._sounds = None

    @property
    def graphics(self):
        if self._graphics == None:
            self._graphics = load_graphics()

        return self._graphics

    @property
    def fonts(self):
        if self._fonts == None:
            self._fonts = load_fonts()

        return self._fonts

    @property
    def sounds(self):
        if self._sounds == None:
            self._sounds = load_sounds()

            # Update volume of the sounds
            for key, _ in self._sounds.items():
                self._sounds[key].set_volume(0.4)

        return self._sounds


ASSET_MANAGER = AssetManager()


def get_asset_manager():
    return ASSET_MANAGER
