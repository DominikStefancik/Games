import pygame

from constants import SCORE_TEXT_COLOR, WINDOW_HEIGHT, WINDOW_WIDTH


def handle_collisions(spaceship, asteroids_group, lasers_group):
    for laser in lasers_group:
        # Check for collisions with asteroids
        # The method "spritecollide" checks if a single sprite collides with any of the sprites in the given sprites group
        # The last boolean argument says if the sprite from the group, with which the single sprite collided, should be
        # removed from the group and destroyed.
        if pygame.sprite.spritecollide(laser, asteroids_group, True):
            laser.kill()

    if pygame.sprite.spritecollide(spaceship, asteroids_group, True):
        spaceship.kill()


def display_score(surface, score_font):
    # The method "pygame.time.get_ticks()" returns the time which passed since the game started
    current_time = pygame.time.get_ticks() // 100
    text_surface = score_font.render(str(current_time), True, SCORE_TEXT_COLOR)
    text_rectangle = text_surface.get_frect(midbottom = (WINDOW_WIDTH / 2, WINDOW_HEIGHT - 50))

    # "blit"  is a shortcut for block-image-transfer, which esssentially means "put one surface on another surface".
    surface.blit(text_surface, text_rectangle)

    # The method "inflate" can grow or shrink the rectangle size
    # (depending on positive or negative values passed as parameters)
    pygame.draw.rect(surface, SCORE_TEXT_COLOR, text_rectangle.inflate(20, 20).move(0, -8), 5, 10)
