import pygame

from constants import FPS, WINDOW_HEIGHT, WINDOW_WIDTH

# General setup
pygame.init()

WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Python Asteroid Shooter")

is_running = True

while is_running:
    ## In the event loop we check for keyboard input, mouse input, timers and UI interactions
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

    ## Draw game elements
    WINDOW.fill("blue")

    # The methods "pygame.display.update()" and "pygame.display.flip()" draw game elements on a window screen.
    # However, the "update()" draws the entire screen whereas with the "flip" we can specify
    # which part of the screen we want to be drawn.
    pygame.display.update()

# Close the game properly
pygame.quit()
