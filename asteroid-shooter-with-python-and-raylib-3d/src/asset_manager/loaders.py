from os.path import join

from settings import load_model, load_texture

from .constants import ModelAsset, TextureAsset


def load_textures():
    return {
        TextureAsset.DARK: load_texture(join("assets", "textures", "dark.png")),
        TextureAsset.RED: load_texture(join("assets", "textures", "red.png")),
    }


def load_models():
    return {
        ModelAsset.SPACESHIP: load_model(join("assets", "models", "spaceship.glb")),
        ModelAsset.LASER: load_model(join("assets", "models", "laser.glb")),
    }
