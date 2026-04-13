from os.path import join

import pygame

from .constants import FontAsset, ImageAsset


def load_graphics():
    return {
        ImageAsset.TABLE: pygame.image.load(
            join("assets", "images", "table.png")
        ).convert_alpha(),
        ImageAsset.CUE: pygame.image.load(
            join("assets", "images", "cue.png")
        ).convert_alpha(),
        ImageAsset.BALL_1: pygame.image.load(
            join("assets", "images", "balls", "ball_1.png")
        ).convert_alpha(),
        ImageAsset.BALL_2: pygame.image.load(
            join("assets", "images", "balls", "ball_2.png")
        ).convert_alpha(),
        ImageAsset.BALL_3: pygame.image.load(
            join("assets", "images", "balls", "ball_3.png")
        ).convert_alpha(),
        ImageAsset.BALL_4: pygame.image.load(
            join("assets", "images", "balls", "ball_4.png")
        ).convert_alpha(),
        ImageAsset.BALL_5: pygame.image.load(
            join("assets", "images", "balls", "ball_5.png")
        ).convert_alpha(),
        ImageAsset.BALL_6: pygame.image.load(
            join("assets", "images", "balls", "ball_6.png")
        ).convert_alpha(),
        ImageAsset.BALL_7: pygame.image.load(
            join("assets", "images", "balls", "ball_7.png")
        ).convert_alpha(),
        ImageAsset.BALL_8: pygame.image.load(
            join("assets", "images", "balls", "ball_8.png")
        ).convert_alpha(),
        ImageAsset.BALL_9: pygame.image.load(
            join("assets", "images", "balls", "ball_9.png")
        ).convert_alpha(),
        ImageAsset.BALL_10: pygame.image.load(
            join("assets", "images", "balls", "ball_10.png")
        ).convert_alpha(),
        ImageAsset.BALL_11: pygame.image.load(
            join("assets", "images", "balls", "ball_11.png")
        ).convert_alpha(),
        ImageAsset.BALL_12: pygame.image.load(
            join("assets", "images", "balls", "ball_12.png")
        ).convert_alpha(),
        ImageAsset.BALL_13: pygame.image.load(
            join("assets", "images", "balls", "ball_13.png")
        ).convert_alpha(),
        ImageAsset.BALL_14: pygame.image.load(
            join("assets", "images", "balls", "ball_14.png")
        ).convert_alpha(),
        ImageAsset.BALL_15: pygame.image.load(
            join("assets", "images", "balls", "ball_15.png")
        ).convert_alpha(),
        ImageAsset.CUE_BALL: pygame.image.load(
            join("assets", "images", "balls", "cue_ball.png")
        ).convert_alpha(),
    }


def load_fonts():
    return {
        FontAsset.FUTURA_30: pygame.font.SysFont("Futura", 30),
        FontAsset.FUTURA_60: pygame.font.SysFont("Futura", 60),
    }


def load_sounds():
    return {}
