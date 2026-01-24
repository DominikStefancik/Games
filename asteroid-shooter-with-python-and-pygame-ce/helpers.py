import pygame


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
