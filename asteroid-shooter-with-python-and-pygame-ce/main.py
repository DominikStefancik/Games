import random

import pygame

from constants import (
    ASTEROID_IMAGE_PATH,
    FPS,
    LASER_IMAGE_PATH,
    SPACESHIP_IMAGE_PATH,
    STAR_IMAGE_PATH,
    WINDOW_HEIGHT,
    WINDOW_WIDTH,
)

# General setup
pygame.init()

# A "display surface" is the main surface that we draw on
# and there can be ONLY one and it is always visible
DISPLAY_SURFACE = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Python Asteroid Shooter")

# A regular surface is an image of some kind. You can have any nymber of regular surfaces,
# but they are only visible when attached to the display surface!
# We can create regular surfaces either manually or by loading images  and rendering fonts.

# Load images
#
# If the image we want to load has no transparent pixels, we have to call the "convert()",
# otherwise we have to call "convert_alpha()".
# These two methods are called for improving the game performance.
spaceship_surface = pygame.image.load(SPACESHIP_IMAGE_PATH).convert_alpha()
star_surface = pygame.image.load(STAR_IMAGE_PATH).convert_alpha()
asteroid_surface = pygame.image.load(ASTEROID_IMAGE_PATH).convert_alpha()
laser_surface = pygame.image.load(LASER_IMAGE_PATH).convert_alpha()

# The method "get_frect()" gets "FRect" out of the image.
# The "FRect" is very similar to the rectangle "Rect". The onl difference is that its sizes are measured
# in the floating points.
# The method parameter sasys that the center of the rectangle will be in the middle of the screen
spaceship_rectangle = spaceship_surface.get_frect(
    center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
)
asteroid_rectangle = asteroid_surface.get_frect(
    center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
)
laser_rectangle = laser_surface.get_frect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))

# One line FOR loop
star_positions = [
    (random.randint(0, WINDOW_WIDTH), random.randint(0, WINDOW_HEIGHT))
    for index in range(30)
]

spaceship_direction = 1

is_running = True

while is_running:
    ## In the event loop we check for keyboard input, mouse input, timers and UI interactions
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

    ## Draw game elements
    DISPLAY_SURFACE.fill("darkgrey")

    for position in star_positions:
        DISPLAY_SURFACE.blit(star_surface, position)

    # "blit"  is a shortcut for block-image-transfer, which esssentially means "put one surface on another surface".

    DISPLAY_SURFACE.blit(asteroid_surface, asteroid_rectangle)
    DISPLAY_SURFACE.blit(laser_surface, laser_rectangle)

    spaceship_rectangle.centerx += 0.5 * spaceship_direction

    if spaceship_rectangle.left < 0 or spaceship_rectangle.right > WINDOW_WIDTH:
        spaceship_direction *= -1

    DISPLAY_SURFACE.blit(spaceship_surface, spaceship_rectangle)

    # The methods "pygame.display.update()" and "pygame.display.flip()" draw game elements on a window screen.
    # However, the "update()" draws the entire screen whereas with the "flip" we can specify
    # which part of the screen we want to be drawn.
    pygame.display.update()

# Close the game properly
pygame.quit()
