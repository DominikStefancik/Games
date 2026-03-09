from os.path import join

import pygame

from .constants import AudioAsset, FontAsset, ImageAsset


def load_graphics():
    return {
        ImageAsset.BACKGROUND: pygame.image.load(
            join("assets", "images", "background_blue.png")
        ).convert_alpha(),
        ImageAsset.TABLE: pygame.image.load(
            join("assets", "images", "background_wood.png")
        ).convert_alpha(),
        ImageAsset.CURTAIN_TOP: pygame.image.load(
            join("assets", "images", "curtain_top.png")
        ).convert_alpha(),
        ImageAsset.CURTAIN_SIDE: pygame.image.load(
            join("assets", "images", "curtain_side.png")
        ).convert_alpha(),
        ImageAsset.WATER_BACK: pygame.image.load(
            join("assets", "images", "water1.png")
        ).convert_alpha(),
        ImageAsset.WATER_FRONT: pygame.image.load(
            join("assets", "images", "water2.png")
        ).convert_alpha(),
        ImageAsset.GRASS: pygame.image.load(
            join("assets", "images", "grass.png")
        ).convert_alpha(),
        ImageAsset.DUCK_BROWN: pygame.image.load(
            join("assets", "images", "duck", "duck_outline_brown.png")
        ).convert_alpha(),
        ImageAsset.DUCK_BROWN_TARGET: pygame.image.load(
            join("assets", "images", "duck", "duck_outline_target_brown.png")
        ).convert_alpha(),
        ImageAsset.DUCK_YELLOW: pygame.image.load(
            join("assets", "images", "duck", "duck_outline_yellow.png")
        ).convert_alpha(),
        ImageAsset.DUCK_YELLOW_TARGET: pygame.image.load(
            join("assets", "images", "duck", "duck_outline_target_yellow.png")
        ).convert_alpha(),
        ImageAsset.STICK: pygame.image.load(
            join("assets", "images", "stick_metal.png")
        ).convert_alpha(),
        ImageAsset.CROSSHAIR: pygame.image.load(
            join("assets", "images", "crosshair_outline.png")
        ).convert_alpha(),
        ImageAsset.BULLET: pygame.image.load(
            join("assets", "images", "silver_bullet.png")
        ).convert_alpha(),
        ImageAsset.SCORE: pygame.image.load(
            join("assets", "images", "text", "text_score.png")
        ).convert_alpha(),
        ImageAsset.COLON: pygame.image.load(
            join("assets", "images", "text", "text_dots.png")
        ).convert_alpha(),
        ImageAsset.READY: pygame.image.load(
            join("assets", "images", "text", "text_ready.png")
        ).convert_alpha(),
        ImageAsset.GAME_OVER: pygame.image.load(
            join("assets", "images", "text", "text_gameover.png")
        ).convert_alpha(),
        ImageAsset.NUMBER_0: pygame.image.load(
            join("assets", "images", "text", "text_0.png")
        ).convert_alpha(),
        ImageAsset.NUMBER_1: pygame.image.load(
            join("assets", "images", "text", "text_1.png")
        ).convert_alpha(),
        ImageAsset.NUMBER_2: pygame.image.load(
            join("assets", "images", "text", "text_2.png")
        ).convert_alpha(),
        ImageAsset.NUMBER_3: pygame.image.load(
            join("assets", "images", "text", "text_3.png")
        ).convert_alpha(),
        ImageAsset.NUMBER_4: pygame.image.load(
            join("assets", "images", "text", "text_4.png")
        ).convert_alpha(),
        ImageAsset.NUMBER_5: pygame.image.load(
            join("assets", "images", "text", "text_5.png")
        ).convert_alpha(),
        ImageAsset.NUMBER_6: pygame.image.load(
            join("assets", "images", "text", "text_6.png")
        ).convert_alpha(),
        ImageAsset.NUMBER_7: pygame.image.load(
            join("assets", "images", "text", "text_7.png")
        ).convert_alpha(),
        ImageAsset.NUMBER_8: pygame.image.load(
            join("assets", "images", "text", "text_8.png")
        ).convert_alpha(),
        ImageAsset.NUMBER_9: pygame.image.load(
            join("assets", "images", "text", "text_9.png")
        ).convert_alpha(),
    }


def load_fonts():
    return {
        FontAsset.FUTURA: pygame.font.SysFont("Futura", 35),
    }


def load_sounds():
    return {
        AudioAsset.FUN_FAIR: pygame.mixer.Sound(
            join("assets", "sounds", "funfair_music.mp3")
        ),
        AudioAsset.GAME_OVER: pygame.mixer.Sound(
            join("assets", "sounds", "game_over.mp3")
        ),
        AudioAsset.GUN_SHOT: pygame.mixer.Sound(
            join("assets", "sounds", "gun_shot.mp3")
        ),
        AudioAsset.METAL_HIT_1: pygame.mixer.Sound(
            join("assets", "sounds", "metal_hit_1.mp3")
        ),
        AudioAsset.METAL_HIT_2: pygame.mixer.Sound(
            join("assets", "sounds", "metal_hit_2.mp3")
        ),
        AudioAsset.METAL_HIT_3: pygame.mixer.Sound(
            join("assets", "sounds", "metal_hit_3.mp3")
        ),
        AudioAsset.METAL_HIT_4: pygame.mixer.Sound(
            join("assets", "sounds", "metal_hit_4.mp3")
        ),
        AudioAsset.METAL_HIT_5: pygame.mixer.Sound(
            join("assets", "sounds", "metal_hit_5.mp3")
        ),
        AudioAsset.METAL_HIT_6: pygame.mixer.Sound(
            join("assets", "sounds", "metal_hit_6.mp3")
        ),
        AudioAsset.METAL_HIT_7: pygame.mixer.Sound(
            join("assets", "sounds", "metal_hit_7.mp3")
        ),
        AudioAsset.METAL_HIT_8: pygame.mixer.Sound(
            join("assets", "sounds", "metal_hit_8.mp3")
        ),
        AudioAsset.METAL_HIT_9: pygame.mixer.Sound(
            join("assets", "sounds", "metal_hit_9.mp3")
        ),
    }
