from .loaders import load_models


class AssetManager:
    def __init__(self):
        self._models = None

    @property
    def models(self):
        if self._models == None:
            self._models = load_models()

        return self._models


ASSET_MANAGER = AssetManager()


def get_asset_manager():
    return ASSET_MANAGER
