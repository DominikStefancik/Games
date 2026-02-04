from os.path import join

from settings import ffi, FONT_SIZE, load_font_ex, load_texture

from .constants import FontAsset, ImageAsset


def load_textures():
    return {
        ImageAsset.SPACESHIP: load_texture(join("assets", "images", "spaceship.png")),
        ImageAsset.STAR: load_texture(join("assets", "images", "star.png")),
        ImageAsset.LASER: load_texture(join("assets", "images", "laser.png")),
        ImageAsset.ASTEROID: load_texture(join("assets", "images", "asteroid.png")),
        ImageAsset.EXPLOSION: [
            load_texture(join("assets", "images", "explosion", f"{index}.png"))
            for index in range(1, 29)
        ],
    }


def load_fonts():
    return {
        FontAsset.STORMFAZE: load_font_ex(
            join("assets", "fonts", "Stormfaze.otf"), FONT_SIZE, ffi.NULL, 0
        ),
    }
