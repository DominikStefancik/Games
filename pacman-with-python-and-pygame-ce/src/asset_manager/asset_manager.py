from .loaders import (
    load_audio,
    load_fonts,
    load_graphics,
)


class AssetManager:
    def __init__(self):
        self._graphics = None
        self._fonts = None
        self._audio = None

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
    def audio_files(self):
        if self._audio == None:
            self._audio = load_audio()

            # Update volume of the sounds
            for key, _ in self._audio.items():
                self._audio[key].set_volume(0.4)

        return self._audio


ASSET_MANAGER = AssetManager()


def get_asset_manager():
    return ASSET_MANAGER
