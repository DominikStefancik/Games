from os.path import join

from settings import load_model, load_texture

from .constants import ModelAsset, TextureAsset


def load_textures():
    return {
        TextureAsset.DARK: load_texture(join("assets", "textures", "dark.png")),
    }


def load_models():
    return {
        ModelAsset.SPACESHIP: load_model(join("assets", "models", "spaceship.glb")),
    }
