from os.path import join

from settings import pygame

from .constants import AudioAsset, ImageAsset


def load_graphics():
    return {
        ImageAsset.IMAGE: pygame.image.load(
            join("assets", "graphics", "level", "image.png")
        ).convert_alpha(),
    }


def load_font():
    return pygame.font.Font("freesansbold.ttf", 20)


def load_audio():
    return {
        AudioAsset.SOUND: pygame.mixer.Sound(join("assets", "audio", "sound.wav")),
    }
