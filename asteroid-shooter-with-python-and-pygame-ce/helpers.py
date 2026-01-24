import pygame

from os.path import join

from asteroid_explosion import AnimatedAsteroidExplosion
from constants import SCORE_TEXT_COLOR, WINDOW_HEIGHT, WINDOW_WIDTH


def get_explosion_image_path(index):
    return join("assets", "images", "asteroid_explosion", f"{index}.png")


def handle_collisions(spaceship, all_sprites_group, asteroids_group, lasers_group, asteroid_explosion_frames):
    for laser in lasers_group:
        # Check for collisions with asteroids
        #
        # The method "spritecollide" checks if a single sprite collides with any of the sprites in the given sprites group
        #
        # The third boolean argument says if the sprite from the group, with which the single sprite collided, should be
        # removed from the group and destroyed.
        if pygame.sprite.spritecollide(laser, asteroids_group, True):
            AnimatedAsteroidExplosion(all_sprites_group, asteroid_explosion_frames, laser.rect.midtop)
            laser.kill()

    # The last argument says that when detecting collisions, use sprites' masks, instead of rectangles. With this
    # we can achieve a perfect perfect collision detection which is more precise then the collision detection using
    # sprites' rectangles.
    # Note: In sprite classes (and its descendants), a sprite's mask is created by default from the sprite's
    # image/surface. If we don't want that, we can overwrite creating sorite's mask manually.
    if pygame.sprite.spritecollide(spaceship, asteroids_group, True, pygame.sprite.collide_mask):
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
