import pygame

from constants import (
    BACKGROUND_IMAGE_HEIGHT,
    BLACK,
    PANEL_COLOR,
    SCORE_PANEL_HEIGHT,
    WHITE,
    WINDOW_FADE_RECTANGLE_COUNT,
    WINDOW_HEIGHT,
    WINDOW_WIDTH,
)


def draw_background(surface, background_image, scroll):
    # The second argument is a tuple with coordinates where the top left corner of the image
    # will be placed.
    surface.blit(background_image, (0, 0 + scroll))
    # We add the same background picture twice to achieve an infinite scrolling effect
    surface.blit(background_image, (0, -BACKGROUND_IMAGE_HEIGHT + scroll))


def draw_text(surface, font, text, colour, position):
    # First we have to convert text into an image
    image = font.render(text, True, colour)
    surface.blit(image, position)


def draw_score_panel(surface, font, score):
    pygame.draw.rect(surface, PANEL_COLOR, (0, 0, WINDOW_WIDTH, SCORE_PANEL_HEIGHT))
    pygame.draw.line(surface, WHITE, (0, SCORE_PANEL_HEIGHT), (WINDOW_WIDTH, SCORE_PANEL_HEIGHT), 2)
    draw_text(surface, font, f"SCORE: {score}", WHITE, (10, 3))


def draw_fading_rectangles(surface, window_fade_counter):
    for index in range(0, WINDOW_FADE_RECTANGLE_COUNT, 2):
        pygame.draw.rect(
            surface,
            BLACK,
            (
                0,
                index * 100,
                window_fade_counter,
                WINDOW_HEIGHT / WINDOW_FADE_RECTANGLE_COUNT,
            ),
        )
        pygame.draw.rect(
            surface,
            BLACK,
            (
                WINDOW_WIDTH - window_fade_counter,
                (index + 1) * 100,
                WINDOW_WIDTH,
                WINDOW_HEIGHT / WINDOW_FADE_RECTANGLE_COUNT,
            ),
        )
