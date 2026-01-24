import random

import pygame

from asteroid import Asteroid
from constants import (
    ASTEROID_IMAGE_PATH,
    DISPLAY_SURFACE_COLOR,
    LASER_IMAGE_PATH,
    OXANIUM_BOLD_FONT_PATH,
    SPACESHIP_IMAGE_PATH,
    STAR_IMAGE_PATH,
    WINDOW_HEIGHT,
    WINDOW_WIDTH,
)
from helpers import display_score, get_explosion_image_path, handle_collisions
from spaceship import Spaceship
from star import Star

# General setup
pygame.init()

# A "display surface" is the main surface that we draw on
# and there can be ONLY one and it is always visible
DISPLAY_SURFACE = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Python Asteroid Shooter")

# A regular surface is an image of some kind. You can have any nymber of regular surfaces,
# but they are only visible when attached to the display surface!
# We can create regular surfaces either manually or by loading images  and rendering fonts.

clock = pygame.time.Clock()

# Load images
#
# If the image we want to load has no transparent pixels, we have to call the "convert()",
# otherwise we have to call "convert_alpha()".
# These two methods are called for improving the game performance.
SPACESHIP_SURFACE = pygame.image.load(SPACESHIP_IMAGE_PATH).convert_alpha()
STAR_SURFACE = pygame.image.load(STAR_IMAGE_PATH).convert_alpha()
ASTEROID_SURFACE = pygame.image.load(ASTEROID_IMAGE_PATH).convert_alpha()
LASER_SURFACE = pygame.image.load(LASER_IMAGE_PATH).convert_alpha()
# One-line FOR loop
asteroid_explosion_frames = [pygame.image.load(get_explosion_image_path(index)).convert_alpha() for index in range(21)]

# Load fonts
OXANIUM_BOLD_FONT = pygame.font.Font(OXANIUM_BOLD_FONT_PATH, 40)

all_sprites_group = pygame.sprite.Group()
asteroids_group = pygame.sprite.Group()
lasers_group = pygame.sprite.Group()

for index in range(30):
    Star(all_sprites_group, STAR_SURFACE)
spaceship = Spaceship(all_sprites_group, lasers_group, SPACESHIP_SURFACE, LASER_SURFACE)

# Create an interval timer to create an asteroid every 0.5 seconds.
# We create a custom event and set a timer for that event. Then we will capture/listen to the event
# in the event loop.
asteroid_creation_event = pygame.event.custom_type()
pygame.time.set_timer(asteroid_creation_event, 500)

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

        if event.type == asteroid_creation_event:
            asteroid_position = random.randint(0, WINDOW_WIDTH), -100
            Asteroid((all_sprites_group, asteroids_group), ASTEROID_SURFACE, asteroid_position)

    all_sprites_group.update(delta_time)

    handle_collisions(spaceship, all_sprites_group, asteroids_group, lasers_group, asteroid_explosion_frames)

    ## Draw game elements
    DISPLAY_SURFACE.fill(DISPLAY_SURFACE_COLOR)
    all_sprites_group.draw(DISPLAY_SURFACE)
    display_score(DISPLAY_SURFACE, OXANIUM_BOLD_FONT)

    # The methods "pygame.display.update()" and "pygame.display.flip()" draw game elements on a window screen.
    # However, the "update()" draws the entire screen whereas with the "flip" we can specify
    # which part of the screen we want to be drawn.
    pygame.display.update()

# Close the game properly
pygame.quit()
