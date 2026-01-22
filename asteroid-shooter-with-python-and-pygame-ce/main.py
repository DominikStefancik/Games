import random

import pygame

from constants import FPS, SPACESHIP_IMAGE_PATH, STAR_IMAGE_PATH, WINDOW_HEIGHT, WINDOW_WIDTH

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

# One line FOR loop
star_positions = [(random.randint(0, WINDOW_WIDTH), random.randint(0, WINDOW_HEIGHT)) for index in range(30)]


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
    DISPLAY_SURFACE.blit(spaceship_surface, (100, 150))

    # The methods "pygame.display.update()" and "pygame.display.flip()" draw game elements on a window screen.
    # However, the "update()" draws the entire screen whereas with the "flip" we can specify
    # which part of the screen we want to be drawn.
    pygame.display.update()

# Close the game properly
pygame.quit()
