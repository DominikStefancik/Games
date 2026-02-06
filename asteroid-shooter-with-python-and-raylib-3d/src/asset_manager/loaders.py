from os.path import join

from settings import load_texture

from .constants import TextureAsset


def load_textures():
    return {
        TextureAsset.DARK: load_texture(join("assets", "textures", "dark.png")),
    }
