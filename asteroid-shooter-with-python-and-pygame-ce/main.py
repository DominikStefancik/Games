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

# If we don't provide any arguments, the initial Vector2 values will be 0, 0
spaceship_direction = pygame.math.Vector2()
spaceship_speed = 300

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

    # The method "get_pressed()" constantly (every frame) checks for pressed buttons
    # Whereas the method "get_just_pressed()" checks only for most recent button presses
    keys = pygame.key.get_pressed()

    # The expression "keys[pygame.K_RIGHT]" returns a boolean value
    # The expression "int(boolean)" returns 1 (for True) or 0 (for False)
    # Then the direction will be either
    #   0 (if we didn't press right or left key)
    #   1 (if we pressed the right key)
    #   -1 (if we pressed the left key)
    spaceship_direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
    spaceship_direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])

    # We cannot normalise the direction vector, if both of its values is 0
    # The one-liner IF says:
    #   "if vector is (0,1), (1,0) or (1,1), then call the method normalize, otherwise keep it as it is"
    spaceship_direction = spaceship_direction.normalize() if spaceship_direction else spaceship_direction

    # With adding the delta time as a multiplier,
    # we are independent of how many frame rates are defined in the clock's tick method
    spaceship_rectangle.center += spaceship_direction * spaceship_speed * delta_time

    if spaceship_rectangle.left < 0:
        spaceship_rectangle.left = 0
    if spaceship_rectangle.right > WINDOW_WIDTH:
        spaceship_rectangle.right = WINDOW_WIDTH
    if spaceship_rectangle.top < 0:
        spaceship_rectangle.top = 0
    if spaceship_rectangle.bottom > WINDOW_HEIGHT:
        spaceship_rectangle.bottom = WINDOW_HEIGHT


    ## Draw game elements
    DISPLAY_SURFACE.fill("darkgrey")

    for position in star_positions:
        DISPLAY_SURFACE.blit(star_surface, position)

    # "blit"  is a shortcut for block-image-transfer, which esssentially means "put one surface on another surface".
    DISPLAY_SURFACE.blit(asteroid_surface, asteroid_rectangle)
    DISPLAY_SURFACE.blit(laser_surface, laser_rectangle)
    DISPLAY_SURFACE.blit(spaceship_surface, spaceship_rectangle)

    # The methods "pygame.display.update()" and "pygame.display.flip()" draw game elements on a window screen.
    # However, the "update()" draws the entire screen whereas with the "flip" we can specify
    # which part of the screen we want to be drawn.
    pygame.display.update()

# Close the game properly
pygame.quit()
