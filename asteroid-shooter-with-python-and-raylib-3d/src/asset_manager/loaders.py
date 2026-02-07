from os.path import join

from settings import ffi, FONT_SIZE, load_font_ex, load_model, load_texture

from .constants import FontAsset, ModelAsset, TextureAsset


def load_textures():
    return {
        TextureAsset.DARK: load_texture(join("assets", "textures", "dark.png")),
        TextureAsset.GREEN: load_texture(join("assets", "textures", "green.png")),
        TextureAsset.LIGHT: load_texture(join("assets", "textures", "light.png")),
        TextureAsset.ORANGE: load_texture(join("assets", "textures", "orange.png")),
        TextureAsset.PURPLE: load_texture(join("assets", "textures", "purple.png")),
        TextureAsset.RED: load_texture(join("assets", "textures", "red.png")),
    }


def load_models():
    return {
        ModelAsset.SPACESHIP: load_model(join("assets", "models", "spaceship.glb")),
        ModelAsset.LASER: load_model(join("assets", "models", "laser.glb")),
    }


def load_fonts():
    return {
        FontAsset.STORMFAZE: load_font_ex(
            join("assets", "fonts", "Stormfaze.otf"), FONT_SIZE, ffi.NULL, 0
        ),
    }
