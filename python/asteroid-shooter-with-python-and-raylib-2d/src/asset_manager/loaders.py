from os.path import join

from settings import (
    ffi,
    FONT_SIZE,
    load_font_ex,
    load_music_stream,
    load_sound,
    load_texture,
)

from .constants import FontAsset, ImageAsset, SoundAsset


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


def load_sounds():
    return {
        SoundAsset.LASER: load_sound(join("assets", "audio", "laser.wav")),
        SoundAsset.ASTEROID_EXPLOSION: load_sound(
            join("assets", "audio", "asteroid_explosion.wav")
        ),
        SoundAsset.SPACESHIP_EXPLOSION: load_sound(
            join("assets", "audio", "spaceship_explosion.mp3")
        ),
        SoundAsset.BACKGROUND_MUSIC: load_music_stream(
            join("assets", "audio", "music.wav")
        ),
    }
