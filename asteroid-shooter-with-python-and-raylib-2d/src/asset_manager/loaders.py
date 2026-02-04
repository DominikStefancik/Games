from os.path import join

from settings import load_texture

from .constants import ImageAsset


def load_textures():
    return {
        ImageAsset.SPACESHIP: load_texture(join("assets", "images", "spaceship.png")),
        ImageAsset.STAR: load_texture(join("assets", "images", "star.png")),
    }
