import random

import pygame

from constants import (
    ASTEROID_IMAGE_PATH,
    LASER_IMAGE_PATH,
    SPACESHIP_IMAGE_PATH,
    STAR_IMAGE_PATH,
    WINDOW_HEIGHT,
    WINDOW_WIDTH,
)
from spaceship import Spaceship
from star import Star

# General setup
pygame.init()

# A "display surface" is the main surface that we draw on
# and there can be ONLY one and it is always visible
DISPLAY_SURFACE = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Python Asteroid Shooter")

clock = pygame.time.Clock()

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

asteroid_rectangle = asteroid_surface.get_frect(
    center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
)
laser_rectangle = laser_surface.get_frect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))


all_sprites_group = pygame.sprite.Group()
for index in range(30):
    Star(all_sprites_group, star_surface)
spaceship = Spaceship(all_sprites_group, spaceship_surface)

is_running = True

while is_running:
    # Delta time is the time it took your computer to render the current frame.
    # It might take different delta time to render each frame depending on how busy your computer is
    # with processing the game logic and also other programs running on the computer.
    #
    # The value of delta time is in miliseconds
    delta_time = clock.tick() / 1000 # convert delta time to seconds

    ## In the event loop we check for keyboard input, mouse input, timers and UI interactions
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

    all_sprites_group.update(delta_time)

    ## Draw game elements
    DISPLAY_SURFACE.fill("darkgrey")

    # "blit"  is a shortcut for block-image-transfer, which esssentially means "put one surface on another surface".
    DISPLAY_SURFACE.blit(asteroid_surface, asteroid_rectangle)

    all_sprites_group.draw(DISPLAY_SURFACE)

    # The methods "pygame.display.update()" and "pygame.display.flip()" draw game elements on a window screen.
    # However, the "update()" draws the entire screen whereas with the "flip" we can specify
    # which part of the screen we want to be drawn.
    pygame.display.update()

# Close the game properly
pygame.quit()
